"""Arena Studio Panda3D backend foundation.

Phase 1 deliberately contains no Pygame or ModernGL calls. It establishes the
renderer-independent scene boundary needed before Panda3D can own the viewport.
Panda imports are lazy, so existing projects still open when Panda3D is absent.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import os
import time

import numpy as np


class PandaBackendUnavailable(RuntimeError):
    pass


def panda3d_available() -> tuple[bool, str]:
    try:
        import panda3d  # noqa: F401
        from panda3d.core import PandaSystem
        return True, PandaSystem.get_version_string()
    except Exception as exc:
        return False, str(exc)


@dataclass(slots=True)
class MeshPayload:
    object_id: str
    vertices: np.ndarray
    indices: np.ndarray
    texture: str = ""
    revision: int = 0


@dataclass(slots=True)
class PosePayload:
    object_id: str
    bone_ids: tuple[str, ...]
    matrices: np.ndarray
    revision: int = 0


@dataclass(slots=True)
class SceneObjectState:
    object_id: str
    name: str
    visible: bool
    position: tuple[float, float, float]
    rotation: tuple[float, float, float]
    scale: tuple[float, float, float]
    mesh_revision:int
    pose_revision:int
    texture:str=""


@dataclass
class PandaBackendStats:
    sync_ms: float = 0.0
    objects: int = 0
    meshes: int = 0
    poses: int = 0
    uploads: int = 0
    last_error: str = ""


class PandaSceneBridge:
    """Renderer-independent scene mirror used during backend migration.

    The bridge tracks revisions rather than retaining editor dictionaries.
    Panda resources are created only on the Panda owner thread in phase 2.
    """

    def __init__(self) -> None:
        ok, detail = panda3d_available()
        self.available = ok
        self.version = detail if ok else ""
        self.unavailable_reason = "" if ok else detail
        self.states: dict[str, SceneObjectState] = {}
        self.mesh_queue: dict[str, MeshPayload] = {}
        self.pose_queue: dict[str, PosePayload] = {}
        self.stats = PandaBackendStats()

    @staticmethod
    def _v3(value: Any, default: tuple[float, float, float]) -> tuple[float, float, float]:
        try:
            return tuple(float(v) for v in list(value)[:3])  # type: ignore[return-value]
        except Exception:
            return default

    def sync_editor_objects(self, objects: list[dict[str, Any]]) -> set[str]:
        start = time.perf_counter()
        live: set[str] = set()
        for obj in objects:
            oid = str(obj.get("id") or "")
            if not oid:
                continue
            live.add(oid)
            arm = obj.get("armature") if isinstance(obj.get("armature"), dict) else {}
            state = SceneObjectState(
                object_id=oid,
                name=str(obj.get("name") or "Object"),
                visible=obj.get("visible") is not False,
                position=self._v3(obj.get("pos"), (0.0, 0.0, 0.0)),
                rotation=self._v3(obj.get("rot"), (0.0, 0.0, 0.0)),
                scale=self._v3(obj.get("scale"), (1.0, 1.0, 1.0)),
                mesh_revision=int(obj.get("_mesh_revision") or 0),
                pose_revision=int(arm.get("_pose_serial") or 0),
                texture=os.path.abspath(str(obj.get("texture") or "")) if obj.get("texture") else "",
            )
            old = self.states.get(oid)
            self.states[oid] = state
            if old is None or old.mesh_revision!=state.mesh_revision or old.texture!=state.texture:
                rows = obj.get("_corner_rows")
                if isinstance(rows, np.ndarray) and rows.ndim == 2 and rows.shape[1] >= 8:
                    unique, inverse = np.unique(
                        np.ascontiguousarray(rows[:, :8]).view(
                            np.dtype((np.void, rows[:, :8].dtype.itemsize * 8))
                        ).reshape(-1),
                        return_inverse=True,
                    )
                    # first occurrence for each exact vertex key
                    _, first = np.unique(inverse, return_index=True)
                    self.mesh_queue[oid] = MeshPayload(
                        oid,
                        np.ascontiguousarray(rows[first, :8], dtype=np.float32),
                        np.ascontiguousarray(inverse, dtype=np.uint32),
                        state.texture,
                        state.mesh_revision,
                    )
            if arm and (old is None or old.pose_revision != state.pose_revision):
                bones = [b for b in arm.get("bones", []) if b.get("deform") is not False]
                matrices = arm.get("_panda_skin_matrices")
                if isinstance(matrices, np.ndarray):
                    self.pose_queue[oid] = PosePayload(
                        oid,
                        tuple(str(b.get("id")) for b in bones),
                        np.ascontiguousarray(matrices, dtype=np.float32),
                        state.pose_revision,
                    )
        for oid in set(self.states) - live:
            self.states.pop(oid, None)
            self.mesh_queue.pop(oid, None)
            self.pose_queue.pop(oid, None)
        self.stats.objects = len(self.states)
        self.stats.meshes = len(self.mesh_queue)
        self.stats.poses = len(self.pose_queue)
        self.stats.sync_ms = (time.perf_counter() - start) * 1000.0
        return live

    def status(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "version": self.version,
            "unavailable_reason": self.unavailable_reason,
            "objects": self.stats.objects,
            "pending_meshes": len(self.mesh_queue),
            "pending_poses": len(self.pose_queue),
            "sync_ms": self.stats.sync_ms,
            "uploads": self.stats.uploads,
            "last_error": self.stats.last_error,
        }


__all__ = [
    "PandaBackendUnavailable",
    "PandaSceneBridge",
    "MeshPayload",
    "PosePayload",
    "SceneObjectState",
    "panda3d_available",
]

class PandaViewportRuntime:
    """Phase-2 Panda owner: offscreen window, camera, scene graph and Geom upload.

    This runtime is intentionally opt-in until DirectGUI/editor composition is
    ported. It proves resource and camera parity without stealing Pygame's window.
    """
    def __init__(self,width:int=960,height:int=600,onscreen:bool=False) -> None:
        ok, detail = panda3d_available()
        if not ok:
            raise PandaBackendUnavailable(detail)
        from panda3d.core import loadPrcFileData
        window_type="onscreen" if onscreen else "offscreen"
        # On Windows use Panda's Direct3D pipe by default. Running a second WGL
        # context beside Arena's standalone ModernGL context caused 0x501/0x502
        # errors on several drivers. ARENA_PANDA_PIPE can override this.
        pipe=os.environ.get("ARENA_PANDA_PIPE") or ("pandadx9" if os.name=="nt" else "pandagl")
        loadPrcFileData("",f"load-display {pipe}\nwindow-type {window_type}\nwin-size {int(width)} {int(height)}\nwindow-title Arena Studio - Panda3D Live Viewport\naudio-library-name null\nsync-video false\nshow-frame-rate-meter false\nnotify-level-display warning\n")
        self.display_pipe=pipe
        from direct.showbase.ShowBase import ShowBase
        self.base=ShowBase(windowType=window_type);self.onscreen=bool(onscreen)
        self.root=self.base.render.attach_new_node("arena_scene");self.guide_root=self.base.render.attach_new_node("arena_guides")
        self.nodes: dict[str, Any] = {}
        self.mesh_revisions: dict[str, int] = {}
        self.pose_revisions: dict[str, int] = {}
        self.width, self.height = int(width), int(height)
        self.frames=0;self.uploads=0;self.rig_nodes={};self.rig_revisions={}
        self.last_render_ms = 0.0
        self.last_upload_ms=0.0;self.selected_id="";self.selection_overlay=None;self.last_pick=""
        try:self.base.accept("mouse1",self.pick_mouse)
        except Exception:pass
        self.base.cam.set_pos(5.4, -6.2, 3.8)
        self.base.cam.look_at(0.0, 0.0, 0.45)
        try:
            self.base.camLens.set_fov(46.0);self.base.camLens.set_near_far(0.1,100.0)
            from panda3d.core import AmbientLight,DirectionalLight,Vec4
            amb=AmbientLight("arena_ambient");amb.set_color(Vec4(.38,.40,.46,1));self.root.set_light(self.root.attach_new_node(amb))
            sun=DirectionalLight("arena_sun");sun.set_color(Vec4(.82,.84,.90,1));snp=self.root.attach_new_node(sun);snp.set_hpr(-35,-55,0);self.root.set_light(snp)
            self.base.set_background_color(.055,.06,.075,1)
        except Exception:pass
        self.grid_visible=True;self.axes_visible=True;self.view_mode="textured";self._build_guides()

    def _build_guides(self) -> None:
        from panda3d.core import LineSegs
        try:self.guide_root.node().remove_all_children()
        except Exception:pass
        grid=LineSegs("arena_grid");grid.set_thickness(1.0)
        for i in range(-10,11):
            c=.34 if i==0 else (.18 if i%5==0 else .105);grid.set_color(c,c,c+.025,1)
            grid.move_to(float(i),-10.,0.);grid.draw_to(float(i),10.,0.);grid.move_to(-10.,float(i),0.);grid.draw_to(10.,float(i),0.)
        self.grid_node=self.guide_root.attach_new_node(grid.create())
        axes=LineSegs("arena_axes");axes.set_thickness(2.2);axes.set_color(1,.16,.14,1);axes.move_to(0,0,0);axes.draw_to(2,0,0);axes.set_color(.16,1,.25,1);axes.move_to(0,0,0);axes.draw_to(0,2,0);axes.set_color(.18,.45,1,1);axes.move_to(0,0,0);axes.draw_to(0,0,2);self.axes_node=self.guide_root.attach_new_node(axes.create())
        self.guide_root.set_light_off(1);self.guide_root.set_bin("background",0)

    def set_guides(self,grid=None,axes=None) -> None:
        if grid is not None:self.grid_visible=bool(grid);self.grid_node.show() if self.grid_visible else self.grid_node.hide()
        if axes is not None:self.axes_visible=bool(axes);self.axes_node.show() if self.axes_visible else self.axes_node.hide()

    def set_view_mode(self,mode:str) -> str:
        mode=str(mode).lower()
        if mode not in ("textured","solid","wire"):raise ValueError("view mode must be textured, solid, or wire")
        self.view_mode=mode
        if mode=="wire":self.root.set_render_mode_wireframe()
        else:
            self.root.clear_render_mode()
            if mode=="solid":self.root.set_texture_off(50)
            else:self.root.clear_texture()
        return mode

    def _upload_mesh(self,payload:MeshPayload):
        """Upload with Panda's typed writers (portable across GL drivers)."""
        from panda3d.core import Geom,GeomNode,GeomTriangles,GeomVertexData,GeomVertexFormat,GeomVertexWriter,TextureStage,BitMask32,Filename
        vertices=np.ascontiguousarray(payload.vertices,dtype=np.float32);indices=np.ascontiguousarray(payload.indices,dtype=np.uint32).reshape(-1)
        if len(vertices)<3 or len(indices)<3:return None
        if int(indices.max(initial=0))>=len(vertices):raise ValueError(f"Panda mesh {payload.object_id}: index outside {len(vertices)} vertices")
        fmt=GeomVertexFormat.get_v3n3t2();vdata=GeomVertexData(payload.object_id,fmt,Geom.UH_static);vdata.set_num_rows(len(vertices))
        vw=GeomVertexWriter(vdata,"vertex");nw=GeomVertexWriter(vdata,"normal");tw=GeomVertexWriter(vdata,"texcoord")
        # Arena is Y-up, Panda is Z-up. Convert geometry itself, not only nodes.
        for row in vertices:
            vw.add_data3f(float(row[0]),-float(row[2]),float(row[1]));nw.add_data3f(float(row[3]),-float(row[5]),float(row[4]));tw.add_data2f(float(row[6]),1.0-float(row[7]))
        prim=GeomTriangles(Geom.UH_static)
        for i in range(0,len(indices)-2,3):prim.add_vertices(int(indices[i]),int(indices[i+1]),int(indices[i+2]))
        prim.close_primitive();geom=Geom(vdata);geom.add_primitive(prim);gnode=GeomNode(payload.object_id);gnode.add_geom(geom)
        old=self.nodes.pop(payload.object_id,None)
        if old is not None:
            try:old.remove_node()
            except Exception:pass
        node=self.root.attach_new_node(gnode);node.set_tag("arena_object_id",payload.object_id);node.node().set_into_collide_mask(BitMask32.bit(1))
        if payload.texture and os.path.isfile(payload.texture):
            try:
                tex=self.base.loader.load_texture(Filename.from_os_specific(os.path.abspath(payload.texture)))
                if tex:
                    # Arena's authored UV convention matches its ModernGL
                    # shader (V inverted). Keep repeat semantics for UV islands
                    # outside 0..1 and improve oblique filtering.
                    try:
                        from panda3d.core import Texture
                        tex.set_wrap_u(Texture.WM_repeat);tex.set_wrap_v(Texture.WM_repeat);tex.set_anisotropic_degree(4)
                    except Exception:pass
                    node.set_texture(TextureStage.get_default(),tex,1)
            except Exception:pass
        self.nodes[payload.object_id]=node;self.mesh_revisions[payload.object_id]=payload.revision;self.uploads+=1;return node

    def consume_bridge(self, bridge: PandaSceneBridge, max_uploads: int = 2) -> int:
        start = time.perf_counter(); done = 0
        for oid, payload in list(bridge.mesh_queue.items()):
            if done >= max_uploads: break
            self._upload_mesh(payload); bridge.mesh_queue.pop(oid, None); done += 1
        for oid, state in bridge.states.items():
            node = self.nodes.get(oid)
            if node is None: continue
            node.show() if state.visible else node.hide()
            x,y,z=state.position;node.set_pos(x,-z,y)
            # Arena is Y-up and stores radians; Panda is Z-up and HPR is degrees.
            r=tuple(float(v)*57.29577951308232 for v in state.rotation)
            node.set_hpr(-r[1],r[0],-r[2]);sx,sy,sz=state.scale;node.set_scale(sx,sz,sy)
        for oid in set(self.nodes)-set(bridge.states):
            if oid==self.selected_id:self.clear_selection()
            try:self.nodes.pop(oid).remove_node()
            except Exception: pass
            self.mesh_revisions.pop(oid,None);self.pose_revisions.pop(oid,None);self.remove_rig_overlay(oid)
        self.last_upload_ms = (time.perf_counter() - start) * 1000.0
        bridge.stats.uploads += done
        return done

    def set_camera(self, eye, target, up=(0.0, 1.0, 0.0), perspective=True) -> None:
        # Arena is Y-up; Panda is Z-up. Convert (x,y,z) -> (x,-z,y).
        ex, ey, ez = (float(v) for v in eye); tx, ty, tz = (float(v) for v in target)
        self.base.cam.set_pos(ex, -ez, ey); self.base.cam.look_at(tx, -tz, ty)
        try: self.base.camLens.set_fov(46.0 if perspective else 35.0)
        except Exception: pass

    def render_frame(self) -> None:
        start = time.perf_counter(); self.base.graphicsEngine.render_frame(); self.frames += 1
        self.last_render_ms = (time.perf_counter() - start) * 1000.0

    @staticmethod
    def _arena_point_to_panda(p):
        x,y,z=(float(v) for v in p);return (x,-z,y)

    def update_rig_overlay(self,object_id:str,segments,targets=(),revision:int=0) -> None:
        """Draw posed bones/IK targets above the Panda model without mesh copies."""
        oid=str(object_id)
        if self.rig_revisions.get(oid)==int(revision):return
        old=self.rig_nodes.pop(oid,None)
        if old is not None:
            try:old.remove_node()
            except Exception:pass
        parent=self.nodes.get(oid)
        if parent is None:return
        from panda3d.core import LineSegs
        lines=LineSegs("arena_rig_"+oid);lines.set_thickness(2.2);lines.set_color(.20,.88,1.0,1.0)
        for a,b in segments:
            lines.move_to(*self._arena_point_to_panda(a));lines.draw_to(*self._arena_point_to_panda(b))
        for target in targets:
            x,y,z=self._arena_point_to_panda(target);r=.055;lines.set_color(1.0,.70,.12,1.0)
            lines.move_to(x-r,y,z);lines.draw_to(x+r,y,z);lines.move_to(x,y-r,z);lines.draw_to(x,y+r,z);lines.move_to(x,y,z-r);lines.draw_to(x,y,z+r)
        node=parent.attach_new_node(lines.create());node.set_depth_test(False);node.set_bin("fixed",60);node.set_light_off(1)
        self.rig_nodes[oid]=node;self.rig_revisions[oid]=int(revision)

    def remove_rig_overlay(self,object_id:str) -> None:
        old=self.rig_nodes.pop(str(object_id),None);self.rig_revisions.pop(str(object_id),None)
        if old is not None:
            try:old.remove_node()
            except Exception:pass

    def clear_selection(self) -> None:
        if self.selection_overlay is not None:
            try:self.selection_overlay.remove_node()
            except Exception:pass
        self.selection_overlay=None;self.selected_id=""

    def select(self,object_id:str) -> bool:
        self.clear_selection();node=self.nodes.get(str(object_id))
        if node is None:return False
        # Shared-geometry copy: a gold wire pass without duplicating mesh data.
        overlay=node.copy_to(self.root);overlay.set_render_mode_wireframe();overlay.set_color(1.0,.58,.12,1.0);overlay.set_light_off(1);overlay.set_depth_offset(2);overlay.set_bin("fixed",40);overlay.set_tag("arena_selection_overlay","1")
        self.selection_overlay=overlay;self.selected_id=str(object_id);return True

    def pick_ndc(self,x:float,y:float) -> str:
        from panda3d.core import CollisionNode,CollisionRay,CollisionTraverser,CollisionHandlerQueue,BitMask32
        picker=CollisionNode("arena_picker");picker.set_from_collide_mask(BitMask32.bit(1));picker.set_into_collide_mask(BitMask32.all_off());ray=CollisionRay();picker.add_solid(ray);npick=self.base.cam.attach_new_node(picker);queue=CollisionHandlerQueue();trav=CollisionTraverser();trav.add_collider(npick,queue)
        try:
            ray.set_from_lens(self.base.camNode,float(x),float(y));trav.traverse(self.root);queue.sort_entries()
            if queue.get_num_entries():
                hit=queue.get_entry(0).get_into_node_path();cur=hit
                while not cur.is_empty():
                    oid=cur.get_tag("arena_object_id")
                    if oid:self.last_pick=oid;self.select(oid);return oid
                    cur=cur.get_parent()
            self.clear_selection();self.last_pick="";return ""
        finally:npick.remove_node()

    def pick_pixel(self,x:float,y:float) -> str:
        nx=(float(x)/max(1,self.width))*2.-1.;ny=1.-(float(y)/max(1,self.height))*2.;return self.pick_ndc(nx,ny)

    def pick_mouse(self) -> str:
        try:
            mw=self.base.mouseWatcherNode
            if mw.has_mouse():m=mw.get_mouse();return self.pick_ndc(m.x,m.y)
        except Exception:pass
        return ""

    def step(self) -> None:
        """Process one Panda window/event/render iteration without taking over Arena's loop."""
        start=time.perf_counter()
        try:self.base.taskMgr.step()
        except Exception:self.base.graphicsEngine.render_frame()
        self.frames+=1;self.last_render_ms=(time.perf_counter()-start)*1000.0

    def set_wireframe(self,enabled:bool) -> None:
        if enabled:self.root.set_render_mode_wireframe()
        else:self.root.clear_render_mode()

    def window_open(self) -> bool:
        try:return bool(self.base.win is not None and self.base.win.is_valid())
        except Exception:return False

    def screenshot(self, path: str) -> str:
        path = os.path.abspath(path)
        from panda3d.core import Filename
        image=self.base.win.get_screenshot()
        if image is None or not image.write(Filename.from_os_specific(path)):
            raise RuntimeError("Panda3D could not write the offscreen screenshot")
        return path

    def status(self) -> dict[str, Any]:
        return {"mode":"onscreen" if self.onscreen else "offscreen","pipe":self.display_pipe,"view":self.view_mode,"grid":self.grid_visible,"axes":self.axes_visible,"objects":len(self.nodes),"selected":self.selected_id or "-","last_pick":self.last_pick or "-","uploads":self.uploads,"frames":self.frames,
                "render_ms":self.last_render_ms,"upload_ms":self.last_upload_ms,"size":(self.width,self.height)}

    def close(self) -> None:
        try: self.base.destroy()
        except Exception: pass
        self.nodes.clear();self.rig_nodes.clear();self.rig_revisions.clear()

__all__.append("PandaViewportRuntime")
