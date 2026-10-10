#!/usr/bin/env python3
r"""
Compiles Arena Studio recordings and adds their metadata audio.

CPU Recording uses deterministic PNG screenshots: slower to create, but the
compiled video is frame-perfect even when live rendering stutters. GPU Recording
uses a fast live window capture: it reflects the PC's actual displayed FPS, so
visible lag spikes remain visible in the result.

Requires ffmpeg. Legacy recording metadata may additionally require Pillow.
If ffmpeg is not on your PATH, the picker window below has a
"Browse..." button to point straight at wherever you have it installed.

Audio cues that fired during the recording (character/global "Audio Cues")
are mixed into the exported video automatically, placed at the correct
time and volume. Exporting at a different fps than you recorded at only
changes how smooth the output looks (frames are duplicated/dropped to hit
the requested fps) -- it does not speed up or slow down the video, and
audio stays lined up with the picture either way.

DOUBLE-CLICK / no arguments -> opens the Arena CPU Recording Workstation:
  - browse a recording library or select one recording folder directly
  - sort by creation date, modified date, name, frame count, or duration
  - replay CPU PNG sequences in-app with play/pause, stepping, looping, and scrub
  - watch the current source frame and encoded frame number while ffmpeg compiles
  - Browse... to your ffmpeg executable (remembered after the first time)
  - Browse... to choose where to save the .mp4
  - virtual-camera aspect is already baked into the recorded PNG frames
  - optional width/height (blank = native; preserves camera aspect), fps, and quality
  - recorded audio, Faux overlays, GPU sources, CLI exporting, and job logs remain supported

COMMAND LINE (optional, for scripting):
  python rec.py --list
  python rec.py --rec rec_20260710_141230
  python rec.py --rec "C:\full\path\to\rec_20260710_141230"
  python rec.py --width 1080 --height 1920
  python rec.py --out my_fight.mp4 --fps 30
  python rec.py --ffmpeg "C:\\path\\to\\ffmpeg.exe"
  python rec.py --gui       # force the picker window from the CLI too
"""

import argparse
import glob
import gzip
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys

FROZEN = bool(getattr(sys, "frozen", False))
RESOURCE_DIR = os.path.abspath(getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(os.path.abspath(sys.executable)) if FROZEN else os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.abspath(os.environ.get("BOX_GAME_DIR") or BASE_DIR)
RECORDINGS_DIR = os.path.abspath(os.environ.get("BOX_GAME_RECORDINGS") or os.path.join(GAME_DIR, "recordings"))
# Configuration must never be written into PyInstaller's read-only _internal or
# one-file extraction directory. Keep it beside Arena Studio instead.
CONFIG_PATH = os.path.join(GAME_DIR, ".export_recording_config.json")
FAUX_COMPOSITOR_VERSION = 1


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass


def resolve_ffmpeg(explicit_path):
    """Figures out which ffmpeg binary to use, in order:
    1. --ffmpeg path given on this run (also saved for next time)
    2. a path remembered from a previous --ffmpeg run
    3. ffmpeg already on PATH
    Returns the path/command to use, or None if nothing works."""
    if explicit_path:
        exe = explicit_path
        if os.path.isdir(exe):
            # they pointed at the folder, not the .exe -- find it for them
            for name in ("ffmpeg.exe", "ffmpeg"):
                candidate = os.path.join(exe, name)
                if os.path.exists(candidate):
                    exe = candidate
                    break
        if os.path.exists(exe):
            cfg = load_config()
            cfg["ffmpeg_path"] = exe
            save_config(cfg)
            return exe
        print(f"--ffmpeg path doesn't exist: {exe}")
        return None

    cfg = load_config()
    remembered = cfg.get("ffmpeg_path")
    if remembered and os.path.exists(remembered):
        return remembered

    # Arena EXE Builder can package FFmpeg into _internal/ (one-folder) or
    # sys._MEIPASS (one-file). Prefer that self-contained copy before PATH.
    for root in dict.fromkeys((GAME_DIR, RESOURCE_DIR)):
        for rel in ("ffmpeg.exe", "ffmpeg", os.path.join("ffmpeg","bin","ffmpeg.exe"),
                    os.path.join("ffmpeg","bin","ffmpeg"),os.path.join("_internal","ffmpeg.exe"),
                    os.path.join("_internal","ffmpeg")):
            candidate=os.path.join(root,rel)
            if os.path.isfile(candidate):return candidate

    on_path = shutil.which("ffmpeg")
    if on_path:
        return on_path

    return None


def verify_ffmpeg_runnable(ffmpeg_bin):
    """Confirms ffmpeg_bin doesn't just *exist* on disk but can actually be
    launched. A FileNotFoundError from subprocess can mean the file exists
    but isn't really runnable -- most commonly because it's a OneDrive
    'Files On-Demand' placeholder (looks like a real file in Explorer, but
    the bytes aren't downloaded), or a corrupt/partial download missing
    required DLLs. Returns (ok, message)."""
    try:
        subprocess.run([ffmpeg_bin, "-version"], capture_output=True, timeout=10)
        return True, ""
    except FileNotFoundError:
        size = None
        try:
            size = os.path.getsize(ffmpeg_bin)
        except Exception:
            pass
        msg = f"'{ffmpeg_bin}' exists on disk but Windows couldn't actually launch it.\n\n"
        if size is not None and size < 1024:
            msg += (f"It's only {size} bytes -- that's almost certainly a OneDrive "
                    "'Files On-Demand' placeholder, not the real executable.\n"
                    "Fix: right-click ffmpeg.exe in Explorer -> \"Always keep on this device\", "
                    "then try again.")
        else:
            msg += ("Most likely causes:\n"
                    "  - OneDrive 'Files On-Demand': right-click ffmpeg.exe -> "
                    "\"Always keep on this device\"\n"
                    "  - A corrupt/partial download missing required DLLs -- redownload "
                    "the full/static ffmpeg build\n"
                    "  - Antivirus quarantined or blocked it")
        return False, msg
    except subprocess.TimeoutExpired:
        return True, ""  # it launched, just slow to report version -- good enough
    except Exception as e:
        return False, f"Couldn't run '{ffmpeg_bin}': {e}"


def list_recordings():
    if not os.path.isdir(RECORDINGS_DIR):
        return []
    out = []
    for name in sorted(os.listdir(RECORDINGS_DIR)):
        d = os.path.join(RECORDINGS_DIR, name)
        if not os.path.isdir(d):
            continue
        if os.path.exists(os.path.join(d, "meta.json")) or glob.glob(os.path.join(d, "frame_*.png")):
            out.append(d)
    return out


def load_meta(rec_dir):
    meta_path = os.path.join(rec_dir, "meta.json")
    frame_count_on_disk = len(glob.glob(os.path.join(rec_dir, "frame_*.png")))
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            meta = json.load(f)
        meta.setdefault("audio_events", [])
        video_rel = meta.get("video_file") or ""
        video_path = video_rel if os.path.isabs(str(video_rel)) else os.path.join(rec_dir, str(video_rel))
        video_on_disk = bool(video_rel and os.path.isfile(video_path) and os.path.getsize(video_path) > 0)
        meta.setdefault("rendered", frame_count_on_disk > 0 or video_on_disk)
        meta["frames_on_disk"] = frame_count_on_disk
        meta["video_on_disk"] = video_on_disk
        # New: background music fields added in 5.1.2+
        meta.setdefault("background_music", "")
        meta.setdefault("background_music_volume", 0.7)
        meta.setdefault("game_end_cue", "")
        meta.setdefault("game_end_volume", 1.0)
        meta.setdefault("faux_rec", None)
        return meta
    return {"fps": 60, "width": None, "height": None, "frame_count": frame_count_on_disk,
            "audio_events": [], "rendered": frame_count_on_disk > 0, "frames_on_disk": frame_count_on_disk,
            "background_music": "", "background_music_volume": 0.7, "faux_rec": None,
            "video_file": None, "video_on_disk": False}


def _event_time_ms(event, capture_fps):
    if event.get("frame") is not None:
        return max(0, round((float(event.get("frame", 0)) / max(1, capture_fps)) * 1000))
    return max(0, round(float(event.get("time", 0.0)) * 1000))


def resolve_audio_events(meta, capture_fps):
    """Return (path, delay_ms, volume, pitch) for one-shot recorded sounds."""
    resolved = []
    lifecycle = {"background_music", "background_music_fade", "background_music_stop"}
    for ev in (meta or {}).get("audio_events", []):
        if str(ev.get("event", "")) in lifecycle:
            continue
        rel_path = ev.get("path")
        if not rel_path:
            continue
        abs_path = rel_path if os.path.isabs(str(rel_path)) else os.path.join(GAME_DIR, str(rel_path).replace("/", os.sep))
        if not os.path.isfile(abs_path):
            continue
        delay_ms = _event_time_ms(ev, capture_fps)
        volume = max(0.0, min(1.0, float(ev.get("volume", 1.0))))
        pitch = max(0.05, min(8.0, float(ev.get("pitch", 1.0) or 1.0)))
        resolved.append((abs_path, delay_ms, volume, pitch))
    return resolved


def resolve_bgm(meta, capture_fps):
    """Resolve looping BGM plus its actual recorded start/fade/stop timeline."""
    events = list((meta or {}).get("audio_events", []))
    starts = [ev for ev in events if ev.get("event") == "background_music"]
    fades = [ev for ev in events if ev.get("event") == "background_music_fade"]
    stops = [ev for ev in events if ev.get("event") == "background_music_stop"]
    start_ev = starts[0] if starts else None
    rel = ((start_ev or {}).get("path") or (meta or {}).get("background_music") or "")
    if not rel:
        return None
    abs_path = rel if os.path.isabs(str(rel)) else os.path.join(GAME_DIR, str(rel).replace("/", os.sep))
    if not os.path.isfile(abs_path):
        return None
    start_ms = _event_time_ms(start_ev, capture_fps) if start_ev else 0
    volume = max(0.0, min(1.0, float((start_ev or {}).get(
        "volume", (meta or {}).get("background_music_volume", 0.7)))))
    fade = None
    if fades:
        ev = fades[0]
        fade = {"start_ms": _event_time_ms(ev, capture_fps),
                "duration": max(0.01, float(ev.get("duration", 2.0)))}
    stop_ms = _event_time_ms(stops[0], capture_fps) if stops else None
    return {"path": abs_path, "volume": volume, "start_ms": start_ms,
            "fade": fade, "stop_ms": stop_ms}


# ---------------------------------------------------------------------------
# Experimental Faux Rec compositor (Pillow)
# ---------------------------------------------------------------------------
def _faux_descriptor(meta):
    info = (meta or {}).get("faux_rec")
    return info if isinstance(info, dict) and info.get("enabled") else None


def _faux_timeline_path(rec_dir, meta):
    info = _faux_descriptor(meta)
    if not info:
        return None
    rel = info.get("timeline", "faux_scene.json.gz")
    path = rel if os.path.isabs(str(rel)) else os.path.join(rec_dir, str(rel))
    return path if os.path.isfile(path) else None


def _load_faux_timeline(rec_dir, meta):
    path = _faux_timeline_path(rec_dir, meta)
    if not path:
        raise RuntimeError("Faux Rec timeline is missing (expected faux_scene.json.gz).")
    opener = gzip.open if path.lower().endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as fh:
        data = json.load(fh)
    if data.get("format") != "arena-faux-rec":
        raise RuntimeError("Unsupported Faux Rec timeline format.")
    return path, data


def _faux_asset_path(rec_dir, raw):
    if not raw:
        return None
    raw = str(raw)
    candidates = [raw] if os.path.isabs(raw) else [
        os.path.join(rec_dir, raw.replace("/", os.sep)),
        os.path.join(GAME_DIR, raw.replace("/", os.sep)),
        os.path.join(BASE_DIR, raw.replace("/", os.sep)),
    ]
    return next((p for p in candidates if os.path.isfile(p)), None)


def _faux_color(value, alpha=255, default=(255, 255, 255)):
    try:
        vals = list(value)
        rgb = tuple(max(0, min(255, int(vals[i]))) for i in range(3))
    except Exception:
        rgb = default
    return rgb + (max(0, min(255, int(alpha))),)


def _faux_alpha_image(image, opacity):
    opacity = max(0, min(255, int(opacity)))
    if opacity >= 255:
        return image
    image = image.copy()
    a = image.getchannel("A").point(lambda v: (v * opacity) // 255)
    image.putalpha(a)
    return image


def _faux_font(ImageFont, name, size, bold=False):
    size = max(8, int(size))
    raw = str(name or "segoeui")
    norm = raw.lower().replace(" ", "").replace("-", "").replace("_", "")
    aliases = {
        "segoeui": ("segoeuib.ttf" if bold else "segoeui.ttf"),
        "arial": ("arialbd.ttf" if bold else "arial.ttf"),
        "consolas": ("consolab.ttf" if bold else "consola.ttf"),
        "couriernew": ("courbd.ttf" if bold else "cour.ttf"),
    }
    names = [aliases.get(norm, raw)]
    if not str(names[0]).lower().endswith((".ttf", ".otf", ".ttc")):
        names += [str(names[0]) + ".ttf"]
    roots = [os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
             "/usr/share/fonts/truetype/dejavu", "/Library/Fonts"]
    for candidate in list(names) + [os.path.join(root, n) for root in roots for n in names]:
        try:
            return ImageFont.truetype(candidate, size=size)
        except Exception:
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def _faux_text_sprite(Image, ImageDraw, ImageFont, text, size, color, font_name,
                      bold=False, stroke=0, opacity=255, rotation=0.0, bg=None, bg_alpha=0):
    font = _faux_font(ImageFont, font_name, size, bold)
    probe = Image.new("RGBA", (4, 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(probe)
    text = str(text or "")
    try:
        box = d.textbbox((0, 0), text, font=font, stroke_width=max(0, int(stroke)))
    except Exception:
        box = (0, 0, max(1, int(len(text) * size * .62)), max(1, int(size * 1.3)))
    pad = max(3, int(stroke) + 3)
    tw, th = max(1, box[2] - box[0]), max(1, box[3] - box[1])
    sprite = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sprite)
    if bg is not None:
        sd.rounded_rectangle((0, 0, sprite.width - 1, sprite.height - 1), radius=max(1, pad),
                             fill=_faux_color(bg, bg_alpha, (0, 0, 0)))
    sd.text((pad - box[0], pad - box[1]), text, font=font,
            fill=_faux_color(color, 255), stroke_width=max(0, int(stroke)),
            stroke_fill=(0, 0, 0, 255))
    sprite = _faux_alpha_image(sprite, opacity)
    if float(rotation or 0) % 360:
        sprite = sprite.rotate(-float(rotation), expand=True, resample=Image.Resampling.BICUBIC)
    return sprite


def _faux_paste_center(layer, sprite, x, y):
    layer.alpha_composite(sprite, (int(round(x - sprite.width / 2)), int(round(y - sprite.height / 2))))


def _faux_load_image(Image, rec_dir, path, cache):
    full = _faux_asset_path(rec_dir, path)
    if not full:
        return None
    try:
        stamp = (full, os.path.getmtime(full), os.path.getsize(full))
    except Exception:
        stamp = (full, 0, 0)
    hit = cache.get(stamp)
    if hit is None:
        try:
            hit = Image.open(full).convert("RGBA")
            cache[stamp] = hit
        except Exception:
            return None
    return hit.copy()


def _faux_render_image_item(layer, props, rec_dir, pil, cache, centered=False):
    Image, ImageDraw, ImageFont, ImageOps = pil
    image = _faux_load_image(Image, rec_dir,
                             props.get("_asset_path") or props.get("image_path") or props.get("source_path"), cache)
    if image is None:
        return
    scale = max(0.001, float(props.get("_draw_scale", props.get("scale", 1.0)) or 1.0))
    nw, nh = max(1, round(image.width * scale)), max(1, round(image.height * scale))
    resample = Image.Resampling.NEAREST if props.get("pixel_perfect") else Image.Resampling.LANCZOS
    if (nw, nh) != image.size:
        image = image.resize((nw, nh), resample)
    if props.get("flip_x"):
        image = ImageOps.mirror(image)
    if props.get("flip_y"):
        image = ImageOps.flip(image)
    splice = props.get("splice") or {}
    if splice.get("enabled"):
        alpha = image.getchannel("A")
        ad = ImageDraw.Draw(alpha)
        pos = max(0.0, min(1.0, float(splice.get("pos", .5))))
        keep = splice.get("keep", "start")
        if splice.get("axis", "v") == "v":
            cut = round(image.width * pos)
            rect = (cut, 0, image.width, image.height) if keep == "start" else (0, 0, cut, image.height)
        else:
            cut = round(image.height * pos)
            rect = (0, cut, image.width, image.height) if keep == "start" else (0, 0, image.width, cut)
        ad.rectangle(rect, fill=0)
        image.putalpha(alpha)
    opacity = int(float(props.get("alpha", 255)) * int(props.get("_effective_opacity", 255)) / 255)
    image = _faux_alpha_image(image, opacity)
    sx, sy = float(props.get("_screen_x", 0)), float(props.get("_screen_y", 0))
    ax = .5 if centered else float(props.get("anchor_x", .5))
    ay = .5 if centered else float(props.get("anchor_y", .5))
    cx, cy = sx + (.5 - ax) * nw, sy + (.5 - ay) * nh
    rotation = float(props.get("rotation", 0) or 0)
    if rotation % 360:
        image = image.rotate(-rotation, expand=True, resample=Image.Resampling.BICUBIC)
    shadow = props.get("shadow") or {}
    if shadow.get("enabled"):
        a = image.getchannel("A")
        sh = Image.new("RGBA", image.size, _faux_color(shadow.get("color", (0, 0, 0)), 0, (0, 0, 0)))
        sh.putalpha(a.point(lambda v: (v * int(shadow.get("alpha", 160))) // 255))
        _faux_paste_center(layer, sh, cx + float(shadow.get("offset_x", 6)), cy + float(shadow.get("offset_y", 6)))
    _faux_paste_center(layer, image, cx, cy)


def _faux_render_bar(layer, props, rec_dir, pil, cache, custom=False):
    Image, ImageDraw, ImageFont, ImageOps = pil
    scl = max(.01, float(props.get("_draw_scale", 1.0)))
    bw, bh = max(10, int(float(props.get("w", 120)) * scl)), max(3, int(float(props.get("h", 16)) * scl))
    bar = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(bar)
    val = props.get("_smooth_val")
    if val is None: val = props.get("value", 1.0)
    maximum = max(.0001, float(props.get("max_value", 1.0) or 1.0))
    frac = max(0.0, min(1.0, float(val or 0.0) / maximum))
    radius = max(0, min(bh // 2, int(float(props.get("border_radius", 4)) * scl)))
    bg_path = props.get("bg_path") if custom else None
    fill_path = props.get("fill_path") or props.get("fill_m_path") if custom else None
    frame_path = props.get("frame_path") if custom else None
    bg_img = _faux_load_image(Image, rec_dir, bg_path, cache) if bg_path else None
    if bg_img:
        bar.alpha_composite(bg_img.resize((bw, bh), Image.Resampling.LANCZOS))
    else:
        d.rounded_rectangle((0, 0, bw - 1, bh - 1), radius=radius,
                            fill=_faux_color(props.get("bg_color", (30, 30, 40)), 255, (30, 30, 40)))
    vertical = str(props.get("orientation", "horizontal")).lower().startswith("v")
    if frac > 0:
        if vertical:
            amount = max(1, round(bh * frac)); box = (0, bh - amount, bw, bh)
        else:
            amount = max(1, round(bw * frac))
            if str(props.get("fill_direction", "left_to_right")) == "right_to_left": box = (bw - amount, 0, bw, bh)
            else: box = (0, 0, amount, bh)
        fill_img = _faux_load_image(Image, rec_dir, fill_path, cache) if fill_path else None
        if fill_img:
            full_fill = fill_img.resize((bw, bh), Image.Resampling.LANCZOS)
            bar.alpha_composite(full_fill.crop(box), (box[0], box[1]))
        else:
            d.rounded_rectangle((box[0], box[1], max(box[0], box[2] - 1), max(box[1], box[3] - 1)),
                                radius=radius, fill=_faux_color(props.get("color", (78, 210, 138)), 255, (78, 210, 138)))
    frame_img = _faux_load_image(Image, rec_dir, frame_path, cache) if frame_path else None
    if frame_img:
        bar.alpha_composite(frame_img.resize((bw, bh), Image.Resampling.LANCZOS))
    label = str(props.get("label", "") or "")
    show_text = props.get("show_text", custom)
    if show_text:
        fmt = props.get("text_format", "{value:.0f}/{max:.0f}" if custom else "{value:.0f}")
        try: text = str(fmt).format(value=float(val or 0), max=maximum, percent=frac * 100, label=label)
        except Exception: text = label or f"{float(val or 0):.0f}"
        if label and "{label" not in str(fmt): text = f"{label} {text}".strip()
        ts = _faux_text_sprite(Image, ImageDraw, ImageFont, text, max(8, int(float(props.get("text_size", bh * .72)) * scl)),
                               props.get("text_color", (255, 255, 255)), props.get("text_font_name", "segoeui"),
                               bold=True, stroke=max(0, int(props.get("text_outline_thickness", 1))))
        _faux_paste_center(bar, ts, bw / 2, bh / 2)
    bar = _faux_alpha_image(bar, props.get("_effective_opacity", 255))
    _faux_paste_center(layer, bar, float(props.get("_screen_x", 0)), float(props.get("_screen_y", 0)))


def _faux_render_node(layer, props, rec_dir, pil, cache):
    Image, ImageDraw, ImageFont, ImageOps = pil
    if not props.get("visible", True) or props.get("_group_hidden"):
        return
    kind = str(props.get("kind", "text_label"))
    x, y = float(props.get("_screen_x", 0)), float(props.get("_screen_y", 0))
    scl = max(.01, float(props.get("_draw_scale", 1.0)))
    opacity = int(props.get("_effective_opacity", 255))
    if kind == "image_node":
        return _faux_render_image_item(layer, props, rec_dir, pil, cache, centered=True)
    if kind == "text_label":
        sprite = _faux_text_sprite(Image, ImageDraw, ImageFont, props.get("text", ""),
            max(8, int(float(props.get("size", 24)) * scl)), props.get("color", (255, 255, 255)),
            props.get("font_name", "segoeui"), bold=True,
            stroke=max(1, int(2 * scl)) if props.get("outline") else 0,
            opacity=int(float(props.get("alpha", 255)) * opacity / 255), rotation=props.get("rotation", 0),
            bg=props.get("bg_color"), bg_alpha=props.get("bg_alpha", 0))
        return _faux_paste_center(layer, sprite, x, y)
    if kind == "custom_progress_bar":
        return _faux_render_bar(layer, props, rec_dir, pil, cache, custom=True)
    if kind == "progress_bar":
        return _faux_render_bar(layer, props, rec_dir, pil, cache, custom=False)
    if kind in ("counter", "timer"):
        val = props.get("_smooth_val")
        if val is None: val = props.get("value", 0)
        try: text = str(props.get("fmt", "{value}")).format(value=(f"{float(val):.2f}".rstrip("0").rstrip(".")))
        except Exception: text = str(val)
        sprite = _faux_text_sprite(Image, ImageDraw, ImageFont, text,
            max(8, int(float(props.get("size", 32)) * scl)), props.get("color", (255, 210, 60)),
            props.get("font_name", "segoeui"), bold=True,
            stroke=max(1, int(2 * scl)) if props.get("outline") else 0, opacity=opacity)
        return _faux_paste_center(layer, sprite, x, y)
    draw = ImageDraw.Draw(layer, "RGBA")
    if kind in ("line", "wall"):
        x2, y2 = float(props.get("_screen_x2", x)), float(props.get("_screen_y2", y))
        width = max(1, int(float(props.get("thickness", 8 if kind == "wall" else 2)) * (scl if kind == "wall" else 1)))
        col = _faux_color(props.get("color", (80, 80, 100)), opacity, (80, 80, 100))
        draw.line((x, y, x2, y2), fill=col, width=width)
        return
    if kind == "circle":
        r = max(2, int(float(props.get("radius", 40)) * scl)); box = (x-r, y-r, x+r, y+r)
        fa = int(float(props.get("fill_alpha", 0)) * opacity / 255)
        if fa: draw.ellipse(box, fill=_faux_color(props.get("fill_color", props.get("color", (130,105,255))), fa))
        draw.ellipse(box, outline=_faux_color(props.get("color", (130,105,255)), opacity),
                     width=max(1, int(props.get("thickness", 2))))
        return
    if kind == "grid":
        cols, rows = max(1, int(props.get("cols",4))), max(1, int(props.get("rows",4)))
        cw, ch = max(4,int(float(props.get("cell_w",40))*scl)), max(4,int(float(props.get("cell_h",40))*scl))
        ox, oy = x-cols*cw/2, y-rows*ch/2
        for key, col in (props.get("fill_data") or {}).items():
            try: c,r=(int(v) for v in str(key).split(",")[:2]); draw.rectangle((ox+c*cw,oy+r*ch,ox+(c+1)*cw,oy+(r+1)*ch),fill=_faux_color(col,opacity))
            except Exception: pass
        color=_faux_color(props.get("color",(80,80,100)),opacity); thick=max(1,int(float(props.get("thickness",1))*scl))
        for c in range(cols+1): draw.line((ox+c*cw,oy,ox+c*cw,oy+rows*ch),fill=color,width=thick)
        for r in range(rows+1): draw.line((ox,oy+r*ch,ox+cols*cw,oy+r*ch),fill=color,width=thick)
        return
    # rect_box and unknown rectangular visual nodes.
    rw, rh = max(4,int(float(props.get("w",100))*scl)), max(4,int(float(props.get("h",60))*scl))
    pad=max(4,int(float(props.get("thickness",2))*scl)*2)
    sprite=Image.new("RGBA",(rw+pad*2,rh+pad*2),(0,0,0,0)); sd=ImageDraw.Draw(sprite,"RGBA")
    rect=(pad,pad,pad+rw-1,pad+rh-1); rad=max(0,int(float(props.get("radius",6))*scl))
    fa=int(float(props.get("fill_alpha",0))*opacity/255)
    if fa: sd.rounded_rectangle(rect,radius=rad,fill=_faux_color(props.get("fill_color",props.get("color",(130,105,255))),fa))
    sd.rounded_rectangle(rect,radius=rad,outline=_faux_color(props.get("color",(130,105,255)),opacity),width=max(1,int(float(props.get("thickness",2))*scl)))
    if float(props.get("rotation",0) or 0)%360: sprite=sprite.rotate(-float(props.get("rotation",0)),expand=True,resample=Image.Resampling.BICUBIC)
    _faux_paste_center(layer,sprite,x,y)


def _faux_render_item(layer, state, rec_dir, pil, cache):
    props = state.get("props") or {}
    if not props.get("visible", True) or props.get("_group_hidden"):
        return
    typ = state.get("type")
    if typ == "text":
        Image, ImageDraw, ImageFont, ImageOps = pil
        sprite = _faux_text_sprite(Image, ImageDraw, ImageFont, props.get("text", ""),
            props.get("_pixel_size", 28), props.get("color", (255,255,255)),
            props.get("font_name", "segoeui"), bold=bool(props.get("bold",False)),
            stroke=props.get("_outline_px",0), opacity=props.get("_effective_opacity",255),
            rotation=props.get("rotation",0))
        _faux_paste_center(layer, sprite, float(props.get("_screen_x",0)), float(props.get("_screen_y",0)))
    elif typ == "image":
        _faux_render_image_item(layer, props, rec_dir, pil, cache, centered=False)
    else:
        _faux_render_node(layer, props, rec_dir, pil, cache)


def prepare_faux_overlay(rec_dir, meta, progress=None):
    """Build/reuse transparent Faux scene frames for ffmpeg overlay."""
    if not _faux_descriptor(meta):
        return None
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except Exception as exc:
        raise RuntimeError("Faux Rec export requires Pillow. Install it with: pip install Pillow") from exc
    timeline_path, data = _load_faux_timeline(rec_dir, meta)
    width = int(data.get("width") or meta.get("width") or 1920)
    height = int(data.get("height") or meta.get("height") or 1080)
    total = int(data.get("frame_count") or meta.get("frame_count") or 0)
    if total <= 0:
        raise RuntimeError("Faux Rec timeline has no frames.")
    out_dir = os.path.join(rec_dir, "faux_overlay")
    marker_path = os.path.join(out_dir, "ready.json")
    stat = os.stat(timeline_path)
    signature = {"version": FAUX_COMPOSITOR_VERSION, "timeline_size": stat.st_size,
                 "timeline_mtime_ns": stat.st_mtime_ns, "frames": total,
                 "width": width, "height": height}
    try:
        with open(marker_path, encoding="utf-8") as fh: old = json.load(fh)
        if old == signature and os.path.isfile(os.path.join(out_dir, f"overlay_{total-1:06d}.png")):
            if progress: progress(f"Faux overlay cache ready: {total} frames")
            return os.path.join(out_dir, "overlay_%06d.png")
    except Exception:
        pass
    if os.path.isdir(out_dir): shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir, exist_ok=True)
    events = {}
    for ev in data.get("events", []): events.setdefault(int(ev.get("f",0)), []).append(ev)
    states = {}; overlay_state = {"countdown": None, "fade_alpha": 0}; cache = {}
    pil = (Image, ImageDraw, ImageFont, ImageOps)
    report_step = max(1, total // 20)
    for frame in range(total):
        for ev in events.get(frame, []):
            for uid, state in (ev.get("set") or {}).items(): states[uid] = state
            for uid in ev.get("remove") or []: states.pop(uid, None)
            if isinstance(ev.get("overlay"), dict): overlay_state.update(ev["overlay"])
        layer = Image.new("RGBA", (width, height), (0,0,0,0))
        for state in sorted(states.values(), key=lambda st: (float(st.get("depth",0)), str(st.get("id","")))):
            _faux_render_item(layer, state, rec_dir, pil, cache)
        countdown = overlay_state.get("countdown")
        if countdown is not None:
            sprite = _faux_text_sprite(Image, ImageDraw, ImageFont, str(countdown),
                max(48,int(min(width,height)*.16)),(255,255,255),"segoeui",bold=True,stroke=max(4,int(min(width,height)*.004)))
            _faux_paste_center(layer,sprite,width/2,height/2)
        fade = max(0,min(255,int(overlay_state.get("fade_alpha",0) or 0)))
        if fade: ImageDraw.Draw(layer,"RGBA").rectangle((0,0,width,height),fill=(0,0,0,fade))
        layer.save(os.path.join(out_dir, f"overlay_{frame:06d}.png"), "PNG", compress_level=1)
        if progress and (frame == 0 or frame + 1 == total or (frame + 1) % report_step == 0):
            progress(f"Faux compositor: {frame+1}/{total} frames")
    with open(marker_path,"w",encoding="utf-8") as fh: json.dump(signature,fh,indent=2)
    return os.path.join(out_dir, "overlay_%06d.png")


def recording_video_path(rec_dir, meta):
    """Return a finalized GPU Recording source, or None for PNG recordings."""
    rel = (meta or {}).get("video_file") or ""
    if not rel:
        return None
    path = rel if os.path.isabs(str(rel)) else os.path.join(rec_dir, str(rel))
    try:
        return path if os.path.isfile(path) and os.path.getsize(path) > 0 else None
    except Exception:
        return None


def recording_has_visuals(rec_dir, meta):
    return bool(recording_video_path(rec_dir, meta) or
                glob.glob(os.path.join(rec_dir, "frame_*.png")))


def build_cmd(ffmpeg_bin, rec_dir, out_path, fps, width, height, crf, meta=None, include_audio=True):
    frame_glob = os.path.join(rec_dir, "frame_%06d.png")
    capture_fps = (meta or {}).get("fps") or fps
    direct_video = recording_video_path(rec_dir, meta)
    direct_info = (meta or {}).get("direct_video")
    if not isinstance(direct_info, dict):
        direct_info = {}
    # GPU Recording captures the native displayed viewport with no live
    # upscale burden. Honor its selected final resolution here, after the
    # capture has stopped, so 1440p/4K cannot make live footage choppy.
    if direct_video and not width and not height and direct_info.get("scale_deferred"):
        width = int(direct_info.get("output_width") or (meta or {}).get("width") or 0) or None
        height = int(direct_info.get("output_height") or (meta or {}).get("height") or 0) or None
    if direct_video:
        cmd = [ffmpeg_bin, "-y", "-i", direct_video]
    else:
        cmd = [ffmpeg_bin, "-y", "-framerate", str(capture_fps), "-i", frame_glob]

    overlay_glob = None
    if _faux_descriptor(meta):
        candidate = os.path.join(rec_dir, "faux_overlay", "overlay_%06d.png")
        if glob.glob(os.path.join(rec_dir, "faux_overlay", "overlay_*.png")):
            overlay_glob = candidate
            cmd += ["-framerate", str(capture_fps), "-i", overlay_glob]

    input_index = 2 if overlay_glob else 1
    audio_events = resolve_audio_events(meta, capture_fps) if include_audio else []
    bgm = resolve_bgm(meta, capture_fps) if include_audio else None
    bgm_input_idx = None
    if bgm:
        cmd += ["-stream_loop", "-1", "-i", bgm["path"]]
        bgm_input_idx = input_index; input_index += 1
    sfx_input_idx = {}; events_with_input = []
    for abs_path, delay_ms, volume, pitch in audio_events:
        idx = sfx_input_idx.get(abs_path)
        if idx is None:
            cmd += ["-i", abs_path]; idx = input_index; input_index += 1; sfx_input_idx[abs_path] = idx
        events_with_input.append((idx, delay_ms, volume, pitch))

    vf = None
    if width or height:
        _scale_flags="lanczos"
        if direct_video and direct_info.get("upscale_method")=="crisp":
            try:
                _cw=int(direct_info.get("capture_width") or 0);_ch=int(direct_info.get("capture_height") or 0)
                if (not width or int(width)>=_cw) and (not height or int(height)>=_ch):_scale_flags="neighbor"
            except Exception:pass
        if width and height:
            vf = (f"scale={width}:{height}:flags={_scale_flags}:force_original_aspect_ratio=decrease,"
                  f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black")
        elif width: vf = f"scale={width}:-2:flags={_scale_flags}"
        else: vf = f"scale=-2:{height}:flags={_scale_flags}"

    filters=[]; video_label=None
    if overlay_glob:
        filters.append("[0:v][1:v]overlay=0:0:format=auto[vfaux]"); video_label="vfaux"
    if direct_video and direct_info.get("portrait_rotated"):
        src=f"[{video_label}]" if video_label else "[0:v]"
        filters.append(f"{src}transpose=cclock[vportrait]"); video_label="vportrait"
    if vf:
        src=f"[{video_label}]" if video_label else "[0:v]"
        filters.append(f"{src}{vf}[vout]"); video_label="vout"

    mix_labels=[]
    if bgm:
        chain=f"volume={bgm['volume']:.4f}"
        if bgm.get("start_ms",0)>0: chain += f",adelay={int(bgm['start_ms'])}:all=1"
        if bgm.get("fade"):
            fade=bgm["fade"]; chain += f",afade=t=out:st={fade['start_ms']/1000.0:.6f}:d={fade['duration']:.6f}"
        if bgm.get("stop_ms") is not None: chain += f",atrim=duration={bgm['stop_ms']/1000.0:.6f}"
        filters.append(f"[{bgm_input_idx}:a]{chain}[bgm]"); mix_labels.append("[bgm]")
    for idx,(in_idx,delay_ms,volume,pitch) in enumerate(events_with_input):
        chain=f"volume={volume:.4f}"
        if abs(pitch-1.0)>0.001: chain += f",asetrate=44100*{pitch:.6f},aresample=44100"
        chain += f",adelay={delay_ms}:all=1"
        label=f"a{idx}"; filters.append(f"[{in_idx}:a]{chain}[{label}]"); mix_labels.append(f"[{label}]")
    if mix_labels:
        filters.append(f"{''.join(mix_labels)}amix=inputs={len(mix_labels)}:normalize=0:duration=longest:dropout_transition=0[aout]")

    if filters: cmd += ["-filter_complex",";".join(filters)]
    cmd += ["-map",f"[{video_label}]" if video_label else "0:v"]
    if mix_labels:
        cmd += ["-map", "[aout]"]
        # Only an infinitely-looped BGM needs -shortest. Using it for finite
        # SFX alone could cut the video off as soon as the final sound ended.
        if bgm:
            cmd += ["-shortest"]
    # GPU Recording is already H.264. With native size/fps and no visual filter,
    # copy it bit-for-bit while muxing audio instead of encoding it a second time.
    try:
        same_fps = int(fps) == int(capture_fps)
    except Exception:
        same_fps = False
    copy_video = bool(direct_video and not video_label and not vf and same_fps)
    if copy_video:
        cmd += ["-c:v", "copy"]
    else:
        cmd += ["-r",str(fps),"-c:v","libx264","-pix_fmt","yuv420p","-crf",str(crf)]
    if mix_labels: cmd += ["-c:a","aac","-b:a","192k"]
    if str(out_path).lower().endswith(".mp4"): cmd += ["-movflags", "+faststart"]
    cmd += [out_path]
    return cmd


def _pause_before_exit():
    """Keeps a double-clicked console window open long enough to actually
    read the error, instead of it flashing shut the instant the script
    exits. No-op when stdin isn't a real interactive console (e.g. run
    from another script or CI)."""
    try:
        if sys.stdin.isatty():
            input("\nPress Enter to close...")
    except Exception:
        pass


def main_cli():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rec", help="Recording folder name (e.g. rec_20260710_141230) or full path. Defaults to most recent.")
    ap.add_argument("rec_positional", nargs="?", help="Recording folder (positional alternative to --rec, accepts full path)")
    ap.add_argument("--list", action="store_true", help="List available recordings and exit")
    ap.add_argument("--out", help="Output .mp4 path. Defaults to <rec_name>.mp4 in this folder.")
    ap.add_argument("--width", type=int, help="Output width in pixels. Defaults to captured resolution.")
    ap.add_argument("--height", type=int, help="Output height in pixels. Defaults to captured resolution.")
    ap.add_argument("--fps", type=int, help="Output frame rate. Defaults to capture rate (usually 60).")
    ap.add_argument("--crf", type=int, default=18, help="Video quality (lower = better/larger, 0-51). Default 18.")
    ap.add_argument("--ffmpeg", help=r"Path to ffmpeg(.exe) or folder containing it, if not on PATH. Remembered for next time once you give it.")
    ap.add_argument("--gui", action="store_true", help="Open picker window instead of using CLI.")
    ap.add_argument("--auto-gpu-audio", action="store_true", help="Arena Studio background job: finalize deferred GPU resolution and embed metadata audio into video.mp4.")
    args = ap.parse_args()

    if args.gui:
        main_gui()
        return

    recs=list_recordings();_explicit_rec=bool(args.rec or args.rec_positional)
    if args.list or (not recs and not _explicit_rec):
        if not recs:print(f"No recordings found in {RECORDINGS_DIR}")
        else:
            print("Available recordings:")
            for r in recs:
                meta=load_meta(r)
                if meta.get("rendered",True):status="ready · GPU Recording" if recording_video_path(r,meta) else ("ready · Legacy metadata" if _faux_descriptor(meta) else "ready")
                else:status="PENDING -- not rendered yet, open box_game.py"
                print(" -",os.path.basename(r),"|",meta.get("frame_count","?"),"frames","|",status)
        return

    # Support both --rec and positional arg, and full path vs folder name
    rec_arg = args.rec or args.rec_positional
    if rec_arg:
        # If it's a full path and exists, use it directly
        if os.path.isdir(rec_arg):
            rec_dir = rec_arg
        else:
            # Try as folder name inside RECORDINGS_DIR
            candidate = os.path.join(RECORDINGS_DIR, rec_arg)
            if os.path.isdir(candidate):
                rec_dir = candidate
            else:
                # Try basename if full path was given but RECORDINGS_DIR join failed
                # e.g., C:\...\recordings\GUIDEvsEYE_... -> basename = GUIDEvsEYE_...
                base = os.path.basename(rec_arg.rstrip("/\\"))
                candidate2 = os.path.join(RECORDINGS_DIR, base)
                if os.path.isdir(candidate2):
                    rec_dir = candidate2
                else:
                    # Last resort: use rec_arg as is if it exists
                    rec_dir = rec_arg
    else:
        rec_dir = recs[-1]

    if not os.path.isdir(rec_dir):
        print(f"Recording not found: {rec_dir}")
        print(f"Try: python {os.path.basename(__file__)} --list to see available")
        sys.exit(1)

    meta = load_meta(rec_dir)
    if not meta.get("rendered", True):
        if meta.get("record_mode") == "stream":
            print(f"'{os.path.basename(rec_dir)}' has an incomplete GPU Recording capture. Check window_capture_ffmpeg.log in that recording folder.")
        else:
            print(f"'{os.path.basename(rec_dir)}' is an interpolated recording that hasn't been rendered yet. Open box_game.py -> Win Conditions -> Recording -> Pending Recordings and click Render first.")
        sys.exit(1)
    fps=args.fps or meta.get("fps") or 60
    out_path=(os.path.join(rec_dir,"video.mp4") if args.auto_gpu_audio else args.out or os.path.join(os.path.dirname(RECORDINGS_DIR),f"{os.path.basename(rec_dir)}.mp4"))

    if not recording_has_visuals(rec_dir, meta):
        print(f"No PNG frames or GPU Recording source found in {rec_dir}")
        sys.exit(1)

    ffmpeg_bin = resolve_ffmpeg(args.ffmpeg)
    if not ffmpeg_bin:
        print("\nffmpeg was not found on your PATH, and none is remembered yet.")
        print("If you have it installed somewhere, just point at it once:")
        print(r'  python rec.py --ffmpeg "C:\path\to\ffmpeg\bin\ffmpeg.exe"')
        print("  (or just the folder containing ffmpeg.exe/ffmpeg -- it'll find the binary)")
        print("It'll be remembered automatically after that. Or run with --gui to browse for it.")
        print("\nOr install ffmpeg properly:")
        print("  Windows:  winget install ffmpeg")
        print("  macOS:    brew install ffmpeg")
        print("  Linux:    sudo apt install ffmpeg")
        sys.exit(1)

    ok, why = verify_ffmpeg_runnable(ffmpeg_bin)
    if not ok:
        print(f"\n{why}")
        sys.exit(1)

    if _faux_descriptor(meta):
        try:
            prepare_faux_overlay(rec_dir, meta, progress=print)
        except Exception as exc:
            print(f"Faux Rec compositor failed: {exc}")
            _pause_before_exit()
            sys.exit(1)
    cmd = build_cmd(ffmpeg_bin, rec_dir, out_path, fps, args.width, args.height, args.crf, meta=meta)

    print("Running:", " ".join(f'"{c}"' if " " in c else c for c in cmd))
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        tail = []
        for line in proc.stdout:
            print(line, end="")
            tail.append(line)
            tail = tail[-40:]
        proc.wait()
        if proc.returncode != 0:
            print(f"\nffmpeg failed with exit code {proc.returncode}. Last output above ^ is the actual reason.")
            _pause_before_exit()
            sys.exit(proc.returncode)
    except FileNotFoundError:
        print(f"\nCouldn't run ffmpeg at: {ffmpeg_bin}")
        print("Double-check that path points at the actual ffmpeg executable.")
        _pause_before_exit()
        sys.exit(1)

    if args.auto_gpu_audio:
        try:
            meta_path=os.path.join(rec_dir,"meta.json")
            with open(meta_path,encoding="utf-8") as fh:finished_meta=json.load(fh)
            finished_meta["video_file"]="video.mp4";finished_meta["gpu_audio_embedded"]=True
            direct=finished_meta.get("direct_video")
            if isinstance(direct,dict):
                direct["audio_deferred"]=False;direct["audio_embedded"]=True
                if direct.get("scale_deferred"):
                    direct["scale_deferred"]=False;direct["scale_applied"]=True
                    direct["final_width"]=int(direct.get("output_width") or finished_meta.get("width") or 0)
                    direct["final_height"]=int(direct.get("output_height") or finished_meta.get("height") or 0)
            with open(meta_path,"w",encoding="utf-8") as fh:json.dump(finished_meta,fh,indent=2)
        except Exception as exc:print("Could not mark embedded audio:",exc)
    print(f"\nDone: {out_path}")
    if not args.auto_gpu_audio:_pause_before_exit()


def recording_frame_paths(rec_dir):
    """Numerically ordered CPU Recording frames, including older unpadded names."""
    def _frame_number(path):
        match = re.search(r"(\d+)(?=\.png$)", os.path.basename(path), re.IGNORECASE)
        return int(match.group(1)) if match else 10**18
    return sorted(glob.glob(os.path.join(rec_dir, "frame_*.png")),
                  key=lambda p: (_frame_number(p), p.lower()))


def scan_recording_folder(folder):
    """Return recording directories from a library folder or one recording itself."""
    folder = os.path.abspath(os.path.expanduser(str(folder or "")))
    if not os.path.isdir(folder):
        return []
    if (os.path.isfile(os.path.join(folder, "meta.json")) or
            glob.glob(os.path.join(folder, "frame_*.png"))):
        return [folder]
    result = []
    try:
        names = os.listdir(folder)
    except OSError:
        return []
    for name in names:
        candidate = os.path.join(folder, name)
        if not os.path.isdir(candidate):
            continue
        if (os.path.isfile(os.path.join(candidate, "meta.json")) or
                glob.glob(os.path.join(candidate, "frame_*.png"))):
            result.append(candidate)
    return result


def ffmpeg_progress_frame(line):
    """Extract an encoded frame number from -progress or ordinary ffmpeg status."""
    text = str(line or "").strip()
    match = re.match(r"frame\s*=\s*(\d+)", text)
    return int(match.group(1)) if match else None


def main_gui():
    import datetime
    import threading
    import time
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    try:
        from PIL import Image, ImageTk
    except Exception:
        Image = ImageTk = None

    # Restrained late-90s workstation shell: familiar raised controls, compact
    # information density, and Arena's violet/amber identity in the title/status.
    FACE = "#c6c8cc"
    FACE_2 = "#d7d9dc"
    LIGHT = "#f5f6f7"
    SHADOW = "#6c7077"
    INK = "#101216"
    DIM = "#4b5058"
    NAVY = "#17264d"
    NAVY_2 = "#24386f"
    VIOLET = "#6750c8"
    AMBER = "#d99b32"
    GOOD = "#176f3a"
    WARN = "#8a5b00"
    BAD = "#9c2525"
    PREVIEW_BG = "#080a10"
    WHITE = "#ffffff"
    MONO = ("Courier New", 9)
    UI_FONT = ("Tahoma", 9)
    UI_BOLD = ("Tahoma", 9, "bold")

    root = tk.Tk()
    root.title("Arena Studio - CPU Recording Workstation")
    root.configure(bg=FACE)
    root.geometry("1180x790")
    root.minsize(980, 680)

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure("Retro.Treeview", background=WHITE, foreground=INK,
                    fieldbackground=WHITE, rowheight=22, borderwidth=1,
                    font=UI_FONT)
    style.map("Retro.Treeview", background=[("selected", NAVY_2)],
              foreground=[("selected", WHITE)])
    style.configure("Retro.Treeview.Heading", background=FACE_2, foreground=INK,
                    relief="raised", borderwidth=1, font=UI_BOLD, padding=(4, 4))
    style.map("Retro.Treeview.Heading", background=[("active", LIGHT)])
    style.configure("Retro.TCombobox", fieldbackground=WHITE, foreground=INK,
                    background=FACE_2, arrowcolor=INK, padding=2, font=UI_FONT)
    style.map("Retro.TCombobox", fieldbackground=[("readonly", WHITE)],
              foreground=[("readonly", INK)])
    style.configure("Retro.Horizontal.TProgressbar", troughcolor=WHITE,
                    background=VIOLET, lightcolor="#907ee0", darkcolor="#45329b",
                    bordercolor=SHADOW, thickness=17)
    style.configure("Retro.Vertical.TScrollbar", background=FACE_2,
                    troughcolor=LIGHT, arrowcolor=INK, bordercolor=SHADOW)

    def raised_button(parent, text, command=None, width=None, accent=False, state="normal"):
        return tk.Button(parent, text=text, command=command, width=width,
                         bg=(AMBER if accent else FACE_2), fg=INK,
                         activebackground=("#efb955" if accent else LIGHT),
                         activeforeground=INK, disabledforeground="#777b82",
                         relief="raised", bd=2, padx=8, pady=3,
                         font=UI_BOLD if accent else UI_FONT, state=state,
                         highlightthickness=0)

    def sunken_entry(parent, variable, width=None):
        return tk.Entry(parent, textvariable=variable, width=width, bg=WHITE, fg=INK,
                        insertbackground=INK, relief="sunken", bd=2, font=UI_FONT)

    def group(parent, title):
        return tk.LabelFrame(parent, text=" " + title + " ", bg=FACE, fg=INK,
                             font=UI_BOLD, relief="groove", bd=2, padx=7, pady=7)

    cfg = load_config()
    last_env = os.environ.get("BOX_GAME_LAST_RECORDING", "")
    default_library = cfg.get("recordings_folder") or RECORDINGS_DIR
    if last_env and os.path.isdir(last_env):
        default_library = os.path.dirname(os.path.abspath(last_env))
    if not os.path.isdir(default_library):
        default_library = RECORDINGS_DIR

    # ---- menu -----------------------------------------------------------------
    menu = tk.Menu(root, tearoff=False, bg=FACE_2, fg=INK, activebackground=NAVY_2,
                   activeforeground=WHITE, font=UI_FONT)
    file_menu = tk.Menu(menu, tearoff=False, bg=FACE_2, fg=INK,
                        activebackground=NAVY_2, activeforeground=WHITE, font=UI_FONT)
    view_menu = tk.Menu(menu, tearoff=False, bg=FACE_2, fg=INK,
                        activebackground=NAVY_2, activeforeground=WHITE, font=UI_FONT)
    play_menu = tk.Menu(menu, tearoff=False, bg=FACE_2, fg=INK,
                        activebackground=NAVY_2, activeforeground=WHITE, font=UI_FONT)
    menu.add_cascade(label="File", menu=file_menu)
    menu.add_cascade(label="View", menu=view_menu)
    menu.add_cascade(label="Playback", menu=play_menu)
    root.configure(menu=menu)

    # ---- title strip -----------------------------------------------------------
    titlebar = tk.Frame(root, bg=NAVY, height=50, relief="raised", bd=2)
    titlebar.pack(fill="x")
    titlebar.pack_propagate(False)
    tk.Frame(titlebar, bg=VIOLET, width=8).pack(side="left", fill="y")
    title_text = tk.Frame(titlebar, bg=NAVY)
    title_text.pack(side="left", fill="both", expand=True, padx=10)
    tk.Label(title_text, text="ARENA STUDIO  //  CPU RECORDING WORKSTATION",
             bg=NAVY, fg=WHITE, font=("Tahoma", 12, "bold")).pack(anchor="w", pady=(6, 0))
    tk.Label(title_text, text="FRAME SEQUENCE COMPILER + REPLAY DECK",
             bg=NAVY, fg="#bac6e7", font=("Tahoma", 8)).pack(anchor="w")
    tk.Label(titlebar, text="REC.EXE", bg=NAVY_2, fg=AMBER,
             font=("Courier New", 10, "bold"), relief="sunken", bd=1,
             padx=10, pady=5).pack(side="right", padx=10)

    # ---- recording library path -----------------------------------------------
    folder_bar = tk.Frame(root, bg=FACE, relief="raised", bd=1, padx=7, pady=6)
    folder_bar.pack(fill="x")
    tk.Label(folder_bar, text="RECORDING LIBRARY", bg=FACE, fg=INK,
             font=UI_BOLD).pack(side="left", padx=(0, 7))
    library_var = tk.StringVar(value=os.path.abspath(default_library))
    library_entry = sunken_entry(folder_bar, library_var)
    library_entry.pack(side="left", fill="x", expand=True)

    # ---- main split ------------------------------------------------------------
    body = tk.PanedWindow(root, orient="horizontal", bg=SHADOW, sashwidth=5,
                          sashrelief="raised", bd=1)
    body.pack(fill="both", expand=True, padx=5, pady=5)
    left = tk.Frame(body, bg=FACE, relief="raised", bd=2, padx=6, pady=6)
    right = tk.Frame(body, bg=FACE, relief="raised", bd=2, padx=6, pady=6)
    body.add(left, minsize=430, width=500)
    body.add(right, minsize=510)

    # ---- left: recording browser ----------------------------------------------
    browser = group(left, "RECORDINGS")
    browser.pack(fill="both", expand=True)
    browser.grid_rowconfigure(1, weight=1)
    browser.grid_columnconfigure(0, weight=1)

    browse_tools = tk.Frame(browser, bg=FACE)
    browse_tools.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
    tk.Label(browse_tools, text="Sort:", bg=FACE, fg=INK, font=UI_FONT).pack(side="left")
    sort_choices = ("Date created - newest", "Date created - oldest",
                    "Modified - newest", "Name A-Z", "Name Z-A",
                    "Frame count - most", "Duration - longest")
    sort_var = tk.StringVar(value=cfg.get("recording_sort", sort_choices[0]))
    if sort_var.get() not in sort_choices:
        sort_var.set(sort_choices[0])
    sort_combo = ttk.Combobox(browse_tools, textvariable=sort_var, values=sort_choices,
                              state="readonly", style="Retro.TCombobox", width=23)
    sort_combo.pack(side="left", padx=(5, 5))

    columns = ("created", "frames", "length", "mode", "state")
    tree = ttk.Treeview(browser, columns=columns, show="tree headings",
                        selectmode="browse", style="Retro.Treeview")
    tree.heading("#0", text="Recording")
    tree.heading("created", text="Created")
    tree.heading("frames", text="Frames")
    tree.heading("length", text="Length")
    tree.heading("mode", text="Mode")
    tree.heading("state", text="State")
    tree.column("#0", width=185, minwidth=120, stretch=True)
    tree.column("created", width=122, minwidth=105, anchor="w")
    tree.column("frames", width=58, minwidth=48, anchor="e")
    tree.column("length", width=58, minwidth=50, anchor="e")
    tree.column("mode", width=58, minwidth=50, anchor="center")
    tree.column("state", width=66, minwidth=58, anchor="center")
    tree_scroll = ttk.Scrollbar(browser, orient="vertical", command=tree.yview,
                                style="Retro.Vertical.TScrollbar")
    tree.configure(yscrollcommand=tree_scroll.set)
    tree.grid(row=1, column=0, sticky="nsew")
    tree_scroll.grid(row=1, column=1, sticky="ns")

    details_var = tk.StringVar(value="Select a recording.")
    details = tk.Label(browser, textvariable=details_var, bg=LIGHT, fg=DIM,
                       relief="sunken", bd=2, anchor="w", justify="left",
                       padx=6, pady=5, font=("Tahoma", 8), wraplength=440)
    details.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 0))

    # FFmpeg remains visible and editable, as in the original utility.
    ff_group = group(left, "FFMPEG ENGINE")
    ff_group.pack(fill="x", pady=(6, 0))
    ffmpeg_var = tk.StringVar(value=resolve_ffmpeg(None) or "")
    ff_entry = sunken_entry(ff_group, ffmpeg_var)
    ff_entry.pack(side="left", fill="x", expand=True)

    # Compact event log, intentionally like a period workstation console.
    log_group = group(left, "JOB LOG")
    log_group.pack(fill="both", pady=(6, 0))
    log = tk.Text(log_group, height=8, bg="#111318", fg="#c8d1e6",
                  insertbackground=WHITE, relief="sunken", bd=2, font=MONO,
                  wrap="word", state="disabled", padx=5, pady=4)
    log_scroll = tk.Scrollbar(log_group, orient="vertical", command=log.yview,
                              bg=FACE_2, troughcolor=LIGHT, relief="raised", bd=1)
    log.configure(yscrollcommand=log_scroll.set)
    log.pack(side="left", fill="both", expand=True)
    log_scroll.pack(side="right", fill="y")

    def log_line(text):
        if not root.winfo_exists():
            return
        stamp = time.strftime("%H:%M:%S")
        log.configure(state="normal")
        log.insert("end", f"[{stamp}] {text}\n")
        log.see("end")
        log.configure(state="disabled")

    # ---- right: monitor/replay -------------------------------------------------
    monitor = group(right, "FRAME MONITOR / IN-APP REPLAY")
    monitor.pack(fill="both", expand=True)
    monitor.grid_rowconfigure(0, weight=1)
    monitor.grid_columnconfigure(0, weight=1)
    preview_canvas = tk.Canvas(monitor, bg=PREVIEW_BG, highlightbackground=SHADOW,
                               highlightthickness=2, bd=0, height=330)
    preview_canvas.grid(row=0, column=0, sticky="nsew")
    preview_caption_var = tk.StringVar(value="NO FRAME LOADED")
    preview_caption = tk.Label(monitor, textvariable=preview_caption_var,
                               bg="#171a22", fg="#d6dced", relief="sunken", bd=1,
                               font=("Courier New", 9), anchor="w", padx=6, pady=3)
    preview_caption.grid(row=1, column=0, sticky="ew", pady=(4, 0))

    player_controls = tk.Frame(monitor, bg=FACE)
    player_controls.grid(row=2, column=0, sticky="ew", pady=(6, 0))
    player_controls.grid_columnconfigure(5, weight=1)
    first_btn = raised_button(player_controls, "|<", width=3)
    prev_btn = raised_button(player_controls, "<", width=3)
    play_btn = raised_button(player_controls, "PLAY", width=7, accent=True)
    next_btn = raised_button(player_controls, ">", width=3)
    last_btn = raised_button(player_controls, ">|", width=3)
    first_btn.grid(row=0, column=0, padx=(0, 3))
    prev_btn.grid(row=0, column=1, padx=3)
    play_btn.grid(row=0, column=2, padx=3)
    next_btn.grid(row=0, column=3, padx=3)
    last_btn.grid(row=0, column=4, padx=3)
    scrub_var = tk.DoubleVar(value=0)
    scrub = tk.Scale(player_controls, from_=0, to=0, orient="horizontal",
                     variable=scrub_var, showvalue=False, resolution=1,
                     bg=FACE, fg=INK, troughcolor=WHITE, activebackground=VIOLET,
                     highlightthickness=0, bd=1, sliderlength=14)
    scrub.grid(row=0, column=5, sticky="ew", padx=(8, 6))
    speed_var = tk.StringVar(value="1.0x")
    speed_combo = ttk.Combobox(player_controls, textvariable=speed_var,
                               values=("0.25x", "0.5x", "1.0x", "1.5x", "2.0x"),
                               state="readonly", width=6, style="Retro.TCombobox")
    speed_combo.grid(row=0, column=6)
    loop_var = tk.BooleanVar(value=False)
    tk.Checkbutton(player_controls, text="Loop", variable=loop_var, bg=FACE, fg=INK,
                   activebackground=FACE, selectcolor=WHITE, font=UI_FONT).grid(row=0, column=7, padx=(6, 0))

    player = {"frames": [], "index": 0, "playing": False, "job": None,
              "photo": None, "scrub_internal": False, "meta": {},
              "last_drawn": None, "resize_job": None}

    def preview_message(title, subtitle=""):
        preview_canvas.delete("all")
        w = max(320, preview_canvas.winfo_width())
        h = max(180, preview_canvas.winfo_height())
        preview_canvas.create_rectangle(8, 8, w-8, h-8, outline="#343b4d", width=1)
        preview_canvas.create_text(w/2, h/2-8, text=title, fill="#d0d6e5",
                                   font=("Courier New", 13, "bold"))
        if subtitle:
            preview_canvas.create_text(w/2, h/2+18, text=subtitle, fill="#77839e",
                                       font=("Courier New", 9))
        player["photo"] = None
        player["last_drawn"] = None

    def draw_frame(index, reason="REPLAY", force=False):
        frames = player.get("frames") or []
        if not frames:
            preview_message("NO CPU FRAMES", "Select a rendered CPU Recording")
            preview_caption_var.set("NO FRAME SEQUENCE AVAILABLE")
            return
        index = max(0, min(len(frames)-1, int(index)))
        path = frames[index]
        w = max(320, preview_canvas.winfo_width())
        h = max(180, preview_canvas.winfo_height())
        signature = (path, w//8, h//8)
        if not force and player.get("last_drawn") == signature:
            player["index"] = index
            return
        try:
            if Image is not None and ImageTk is not None:
                with Image.open(path) as source:
                    image = source.convert("RGB")
                image.thumbnail((max(40, w-18), max(40, h-18)), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
            else:
                photo = tk.PhotoImage(file=path)
                sx = max(1, math.ceil(photo.width() / max(40, w-18)))
                sy = max(1, math.ceil(photo.height() / max(40, h-18)))
                factor = max(sx, sy)
                if factor > 1:
                    photo = photo.subsample(factor, factor)
            preview_canvas.delete("all")
            preview_canvas.create_image(w/2, h/2, image=photo, anchor="center")
            preview_canvas.create_rectangle(5, 5, w-5, h-5, outline="#343b4d", width=1)
            preview_canvas.create_text(12, 11, text=reason, anchor="nw", fill=AMBER,
                                       font=("Courier New", 9, "bold"))
            player["photo"] = photo
            player["last_drawn"] = signature
            player["index"] = index
            player["scrub_internal"] = True
            scrub_var.set(index)
            player["scrub_internal"] = False
            preview_caption_var.set(
                f"{reason}  //  FRAME {index+1:06d} / {len(frames):06d}  //  {os.path.basename(path)}")
        except Exception as exc:
            preview_message("FRAME READ ERROR", str(exc)[:90])
            preview_caption_var.set(f"Could not display {os.path.basename(path)}")

    def cancel_player_job():
        job = player.get("job")
        if job is not None:
            try:
                root.after_cancel(job)
            except Exception:
                pass
        player["job"] = None

    def pause_playback():
        player["playing"] = False
        cancel_player_job()
        play_btn.configure(text="PLAY")

    def stop_playback(reset=False):
        pause_playback()
        if reset and player.get("frames"):
            draw_frame(0, "REPLAY")

    def playback_delay_ms():
        fps = float((player.get("meta") or {}).get("fps") or 60)
        try:
            speed = float(speed_var.get().rstrip("x"))
        except Exception:
            speed = 1.0
        return max(1, int(round(1000.0 / max(1.0, fps * speed))))

    def playback_tick():
        if not player.get("playing"):
            return
        started = time.perf_counter()
        frames = player.get("frames") or []
        if not frames:
            pause_playback()
            return
        index = int(player.get("index", 0))
        draw_frame(index, "REPLAY")
        if index >= len(frames)-1:
            if loop_var.get():
                next_index = 0
            else:
                pause_playback()
                return
        else:
            next_index = index + 1
        elapsed_ms = int((time.perf_counter()-started)*1000)
        def advance():
            if player.get("playing"):
                player["index"] = next_index
                playback_tick()
        player["job"] = root.after(max(1, playback_delay_ms()-elapsed_ms), advance)

    def toggle_playback():
        if not player.get("frames"):
            messagebox.showinfo("No frame sequence", "This recording has no CPU PNG frames to replay in-app.")
            return
        if player.get("playing"):
            pause_playback()
        else:
            player["playing"] = True
            play_btn.configure(text="PAUSE")
            playback_tick()

    def step_frame(amount):
        pause_playback()
        frames = player.get("frames") or []
        if frames:
            draw_frame(max(0, min(len(frames)-1, int(player.get("index", 0))+amount)), "REPLAY")

    def scrub_changed(value):
        if player.get("scrub_internal") or not player.get("frames"):
            return
        pause_playback()
        draw_frame(int(float(value)), "SCRUB")

    first_btn.configure(command=lambda: (pause_playback(), draw_frame(0, "REPLAY")) if player.get("frames") else None)
    prev_btn.configure(command=lambda: step_frame(-1))
    play_btn.configure(command=toggle_playback)
    next_btn.configure(command=lambda: step_frame(1))
    last_btn.configure(command=lambda: (pause_playback(), draw_frame(len(player["frames"])-1, "REPLAY")) if player.get("frames") else None)
    scrub.configure(command=scrub_changed)

    def preview_resized(_event=None):
        if player.get("resize_job") is not None:
            try: root.after_cancel(player["resize_job"])
            except Exception: pass
        if player.get("frames"):
            player["resize_job"] = root.after(120, lambda: draw_frame(player.get("index",0), "REPLAY", True))

    preview_canvas.bind("<Configure>", preview_resized)

    # ---- right: export controls ------------------------------------------------
    export_group = group(right, "EXPORT VIDEO")
    export_group.pack(fill="x", pady=(6, 0))
    export_group.grid_columnconfigure(1, weight=1)

    tk.Label(export_group, text="Save as:", bg=FACE, fg=INK, font=UI_FONT).grid(row=0, column=0, sticky="w")
    out_var = tk.StringVar(value="")
    out_entry = sunken_entry(export_group, out_var)
    out_entry.grid(row=0, column=1, columnspan=5, sticky="ew", padx=(6, 5))

    tk.Label(export_group, text="Width:", bg=FACE, fg=INK, font=UI_FONT).grid(row=1, column=0, sticky="w", pady=(6,0))
    width_var = tk.StringVar()
    sunken_entry(export_group, width_var, 7).grid(row=1, column=1, sticky="w", padx=(6,12), pady=(6,0))
    tk.Label(export_group, text="Height:", bg=FACE, fg=INK, font=UI_FONT).grid(row=1, column=2, sticky="e", pady=(6,0))
    height_var = tk.StringVar()
    sunken_entry(export_group, height_var, 7).grid(row=1, column=3, sticky="w", padx=(6,12), pady=(6,0))
    tk.Label(export_group, text="FPS:", bg=FACE, fg=INK, font=UI_FONT).grid(row=1, column=4, sticky="e", pady=(6,0))
    fps_var = tk.StringVar()
    sunken_entry(export_group, fps_var, 6).grid(row=1, column=5, sticky="w", padx=(6,0), pady=(6,0))

    preset_row = tk.Frame(export_group, bg=FACE)
    preset_row.grid(row=2, column=0, columnspan=6, sticky="ew", pady=(6,0))
    tk.Label(preset_row, text="FPS presets:", bg=FACE, fg=DIM, font=("Tahoma",8)).pack(side="left")
    for preset in (24,30,60,120):
        raised_button(preset_row, str(preset), lambda v=preset: fps_var.set(str(v)), width=3).pack(side="left", padx=(4,0))
    tk.Label(preset_row, text="  CRF:", bg=FACE, fg=DIM, font=("Tahoma",8)).pack(side="left", padx=(8,0))
    crf_var = tk.StringVar(value="18")
    sunken_entry(preset_row, crf_var, 4).pack(side="left", padx=(4,0))
    tk.Label(preset_row, text=" lower = better", bg=FACE, fg=DIM, font=("Tahoma",8)).pack(side="left")
    include_audio_var = tk.BooleanVar(value=True)
    tk.Checkbutton(preset_row, text="Mix recorded audio", variable=include_audio_var,
                   bg=FACE, fg=INK, activebackground=FACE, selectcolor=WHITE,
                   font=UI_FONT).pack(side="right")

    export_progress = ttk.Progressbar(export_group, orient="horizontal", mode="determinate",
                                      style="Retro.Horizontal.TProgressbar", maximum=100)
    export_progress.grid(row=3, column=0, columnspan=6, sticky="ew", pady=(8,2))
    compile_var = tk.StringVar(value="IDLE // READY FOR JOB")
    tk.Label(export_group, textvariable=compile_var, bg=FACE, fg=NAVY,
             font=("Courier New", 9, "bold"), anchor="w").grid(
                 row=4, column=0, columnspan=6, sticky="ew")

    action_row = tk.Frame(export_group, bg=FACE)
    action_row.grid(row=5, column=0, columnspan=6, sticky="ew", pady=(7,0))
    export_btn = raised_button(action_row, "EXPORT VIDEO", accent=True, state="disabled")
    cancel_btn = raised_button(action_row, "CANCEL JOB", state="disabled")
    open_video_btn = raised_button(action_row, "OPEN VIDEO", state="disabled")
    open_folder_btn = raised_button(action_row, "OPEN RECORDING")
    export_btn.pack(side="left")
    cancel_btn.pack(side="left", padx=(6,0))
    open_video_btn.pack(side="left", padx=(6,0))
    open_folder_btn.pack(side="right")

    # ---- status bar ------------------------------------------------------------
    status_frame = tk.Frame(root, bg=FACE, relief="sunken", bd=2, height=24)
    status_frame.pack(fill="x", side="bottom", padx=3, pady=(0,3))
    status_var = tk.StringVar(value="READY")
    status_label = tk.Label(status_frame, textvariable=status_var, bg=FACE, fg=INK,
                            anchor="w", font=("Tahoma",8), padx=5)
    status_label.pack(side="left", fill="x", expand=True)
    tk.Label(status_frame, text="ARENA/CPU", bg=NAVY, fg=AMBER,
             relief="sunken", bd=1, font=("Courier New",8,"bold"), padx=8).pack(side="right")

    # ---- library model + selection --------------------------------------------
    entries = []
    entry_by_iid = {}

    def safe_meta(path):
        try:
            return load_meta(path)
        except Exception as exc:
            return {"rendered":False, "frame_count":0, "frames_on_disk":0,
                    "fps":60, "_error":str(exc)}

    def build_entry(path):
        meta = safe_meta(path)
        try: created = os.path.getctime(path)
        except OSError: created = 0.0
        try: modified = os.path.getmtime(os.path.join(path,"meta.json"))
        except OSError:
            try: modified = os.path.getmtime(path)
            except OSError: modified = 0.0
        disk_frames = int(meta.get("frames_on_disk") or 0)
        logical_frames = int(meta.get("frame_count") or disk_frames or 0)
        display_frames = disk_frames or logical_frames
        fps = float(meta.get("fps") or 60)
        duration = logical_frames / max(1.0, fps)
        direct = recording_video_path(path, meta)
        mode = "GPU" if direct or meta.get("record_mode")=="stream" else ("FAUX" if _faux_descriptor(meta) else "CPU")
        ready = bool(meta.get("rendered", True) and recording_has_visuals(path, meta))
        state = "READY" if ready else "PENDING"
        return {"path":path,"name":os.path.basename(path),"meta":meta,
                "created":created,"modified":modified,"frames":display_frames,
                "logical_frames":logical_frames,"duration":duration,"mode":mode,
                "ready":ready,"state":state}

    def sort_entries(items):
        mode = sort_var.get()
        if mode == "Date created - oldest": return sorted(items,key=lambda e:(e["created"],e["name"].lower()))
        if mode == "Modified - newest": return sorted(items,key=lambda e:(-e["modified"],e["name"].lower()))
        if mode == "Name A-Z": return sorted(items,key=lambda e:e["name"].lower())
        if mode == "Name Z-A": return sorted(items,key=lambda e:e["name"].lower(),reverse=True)
        if mode == "Frame count - most": return sorted(items,key=lambda e:(-e["frames"],-e["created"]))
        if mode == "Duration - longest": return sorted(items,key=lambda e:(-e["duration"],-e["created"]))
        return sorted(items,key=lambda e:(-e["created"],e["name"].lower()))

    def selected_entry():
        selected = tree.selection()
        return entry_by_iid.get(selected[0]) if selected else None

    def selected_rec_dir():
        entry = selected_entry()
        return entry["path"] if entry else None

    def launch_path(path):
        if not path or not os.path.exists(path):
            messagebox.showerror("Not found", f"Could not find:\n{path}")
            return
        try:
            if os.name == "nt":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as exc:
            messagebox.showerror("Could not open", str(exc))

    def output_default_for(entry):
        output_dir = cfg.get("output_folder") or os.path.dirname(os.path.abspath(library_var.get()))
        if not os.path.isdir(output_dir):
            output_dir = os.path.dirname(entry["path"])
        return os.path.join(output_dir, entry["name"] + ".mp4")

    def update_selection(_event=None):
        pause_playback()
        entry = selected_entry()
        if not entry:
            details_var.set("No recording selected.")
            player.update(frames=[],index=0,meta={})
            scrub.configure(to=0, state="disabled")
            preview_message("NO RECORDING SELECTED")
            export_btn.configure(state="disabled")
            open_folder_btn.configure(state="disabled")
            return
        meta = entry["meta"]
        frames = recording_frame_paths(entry["path"])
        player.update(frames=frames,index=0,meta=meta,last_drawn=None)
        scrub.configure(to=max(0,len(frames)-1), state=("normal" if frames else "disabled"))
        scrub_var.set(0)
        created = datetime.datetime.fromtimestamp(entry["created"]).strftime("%Y-%m-%d %H:%M:%S") if entry["created"] else "unknown"
        dims = f"{meta.get('width','?')}x{meta.get('height','?')}"
        details_var.set(
            f"{entry['path']}\nCreated {created}  |  {entry['frames']} disk frames  |  "
            f"{entry['duration']:.2f}s  |  {dims} @ {meta.get('fps','?')} fps  |  {entry['mode']}  |  {entry['state']}")
        if not out_var.get().strip() or not cfg.get("keep_output_name",False):
            out_var.set(output_default_for(entry))
        fps_var.set("")
        export_progress.configure(maximum=max(1,entry["logical_frames"] or entry["frames"] or 1), value=0)
        compile_var.set("IDLE // READY FOR JOB" if entry["ready"] else "SOURCE IS NOT READY")
        status_var.set(f"SELECTED: {entry['name']} // {entry['mode']} // {entry['state']}")
        export_btn.configure(state=("normal" if entry["ready"] else "disabled"))
        open_folder_btn.configure(state="normal")
        video_candidate = out_var.get().strip()
        open_video_btn.configure(state=("normal" if os.path.isfile(video_candidate) else "disabled"))
        if frames:
            draw_frame(0,"REPLAY",True)
        else:
            direct = recording_video_path(entry["path"],meta)
            if direct:
                preview_message("GPU VIDEO SOURCE", "Use OPEN VIDEO for the finalized capture")
                preview_caption_var.set(os.path.basename(direct))
            else:
                preview_message("NO RENDERED FRAMES", "Render the recording in Arena Studio first")

    def refresh_recordings(preserve_path=None):
        nonlocal entries
        preserve_path = preserve_path or selected_rec_dir() or (os.path.abspath(last_env) if last_env else None)
        root_path = os.path.abspath(os.path.expanduser(library_var.get().strip() or RECORDINGS_DIR))
        library_var.set(root_path)
        cfg["recordings_folder"] = root_path
        cfg["recording_sort"] = sort_var.get()
        save_config(cfg)
        status_var.set("SCANNING RECORDING LIBRARY...")
        root.update_idletasks()
        found = scan_recording_folder(root_path)
        entries = sort_entries([build_entry(path) for path in found])
        tree.delete(*tree.get_children())
        entry_by_iid.clear()
        selected_iid = None
        for index, entry in enumerate(entries):
            iid = f"rec{index}"
            entry_by_iid[iid] = entry
            created = (datetime.datetime.fromtimestamp(entry["created"]).strftime("%Y-%m-%d %H:%M")
                       if entry["created"] else "unknown")
            mins = int(entry["duration"]//60); secs = entry["duration"]-mins*60
            length = f"{mins}:{secs:04.1f}" if mins else f"{secs:.1f}s"
            tree.insert("", "end", iid=iid, text=entry["name"],
                        values=(created,entry["frames"],length,entry["mode"],entry["state"]),
                        tags=("ready" if entry["ready"] else "pending",))
            if preserve_path and os.path.normcase(entry["path"]) == os.path.normcase(preserve_path):
                selected_iid = iid
        tree.tag_configure("ready", foreground=INK)
        tree.tag_configure("pending", foreground=WARN)
        if not selected_iid and entries:
            selected_iid = "rec0"
        if selected_iid:
            tree.selection_set(selected_iid); tree.focus(selected_iid); tree.see(selected_iid)
        update_selection()
        log_line(f"Library scan: {len(entries)} recording(s) in {root_path}")
        if not entries:
            status_var.set("NO RECORDINGS FOUND")
            preview_message("EMPTY RECORDING LIBRARY", root_path)

    def browse_library():
        path = filedialog.askdirectory(title="Choose a recording library or one recording folder",
                                       initialdir=library_var.get() if os.path.isdir(library_var.get()) else GAME_DIR)
        if path:
            library_var.set(path)
            refresh_recordings()

    def browse_ffmpeg():
        path = filedialog.askopenfilename(title="Select ffmpeg executable",
            initialdir=os.path.dirname(ffmpeg_var.get()) if os.path.isfile(ffmpeg_var.get()) else GAME_DIR,
            filetypes=[("ffmpeg executable","ffmpeg.exe ffmpeg"),("All files","*.*")])
        if path:
            ffmpeg_var.set(path)
            resolve_ffmpeg(path)
            log_line(f"FFmpeg selected: {path}")

    def browse_output():
        entry = selected_entry()
        initial = (entry["name"]+".mp4") if entry else "arena_recording.mp4"
        current = out_var.get().strip()
        path = filedialog.asksaveasfilename(title="Choose export video path",
            initialdir=os.path.dirname(current) if current and os.path.isdir(os.path.dirname(current)) else GAME_DIR,
            initialfile=os.path.basename(current) if current else initial,
            defaultextension=".mp4",
            filetypes=[("MP4 video","*.mp4"),("All files","*.*")])
        if path:
            out_var.set(path)
            cfg["output_folder"] = os.path.dirname(path)
            save_config(cfg)
            open_video_btn.configure(state=("normal" if os.path.isfile(path) else "disabled"))

    library_browse_btn = raised_button(folder_bar, "FOLDER...", browse_library)
    library_browse_btn.pack(side="left", padx=(6,0))
    library_refresh_btn = raised_button(folder_bar, "REFRESH", lambda: refresh_recordings())
    library_refresh_btn.pack(side="left", padx=(5,0))
    ff_browse_btn = raised_button(ff_group, "BROWSE...", browse_ffmpeg)
    ff_browse_btn.pack(side="left", padx=(5,0))
    out_browse_btn = raised_button(export_group, "BROWSE...", browse_output)
    out_browse_btn.grid(row=0, column=6, sticky="e")

    sort_combo.bind("<<ComboboxSelected>>", lambda _e: refresh_recordings())
    tree.bind("<<TreeviewSelect>>", update_selection)
    tree.heading("#0", command=lambda: (sort_var.set("Name A-Z"),refresh_recordings()))
    tree.heading("created", command=lambda: (sort_var.set("Date created - newest"),refresh_recordings()))
    tree.heading("frames", command=lambda: (sort_var.set("Frame count - most"),refresh_recordings()))
    tree.heading("length", command=lambda: (sort_var.set("Duration - longest"),refresh_recordings()))

    # ---- exporting -------------------------------------------------------------
    export_state = {"running":False,"proc":None,"cancelled":False,
                    "rec_dir":None,"out":None,"source_frames":[]}

    def int_or_none(value):
        try:
            return int(str(value).strip()) if str(value).strip() else None
        except (TypeError,ValueError):
            return None

    def set_export_controls(running):
        state = "disabled" if running else "normal"
        export_btn.configure(state=("disabled" if running or not (selected_entry() and selected_entry()["ready"]) else "normal"))
        cancel_btn.configure(state=("normal" if running else "disabled"))
        tree.configure(selectmode=("none" if running else "browse"))
        for widget in (library_browse_btn,library_refresh_btn,ff_browse_btn,out_browse_btn):
            widget.configure(state=state)

    def export_progress_ui(frame_no, total, source_index, speed_text=""):
        if not export_state.get("running"):
            return
        total = max(1,int(total or 1)); frame_no=max(0,min(total,int(frame_no)))
        export_progress.configure(maximum=total,value=frame_no)
        pct=100.0*frame_no/total
        compile_var.set(f"COMPILING FRAME {frame_no:06d} / {total:06d}  [{pct:5.1f}%] {speed_text}".rstrip())
        status_var.set(f"ENCODING {pct:5.1f}% // {os.path.basename(export_state.get('out') or '')}")
        frames=export_state.get("source_frames") or []
        if frames:
            player["frames"]=frames
            draw_frame(max(0,min(len(frames)-1,int(source_index))),"COMPILING")

    def finish_export(success, message, out_path, cancelled=False):
        export_state.update(running=False,proc=None,cancelled=False)
        set_export_controls(False)
        if cancelled:
            compile_var.set("JOB CANCELLED")
            status_var.set("EXPORT CANCELLED")
            log_line("Export cancelled by user.")
            return
        if success:
            export_progress.configure(value=export_progress.cget("maximum"))
            compile_var.set("COMPLETE // VIDEO READY")
            status_var.set(f"DONE: {out_path}")
            open_video_btn.configure(state="normal")
            log_line(f"Export complete: {out_path}")
            messagebox.showinfo("Export complete", f"Saved video:\n{out_path}\n\nYou can replay the CPU frames here or open the finished video.")
        else:
            compile_var.set("EXPORT FAILED // CHECK JOB LOG")
            status_var.set(message)
            log_line(message)
            messagebox.showerror("Export failed", message)

    def cancel_export():
        if not export_state.get("running"):
            return
        export_state["cancelled"]=True
        proc=export_state.get("proc")
        compile_var.set("CANCELLING JOB...")
        if proc is not None:
            try: proc.terminate()
            except Exception: pass

    def run_export():
        entry=selected_entry()
        if not entry or not os.path.isdir(entry["path"]):
            messagebox.showerror("No recording","Select a recording first.")
            return
        if not entry["ready"]:
            messagebox.showerror("Recording not ready","This recording has not produced usable PNG frames/video yet. Render it in Arena Studio first.")
            return
        meta=safe_meta(entry["path"])
        if not recording_has_visuals(entry["path"],meta):
            messagebox.showerror("Empty recording","No CPU frames or finalized GPU source were found.")
            return
        ffmpeg_path=ffmpeg_var.get().strip()
        if os.path.isdir(ffmpeg_path):
            ffmpeg_path=resolve_ffmpeg(ffmpeg_path) or ffmpeg_path
        if not ffmpeg_path or not os.path.exists(ffmpeg_path):
            messagebox.showerror("ffmpeg not found","Use BROWSE beside FFMPEG ENGINE and select ffmpeg.exe.")
            return
        ok,why=verify_ffmpeg_runnable(ffmpeg_path)
        if not ok:
            messagebox.showerror("ffmpeg will not run",why)
            return
        out_path=out_var.get().strip()
        if not out_path:
            messagebox.showerror("No output path","Choose where to save the MP4.")
            return
        try:
            os.makedirs(os.path.dirname(os.path.abspath(out_path)),exist_ok=True)
        except OSError as exc:
            messagebox.showerror("Output folder error",str(exc));return
        fps=int_or_none(fps_var.get()) or int(meta.get("fps") or 60)
        width=int_or_none(width_var.get());height=int_or_none(height_var.get())
        crf=max(0,min(51,int_or_none(crf_var.get()) if int_or_none(crf_var.get()) is not None else 18))
        source_frames=recording_frame_paths(entry["path"])
        include_audio=bool(include_audio_var.get())
        capture_fps=float(meta.get("fps") or fps or 60)
        source_count=len(source_frames) or int(meta.get("frame_count") or 1)
        total=max(1,int(round(source_count*float(fps)/max(1.0,capture_fps))))
        cfg.update(ffmpeg_path=ffmpeg_path,output_folder=os.path.dirname(os.path.abspath(out_path)),
                   recording_sort=sort_var.get(),recordings_folder=library_var.get())
        save_config(cfg)
        pause_playback()
        export_state.update(running=True,proc=None,cancelled=False,rec_dir=entry["path"],
                            out=out_path,source_frames=source_frames)
        export_progress.configure(maximum=total,value=0)
        compile_var.set("PREPARING FRAME JOB...")
        status_var.set("PREPARING EXPORT")
        set_export_controls(True)
        log_line(f"Export source: {entry['path']}")
        log_line(f"Export target: {out_path}")

        def worker():
            last_frame=0;last_speed=""
            try:
                if _faux_descriptor(meta):
                    def faux_progress(message):
                        root.after(0,log_line,message)
                        root.after(0,status_var.set,message.upper())
                    prepare_faux_overlay(entry["path"],meta,progress=faux_progress)
                cmd=build_cmd(ffmpeg_path,entry["path"],out_path,fps,width,height,crf,
                              meta=meta,include_audio=include_audio)
                # Machine-readable progress gives the monitor an encoded frame
                # number. A short stats period makes the displayed PNG track the
                # encoder closely instead of jumping only every several seconds.
                cmd[1:1]=["-progress","pipe:1","-stats_period","0.05","-nostats"]
                root.after(0,log_line,"Running: "+" ".join(f'\"{c}\"' if " " in c else c for c in cmd))
                proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                                      text=True,bufsize=1,universal_newlines=True)
                export_state["proc"]=proc
                for raw in proc.stdout:
                    line=raw.strip()
                    if not line:
                        continue
                    frame=ffmpeg_progress_frame(line)
                    if line.startswith("speed="):
                        last_speed=line.split("=",1)[1]
                    if frame is not None:
                        last_frame=frame
                        source_index=int(max(0,frame-1)*capture_fps/max(1.0,float(fps)))
                        root.after(0,lambda f=frame,si=source_index,sp=last_speed:
                                   export_progress_ui(f,total,si,("// "+sp if sp else "")))
                    elif not line.startswith(("fps=","stream_","bitrate=","total_size=","out_time_","dup_frames=","drop_frames=","progress=")):
                        root.after(0,log_line,line)
                proc.wait()
                cancelled=bool(export_state.get("cancelled"))
                if proc.returncode==0 and not cancelled:
                    root.after(0,export_progress_ui,total,total,max(0,len(source_frames)-1),"// DONE")
                    root.after(0,finish_export,True,"Done",out_path,False)
                elif cancelled:
                    root.after(0,finish_export,False,"Cancelled",out_path,True)
                else:
                    root.after(0,finish_export,False,f"ffmpeg exited with code {proc.returncode}",out_path,False)
            except FileNotFoundError:
                root.after(0,finish_export,False,f"Could not run ffmpeg at: {ffmpeg_path}",out_path,False)
            except Exception as exc:
                root.after(0,finish_export,False,f"Export preparation failed: {exc}",out_path,False)
            finally:
                export_state["proc"]=None

        threading.Thread(target=worker,daemon=True).start()

    def open_current_video():
        path=out_var.get().strip()
        entry=selected_entry()
        if not os.path.isfile(path) and entry:
            path=recording_video_path(entry["path"],entry["meta"]) or path
        launch_path(path)

    export_btn.configure(command=run_export)
    cancel_btn.configure(command=cancel_export)
    open_video_btn.configure(command=open_current_video)
    open_folder_btn.configure(command=lambda: launch_path(selected_rec_dir()))

    # Menu wiring is late so every callback exists.
    file_menu.add_command(label="Choose Recording Folder...",command=browse_library)
    file_menu.add_command(label="Choose Output Video...",command=browse_output)
    file_menu.add_separator()
    file_menu.add_command(label="Exit",command=lambda:close_window())
    view_menu.add_command(label="Refresh Recording List",command=lambda:refresh_recordings())
    view_menu.add_command(label="Sort by Date Created",command=lambda:(sort_var.set(sort_choices[0]),refresh_recordings()))
    play_menu.add_command(label="Play / Pause",command=toggle_playback,accelerator="Space")
    play_menu.add_command(label="First Frame",command=lambda:(pause_playback(),draw_frame(0,"REPLAY")) if player.get("frames") else None)
    play_menu.add_command(label="Open Finished Video",command=open_current_video)
    root.bind("<space>",lambda _e:toggle_playback())
    root.bind("<Left>",lambda _e:step_frame(-1))
    root.bind("<Right>",lambda _e:step_frame(1))
    root.bind("<F5>",lambda _e:refresh_recordings())

    def close_window():
        pause_playback()
        if export_state.get("running"):
            if not messagebox.askyesno("Export running","Cancel the active export and close?"):
                return
            cancel_export()
        cfg.update(recordings_folder=library_var.get(),recording_sort=sort_var.get(),
                   ffmpeg_path=ffmpeg_var.get().strip())
        save_config(cfg)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW",close_window)
    preview_message("ARENA FRAME MONITOR","Choose a CPU recording from the library")
    refresh_recordings()
    log_line("Replay deck ready. Space = play/pause, arrows = frame step, F5 = refresh.")
    root.mainloop()
if __name__ == "__main__":
    # Use content, not just count: a shortcut, .bat wrapper, or IDE "Run"
    # config that passes one stray empty argument used to be enough to
    # push this into silent CLI auto-export mode instead of opening the
    # picker window. Only genuinely non-empty arguments count now.
    real_args = [a for a in sys.argv[1:] if a.strip()]
    if real_args:
        main_cli()
    else:
        main_gui()
