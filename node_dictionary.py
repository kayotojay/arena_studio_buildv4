"""
node_dictionary.py
==================
Updated dictionary for the Box Game Blueprint Visual Scripter.

Includes all statically registered nodes plus dynamically generated Weapon Rig,
Position Rig, Projectile, Collision, Universal, Query, Collection Effect, and
Graph Group nodes found in box_game_part12.py.
"""

NODE_TIPS = {'adv_accel': {'example': '1. G-force measurement',
               'tip': 'Simulates acceleration based on velocity changes. Execution input: exec. Execution output: '
                      'exec. Data inputs: Character (object). Data outputs: Accel (vector). Use the white execution '
                      'path for ordering and the colored pins for values.'},
 'adv_altimeter': {'example': '1. Flight path',
                   'tip': 'Returns strictly negative Y as height. Data inputs: Character (object). Data outputs: '
                          'Height (number).'},
 'adv_baro': {'example': '1. Altitude check',
              'tip': 'Returns simulated air pressure based on Y level. Data inputs: Character (object). Data '
                     'outputs: Pressure (number).'},
 'adv_gps': {'example': '1. Location ping',
             'tip': 'Returns absolute X and Y separately. Data inputs: Character (object). Data outputs: X (number), '
                    'Y (number).'},
 'adv_gyro': {'example': '1. Spin detection',
              'tip': 'Simulates angular velocity based on rotation changes. Execution input: exec. Execution output: '
                     'exec. Data inputs: Angle (number). Data outputs: Ang Vel (number). Use the white execution '
                     'path for ordering and the colored pins for values.'},
 'adv_kalman': {'example': '1. Drone stabilization',
                'tip': 'Simplified 1D Kalman filter for noise reduction. Execution input: exec. Execution output: '
                       'exec. Data inputs: Measurement (number), Noise (number). Data outputs: Estimate (number). '
                       'Use the white execution path for ordering and the colored pins for values.'},
 'adv_magneto': {'example': '1. Compass',
                 'tip': 'Returns a vector pointing to 0,0. Data inputs: Character (object). Data outputs: Heading '
                        '(vector).'},
 'adv_matrix': {'example': '1. Skew / transform',
                'tip': 'Simulates 2x2 matrix multiplication with a vector. Data inputs: Vector (vector), M00 '
                       '(number), M01 (number), M10 (number), M11 (number). Data outputs: Result (vector).'},
 'adv_pid': {'example': '1. Smooth homing missile',
             'tip': 'Classic Proportional-Integral-Derivative controller. Execution input: exec. Execution output: '
                    'exec. Data inputs: Error (number), P (number), I (number), D (number). Data outputs: Correction '
                    '(number). Use the white execution path for ordering and the colored pins for values.'},
 'adv_quat': {'example': '1. Advanced rotation',
              'tip': 'Simulates complex 2D rotation via matrices. Data inputs: Vector (vector), CosA (number), SinA '
                     '(number). Data outputs: Rotated (vector).'},
 'algebra_abs_root': {'example': '1. Add Absolute Equation Root from the Math category.\n'
                                 '2. Connect value.\n'
                                 '3. Use root in the next calculation or condition.',
                      'tip': 'Solves X squared equals Value for the positive root. Data inputs: value (number, '
                             'default=0). Data outputs: root (number). This is a pure data node: wire its colored '
                             'output directly into another input; no white execution wire is required.'},
 'algebra_circle_x': {'example': '1. Add Circle X from the Math category.\n'
                                 '2. Connect center_x, center_y, radius.\n'
                                 '3. Use x in the next calculation or condition.',
                      'tip': 'Returns a circle X coordinate for Y and a chosen side. Data inputs: center_x (number, '
                             'default=0), center_y (number, default=0), radius (number, default=1), y (number, '
                             'default=0), side (number, default=1). Data outputs: x (number). This is a pure data '
                             'node: wire its colored output directly into another input; no white execution wire is '
                             'required.'},
 'algebra_circle_y': {'example': '1. Add Circle Y from the Math category.\n'
                                 '2. Connect center_x, center_y, radius.\n'
                                 '3. Use y in the next calculation or condition.',
                      'tip': 'Returns a circle Y coordinate for X and a chosen side. Data inputs: center_x (number, '
                             'default=0), center_y (number, default=0), radius (number, default=1), x (number, '
                             'default=0), side (number, default=1). Data outputs: y (number). This is a pure data '
                             'node: wire its colored output directly into another input; no white execution wire is '
                             'required.'},
 'algebra_intersection_x': {'example': '1. Add Line Intersection X from the Math category.\n'
                                       '2. Connect m1, b1, m2.\n'
                                       '3. Use x in the next calculation or condition.',
                            'tip': 'Solves where y=M1x+B1 intersects y=M2x+B2. Data inputs: m1 (number, default=1), '
                                   'b1 (number, default=0), m2 (number, default=-1), b2 (number, default=0). Data '
                                   'outputs: x (number). This is a pure data node: wire its colored output directly '
                                   'into another input; no white execution wire is required.'},
 'algebra_intersection_y': {'example': '1. Add Line Intersection Y from the Math category.\n'
                                       '2. Connect m, b, x.\n'
                                       '3. Use y in the next calculation or condition.',
                            'tip': 'Returns Y on line M1/B1 at X. Data inputs: m (number, default=1), b (number, '
                                   'default=0), x (number, default=0). Data outputs: y (number). This is a pure data '
                                   'node: wire its colored output directly into another input; no white execution '
                                   'wire is required.'},
 'algebra_midpoint': {'example': '1. Add Midpoint from the Math category.\n'
                                 '2. Connect a, b.\n'
                                 '3. Use midpoint in the next calculation or condition.',
                      'tip': 'Returns the midpoint between A and B. Data inputs: a (number, default=0), b (number, '
                             'default=1). Data outputs: midpoint (number). This is a pure data node: wire its '
                             'colored output directly into another input; no white execution wire is required.'},
 'animation_at_position': {'example': '1. Play "explosion_vfx" at Target Position\n2. Play "hit_spark" at Self',
                           'tip': 'Plays a VFX animation clip at a specific world position. Execution input: exec. '
                                  'Execution output: exec. Data inputs: position (vector), animation (string, '
                                  "default=''), duration (number, default=0), scale (number, default=1). Data "
                                  'outputs: effect (object). Settings: animation, duration, scale. Use the white '
                                  'execution path for ordering and the colored pins for values.'},
 'animation_choose': {'example': '1. Choose "spin_attack" -> Play Animation\n2. Select effect animation',
                      'tip': 'Select a reusable animation and output its name for any animation input. Data outputs: '
                             'animation (string). Settings: animation.'},
 'animation_clear_queue': {'example': '1. Add Clear Animation Queue from the Animation category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Clear queued animation states on a character.'},
 'animation_create_clip': {'example': '1. Create "my_attack" from "sword_swing"\n2. Allows custom fps/durations',
                           'tip': 'Create a character-local named clip from a reusable library clip. Execution '
                                  'input: exec. Execution output: exec. Data inputs: target (object). Settings: '
                                  'new_name, source_animation. Use the white execution path for ordering and the '
                                  'colored pins for values.'},
 'animation_crossfade_state': {'example': '1. Add Crossfade Animation State from the Animation category.\n'
                                          '2. Connect its compatible inputs.\n'
                                          '3. Use its output or execution path in the next operation.',
                               'tip': 'Switch state with blend metadata. Runtime that supports blend fields will '
                                      'crossfade; older runtime still changes state safely.'},
 'animation_finished_condition': {'example': '1. If Anim Finished -> Move\n2. Wait for attack anim to finish',
                                  'tip': 'Returns True if the specified animation has finished playing. Data inputs: '
                                         'target (object). Data outputs: result (boolean).'},
 'animation_flip_from_direction': {'example': '1. Add Flip Sprite From Direction from the Animation category.\n'
                                              '2. Connect its compatible inputs.\n'
                                              '3. Use its output or execution path in the next operation.',
                                   'tip': "Set flip_x based on a direction vector's X component."},
 'animation_loop_effect': {'example': '1. Loop "fire_aura" on Self\n2. Loop "stunned" on Target',
                           'tip': 'Starts a looping animation effect on a target that runs until stopped.'},
 'animation_method_select': {'example': '1. Add Animation Method Select from the Animation category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Pure node: output an animation playback method string for method-driven '
                                    'graphs.'},
 'animation_on_target': {'example': '1. Play "stun_stars" on Target\n2. Play "healing_aura" on Self',
                         'tip': 'Plays a VFX animation clip attached to and following a character. Execution input: '
                                'exec. Execution output: exec. Data inputs: target (object), animation (string, '
                                "default=''), duration (number, default=0), scale (number, default=1). Data outputs: "
                                'effect (object). Settings: animation, duration, scale. Use the white execution path '
                                'for ordering and the colored pins for values.'},
 'animation_pause': {'example': '1. Add Pause Animation from the Animation category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': 'Set a pause flag for animation-aware runtimes/tools.'},
 'animation_play': {'example': '1. Play "spin_attack" on hit\n2. Play "cast_spell"',
                    'tip': 'Choose a reusable named animation. Duration 0 uses its authored frame timing, then '
                           'returns to Idle. Execution input: exec. Execution output: exec. Data inputs: target '
                           "(object), state (string, default='attack'), duration (number, default=0.0). Settings: "
                           'state, duration. Use the white execution path for ordering and the colored pins for '
                           'values.'},
 'animation_queue_state': {'example': '1. Add Queue Animation State from the Animation category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Append a state/duration pair to a per-character animation queue for '
                                  'scripts/controllers to consume.'},
 'animation_random_state': {'example': '1. Add Random Animation State from the Animation category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Pure node: choose one state from a comma-separated list.'},
 'animation_resume': {'example': '1. Add Resume Animation from the Animation category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Clear the animation pause flag.'},
 'animation_set_speed': {'example': '1. Add Set Animation Speed from the Animation category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Store an animation playback speed multiplier on the character.'},
 'animation_set_sprite': {'example': '1. Set Sprite "dead_body"\n2. Set Sprite "shield_up"',
                          'tip': 'Switches to a static single image instead of an animated clip. Execution input: '
                                 'exec. Execution output: exec. Data inputs: target (object), sprite_tag (string, '
                                 "default='idle'). Settings: sprite_tag. Use the white execution path for ordering "
                                 'and the colored pins for values.'},
 'animation_set_state': {'example': '1. Set State "defend" for 1.0s\n2. Engine auto-reverts to "idle"',
                         'tip': 'Forces the character into a specific visual state (e.g. attack, idle, hit) for a '
                                'duration. Execution input: exec. Execution output: exec. Data inputs: target '
                                "(object), state (string, default='idle'). Settings: state. Use the white execution "
                                'path for ordering and the colored pins for values.'},
 'animation_state_equals': {'example': '1. Add Animation State Equals from the Animation category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': "Pure condition: test the character's current visual_state."},
 'animation_stop_effect': {'example': '1. Stop "fire_aura"\n2. On Cleanse -> Stop "stunned"',
                           'tip': 'Stops a named looping animation effect that was started with Loop Effect. '
                                  'Execution input: exec. Execution output: exec. Data inputs: effect (object). Use '
                                  'the white execution path for ordering and the colored pins for values.'},
 'animation_with_damage': {'example': '1. Anim + 50 Damage -> Syncs damage to impact frame\n2. Fireball impact',
                           'tip': 'Plays an animation and deals damage timed to sync with the impact frame. '
                                  'Settings: radius, damage, force, animation, team_filter, allow_self, falloff.'},
 'area_damage_cone': {'example': '1. Damage Cone (Facing, 45 degrees, 300 range, 20 damage)\n'
                                 '2. Fire Breath -> Damage Cone',
                      'tip': 'Deals damage in a directional arc -- like a shotgun blast or dragon breath. Execution '
                             'input: exec. Execution output: exec. Data inputs: origin (vector), direction (vector), '
                             'damage (number, default=20). Settings: damage, angle, range, team_filter, allow_self. '
                             'Use the white execution path for ordering and the colored pins for values.'},
 'area_damage_line': {'example': '1. Damage Line (Self to Target, 50 width, 100 damage)\n2. Railgun -> Damage Line',
                      'tip': 'Deals damage along a thick line from point A to point B -- laser beams, railguns. '
                             'Execution input: exec. Execution output: exec. Data inputs: start (vector), end '
                             '(vector), damage (number, default=25). Settings: damage, width, team_filter, '
                             'allow_self. Use the white execution path for ordering and the colored pins for '
                             'values.'},
 'area_damage_position': {'example': '1. Damage At Position (Random Point)\n2. Damage At Position (Target Position)',
                          'tip': 'Deals damage instantly at a specific world coordinate. Settings: damage, radius, '
                                 'team_filter, allow_self, falloff.'},
 'area_damage_radius': {'example': '1. Damage In Radius (200, 50 damage)\n'
                                   '2. On Death -> Damage In Radius (explode on death)',
                        'tip': 'Damage all filtered characters around a world point. Execution input: exec. '
                               'Execution output: exec. Data inputs: position (vector), damage (number, default=20), '
                               'radius (number, default=80). Data outputs: hit_characters (object). Settings: '
                               'damage, radius, team_filter, allow_self, falloff. Use the white execution path for '
                               'ordering and the colored pins for values.'},
 'area_distance_between': {'example': '1. Distance Between Me and Target -> If < 50 -> Attack\n'
                                      '2. Distance -> Math Divide',
                           'tip': 'Returns the exact floating-point distance between two positions. Data inputs: a '
                                  '(object), b (object). Data outputs: distance (number).'},
 'area_get_by_name': {'example': '1. Get Characters With Name "Skeleton" -> For Each\n2. Get "King" -> Protect',
                      'tip': 'Find characters whose name matches exactly, regardless of team. Data inputs: position '
                             "(vector), name (string, default=''), radius (number, default=200). Data outputs: "
                             'characters (object). Settings: name, radius, include_self.'},
 'area_get_by_tag': {'example': '1. Get Characters With Tag "boss" -> Move Toward\n2. Get "minion" -> Count',
                     'tip': 'Find characters carrying a given tag, regardless of team. Data inputs: position '
                            "(vector), tag (string, default=''), radius (number, default=200). Data outputs: "
                            'characters (object). Settings: tag, radius, include_self.'},
 'area_get_direction': {'example': '1. Get Characters In Direction (North) -> Deal Damage\n'
                                   '2. Get Characters Facing -> Push',
                        'tip': 'Returns characters found in a specific direction from a source. Data inputs: origin '
                               '(vector), direction (vector). Data outputs: characters (object). Settings: angle, '
                               'range, team_filter.'},
 'area_get_radius': {'example': '1. Get Characters In 500 -> For Each -> Add Shield\n'
                                '2. Get Characters -> Filter List',
                     'tip': 'Returns a list of all characters inside a circle. Feed the list into a For Each loop. '
                            'Data inputs: position (vector), radius (number, default=100). Data outputs: characters '
                            '(object). Settings: radius, team_filter, include_self.'},
 'area_is_in_range': {'example': '1. Is Target In Range (100)? -> True -> Attack\n2. False -> Move Toward',
                      'tip': 'Returns True if position A is within range of position B. Data inputs: a (object), b '
                             '(object), range (number, default=100). Data outputs: result (boolean). Settings: '
                             'range.'},
 'area_nearest_team': {'example': '1. Get Nearest Enemy -> Deal Damage\n2. Get Nearest Ally -> Heal',
                       'tip': 'Returns the closest ally or enemy to a given point. Data inputs: origin (object). '
                              'Data outputs: character (object). Settings: team_filter, radius.'},
 'area_push_pull': {'example': '1. Black Hole: Pull Radius (300, Force 500)\n'
                               '2. Repulse: Push Radius (200, Force 800)',
                    'tip': 'Applies a radial physics force -- push everything outward or pull everything inward. '
                           'Execution input: exec. Execution output: exec. Data inputs: position (vector). Settings: '
                           'radius, force, mode, team_filter, include_self. Use the white execution path for '
                           'ordering and the colored pins for values.'},
 'audio_branch': {'example': '1. If Audio Playing -> Do nothing, Else -> Play Audio\n2. Prevent overlapping sounds',
                  'tip': 'Branch audio execution based on a condition. Connect condition to boolean input, then '
                         'different audio nodes to true/false outputs. Execution input: exec. Execution output: '
                         'then, else. Data inputs: condition (boolean, default=True). Use the white execution path '
                         'for ordering and the colored pins for values.'},
 'audio_condition_distance': {'example': '1. If Distance < 100 -> Play "footsteps.wav"\n2. Proximity alarms',
                              'tip': 'Check distance between two characters/objects for spatial audio logic. '
                                     'Execution input: exec. Execution output: true, false. Data inputs: a (object), '
                                     'b (object), distance (number, default=100). Data outputs: distance (number). '
                                     'Settings: operation, distance. Use the white execution path for ordering and '
                                     'the colored pins for values.'},
 'audio_condition_hp': {'example': '1. If HP < 20% -> Play "heartbeat.wav"\n2. Dynamic music intensity',
                        'tip': "Check character HP and branch audio. Perfect for 'if HP > 50 play this, else play "
                               "that'. Execution input: exec. Execution output: true, false. Data inputs: target "
                               '(object), threshold (number, default=50). Data outputs: hp (number), hp_pct '
                               '(number). Settings: operation, threshold. Use the white execution path for ordering '
                               'and the colored pins for values.'},
 'audio_condition_random': {'example': '1. 10% Chance -> Play "rare_voice_line.wav"\n2. Break up repetitive sounds',
                            'tip': 'Random probability branch for audio variation. E.g., 30% chance for rare sound. '
                                   'Execution input: exec. Execution output: success, fail. Data inputs: chance '
                                   '(number, default=50). Data outputs: roll (number). Settings: chance. Use the '
                                   'white execution path for ordering and the colored pins for values.'},
 'audio_condition_status': {'example': '1. If Stunned -> Play "dizzy.wav"\n2. If Poisoned -> Play "cough.wav"',
                            'tip': 'Check if character has a specific status effect (stun, poison, burn, etc.). '
                                   'Execution input: exec. Execution output: true, false. Data inputs: target '
                                   "(object), status (string, default='stun'). Settings: status, invert. Use the "
                                   'white execution path for ordering and the colored pins for values.'},
 'audio_constant_cue': {'example': '1. Constant "death" -> Play Audio\n2. Static routing',
                        'tip': 'A constant audio cue name string. Data outputs: cue (string). Settings: cue.'},
 'audio_crossfade': {'example': '1. Crossfade "calm_music" to "combat_music" (2.0s)\n2. Ambient transitions',
                     'tip': 'Smoothly crossfade between two audio cues. Useful for music transitions, or blending '
                            'between combat states. Execution input: exec. Execution output: exec, completed. Data '
                            "inputs: target (object), from_cue (string, default=''), to_cue (string, default=''), "
                            'from_volume (number, default=1.0), to_volume (number, default=1.0), duration (number, '
                            'default=1.0). Data outputs: from_channel (object), to_channel (object), progress '
                            '(number). Settings: duration, curve. Use the white execution path for ordering and the '
                            'colored pins for values.'},
 'audio_debug': {'example': '1. Debug Audio Channel -> Console\n2. Check volume levels',
                 'tip': 'Print audio debug info: playing channels, cue mappings, volume levels. Execution input: '
                        'exec. Execution output: exec. Data inputs: target (object). Settings: show_channels, '
                        'show_cues. Use the white execution path for ordering and the colored pins for values.'},
 'audio_file_browser': {'example': '1. Pick "music.ogg" -> Play Audio From Path\n2. Direct disk access',
                        'tip': 'Browse and select an audio file from the audio/_imported folder. Returns the '
                               'relative path for direct playback. Execution input: exec. Execution output: exec. '
                               'Data outputs: path (string). Settings: selected_path, refresh. Use the white '
                               'execution path for ordering and the colored pins for values.'},
 'audio_get_cue': {'example': '1. Get Cue "attack" -> Play Audio\n2. Dynamic routing',
                   'tip': "Resolve an audio cue name from a character's audio_map. Returns the file path. Data "
                          "inputs: target (object), cue (string, default='hit'), fallback (string, default=''). Data "
                          'outputs: path (string), found (boolean). Settings: fallback.'},
 'audio_group': {'example': '1. Group: Play "explosion.wav" AND "glass_shatter.wav"\n2. Layering sounds',
                 'tip': 'Organizational node: groups multiple audio nodes together. Has no runtime effect but makes '
                        'graphs readable. Can be collapsed/expanded in the editor. Execution input: exec. Execution '
                        'output: exec. Settings: label, color, collapsed. Use the white execution path for ordering '
                        'and the colored pins for values.'},
 'audio_layer': {'example': '1. Layer "bass_drop" with "laser_zap"\n2. Complex sound design',
                 'tip': 'Play multiple audio cues simultaneously. Each layer has independent volume, pitch, and '
                        "spatial settings. Great for impact sounds: layer a 'thud' with a 'crack'. Execution input: "
                        'exec. Execution output: exec, layer. Data inputs: target (object). Data outputs: channels '
                        '(object). Settings: count, stagger. Use the white execution path for ordering and the '
                        'colored pins for values.'},
 'audio_list_cues': {'example': '1. List Cues -> For Each -> Check\n2. Debugging',
                     'tip': 'Get all available audio cue names for a character. Useful for debugging or dynamic UIs. '
                            'Data inputs: target (object). Data outputs: cues (object).'},
 'audio_param_pitch': {'example': '1. Link Speed to Pitch -> Faster movement = higher pitch\n'
                                  '2. Engine revving sounds',
                       'tip': 'Generate a pitch value with randomization. Can be driven by game state (speed, HP, '
                              'combo count, etc.) for dynamic pitch. Data inputs: target (object), base (number, '
                              'default=1.0), random (number, default=0.0), speed_factor (number, default=0.0), '
                              'hp_factor (number, default=0.0). Data outputs: pitch (number). Settings: base, '
                              'random, speed_factor, hp_factor.'},
 'audio_param_volume': {'example': '1. Link Distance to Volume -> Closer = louder\n2. Distance attenuation',
                        'tip': 'Generate a volume value with distance attenuation, HP scaling, etc. Data inputs: '
                               'target (object), listener (object), base (number, default=1.0), combo_count (number, '
                               'default=1). Data outputs: volume (number). Settings: base, distance_attenuation, '
                               'hp_factor, combo_factor.'},
 'audio_play': {'example': '1. Play Cue "attack"\n2. Play Cue "spell_cast"',
                'tip': 'Play an audio cue with full control: pitch randomization, volume, spatial positioning, and '
                       'optional looping. Works with character audio_map or global cues. Execution input: exec. '
                       "Execution output: exec. Data inputs: target (object), cue (string, default='hit'), volume "
                       '(number, default=1.0), pitch (number, default=1.0), pitch_random (number, default=0.0), '
                       'position (vector). Data outputs: channel (object), actual_pitch (number). Settings: cue, '
                       'volume, pitch, pitch_random, loop, spatial, falloff, max_distance. Use the white execution '
                       'path for ordering and the colored pins for values.'},
 'audio_play_path': {'example': '1. Audio File Browser -> Play Audio From Path\n'
                                '2. Play "audio/_imported/bgm.mp3" directly',
                     'tip': 'Play an audio file directly from a file path (bypasses character audio_map). Great for '
                            'one-off sounds or when using Audio File Browser. Execution input: exec. Execution '
                            "output: exec. Data inputs: path (string, default=''), audio_file (string, default=''), "
                            'position (vector), volume (number, default=1.0), pitch (number, default=1.0), '
                            'pitch_random (number, default=0.0). Data outputs: channel (object), actual_pitch '
                            '(number). Settings: volume, pitch, pitch_random, loop, spatial, falloff, max_distance, '
                            'audio_file. Use the white execution path for ordering and the colored pins for values.'},
 'audio_random': {'example': '1. Random: "hit1.wav", "hit2.wav", "hit3.wav"\n2. Avoids repetitive audio fatigue',
                  'tip': 'Randomly select one audio cue from a list. Supports weighted random selection. Perfect for '
                         'footstep variations, impact variations, etc. Execution input: exec. Execution output: '
                         'exec, pick. Data inputs: target (object). Data outputs: cue (string), index (number). '
                         'Settings: count, weighted, no_repeat. Use the white execution path for ordering and the '
                         'colored pins for values.'},
 'audio_sequence': {'example': '1. Sequence: "step_left.wav" then "step_right.wav"\n2. Footstep loops',
                    'tip': 'Play multiple audio cues in sequence with configurable delays between each. Great for '
                           'combo sounds, multi-hit effects, or layered sequences. Execution input: exec. Execution '
                           'output: exec, step, completed. Data inputs: target (object). Data outputs: index '
                           '(number). Settings: count, loop, loop_delay. Use the white execution path for ordering '
                           'and the colored pins for values.'},
 'audio_set_pitch': {'example': '1. Pitch 1.5 (Fast/High)\n2. Pitch 0.5 (Slow/Low)',
                     'tip': 'Change pitch of a playing audio channel in real-time. Execution input: exec. Execution '
                            'output: exec. Data inputs: channel (object), pitch (number, default=1.0), fade_time '
                            '(number, default=0.1). Settings: fade_time. Use the white execution path for ordering '
                            'and the colored pins for values.'},
 'audio_set_volume': {'example': '1. Set Volume to 0.5\n2. Fade volume in over time',
                      'tip': 'Change volume of a playing audio channel in real-time. Execution input: exec. '
                             'Execution output: exec. Data inputs: channel (object), volume (number, default=1.0), '
                             'fade_time (number, default=0.1). Settings: fade_time. Use the white execution path for '
                             'ordering and the colored pins for values.'},
 'audio_shuffle': {'example': '1. Shuffle: Voice lines\n2. Shuffle: Gunshots',
                   'tip': 'Shuffle bag / bag of holding pattern: picks all options before repeating. Ensures even '
                          'distribution without immediate repeats. Execution input: exec. Execution output: exec, '
                          'pick. Data inputs: target (object). Data outputs: cue (string), index (number), '
                          'bag_remaining (number). Settings: count, refill_early. Use the white execution path for '
                          'ordering and the colored pins for values.'},
 'audio_state_machine': {'example': '1. State Machine: Idle -> Walk -> Attack\n2. Character audio controller',
                         'tip': 'Define audio behavior per character state (idle, attack, hit, death, etc.). Each '
                                'state can have its own sound, pitch, volume, and transition rules. Execution input: '
                                'exec. Execution output: exec, state_changed. Data inputs: target (object), state '
                                "(string, default='idle'). Data outputs: current_state (string). Settings: states, "
                                'default_state. Use the white execution path for ordering and the colored pins for '
                                'values.'},
 'audio_stop': {'example': '1. Stop Channel (from Play Audio node)\n2. Fade out over 1.0s',
                'tip': 'Stop a playing audio channel (from Play Audio node). Supports fade out. Execution input: '
                       'exec. Execution output: exec. Data inputs: channel (object), fade_time (number, '
                       'default=0.0). Settings: fade_time. Use the white execution path for ordering and the colored '
                       'pins for values.'},
 'bit_and': {'example': '1. Masking flags',
             'tip': 'Bitwise AND on integers. Data inputs: A (number), B (number). Data outputs: Out (number).'},
 'bit_not': {'example': '1. Inverting bits',
             'tip': 'Bitwise NOT on integers. Data inputs: In (number). Data outputs: Out (number).'},
 'bit_or': {'example': '1. Setting flags',
            'tip': 'Bitwise OR on integers. Data inputs: A (number), B (number). Data outputs: Out (number).'},
 'bit_rol': {'example': '1. Cryptography / RNG',
             'tip': '8-bit Left Rotation. Data inputs: Val (number), Shift (number). Data outputs: Out (number).'},
 'bit_ror': {'example': '1. Cryptography / RNG',
             'tip': '8-bit Right Rotation. Data inputs: Val (number), Shift (number). Data outputs: Out (number).'},
 'bit_shl': {'example': '1. Fast multiply by 2',
             'tip': 'Bitwise Left Shift. Data inputs: Val (number), Shift (number). Data outputs: Out (number).'},
 'bit_shr': {'example': '1. Fast divide by 2',
             'tip': 'Bitwise Right Shift. Data inputs: Val (number), Shift (number). Data outputs: Out (number).'},
 'bit_xor': {'example': '1. Toggling flags',
             'tip': 'Bitwise XOR on integers. Data inputs: A (number), B (number). Data outputs: Out (number).'},
 'calculus_acceleration': {'example': '1. Add Acceleration from the Math category.\n'
                                      '2. Connect velocity, previous, dt.\n'
                                      '3. Use acceleration in the next calculation or condition.',
                           'tip': 'Approximates acceleration from velocity change over time. Data inputs: velocity '
                                  '(number, default=0), previous (number, default=0), dt (number, default=1). Data '
                                  'outputs: acceleration (number). This is a pure data node: wire its colored output '
                                  'directly into another input; no white execution wire is required.'},
 'calculus_average_rate': {'example': '1. Add Average Rate from the Math category.\n'
                                      '2. Connect start, end, dt.\n'
                                      '3. Use rate in the next calculation or condition.',
                           'tip': 'Calculates change divided by elapsed time. Data inputs: start (number, '
                                  'default=0), end (number, default=1), dt (number, default=1). Data outputs: rate '
                                  '(number). This is a pure data node: wire its colored output directly into another '
                                  'input; no white execution wire is required.'},
 'calculus_compound_interest': {'example': '1. Add Compound Interest from the Math category.\n'
                                           '2. Connect principal, rate, periods.\n'
                                           '3. Use amount in the next calculation or condition.',
                                'tip': 'Calculates compounded growth from principal, rate, periods, and time. Data '
                                       'inputs: principal (number, default=100), rate (number, default=0.05), '
                                       'periods (number, default=12), time (number, default=1). Data outputs: amount '
                                       '(number). This is a pure data node: wire its colored output directly into '
                                       'another input; no white execution wire is required.'},
 'calculus_derivative': {'example': '1. Add Derivative from the Math category.\n'
                                    '2. Connect value, previous, dt.\n'
                                    '3. Use derivative in the next calculation or condition.',
                         'tip': 'Approximates dValue/dt from the current and previous values. Data inputs: value '
                                '(number, default=0), previous (number, default=0), dt (number, default=1). Data '
                                'outputs: derivative (number). This is a pure data node: wire its colored output '
                                'directly into another input; no white execution wire is required.'},
 'calculus_exponential_growth': {'example': '1. Add Exponential Growth from the Math category.\n'
                                            '2. Connect initial, rate, time.\n'
                                            '3. Use value in the next calculation or condition.',
                                 'tip': 'Calculates Initial times e to the Rate times Time. Data inputs: initial '
                                        '(number, default=1), rate (number, default=1), time (number, default=0). '
                                        'Data outputs: value (number). This is a pure data node: wire its colored '
                                        'output directly into another input; no white execution wire is required.'},
 'calculus_integral': {'example': '1. Add Integral from the Math category.\n'
                                  '2. Connect value, dt.\n'
                                  '3. Use total in the next calculation or condition.',
                       'tip': 'Accumulates Value times dt every time its white input executes. Execution input: '
                              'exec. Execution output: exec. Data inputs: value (number, default=0), dt (number, '
                              'default=1). Data outputs: total (number). Settings: initial. Use the white execution '
                              'path for ordering and the colored pins for values.'},
 'calculus_kinetic_energy': {'example': '1. Add Kinetic Energy from the Math category.\n'
                                        '2. Connect mass, velocity.\n'
                                        '3. Use energy in the next calculation or condition.',
                             'tip': 'Calculates one half mass velocity squared. Data inputs: mass (number, '
                                    'default=1), velocity (number, default=0). Data outputs: energy (number). This '
                                    'is a pure data node: wire its colored output directly into another input; no '
                                    'white execution wire is required.'},
 'calculus_logistic': {'example': '1. Add Logistic Curve from the Math category.\n'
                                  '2. Connect capacity, rate, time.\n'
                                  '3. Use value in the next calculation or condition.',
                       'tip': 'S-curve growth toward Capacity. Data inputs: capacity (number, default=1), rate '
                              '(number, default=1), time (number, default=0), midpoint (number, default=0). Data '
                              'outputs: value (number). This is a pure data node: wire its colored output directly '
                              'into another input; no white execution wire is required.'},
 'calculus_potential_energy': {'example': '1. Add Potential Energy from the Math category.\n'
                                          '2. Connect mass, gravity, height.\n'
                                          '3. Use energy in the next calculation or condition.',
                               'tip': 'Calculates mass times gravity times height. Data inputs: mass (number, '
                                      'default=1), gravity (number, default=9.81), height (number, default=0). Data '
                                      'outputs: energy (number). This is a pure data node: wire its colored output '
                                      'directly into another input; no white execution wire is required.'},
 'calculus_power_from_work': {'example': '1. Add Power From Work from the Math category.\n'
                                         '2. Connect work, time.\n'
                                         '3. Use power in the next calculation or condition.',
                              'tip': 'Calculates work divided by time. Data inputs: work (number, default=0), time '
                                     '(number, default=1). Data outputs: power (number). This is a pure data node: '
                                     'wire its colored output directly into another input; no white execution wire '
                                     'is required.'},
 'calculus_second_derivative': {'example': '1. Add Second Derivative from the Math category.\n'
                                           '2. Connect value, previous, previous2.\n'
                                           '3. Use second_derivative in the next calculation or condition.',
                                'tip': 'Finite-difference approximation of the second derivative. Data inputs: value '
                                       '(number, default=0), previous (number, default=0), previous2 (number, '
                                       'default=0), dt (number, default=1). Data outputs: second_derivative '
                                       '(number). This is a pure data node: wire its colored output directly into '
                                       'another input; no white execution wire is required.'},
 'calculus_trapezoid_area': {'example': '1. Add Trapezoid Area from the Math category.\n'
                                        '2. Connect a, b, dt.\n'
                                        '3. Use area in the next calculation or condition.',
                             'tip': 'Approximates area under two samples using the trapezoid rule. Data inputs: a '
                                    '(number, default=0), b (number, default=0), dt (number, default=1). Data '
                                    'outputs: area (number). This is a pure data node: wire its colored output '
                                    'directly into another input; no white execution wire is required.'},
 'calculus_velocity': {'example': '1. Add Velocity from the Math category.\n'
                                  '2. Connect position, previous, dt.\n'
                                  '3. Use velocity in the next calculation or condition.',
                       'tip': 'Approximates velocity from position change over time. Data inputs: position (number, '
                              'default=0), previous (number, default=0), dt (number, default=1). Data outputs: '
                              'velocity (number). This is a pure data node: wire its colored output directly into '
                              'another input; no white execution wire is required.'},
 'calculus_work': {'example': '1. Add Work from the Math category.\n'
                              '2. Connect force, distance, angle.\n'
                              '3. Use work in the next calculation or condition.',
                   'tip': 'Calculates force times distance times cosine of angle. Data inputs: force (number, '
                          'default=1), distance (number, default=1), angle (number, default=0). Data outputs: work '
                          '(number). This is a pure data node: wire its colored output directly into another input; '
                          'no white execution wire is required.'},
 'camera_attach_external': {'example': '1. Add Attach External To Camera from the Camera category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Lock an external node to the virtual camera using an ID.'},
 'camera_clear_follow': {'example': '1. Add Clear Virtual Follow from the Camera category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Stop virtual camera character following.'},
 'camera_detach_external': {'example': '1. Add Detach External From Camera from the Camera category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Return an external node to world-space placement.'},
 'camera_disable_virtual': {'example': '1. Add Disable Virtual Camera from the Camera category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Return recording to the live camera view.'},
 'camera_enable_virtual': {'example': '1. Add Enable Virtual Camera from the Camera category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Use the virtual export camera for preview and recording.'},
 'camera_follow_self': {'example': '1. Add Virtual Camera Follow Self from the Camera category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Attach virtual camera follow to the current character.'},
 'camera_follow_target': {'example': '1. Add Virtual Camera Follow Target from the Camera category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Attach virtual camera follow to a target character.'},
 'camera_hide_preview': {'example': '1. Add Hide Virtual Preview from the Camera category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Hide crop overlay without disabling virtual recording camera.'},
 'camera_set_aspect': {'example': '1. Add Set Virtual Aspect from the Camera category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Set virtual crop aspect such as 16:9, 9:16, 1:1, or 4:3.'},
 'camera_set_position': {'example': '1. Add Set Virtual Position from the Camera category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Set virtual camera world position.'},
 'camera_set_zoom': {'example': '1. Add Set Virtual Zoom from the Camera category.\n'
                                '2. Connect the available inputs.\n'
                                '3. Use the output in the next calculation or condition.',
                     'tip': 'Set virtual camera zoom independently from output resolution.'},
 'camera_show_preview': {'example': '1. Add Show Virtual Preview from the Camera category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Show virtual camera crop overlay in the live editor.'},
 'clip_connector': {'example': '1. Add Connector Clip from the Clips category.\n'
                               '2. Connect the available inputs.\n'
                               '3. Use the output in the next calculation or condition.',
                    'tip': 'Like a layout clip, but also FUSES the inspector: selecting either node shows ONE '
                           'combined settings panel under a shared group name you can edit. Great for treating two '
                           'nodes as a single logical unit without clicking each half separately. Settings: '
                           'clipped_to, node_b, group_name, orientation.'},
 'clip_horizontal': {'example': '1. Clip value A and value B horizontally\n'
                                '2. Move them around together as a single row',
                     'tip': 'Fuses two nodes side-by-side into one larger block. The clip itself hides after both '
                            'sides connect — you see one fused shell with a seam. Drag either half to move the whole '
                            'group; click a half for its own inspector. Press X on the seam to unfuse. Settings: '
                            'clipped_to, node_b, group_name.'},
 'clip_paint_bucket': {'example': '1. Add Paint Bucket Clip from the Clips category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Attach to a node or Smart Group to override its editor color.  The change is '
                              'visual/editor-only and does not alter execution.'},
 'clip_vertical': {'example': '1. Clip variable set and math subtract vertically\n'
                              '2. Group related operations into columns',
                   'tip': "Fuses two nodes into one taller stacked block. Inner-left sockets become the fused node's "
                          'left ports; inner-right sockets become right ports. Drag either half to move the group; '
                          'click a half for its own settings. X unfuses. Settings: clipped_to, node_b, group_name.'},
 'collision_disable_shape': {'example': '1. Add Disable Shape from the Collision category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Disable one shape for queries.'},
 'collision_enable_shape': {'example': '1. Add Enable Shape from the Collision category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Enable one shape for queries.'},
 'collision_get_collider': {'example': '1. Add Get Collider from the Collision category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Return the latest collision object.'},
 'collision_get_depth': {'example': '1. Add Get Penetration Depth from the Collision category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Read contact penetration.'},
 'collision_get_layer': {'example': '1. Add Get Collision Layer from the Collision category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': "Read the body's layer mask."},
 'collision_get_mask': {'example': '1. Add Get Collision Mask from the Collision category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': "Read the body's detection mask."},
 'collision_get_normal': {'example': '1. Add Get Collision Normal from the Collision category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Read the latest contact normal.'},
 'collision_get_point': {'example': '1. Add Get Collision Point from the Collision category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Read the latest contact point.'},
 'collision_ignore_pair': {'example': '1. Add Ignore Collision Pair from the Collision category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Temporarily ignore two bodies.'},
 'collision_layer_add': {'example': '1. Add Add Collision Layer from the Collision category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Enable one collision layer bit.'},
 'collision_layer_remove': {'example': '1. Add Remove Collision Layer from the Collision category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Disable one collision layer bit.'},
 'collision_layer_set': {'example': '1. Add Set Collision Layer from the Collision category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': "Set the body's collision layer bitmask."},
 'collision_mask_add': {'example': '1. Add Add Collision Mask from the Collision category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Enable one detection mask bit.'},
 'collision_mask_remove': {'example': '1. Add Remove Collision Mask from the Collision category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Disable one detection mask bit.'},
 'collision_mask_set': {'example': '1. Add Set Collision Mask from the Collision category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Set which layers the body detects.'},
 'collision_query_area': {'example': '1. Add Area Overlap Query from the Collision category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Return bodies in a named area.'},
 'collision_query_box': {'example': '1. Add Box Overlap Query from the Collision category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Return bodies overlapping a rectangle.'},
 'collision_query_circle': {'example': '1. Add Circle Overlap Query from the Collision category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Return bodies overlapping a circle.'},
 'collision_query_point': {'example': '1. Add Point Collision Query from the Collision category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Check for a body at a point.'},
 'collision_query_ray': {'example': '1. Add Ray Collision Query from the Collision category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Cast a ray and return hit data.'},
 'collision_query_shape': {'example': '1. Add Shape Collision Query from the Collision category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Test a shape against nearby bodies.'},
 'collision_restore_pair': {'example': '1. Add Restore Collision Pair from the Collision category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Restore a previously ignored pair.'},
 'collision_set_continuous': {'example': '1. Add Set Continuous Collision from the Collision category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Enable continuous collision detection.'},
 'collision_set_debug_color': {'example': '1. Add Set Collision Debug Color from the Collision category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Color collision visualization.'},
 'collision_set_margin': {'example': '1. Add Set Collision Margin from the Collision category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Set contact separation margin.'},
 'collision_set_monitorable': {'example': '1. Add Set Monitorable from the Collision category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Allow other sensors to detect this body.'},
 'collision_set_monitoring': {'example': '1. Add Set Monitoring from the Collision category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Enable overlap/contact monitoring.'},
 'collision_set_one_way': {'example': '1. Add Set One Way Collision from the Collision category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Allow one-direction platforms.'},
 'collision_set_safe_margin': {'example': '1. Add Set Safe Margin from the Collision category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Set kinematic collision recovery margin.'},
 'collision_set_shape_offset': {'example': '1. Add Set Shape Offset from the Collision category.\n'
                                           '2. Connect the available inputs.\n'
                                           '3. Use the output in the next calculation or condition.',
                                'tip': 'Move a shape relative to the body.'},
 'collision_set_shape_rotation': {'example': '1. Add Set Shape Rotation from the Collision category.\n'
                                             '2. Connect the available inputs.\n'
                                             '3. Use the output in the next calculation or condition.',
                                  'tip': 'Rotate a shape relative to the body.'},
 'collision_set_trigger': {'example': '1. Add Set Trigger Mode from the Collision category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Make collision sensor-only or solid.'},
 'collision_shape_capsule': {'example': '1. Add Capsule Collision Shape from the Collision category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Create a capsule shape descriptor.'},
 'collision_shape_circle': {'example': '1. Add Circle Collision Shape from the Collision category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Create a circle shape descriptor.'},
 'collision_shape_polygon': {'example': '1. Add Polygon Collision Shape from the Collision category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Create a convex polygon descriptor.'},
 'collision_shape_ray': {'example': '1. Add Ray Collision Shape from the Collision category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Create a one-direction ray query.'},
 'collision_shape_rectangle': {'example': '1. Add Rectangle Collision Shape from the Collision category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Create an axis-aligned rectangle shape.'},
 'collision_shape_rounded_box': {'example': '1. Add Rounded Box Shape from the Collision category.\n'
                                            '2. Connect the available inputs.\n'
                                            '3. Use the output in the next calculation or condition.',
                                 'tip': 'Create a box with rounded corners.'},
 'collision_shape_segment': {'example': '1. Add Segment Collision Shape from the Collision category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Create a line segment collision shape.'},
 'collision_show_debug': {'example': '1. Add Show Collision Debug from the Collision category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Toggle visible collision outlines.'},
 'combat_directional_damage': {'example': '1. If attacked from Front -> Damage 0 (Shield Block)\n'
                                          '2. Backstab -> Damage 2x',
                               'tip': 'Deals bonus or reduced damage based on whether the attack came from front or '
                                      'behind. Execution input: exec. Execution output: exec. Data inputs: target '
                                      '(object). Data outputs: matched (boolean). Settings: side, damage, '
                                      'allow_self. Use the white execution path for ordering and the colored pins '
                                      'for values.'},
 'combat_reflect_damage': {'example': '1. Reflect Damage (50%) on hit\n2. Thorn aura -> Reflect Damage',
                           'tip': 'Returns a percentage of incoming damage back to the attacker automatically. '
                                  'Execution input: exec. Execution output: exec. Data inputs: attacker (object), '
                                  'incoming_damage (number, default=0). Settings: percent, allow_self. Use the white '
                                  'execution path for ordering and the colored pins for values.'},
 'command_set_enabled': {'example': '1. Add Command Set Enabled from the Control category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Set a command enabled state.'},
 'command_set_value': {'example': '1. Add Command Set Value from the Control category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Store a numeric command value.'},
 'command_toggle_value': {'example': '1. Add Command Toggle Value from the Control category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Toggle a numeric command between zero and one.'},
 'condition_and': {'example': '1. Is Moving AND HP < 50\n2. Has Tag "enemy" AND Distance < 100',
                   'tip': 'Returns True ONLY if both inputs A and B are True. Boolean AND gate. Data inputs: a '
                          '(boolean, default=True), b (boolean, default=True). Data outputs: result (boolean). This '
                          'is a pure data node: wire its colored output directly into another input; no white '
                          'execution wire is required.'},
 'condition_between': {'example': '1. HP between 25% and 75% -> normal phase\n'
                                  '2. Distance between 50 and 150 -> melee range',
                       'tip': 'Returns True if value is >= min AND <= max. Saves you wiring two Compare nodes '
                              'together. Data inputs: value (number, default=0), min (number, default=0), max '
                              '(number, default=100). Data outputs: result (boolean). Settings: min_val, max_val. '
                              'This is a pure data node: wire its colored output directly into another input; no '
                              'white execution wire is required.'},
 'condition_branch': {'example': '1. Health Check -> Branch. True -> Flee, False -> Attack\n'
                                 '2. Has Tag -> Branch -> True -> Deal Damage',
                      'tip': 'Standard If/Else gate. True fires one output, False fires the other. Requires a '
                             'Boolean input. Execution input: exec. Execution output: true, false. Data inputs: '
                             'condition (boolean, default=True). Use the white execution path for ordering and the '
                             'colored pins for values.'},
 'condition_compare_boolean': {'example': '1. Is Moving == Is Attacking\n2. Has Tag == True',
                               'tip': 'Checks whether two booleans match each other. Data inputs: a (boolean, '
                                      'default=False), b (boolean, default=False). Data outputs: result (boolean). '
                                      'This is a pure data node: wire its colored output directly into another '
                                      'input; no white execution wire is required.'},
 'condition_compare_number': {'example': '1. HP < 50 -> True\n2. Local Variable "hits" >= 3 -> True',
                              'tip': 'Compares two numbers (A < B, A == B, A >= B etc) and outputs a Boolean result. '
                                     'Data inputs: a (number, default=0), b (number, default=0). Data outputs: '
                                     'result (boolean). Settings: operation. This is a pure data node: wire its '
                                     'colored output directly into another input; no white execution wire is '
                                     'required.'},
 'condition_compare_text': {'example': '1. Tag == "boss" -> True\n2. Name == "Skeleton" -> True',
                            'tip': 'Checks whether two strings are exactly equal. Case-sensitive. Data inputs: a '
                                   "(string, default=''), b (string, default=''). Data outputs: result (boolean). "
                                   'Settings: case_sensitive, operation. This is a pure data node: wire its colored '
                                   'output directly into another input; no white execution wire is required.'},
 'condition_distance_check': {'example': '1. Distance from Me to Target < 50 -> Melee Attack\n'
                                         '2. Distance > 300 -> Move Toward',
                              'tip': 'Measures the distance between two objects and compares it to a threshold. '
                                     'Returns a Boolean. Data inputs: a (object), b (object), distance (number, '
                                     'default=100). Data outputs: result (boolean), distance (number). Settings: '
                                     'operation, distance. This is a pure data node: wire its colored output '
                                     'directly into another input; no white execution wire is required.'},
 'condition_has_status': {'example': '1. If Target has "Stun" -> Deal Double Damage\n'
                                     '2. If Self has "Root" -> Ranged Attack',
                          'tip': 'Returns True if a character is currently affected by a named engine status (Stun, '
                                 'Root, Silence, etc). Data inputs: target (object), status (string, '
                                 "default='poison'). Data outputs: result (boolean). Settings: status. This is a "
                                 'pure data node: wire its colored output directly into another input; no white '
                                 'execution wire is required.'},
 'condition_health_check': {'example': '1. Check if Target HP < 20. If True -> Execute\n'
                                       '2. Check if Self HP < 50% -> Use Potion',
                            'tip': "Instantly compares a character's current HP against a threshold value. Returns a "
                                   'Boolean. Data inputs: target (object), value (number, default=50). Data outputs: '
                                   'result (boolean), hp (number), hp_pct (number). Settings: operation, value. This '
                                   'is a pure data node: wire its colored output directly into another input; no '
                                   'white execution wire is required.'},
 'condition_is_idle': {'example': '1. If Is Idle -> Heal over time\n2. If Is Idle -> Random Wander',
                       'tip': 'Returns True if the character is standing completely still (velocity near zero). Data '
                              'inputs: target (object), threshold (number, default=5.0). Data outputs: result '
                              '(boolean). This is a pure data node: wire its colored output directly into another '
                              'input; no white execution wire is required.'},
 'condition_is_moving': {'example': '1. If Is Moving -> Play "walk" animation\n2. If NOT Is Moving -> Play "idle"',
                         'tip': "Returns True if the character's velocity is greater than zero. Data inputs: target "
                                '(object), threshold (number, default=5.0). Data outputs: result (boolean), speed '
                                '(number). This is a pure data node: wire its colored output directly into another '
                                'input; no white execution wire is required.'},
 'condition_is_playing_animation': {'example': '1. If Is Playing "attack" -> Disable Movement\n'
                                               '2. If NOT Is Playing "stun" -> Attack',
                                    'tip': 'Returns True if a specific named animation state is currently active on '
                                           "the character. Data inputs: target (object), state (string, default=''). "
                                           'Data outputs: result (boolean). This is a pure data node: wire its '
                                           'colored output directly into another input; no white execution wire is '
                                           'required.'},
 'condition_not': {'example': '1. NOT Is Moving -> (Character is stationary)\n'
                              '2. NOT Has Tag "shielded" -> Deal Damage',
                   'tip': 'Inverts a Boolean. True becomes False, False becomes True. Data inputs: value (boolean, '
                          'default=False). Data outputs: result (boolean). This is a pure data node: wire its '
                          'colored output directly into another input; no white execution wire is required.'},
 'condition_or': {'example': '1. Has Tag "boss" OR Has Tag "elite"\n2. HP < 10 OR Distance > 500',
                  'tip': 'Returns True if either input A or B is True. Boolean OR gate. Data inputs: a (boolean, '
                         'default=False), b (boolean, default=False). Data outputs: result (boolean). This is a pure '
                         'data node: wire its colored output directly into another input; no white execution wire is '
                         'required.'},
 'condition_random_chance': {'example': '1. Use as input to a Branch. 30% chance to Crit\n'
                                        '2. 50% chance -> Branch -> Move Left / Move Right',
                             'tip': 'Returns True or False based on a percentage (0-100). The simplest way to add '
                                    'RNG to any logic. Data inputs: chance (number, default=50). Data outputs: '
                                    'result (boolean). Settings: chance. This is a pure data node: wire its colored '
                                    'output directly into another input; no white execution wire is required.'},
 'condition_random_range': {'example': '1. Random Range (1 to 5) -> Deal Damage\n'
                                       '2. Random Range (0.5 to 2.0) -> Delay',
                            'tip': 'Returns a random decimal number between Min and Max each time it is evaluated. '
                                   'Data inputs: min (number, default=0), max (number, default=1). Data outputs: '
                                   'value (number). Settings: integer. This is a pure data node: wire its colored '
                                   'output directly into another input; no white execution wire is required.'},
 'condition_solo_else': {'example': '1. Add ELSE from the Conditions category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'False-only branch that runs when its condition is false.'},
 'condition_solo_if': {'example': '1. Add IF from the Conditions category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'True-only branch. Existing If / Else remains unchanged.'},
 'condition_xor': {'example': '1. Has shield XOR has armour -> unique interaction\n'
                              '2. Trigger A XOR Trigger B -> mutual exclusion',
                   'tip': 'True only when exactly one input is True. If both are True or both are False, returns '
                          'False. Data inputs: a (boolean, default=False), b (boolean, default=False). Data outputs: '
                          'result (boolean). This is a pure data node: wire its colored output directly into another '
                          'input; no white execution wire is required.'},
 'cpu_alu_add': {'example': '1. 8-bit math',
                 'tip': 'Simulates ALU addition with overflow check. Data inputs: A (number), B (number). Data '
                        'outputs: Sum (number), Overflow (boolean).'},
 'cpu_alu_div': {'example': '1. Safe math',
                 'tip': 'Simulates ALU division, handles Div0. Data inputs: A (number), B (number). Data outputs: '
                        'Quot (number), DivZero (boolean).'},
 'cpu_alu_mul': {'example': '1. 16-bit out',
                 'tip': 'Simulates ALU multiplication. Data inputs: A (number), B (number). Data outputs: Prod '
                        '(number), Overflow (boolean).'},
 'cpu_alu_sub': {'example': '1. 8-bit math',
                 'tip': 'Simulates ALU subtraction with underflow flag. Data inputs: A (number), B (number). Data '
                        'outputs: Diff (number), Underflow (boolean).'},
 'cpu_clock_gen': {'example': '1. Pulse an LED',
                   'tip': 'Outputs a repeating clock signal boolean over time. Data inputs: Frequency (number). Data '
                          'outputs: Tick (boolean).'},
 'cpu_inst_dec': {'example': '1. Opcode router',
                  'tip': 'Decodes an opcode into execution branches. Execution input: exec. Execution output: Op 0, '
                         'Op 1, Op 2, Op 3. Data inputs: Opcode (number). Use the white execution path for ordering '
                         'and the colored pins for values.'},
 'cpu_prog_counter': {'example': '1. Array iteration',
                      'tip': 'Increments a counter on execution, resettable. Execution input: exec. Execution '
                             'output: exec. Data inputs: Reset (boolean). Data outputs: Count (number). Use the '
                             'white execution path for ordering and the colored pins for values.'},
 'cpu_tick': {'example': '1. Reliable system tick',
              'tip': 'Fires every X milliseconds exactly. Execution output: exec. Settings: ms. Use the white '
                     'execution path for ordering and the colored pins for values.'},
 'debug_assert': {'example': '1. Assert HP > 0 is True\n'
                             '2. Flashes green checkmark on success, or red cross + alarm beep on failure',
                  'tip': 'Asserts that a connected boolean condition is True, throwing an assertion warning on '
                         'failure. Execution input: exec_in. Execution output: exec_out. Data inputs: condition '
                         '(boolean). Settings: error_message. Use the white execution path for ordering and the '
                         'colored pins for values.'},
 'debug_breakpoint': {'example': '1. Put Breakpoint right before HP set\n'
                                 '2. Simulation pauses, letting you inspect all preceding math values',
                      'tip': 'Immediately pauses step-by-step canvas execution when a signal reaches this node. '
                             'Execution input: exec_in. Execution output: exec_out. Settings: active. Use the white '
                             'execution path for ordering and the colored pins for values.'},
 'debug_button': {'example': '1. Add Debug Button from the Debugging category.\n'
                             '2. Connect the available inputs.\n'
                             '3. Use the output in the next calculation or condition.',
                  'tip': 'A real clickable control node in Canvas Debug. Choose Run, Step, Pause/Resume, Reset, '
                         'Preview, camera-follow, path-dimming, toggle, or force actions in the inspector. Connect '
                         'it to a host or drop it on any node body. Execution output: exec. Settings: label, action. '
                         'Use the white execution path for ordering and the colored pins for values.'},
 'debug_clamp_debug_only': {'example': '1. Add Debug-Only Clip from the Debugging category.\n'
                                       '2. Connect value.\n'
                                       '3. Use value_out in the next calculation or condition.',
                            'tip': 'Clip this onto ANY node to mark it as DEBUG-ONLY / INTERNAL. Canvas debug Play '
                                   'still runs that node (flash, popups, forced values). When the real game script '
                                   "is generated/exported, that node's action is skipped and execution just passes "
                                   'through — perfect for test Deal Damage, mock spawns, etc. Unclip to re-enable '
                                   'the live action. Execution input: exec_in. Execution output: exec_out. Data '
                                   'inputs: value (any). Data outputs: value_out (any). Settings: clamped_to, '
                                   'pass_through, label. Use the white execution path for ordering and the colored '
                                   'pins for values.'},
 'debug_clamp_duration': {'example': '1. Clip Duration Clamp onto Delay node\n'
                                     '2. Multiplier set to 0.1 to accelerate testing of long cooldowns',
                          'tip': 'Clamps onto timing and delay nodes to speed up, slow down, or fully freeze their '
                                 'durations during debugging. Execution input: exec_in. Execution output: exec_out. '
                                 'Settings: clamped_to, time_multiplier. Use the white execution path for ordering '
                                 'and the colored pins for values.'},
 'debug_clamp_loop': {'example': '1. Clip Loop Clamp onto Trigger N Times\n'
                                 '2. Pause loop iterations and verify math outputs per cycle',
                      'tip': 'Clamps onto repeating loop nodes to freeze them and let you manually step through each '
                             'iteration cycle. Execution input: exec_in. Execution output: loop_body, completed. '
                             'Settings: clamped_to, pause_on_each. Use the white execution path for ordering and the '
                             'colored pins for values.'},
 'debug_clamp_standard': {'example': '1. Clip Standard Clamp onto On Hit\n'
                                     '2. Trigger execution manually via Play/Step buttons in Inspector',
                          'tip': 'A universal clamping node. Place directly on top of any other node to clip onto '
                                 'it, allowing you to force its execution or simulate clicks. Execution input: '
                                 'exec_in. Execution output: exec_out. Data inputs: value (any). Data outputs: '
                                 'value_out (any). Settings: clamped_to, force_value. Use the white execution path '
                                 'for ordering and the colored pins for values.'},
 'debug_clamp_step': {'example': '1. Clip Step Clamp onto On Tick\n2. Walk through variables and math step-by-step',
                      'tip': 'Clamps onto a node and runs connected logic exactly one step at a time when you click '
                             "'Step'. Execution input: exec_in. Execution output: exec_out. Settings: clamped_to, "
                             'current_step. Use the white execution path for ordering and the colored pins for '
                             'values.'},
 'debug_clamp_value_forcer': {'example': "1. Clip Value Forcer Clamp onto Subtract's result pin\n"
                                         '2. Force damage dealt to exactly 999 for execute tests',
                              'tip': 'Clamps onto any data connection to force its output to a specific constant '
                                     'value, bypassing calculations. Data inputs: value_in (any). Data outputs: '
                                     'value_out (any). Settings: clamped_to, override_active, forced_number, '
                                     'forced_string.'},
 'debug_cond_switch': {'example': '1. Force route to True path\n'
                                  '2. Verify ability triggers even if condition is evaluate-false',
                       'tip': 'Manually routes the signal down either the True or False path, regardless of input '
                              'condition. Execution input: exec_in. Execution output: on_true, on_false. Data '
                              'inputs: condition (boolean). Settings: force_path. Use the white execution path for '
                              'ordering and the colored pins for values.'},
 'debug_converter': {'example': '1. Route Subtract through Converter\n'
                                '2. Select Subtract to open Canvas Debugger options in inspector',
                     'tip': 'A data and execution bypass. Connect any node through this converter to enable '
                            'debugging options, logging, and custom simulation on that node. Execution input: '
                            'exec_in. Execution output: exec_out. Data inputs: value_in (any). Data outputs: '
                            'value_out (any). Use the white execution path for ordering and the colored pins for '
                            'values.'},
 'debug_dummy_target': {'example': "1. Mock target with Name='TargetDummy' and Team='Blue'\n"
                                   '2. Test broadcast events or friendly-fire logic',
                        'tip': 'Outputs a dummy character object with custom names and teams. Data outputs: target '
                               '(object). Settings: name, team.'},
 'debug_event_simulator': {'example': '1. Simulate On Damage Taken\n'
                                      '2. Force simulated dealt value to 25 to test defense reduction',
                           'tip': 'Fakes core events (On Spawn, On Hit, On Damage) with configurable mock variables. '
                                  'Execution output: exec_out. Data outputs: dealt (number), crit (boolean). '
                                  'Settings: event_type, dealt, crit. Use the white execution path for ordering and '
                                  'the colored pins for values.'},
 'debug_expander': {'example': '1. Clip Expander onto Log Terminal\n'
                               '2. Opens large 420x340px oscilloscope / radar / spacious monospace terminal display',
                    'tip': 'Clip onto a debugger (terminal, graph, vector, watcher). Select it to open the '
                           'right-panel DEBUG tab for the full log / live values — no floating overlay. Execution '
                           'input: exec_in. Execution output: exec_out. Data inputs: value_in (any). Data outputs: '
                           'value_out (any). Settings: clamped_to. Use the white execution path for ordering and the '
                           'colored pins for values.'},
 'debug_math_graph': {'example': '1. Connect speed variable to Grapher\n'
                                 '2. See live scroll wave plotting of acceleration/easing curves',
                      'tip': 'Renders a mini real-time graph of a connected numeric value directly inside the node '
                             'block. Data inputs: value (number).'},
 'debug_mock_fighter': {'example': '1. Output mock fighter with HP=100 and Shield=50\n'
                                   "2. Connect mock fighter as 'target' to damage dealer",
                        'tip': 'Generates a mock character object with custom configurable health, shields, and '
                               'defense statistics. Data outputs: fighter (object). Settings: hp, shield, defense.'},
 'debug_probe': {'example': '1. Put Probe between Delay and Spawn Duplicate\n'
                            '2. Verify the exact timestamp when signal arrived',
                 'tip': 'Logs signals and values passing through it, displaying timestamps on the node itself. '
                        'Execution input: exec_in. Execution output: exec_out. Data inputs: value (any). Settings: '
                        'prefix. Use the white execution path for ordering and the colored pins for values.'},
 'debug_signal_mux': {'example': '1. Route input to Channel B\n'
                                 '2. Dynamically swap active ability paths during canvas tests',
                      'tip': 'Routes an incoming execution signal to one of three manual destination channels (A, B, '
                             'or C). Execution input: exec_in. Execution output: out_a, out_b, out_c. Settings: '
                             'channel. Use the white execution path for ordering and the colored pins for values.'},
 'debug_sound_test': {'example': '1. Connect critical hit output to Sound Test\n'
                                 '2. Listen for beep frequency changes during step-by-step canvas test',
                      'tip': 'Plays a high-fidelity test synthesizer sound when hit by an execution signal. '
                             'Execution input: exec_in. Execution output: exec_out. Settings: frequency, volume. Use '
                             'the white execution path for ordering and the colored pins for values.'},
 'debug_terminal': {'example': '1. Connect On Spawn to Log Terminal\n'
                               '2. View last 5 trace log lines in glowing amber monospace font',
                    'tip': 'Displays a scrollable historical terminal listing of all signals and data passing '
                           'through it. Execution input: exec_in. Execution output: exec_out. Settings: max_lines. '
                           'Use the white execution path for ordering and the colored pins for values.'},
 'debug_timing_gate': {'example': "1. 'Start' on On Spawn, 'Stop' on On Hit\n"
                                  '2. Measure the exact speed of first engagement',
                       'tip': 'Calculates and displays the exact time elapsed (in milliseconds) between start and '
                              'stop inputs. Execution input: start, stop. Execution output: exec_out. Use the white '
                              'execution path for ordering and the colored pins for values.'},
 'debug_trigger_counter': {'example': '1. Increments counter on each repeat cycle\n'
                                      '2. View digit count displayed inside glowing green digital LED screen',
                           'tip': 'Keeps track of how many times execution signals have passed through, with a reset '
                                  'option. Execution input: exec_in. Execution output: exec_out. Settings: count. '
                                  'Use the white execution path for ordering and the colored pins for values.'},
 'debug_vector_visualizer': {'example': '1. Connect fighter velocity to Vector Visualizer\n'
                                        '2. Real-time arrow points in movement angle direction',
                             'tip': 'Visualizes a 2D vector as a graphic arrow showing speed and direction directly '
                                    'on the node. Data inputs: vector (vector).'},
 'debug_watcher': {'example': "1. Connect a variable's output to Watcher\n"
                              '2. View live value update inside retro glowing cyan LCD panel on node',
                   'tip': 'Displays a connected value in real-time. Extremely useful for debugging variables or '
                          'combat mathematics. Data inputs: value (any).'},
 'debug_window_expander': {'example': '1. Add Debug Toggle Window from the Debugging category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'A persistent DEBUG TOOLS window. Clip it onto a Debug Button or host node to '
                                  'expose named debug buttons in one shared, non-closable control panel.'},
 'direction_cardinal': {'example': '1. Cardinal Direction (North) -> Move Toward\n2. Cardinal Direction (North East)',
                        'tip': 'Toggle North/South/East/West. North + East automatically becomes a normalized '
                               'diagonal. Data outputs: direction (vector).'},
 'direction_cardinal_damage': {'example': '1. Cardinal Damage (North, 200) -> Cleave attack\n'
                                          '2. Cross attack -> Cardinal Damage 4-ways',
                               'tip': 'Damage only North/Top, South/Bottom, East/Right, West/Left, or any diagonal '
                                      'combination, between minimum and maximum distance. Execution input: exec. '
                                      'Execution output: exec. Data inputs: origin (vector), direction (vector), '
                                      'damage (number, default=25). Data outputs: hit_characters (object). Settings: '
                                      'shape, min_distance, max_distance, width, angle, damage, team_filter, '
                                      'allow_self. Use the white execution path for ordering and the colored pins '
                                      'for values.'},
 'direction_cardinal_offset': {'example': '1. Target Position + Offset (North, 100) -> Dash to position behind '
                                          'target\n'
                                          '2. Spawn Object at Offset',
                               'tip': 'Move a world position a chosen distance in a cardinal/diagonal direction. '
                                      'Data inputs: origin (vector), direction (vector), distance (number, '
                                      'default=100). Data outputs: position (vector). Settings: distance.'},
 'direction_cardinal_targets': {'example': '1. Get Targets (North) -> For Each -> Heal\n'
                                           '2. Get Targets (East) -> Push',
                                'tip': 'Returns characters strictly in a North/South/East/West direction from the '
                                       'source. Data inputs: origin (vector), direction (vector). Data outputs: '
                                       'characters (object). Settings: shape, min_distance, max_distance, width, '
                                       'angle, team_filter, include_self.'},
 'direction_combine': {'example': '1. Combine (Facing) + (Right) -> Diagonal dodge\n2. Combine North + East',
                       'tip': 'Add two vectors and normalize them; North plus East becomes North East. Data inputs: '
                              'a (vector, default=(0, -1)), b (vector, default=(1, 0)). Data outputs: direction '
                              '(vector).'},
 'direction_facing': {'example': '1. Facing Direction -> Damage Cone\n2. Facing Direction -> Offset -> Spawn Shield',
                      'tip': 'Returns the direction the character is currently moving as a normalized vector. Data '
                             'inputs: character (object). Data outputs: direction (vector).'},
 'direction_front_behind': {'example': '1. Is Target Behind Me? -> True -> Turn Around\n'
                                       '2. Is Target In Front? -> Melee Attack',
                            'tip': 'Returns True if target B is in front of or behind source A based on movement '
                                   'direction. Data inputs: observer (object), target (object). Data outputs: result '
                                   '(boolean). Settings: side.'},
 'direction_preset': {'example': '1. Direction Preset (Up) -> Dash\n2. Direction Preset (Forward)',
                      'tip': 'Outputs a common predefined direction vector (Up, Down, Left, Right, Forward). Data '
                             'outputs: direction (vector). Settings: direction.'},
 'direction_to_target': {'example': '1. Direction To Target -> Dash\n2. Direction To Target -> Spawn Projectile',
                         'tip': 'Calculates the normalized direction vector pointing from A toward B. Data inputs: '
                                'from (object), target (object). Data outputs: direction (vector).'},
 'event_on_ally_died': {'example': '1. On Ally Died -> Revive Ally (50% HP)\n2. On Ally Died -> Set Tag ("enraged")',
                        'tip': 'Event hook for on ally died. Execution output: exec. Use the white execution path '
                               'for ordering and the colored pins for values.'},
 'event_on_ally_spawn': {'example': '1. On Ally Spawn -> Share Target (current target)\n'
                                    '2. On Ally Spawn -> Heal new ally',
                         'tip': 'Event hook for on ally spawn. Execution output: exec. Use the white execution path '
                                'for ordering and the colored pins for values.'},
 'event_on_animation_finished': {'example': '1. On Anim Finished ("reload") -> Set Variable ("ammo", 10)\n'
                                            '2. On Anim Finished ("cast") -> Spawn Explosion',
                                 'tip': 'Event hook for on animation finished. Execution output: exec. Use the white '
                                        'execution path for ordering and the colored pins for values.'},
 'event_on_broadcast': {'example': '1. On Broadcast ("focus_fire") -> Move Toward (Payload Target)\n'
                                   '2. On Broadcast ("retreat") -> Move Away (Enemy)',
                        'tip': 'Event hook for on broadcast. Execution output: exec. Use the white execution path '
                               'for ordering and the colored pins for values.'},
 'event_on_collision': {'example': '1. On Collision -> Knockback (500 force)\n2. On Collision -> Deal Damage (10)',
                        'tip': 'Event hook for on collision. Execution output: exec. Use the white execution path '
                               'for ordering and the colored pins for values.'},
 'event_on_critical_hit': {'example': '1. On Critical Hit -> Spawn Explosion (Radius 50)\n'
                                      '2. On Critical Hit -> Heal Self (20)',
                           'tip': 'Event hook for on critical hit. Execution output: exec. Use the white execution '
                                  'path for ordering and the colored pins for values.'},
 'event_on_critical_taken': {'example': '1. On Critical Taken -> Camera Shake\n'
                                        '2. On Critical Taken -> Counter-attack with Parry Window',
                             'tip': 'Event hook for on critical taken. Execution output: exec. Use the white '
                                    'execution path for ordering and the colored pins for values.'},
 'event_on_damage_dealt': {'example': '1. On Damage Dealt -> Variable Increment ("total_damage_done")\n'
                                      '2. On Damage Dealt -> Print To Screen (Damage Amount)',
                           'tip': 'Event hook for on damage dealt. Execution output: exec. Use the white execution '
                                  'path for ordering and the colored pins for values.'},
 'event_on_damage_taken': {'example': '1. On Damage Taken -> Reflect Damage (50%)\n'
                                      '2. On Damage Taken -> Flash Tint (White)',
                           'tip': 'Event hook for on damage taken. Execution output: exec. Use the white execution '
                                  'path for ordering and the colored pins for values.'},
 'event_on_death': {'example': '1. On Death -> Spawn Swarm (5)\n2. On Death -> Drop Item (Spawn Object)',
                    'tip': 'Event hook for on death. Execution output: exec. Use the white execution path for '
                           'ordering and the colored pins for values.'},
 'event_on_despawn': {'example': '1. On Despawn -> Spawn Particles\n2. On Despawn -> Spawn Explosion at position',
                      'tip': 'Event hook for on despawn. Execution output: exec. Use the white execution path for '
                             'ordering and the colored pins for values.'},
 'event_on_destroy': {'example': '1. On Destroy -> Spawn Particle\n2. On Destroy -> Play Sound ("poof.wav")',
                      'tip': 'Event hook for on destroy. Execution output: exec. Use the white execution path for '
                             'ordering and the colored pins for values.'},
 'event_on_enemy_spawn': {'example': '1. On Enemy Spawn -> Move Toward new enemy\n'
                                     "2. On Enemy Spawn -> Broadcast 'new_threat'",
                          'tip': 'Event hook for on enemy spawn. Execution output: exec. Use the white execution '
                                 'path for ordering and the colored pins for values.'},
 'event_on_external_node_tick': {'example': '1. Add On External Node Tick from the Events category.\n'
                                            '2. Connect the available inputs.\n'
                                            '3. Use the output in the next calculation or condition.',
                                 'tip': 'Event hook for on external node tick. Execution output: exec. Use the white '
                                        'execution path for ordering and the colored pins for values.'},
 'event_on_first_kill': {'example': '1. On First Kill -> Set Speed Limits (max=400) — first blood buff\n'
                                    '2. On First Kill -> Spawn Swarm (2)',
                         'tip': 'Event hook for on first kill. Execution output: exec. Use the white execution path '
                                'for ordering and the colored pins for values.'},
 'event_on_full_heal': {'example': "1. On Full Heal -> Remove Tag 'wounded'\n2. On Full Heal -> Broadcast 'healed'",
                        'tip': 'Event hook for on full heal. Execution output: exec. Use the white execution path '
                               'for ordering and the colored pins for values.'},
 'event_on_game_end': {'example': "1. On Game End -> Play 'victory' animation\n"
                                  '2. On Game End -> Spawn Explosion at self',
                       'tip': 'Event hook for on game end. Execution output: exec. Use the white execution path for '
                              'ordering and the colored pins for values.'},
 'event_on_game_start': {'example': '1. On Game Start -> Set Speed Limits\n'
                                    "2. On Game Start -> Broadcast 'fight_started'",
                         'tip': 'Event hook for on game start. Execution output: exec. Use the white execution path '
                                'for ordering and the colored pins for values.'},
 'event_on_half_hp': {'example': '1. On Half HP -> Set Speed Limits (max=450) — speed boost\n'
                                 '2. On Half HP -> Once -> Transform (change sprite, stats)',
                      'tip': 'Event hook for on half hp. Execution output: exec. Use the white execution path for '
                             'ordering and the colored pins for values.'},
 'event_on_heal': {'example': '1. On Heal -> Spawn Particle ("green_plus")\n2. On Heal -> Print To Screen ("+HP")',
                   'tip': 'Event hook for on heal. Execution output: exec. Use the white execution path for ordering '
                          'and the colored pins for values.'},
 'event_on_hit': {'example': '1. On Hit -> Lifesteal (10%)\n2. On Hit -> Apply Status ("Poison", 3s)',
                  'tip': 'Event hook for on hit. Execution output: exec. Use the white execution path for ordering '
                         'and the colored pins for values.'},
 'event_on_input': {'example': '1. On Input ("Space") -> Dash To Position\n2. On Input ("E") -> Trigger Explosion',
                    'tip': 'Event hook for on input. Execution output: exec. Use the white execution path for '
                           'ordering and the colored pins for values.'},
 'event_on_kill': {'example': '1. On Kill -> Spawn Library Character ("Zombie")\n'
                              '2. On Kill -> Play Sound ("evil_laugh.wav")',
                   'tip': 'Event hook for on kill. Execution output: exec. Use the white execution path for ordering '
                          'and the colored pins for values.'},
 'event_on_kill_streak': {'example': '1. On Kill Streak -> Compare streak >= 3 -> Branch -> Enrage\n'
                                     '2. Kill Streak -> Print Value',
                          'tip': 'Event hook for on kill streak. Execution output: exec. Use the white execution '
                                 'path for ordering and the colored pins for values.'},
 'event_on_low_hp': {'example': '1. Add On Low HP (≤25%) from the Events category.\n'
                                '2. Connect the available inputs.\n'
                                '3. Use the output in the next calculation or condition.',
                     'tip': 'Event hook for on low hp. Execution output: exec. Use the white execution path for '
                            'ordering and the colored pins for values.'},
 'event_on_mouse_click': {'example': '1. On Mouse Click -> Deal Damage (9999) (God hand)\n'
                                     '2. On Mouse Click -> Print Target Details',
                          'tip': 'Event hook for on mouse click. Execution output: exec. Use the white execution '
                                 'path for ordering and the colored pins for values.'},
 'event_on_near_death': {'example': '1. On Near Death -> Set Invulnerable (2s) -> panic mode\n'
                                    '2. On Near Death -> Spawn Swarm (3) — last stand',
                         'tip': 'Event hook for on near death. Execution output: exec. Use the white execution path '
                                'for ordering and the colored pins for values.'},
 'event_on_parry': {'example': '1. On Parry -> Knockback attacker (force 800)\n'
                               '2. On Parry -> Screen Flash + Camera Shake',
                    'tip': 'Event hook for on parry. Execution output: exec. Use the white execution path for '
                           'ordering and the colored pins for values.'},
 'event_on_phase_change': {'example': '1. On Phase Change -> Compare phase == 2 -> Branch -> new AI\n'
                                      "2. On Phase Change -> Print Value (label='Phase')",
                           'tip': 'Event hook for on phase change. Execution output: exec. Use the white execution '
                                  'path for ordering and the colored pins for values.'},
 'event_on_revive': {'example': '1. On Revive -> Set HP to 50% -> Add Shield 100\n'
                                "2. On Revive -> Broadcast 'revived' to allies",
                     'tip': 'Event hook for on revive. Execution output: exec. Use the white execution path for '
                            'ordering and the colored pins for values.'},
 'event_on_shield_broken': {'example': '1. On Shield Broken -> Camera Shake + Screen Flash\n'
                                       '2. On Shield Broken -> Apply Status stun (0.5s)',
                            'tip': 'Event hook for on shield broken. Execution output: exec. Use the white execution '
                                   'path for ordering and the colored pins for values.'},
 'event_on_shield_gained': {'example': "1. On Shield Gained -> Play Animation 'shield_up'\n"
                                       '2. On Shield Gained -> Tint Ease (blue glow)',
                            'tip': 'Event hook for on shield gained. Execution output: exec. Use the white execution '
                                   'path for ordering and the colored pins for values.'},
 'event_on_spawn': {'example': '1. On Spawn -> Set Max HP (500)\n2. On Spawn -> Add Shield (100)',
                    'tip': 'Event hook for on spawn. Execution output: exec. Use the white execution path for '
                           'ordering and the colored pins for values.'},
 'event_on_sprite_changed': {'example': '1. On Sprite Changed ("attack") -> Play Sound ("swing.wav")\n'
                                        '2. On Sprite Changed ("idle") -> Stop Audio',
                             'tip': 'Event hook for on sprite changed. Execution output: exec. Use the white '
                                    'execution path for ordering and the colored pins for values.'},
 'event_on_start': {'example': '1. On Start -> Print To Screen ("Ready!")\n2. On Start -> Move Toward (Center)',
                    'tip': 'Event hook for on start. Execution output: exec. Use the white execution path for '
                           'ordering and the colored pins for values.'},
 'event_on_stun_applied': {'example': "1. On Stunned -> Play 'stun_stars' animation\n"
                                      "2. On Stunned -> Increment local 'times_stunned'",
                           'tip': 'Event hook for on stun applied. Execution output: exec. Use the white execution '
                                  'path for ordering and the colored pins for values.'},
 'event_on_stun_ended': {'example': '1. On Stun Ended -> Move Toward nearest enemy\n'
                                    '2. On Stun Ended -> Counter-attack',
                         'tip': 'Event hook for on stun ended. Execution output: exec. Use the white execution path '
                                'for ordering and the colored pins for values.'},
 'event_on_summoned': {'example': '1. On Summoned -> Set Team same as summoner\n'
                                  "2. On Summoned -> Share Target (summoner's target)",
                       'tip': 'Event hook for on summoned. Execution output: exec. Use the white execution path for '
                              'ordering and the colored pins for values.'},
 'event_on_tag_added': {'example': '1. On Tag Added ("poison") -> Damage Over Time\n'
                                   '2. On Tag Added ("shielded") -> Add Shield (100)',
                        'tip': 'Event hook for on tag added. Execution output: exec. Use the white execution path '
                               'for ordering and the colored pins for values.'},
 'event_on_tag_removed': {'example': '1. On Tag Removed ("shielded") -> Remove Shield\n'
                                     '2. On Tag Removed ("stunned") -> Move Toward (Enemy)',
                          'tip': 'Event hook for on tag removed. Execution output: exec. Use the white execution '
                                 'path for ordering and the colored pins for values.'},
 'event_on_tick': {'example': '1. Every Frame -> Get Local Variable -> Move Toward\n'
                              '2. Every Frame -> Distance Check -> Branch',
                   'tip': 'Event hook for on tick. Execution output: exec. Use the white execution path for ordering '
                          'and the colored pins for values.'},
 'event_on_wall_bounce': {'example': '1. On Wall Bounce -> Deal Damage to nearby enemies\n'
                                     '2. On Wall Bounce -> Spawn Particles',
                          'tip': 'Event hook for on wall bounce. Execution output: exec. Use the white execution '
                                 'path for ordering and the colored pins for values.'},
 'explosive_chain_reaction': {'example': '1. Spawn Explosion -> Chain Reaction (Radius 50)\n'
                                         '2. Chain Reaction -> Massive wipe',
                              'tip': 'Triggers secondary explosions on targets killed by the primary explosion. '
                                     'Settings: radius, damage, force, animation, team_filter, allow_self, falloff.'},
 'explosive_falloff': {'example': '1. Falloff Damage (Max 100, Radius 200) -> Deal Damage\n'
                                  '2. Explosion Falloff -> Deal Damage Over Path',
                       'tip': 'Scales damage based on distance from the epicenter -- full damage at center, less at '
                              'edge. Data inputs: damage (number, default=100), distance (number, default=0), radius '
                              '(number, default=100). Data outputs: damage (number).'},
 'explosive_proximity': {'example': '1. Every Frame -> Proximity Trigger (50) -> Spawn Explosion\n'
                                    '2. Proximity Trigger -> Snap Trap',
                         'tip': 'An execution gate -- only fires when an enemy enters the trigger radius. Like a '
                                'landmine. Data inputs: position (vector). Data outputs: triggered (boolean), '
                                'characters (object). Settings: radius, team_filter.'},
 'explosive_spawn': {'example': '1. On Death -> Spawn Explosion (Radius 100, Damage 50)\n'
                                '2. Grenade -> Spawn Explosion',
                     'tip': 'Creates an AoE explosion: deals damage and knockback to everyone in the radius '
                            'simultaneously. Execution input: exec. Execution output: exec. Data inputs: position '
                            '(vector). Settings: radius, damage, force, animation, team_filter, allow_self, falloff. '
                            'Use the white execution path for ordering and the colored pins for values.'},
 'ext_add_tag': {'example': "1. On Spawn → Create Node → Add Tag 'player_hp'\n"
                            '2. Tag with team name for batch updates',
                 'tip': 'Add a tag to an external node so it can be found by Find By Tag. Execution input: exec. '
                        "Execution output: exec. Data inputs: node (object), tag (string, default='my_tag'). "
                        'Settings: tag, node_id. Use the white execution path for ordering and the colored pins for '
                        'values.'},
 'ext_clear_grid': {'example': '1. Add Clear Grid from the Scene category.\n'
                               '2. Connect node.\n'
                               '3. Use the output in the next calculation or condition.',
                    'tip': 'Clear all painted cells in a Grid external node back to transparent. Execution input: '
                           'exec. Execution output: exec. Data inputs: node (object). Settings: node_id. Use the '
                           'white execution path for ordering and the colored pins for values.'},
 'ext_create_light': {'example': '1. Create Light (Red) -> Attach to Character\n2. Spawn at explosion',
                      'tip': 'Spawns an external node that emits light in the darkness. Execution input: exec. '
                             'Execution output: exec. Data inputs: Position (vector), Color (color), Radius '
                             '(number), Intensity (number). Data outputs: Light Node (object). Use the white '
                             'execution path for ordering and the colored pins for values.'},
 'ext_create_node': {'example': '1. Add Create External Node from the Scene category.\n'
                                '2. Connect position.\n'
                                '3. Use node in the next calculation or condition.',
                     'tip': 'Dynamically create an external node at runtime from a script. Kinds: text_label · '
                            'rect_box · progress_bar · counter · grid Execution input: exec. Execution output: exec. '
                            'Data inputs: position (vector). Data outputs: node (object). Settings: kind. Use the '
                            'white execution path for ordering and the colored pins for values.'},
 'ext_create_typed': {'example': "1. Create text_label, tag='timer', group='hud' at center\n"
                                 "2. Create circle, tag='zone' at character position",
                      'tip': 'Create a specific kind of external node with inline property overrides. More explicit '
                             'than Create External Node — sets kind-specific props directly. Execution input: exec. '
                             'Execution output: exec. Data inputs: position (vector). Data outputs: node (object). '
                             'Settings: kind, name, tag, group, layer. Use the white execution path for ordering and '
                             'the colored pins for values.'},
 'ext_find_group': {'example': "1. Find By Group 'enemies' → For Each → Set Color\n"
                               "2. Find By Group 'walls' → hide all",
                    'tip': 'Return all external nodes in a named group. Data inputs: group (string, '
                           "default='group_1'). Data outputs: nodes (any), count (number). Settings: group."},
 'ext_find_tag': {'example': "1. Find By Tag 'hp_bar' → For Each → Set Node Value\n"
                             "2. Find By Tag 'timer_label' → first → Set Text Formatted",
                  'tip': 'Return all external nodes that carry a specific tag. Wire the tag from a Constant String '
                         'or Format String. Use Get First for a single result. Data inputs: tag (string, '
                         "default='my_tag'). Data outputs: nodes (any), first (object), count (number). Settings: "
                         'tag.'},
 'ext_for_each_tag': {'example': "1. For Each 'hp_bar' → Set Value to HP%\n"
                                 "2. For Each 'wall' → Set Color based on timer",
                      'tip': 'Loop body fires once for every external node that has the given tag. Outputs the '
                             'current node and its index. Execution input: exec. Execution output: body, done. Data '
                             "inputs: tag (string, default='my_tag'). Data outputs: node (object), index (number). "
                             'Settings: tag, max_iterations. Use the white execution path for ordering and the '
                             'colored pins for values.'},
 'ext_get_meta': {'example': "1. Get Meta 'spawn_time' → Subtract Elapsed → age of node\n"
                             "2. Read 'owner' → Get character",
                  'tip': 'Read a metadata value from an external node. Returns the default if not set. Data inputs: '
                         "node (object), key (string, default='my_key'). Data outputs: value (any). Settings: "
                         'node_id, key.'},
 'ext_get_node': {'example': '1. Add Get External Node from the Scene category.\n'
                             '2. Connect A, B.\n'
                             '3. Use Out in the next calculation or condition.',
                  'tip': 'Finds an external scene node by its numeric ID or by name. Returns the node object so '
                         'other nodes can modify it. Data inputs: A (boolean), B (boolean). Data outputs: Out '
                         '(boolean).'},
 'ext_get_value': {'example': '1. Add Get Node Value from the Scene category.\n'
                              '2. Connect node.\n'
                              '3. Use value in the next calculation or condition.',
                   'tip': 'Reads the current numeric value from a Progress Bar or Counter node. Data inputs: node '
                          '(object). Data outputs: value (number). Settings: node_id.'},
 'ext_paint_grid': {'example': '1. Add Paint Grid Cell from the Scene category.\n'
                               '2. Connect node, col, row.\n'
                               '3. Use the output in the next calculation or condition.',
                    'tip': 'Paint or clear a single cell of a Grid external node. Color=None clears the cell. Build '
                           'HP bars, state grids, tile maps. Execution input: exec. Execution output: exec. Data '
                           'inputs: node (object), col (number, default=0), row (number, default=0), color (color, '
                           'default=[130, 105, 255]). Settings: node_id, col, row, color. Use the white execution '
                           'path for ordering and the colored pins for values.'},
 'ext_set_color': {'example': '1. Add Set Node Color from the Scene category.\n'
                              '2. Connect node, color.\n'
                              '3. Use the output in the next calculation or condition.',
                   'tip': 'Sets the display color of any external node — text, rect, bar, or counter. Execution '
                          'input: exec. Execution output: exec. Data inputs: node (object), color (color, '
                          'default=[130, 105, 255]). Settings: node_id, color. Use the white execution path for '
                          'ordering and the colored pins for values.'},
 'ext_set_group': {'example': "1. Set Group 'ui_red_team' → then Find By Group to update all at once\n"
                              '2. Group walls together',
                   'tip': 'Assign an external node to a named group. Groups let you address multiple nodes at once '
                          'with Find By Group. Execution input: exec. Execution output: exec. Data inputs: node '
                          "(object), group (string, default='group_1'). Settings: group, node_id. Use the white "
                          'execution path for ordering and the colored pins for values.'},
 'ext_set_layer': {'example': '1. Layer 10 for HUD elements above characters\n2. Layer -1 for background grids',
                   'tip': 'Set the draw order layer of an external node. Higher numbers draw on top of lower ones. '
                          'Execution input: exec. Execution output: exec. Data inputs: node (object), layer (number, '
                          'default=0). Settings: node_id, layer. Use the white execution path for ordering and the '
                          'colored pins for values.'},
 'ext_set_light_props': {'example': '1. Tween -> Set Light Props (Pulse Intensity)\n2. Change color on phase',
                         'tip': 'Modifies an existing Light Source external node. Execution input: exec. Execution '
                                'output: exec. Data inputs: Node (object), Radius (number), Intensity (number). Use '
                                'the white execution path for ordering and the colored pins for values.'},
 'ext_set_meta': {'example': "1. Set Meta 'spawn_time' = Elapsed Time\n2. Set Meta 'owner' = character name",
                  'tip': 'Store any key-value pair on an external node. Metadata survives save/load and is '
                         'accessible from any script. Execution input: exec. Execution output: exec. Data inputs: '
                         "node (object), key (string, default='my_key'), value (any). Settings: node_id, key. Use "
                         'the white execution path for ordering and the colored pins for values.'},
 'ext_set_parent_node': {'example': '1. Parent hp_bar to name_label so they move together\n'
                                    '2. Parent effect to boss node',
                         'tip': "Parent one external node to another. The child inherits the parent's world position "
                                'offset. Execution input: exec. Execution output: exec. Data inputs: child (object), '
                                'parent (object). Use the white execution path for ordering and the colored pins for '
                                'values.'},
 'ext_set_pos': {'example': '1. Add Set Node Position from the Scene category.\n'
                            '2. Connect node, position.\n'
                            '3. Use the output in the next calculation or condition.',
                 'tip': "Move an external node to a world position. Use with Move Toward or a character's position "
                        'to attach nodes to characters. Execution input: exec. Execution output: exec. Data inputs: '
                        'node (object), position (vector). Settings: node_id. Use the white execution path for '
                        'ordering and the colored pins for values.'},
 'ext_set_prop': {'example': '1. Add Set Node Property from the Scene category.\n'
                             '2. Connect node, key, value.\n'
                             '3. Use the output in the next calculation or condition.',
                  'tip': 'Set any named property on an external node — advanced customization beyond the standard '
                         'Set Text/Value/Color nodes. Execution input: exec. Execution output: exec. Data inputs: '
                         "node (object), key (string, default='text'), value (any). Settings: node_id, key. Use the "
                         'white execution path for ordering and the colored pins for values.'},
 'ext_set_scale_node': {'example': '1. On Spawn → Tween 0→1 → Set Scale (pop-in)\n'
                                   '2. On Death → Set Scale 0 (fade out)',
                        'tip': 'Uniformly scale an external node. 1.0 = original size. Execution input: exec. '
                               'Execution output: exec. Data inputs: node (object), scale (number, default=1.0). '
                               'Settings: node_id, scale. Use the white execution path for ordering and the colored '
                               'pins for values.'},
 'ext_set_text': {'example': '1. Add Set Node Text from the Scene category.\n'
                             '2. Connect node, text.\n'
                             '3. Use the output in the next calculation or condition.',
                  'tip': 'Sets the text of an external Text Label or Counter node. Wire a Format String or any '
                         'string value directly in. Execution input: exec. Execution output: exec. Data inputs: node '
                         "(object), text (string, default=''). Settings: node_id. Use the white execution path for "
                         'ordering and the colored pins for values.'},
 'ext_set_text_fmt': {'example': "1. HP / Max HP → percent → '75%'\n2. Elapsed Time → float_1 + suffix 's' → '3.2s'",
                      'tip': 'Set a text_label or counter from a NUMBER with automatic formatting. Supports: int, '
                             "float_1, float_2, percent. Add prefix/suffix for '10 HP', '0:42', etc. Execution "
                             'input: exec. Execution output: exec. Data inputs: node (object), value (number, '
                             "default=0), prefix (string, default=''), suffix (string, default=''). Settings: "
                             'node_id, fmt, prefix, suffix. Use the white execution path for ordering and the '
                             'colored pins for values.'},
 'ext_set_value': {'example': '1. Add Set Node Value from the Scene category.\n'
                              '2. Connect node, value.\n'
                              '3. Use the output in the next calculation or condition.',
                   'tip': 'Sets the numeric value of a Progress Bar or Counter external node. Great for HP bars, '
                          'countdown displays, score counters. Execution input: exec. Execution output: exec. Data '
                          'inputs: node (object), value (number, default=0). Settings: node_id. Use the white '
                          'execution path for ordering and the colored pins for values.'},
 'ext_set_visible': {'example': '1. Add Set Node Visible from the Scene category.\n'
                                '2. Connect node, visible.\n'
                                '3. Use the output in the next calculation or condition.',
                     'tip': 'Show or hide an external node. Hidden nodes are not drawn but still exist. Execution '
                            'input: exec. Execution output: exec. Data inputs: node (object), visible (boolean, '
                            'default=True). Settings: node_id, visible. Use the white execution path for ordering '
                            'and the colored pins for values.'},
 'ext_track_char': {'example': '1. On Spawn → Track Character → HP bar follows boss\n'
                               '2. Track player → name label stays above them',
                    'tip': "Make an external node follow a character's world position every frame. Great for HP "
                           'bars, name labels, status indicators attached to fighters. Execution input: exec. '
                           'Execution output: exec. Data inputs: node (object), character (object). Settings: '
                           'node_id, char_name. Use the white execution path for ordering and the colored pins for '
                           'values.'},
 'flex_aggregate_count': {'example': '1. Add COUNT from the Queries category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Count query results. Data inputs: source (any, default=None). Data output: result '
                                 '(number). Settings: source. This is a pure data/query node; no white execution '
                                 'wire is required.'},
 'flex_aggregate_damage_sum': {'example': '1. Add SUM Damage from the Queries category.\n'
                                          '2. Connect its compatible inputs.\n'
                                          '3. Use its output or execution path in the next operation.',
                               'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                      'default=None), a (any, default=None), b (any, default=None), value (number, '
                                      "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                      'result (number). Settings: source, a, b, value, count, tag. This is a pure '
                                      'data/query node; no white execution wire is required.'},
 'flex_aggregate_hp_average': {'example': '1. Add AVG HP from the Queries category.\n'
                                          '2. Connect its compatible inputs.\n'
                                          '3. Use its output or execution path in the next operation.',
                               'tip': 'Average result HP. Data inputs: source (any, default=None). Data output: '
                                      'result (number). Settings: source. This is a pure data/query node; no white '
                                      'execution wire is required.'},
 'flex_aggregate_hp_sum': {'example': '1. Add SUM HP from the Queries category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Sum result HP. Data inputs: source (any, default=None). Data output: result '
                                  '(number). Settings: source. This is a pure data/query node; no white execution '
                                  'wire is required.'},
 'flex_aggregate_max_hp': {'example': '1. Add MAX HP from the Queries category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                  'default=None), a (any, default=None), b (any, default=None), value (number, '
                                  "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                  'result (number). Settings: source, a, b, value, count, tag. This is a pure '
                                  'data/query node; no white execution wire is required.'},
 'flex_aggregate_min_hp': {'example': '1. Add MIN HP from the Queries category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                  'default=None), a (any, default=None), b (any, default=None), value (number, '
                                  "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                  'result (number). Settings: source, a, b, value, count, tag. This is a pure '
                                  'data/query node; no white execution wire is required.'},
 'flex_aggregate_speed_average': {'example': '1. Add AVG Speed from the Queries category.\n'
                                             '2. Connect its compatible inputs.\n'
                                             '3. Use its output or execution path in the next operation.',
                                  'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source '
                                         '(any, default=None), a (any, default=None), b (any, default=None), value '
                                         "(number, default=0), count (number, default=1), tag (string, default=''). "
                                         'Data output: result (number). Settings: source, a, b, value, count, tag. '
                                         'This is a pure data/query node; no white execution wire is required.'},
 'flex_aggregate_tag_count': {'example': '1. Add COUNT Tags from the Queries category.\n'
                                         '2. Connect its compatible inputs.\n'
                                         '3. Use its output or execution path in the next operation.',
                              'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                     'default=None), a (any, default=None), b (any, default=None), value (number, '
                                     "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                     'result (number). Settings: source, a, b, value, count, tag. This is a pure '
                                     'data/query node; no white execution wire is required.'},
 'flex_alter': {'example': '1. FROM + TO + Tween progress → ALTER.\n'
                           '2. Send result to offset, color, angle, scale, or opacity.',
                'tip': 'Blend FROM to TO with automatic number/vector/color/angle handling and selectable easing.'},
 'flex_apply_tag': {'example': '1. Add ALTER Add Tag from the Collection Effects category.\n'
                               '2. Connect its compatible inputs.\n'
                               '3. Use its output or execution path in the next operation.',
                    'tip': 'Add tag to every selected result. Execution input: exec. Execution output: exec. Data '
                           "inputs: source (any, default=None), tag (string, default=''). Settings: source, tag. Use "
                           'the white execution path for ordering and colored pins for values.'},
 'flex_collection_append': {'example': '1. Add APPEND from the Queries category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                   'default=None), a (any, default=None), b (any, default=None), value (number, '
                                   "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                   'result (any). Settings: source, a, b, value, count, tag. This is a pure '
                                   'data/query node; no white execution wire is required.'},
 'flex_collection_distinct': {'example': '1. Add DISTINCT from the Queries category.\n'
                                         '2. Connect its compatible inputs.\n'
                                         '3. Use its output or execution path in the next operation.',
                              'tip': 'Remove duplicate results. Data inputs: source (any, default=None). Data '
                                     'output: result (any). Settings: source. This is a pure data/query node; no '
                                     'white execution wire is required.'},
 'flex_collection_except': {'example': '1. Add EXCEPT from the Queries category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Remove B items from A. Data inputs: a (any, default=None), b (any, '
                                   'default=None). Data output: result (any). Settings: a, b. This is a pure '
                                   'data/query node; no white execution wire is required.'},
 'flex_collection_intersect': {'example': '1. Add INTERSECT from the Queries category.\n'
                                          '2. Connect its compatible inputs.\n'
                                          '3. Use its output or execution path in the next operation.',
                               'tip': 'Items present in both collections. Data inputs: a (any, default=None), b '
                                      '(any, default=None). Data output: result (any). Settings: a, b. This is a '
                                      'pure data/query node; no white execution wire is required.'},
 'flex_collection_prepend': {'example': '1. Add PREPEND from the Queries category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                    'default=None), a (any, default=None), b (any, default=None), value (number, '
                                    "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                    'result (any). Settings: source, a, b, value, count, tag. This is a pure '
                                    'data/query node; no white execution wire is required.'},
 'flex_collection_reverse': {'example': '1. Add REVERSE from the Queries category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                    'default=None), a (any, default=None), b (any, default=None), value (number, '
                                    "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                    'result (any). Settings: source, a, b, value, count, tag. This is a pure '
                                    'data/query node; no white execution wire is required.'},
 'flex_collection_shuffle': {'example': '1. Add SHUFFLE from the Queries category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                    'default=None), a (any, default=None), b (any, default=None), value (number, '
                                    "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                    'result (any). Settings: source, a, b, value, count, tag. This is a pure '
                                    'data/query node; no white execution wire is required.'},
 'flex_collection_slice': {'example': '1. Add SLICE from the Queries category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                  'default=None), a (any, default=None), b (any, default=None), value (number, '
                                  "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                  'result (any). Settings: source, a, b, value, count, tag. This is a pure '
                                  'data/query node; no white execution wire is required.'},
 'flex_collection_union': {'example': '1. Add UNION from the Queries category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Combine two collections. Data inputs: a (any, default=None), b (any, '
                                  'default=None). Data output: result (any). Settings: a, b. This is a pure '
                                  'data/query node; no white execution wire is required.'},
 'flex_collision_character': {'example': '1. Add Set Character Collision from the Phase & Touch category.\n'
                                         '2. Connect its compatible inputs.\n'
                                         '3. Use its output or execution path in the next operation.',
                              'tip': 'Disable character-vs-character collision while walls still work. Execution '
                                     'input: exec. Execution output: exec. Data inputs: target (object, '
                                     'default=None), enabled (boolean, default=True). Settings: target, enabled. Use '
                                     'the white execution path for ordering and colored pins for values.'},
 'flex_collision_timed': {'example': '1. Add Disable Character Collision Timed from the Phase & Touch category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Timed phase-through while retaining wall collision. Execution input: exec. '
                                 'Execution output: exec. Data inputs: target (object, default=None), duration '
                                 '(number, default=0.3). Settings: target, duration. Use the white execution path '
                                 'for ordering and colored pins for values.'},
 'flex_condition_above': {'example': '1. Add Target Above from the Spatial Conditions category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Directional condition relative to Self. Data inputs: target (object, '
                                 'default=None). Data output: result (bool). Settings: target. This is a pure '
                                 'data/query node; no white execution wire is required.'},
 'flex_condition_all': {'example': '1. Add ALL Match? from the Queries category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                               'default=None), a (any, default=None), b (any, default=None), value (number, '
                               "default=0), count (number, default=1), tag (string, default=''). Data output: result "
                               '(bool). Settings: source, a, b, value, count, tag. This is a pure data/query node; '
                               'no white execution wire is required.'},
 'flex_condition_any': {'example': '1. Add ANY Results? from the Query Conditions category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'True when collection has results. Data inputs: source (any, default=None). Data '
                               'output: result (bool). Settings: source. This is a pure data/query node; no white '
                               'execution wire is required.'},
 'flex_condition_below': {'example': '1. Add Target Below from the Spatial Conditions category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Directional condition relative to Self. Data inputs: target (object, '
                                 'default=None). Data output: result (bool). Settings: target. This is a pure '
                                 'data/query node; no white execution wire is required.'},
 'flex_condition_between': {'example': '1. Add BETWEEN from the Queries category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                   'default=None), a (any, default=None), b (any, default=None), value (number, '
                                   "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                   'result (bool). Settings: source, a, b, value, count, tag. This is a pure '
                                   'data/query node; no white execution wire is required.'},
 'flex_condition_changed': {'example': '1. Add Value Changed? from the Queries category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                   'default=None), a (any, default=None), b (any, default=None), value (number, '
                                   "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                   'result (bool). Settings: source, a, b, value, count, tag. This is a pure '
                                   'data/query node; no white execution wire is required.'},
 'flex_condition_count': {'example': '1. Add HAVING Count from the Query Conditions category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'True at a minimum result count. Data inputs: source (any, default=None), count '
                                 '(number, default=1). Data output: result (bool). Settings: source, count. This is '
                                 'a pure data/query node; no white execution wire is required.'},
 'flex_condition_exists': {'example': '1. Add EXISTS from the Query Conditions category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'True when a target exists. Data inputs: target (object, default=None). Data '
                                  'output: result (bool). Settings: target. This is a pure data/query node; no white '
                                  'execution wire is required.'},
 'flex_condition_in_range': {'example': '1. Add Target In Range from the Spatial Conditions category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Distance condition using arena world units. Data inputs: target (object, '
                                    'default=None), radius (number, default=100). Data output: result (bool). '
                                    'Settings: target, radius. This is a pure data/query node; no white execution '
                                    'wire is required.'},
 'flex_condition_left': {'example': '1. Add Target Left from the Spatial Conditions category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Directional condition relative to Self. Data inputs: target (object, default=None). '
                                'Data output: result (bool). Settings: target. This is a pure data/query node; no '
                                'white execution wire is required.'},
 'flex_condition_none': {'example': '1. Add NO Results? from the Query Conditions category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'True when collection is empty. Data inputs: source (any, default=None). Data '
                                'output: result (bool). Settings: source. This is a pure data/query node; no white '
                                'execution wire is required.'},
 'flex_condition_not': {'example': '1. Add NOT from the Queries category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                               'default=None), a (any, default=None), b (any, default=None), value (number, '
                               "default=0), count (number, default=1), tag (string, default=''). Data output: result "
                               '(bool). Settings: source, a, b, value, count, tag. This is a pure data/query node; '
                               'no white execution wire is required.'},
 'flex_condition_right': {'example': '1. Add Target Right from the Spatial Conditions category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Directional condition relative to Self. Data inputs: target (object, '
                                 'default=None). Data output: result (bool). Settings: target. This is a pure '
                                 'data/query node; no white execution wire is required.'},
 'flex_condition_sector': {'example': '1. Add Target In Sector from the Spatial Conditions category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Radius plus angle-sector condition. Data inputs: target (object, default=None), '
                                  'radius (number, default=100), angle (number, default=0), arc (number, '
                                  'default=90). Data output: result (bool). Settings: target, radius, angle, arc. '
                                  'This is a pure data/query node; no white execution wire is required.'},
 'flex_condition_xor': {'example': '1. Add XOR from the Queries category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                               'default=None), a (any, default=None), b (any, default=None), value (number, '
                               "default=0), count (number, default=1), tag (string, default=''). Data output: result "
                               '(bool). Settings: source, a, b, value, count, tag. This is a pure data/query node; '
                               'no white execution wire is required.'},
 'flex_damage_collection': {'example': '1. Add ALTER Deal Damage from the Collection Effects category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Explicitly damage every query result. Execution input: exec. Execution output: '
                                   'exec. Data inputs: source (any, default=None), damage (number, default=0). '
                                   'Settings: source, damage. Use the white execution path for ordering and colored '
                                   'pins for values.'},
 'flex_effect_animation': {'example': '1. Add ALTER Character Animation from the Collection Effects category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Composable SQL-inspired collection/value operation. Execution input: exec. '
                                  'Execution output: exec. Data inputs: source (any, default=None), value (number, '
                                  "default=0), tag (string, default=''), color (color, default=[255, 80, 80]), "
                                  'opacity (number, default=140), duration (number, default=0.3). Settings: source, '
                                  'value, tag, color, opacity, duration. Use the white execution path for ordering '
                                  'and colored pins for values.'},
 'flex_effect_clear_tags': {'example': '1. Add Clear Tags In Collection from the Collection Effects category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Composable SQL-inspired collection/value operation. Execution input: exec. '
                                   'Execution output: exec. Data inputs: source (any, default=None), value (number, '
                                   "default=0), tag (string, default=''), color (color, default=[255, 80, 80]), "
                                   'opacity (number, default=140), duration (number, default=0.3). Settings: source, '
                                   'value, tag, color, opacity, duration. Use the white execution path for ordering '
                                   'and colored pins for values.'},
 'flex_effect_copy_tags': {'example': '1. Add Copy Tags Across Collection from the Collection Effects category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Composable SQL-inspired collection/value operation. Execution input: exec. '
                                  'Execution output: exec. Data inputs: source (any, default=None), value (number, '
                                  "default=0), tag (string, default=''), color (color, default=[255, 80, 80]), "
                                  'opacity (number, default=140), duration (number, default=0.3). Settings: source, '
                                  'value, tag, color, opacity, duration. Use the white execution path for ordering '
                                  'and colored pins for values.'},
 'flex_effect_flash': {'example': '1. Add Flash Collection from the Collection Effects category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Composable SQL-inspired collection/value operation. Execution input: exec. Execution '
                              'output: exec. Data inputs: source (any, default=None), value (number, default=0), tag '
                              "(string, default=''), color (color, default=[255, 80, 80]), opacity (number, "
                              'default=140), duration (number, default=0.3). Settings: source, value, tag, color, '
                              'opacity, duration. Use the white execution path for ordering and colored pins for '
                              'values.'},
 'flex_effect_opacity': {'example': '1. Add ALTER Character Opacity from the Collection Effects category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Composable SQL-inspired collection/value operation. Execution input: exec. '
                                'Execution output: exec. Data inputs: source (any, default=None), value (number, '
                                "default=0), tag (string, default=''), color (color, default=[255, 80, 80]), opacity "
                                '(number, default=140), duration (number, default=0.3). Settings: source, value, '
                                'tag, color, opacity, duration. Use the white execution path for ordering and '
                                'colored pins for values.'},
 'flex_effect_rotation': {'example': '1. Add ALTER Facing from the Collection Effects category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Composable SQL-inspired collection/value operation. Execution input: exec. '
                                 'Execution output: exec. Data inputs: source (any, default=None), value (number, '
                                 "default=0), tag (string, default=''), color (color, default=[255, 80, 80]), "
                                 'opacity (number, default=140), duration (number, default=0.3). Settings: source, '
                                 'value, tag, color, opacity, duration. Use the white execution path for ordering '
                                 'and colored pins for values.'},
 'flex_effect_scale': {'example': '1. Add ALTER Character Scale from the Collection Effects category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Composable SQL-inspired collection/value operation. Execution input: exec. Execution '
                              'output: exec. Data inputs: source (any, default=None), value (number, default=0), tag '
                              "(string, default=''), color (color, default=[255, 80, 80]), opacity (number, "
                              'default=140), duration (number, default=0.3). Settings: source, value, tag, color, '
                              'opacity, duration. Use the white execution path for ordering and colored pins for '
                              'values.'},
 'flex_effect_speed': {'example': '1. Add ALTER Character Speed from the Collection Effects category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Composable SQL-inspired collection/value operation. Execution input: exec. Execution '
                              'output: exec. Data inputs: source (any, default=None), value (number, default=0), tag '
                              "(string, default=''), color (color, default=[255, 80, 80]), opacity (number, "
                              'default=140), duration (number, default=0.3). Settings: source, value, tag, color, '
                              'opacity, duration. Use the white execution path for ordering and colored pins for '
                              'values.'},
 'flex_effect_sprite': {'example': '1. Add ALTER Character Sprite from the Collection Effects category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Composable SQL-inspired collection/value operation. Execution input: exec. Execution '
                               'output: exec. Data inputs: source (any, default=None), value (number, default=0), '
                               "tag (string, default=''), color (color, default=[255, 80, 80]), opacity (number, "
                               'default=140), duration (number, default=0.3). Settings: source, value, tag, color, '
                               'opacity, duration. Use the white execution path for ordering and colored pins for '
                               'values.'},
 'flex_effect_stop_shake': {'example': '1. Add Stop Shake from the Collection Effects category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Composable SQL-inspired collection/value operation. Execution input: exec. '
                                   'Execution output: exec. Data inputs: source (any, default=None), value (number, '
                                   "default=0), tag (string, default=''), color (color, default=[255, 80, 80]), "
                                   'opacity (number, default=140), duration (number, default=0.3). Settings: source, '
                                   'value, tag, color, opacity, duration. Use the white execution path for ordering '
                                   'and colored pins for values.'},
 'flex_from': {'example': '1. Connect any starting value to FROM.\n2. Send it into ALTER with a TO value.',
               'tip': 'Start from any value: number, color, vector, object, collection, text, angle, opacity, etc.'},
 'flex_order_distance': {'example': '1. Add ORDER BY Distance from the Queries category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Sort nearest to farthest. Data inputs: source (any, default=None), position '
                                '(vector, default=(0, 0)). Data output: result (any). Settings: source, position. '
                                'This is a pure data/query node; no white execution wire is required.'},
 'flex_order_hp_asc': {'example': '1. Add ORDER BY HP Ascending from the Queries category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Sort low to high HP. Data inputs: source (any, default=None). Data output: result '
                              '(any). Settings: source. This is a pure data/query node; no white execution wire is '
                              'required.'},
 'flex_order_hp_desc': {'example': '1. Add ORDER BY HP Descending from the Queries category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Sort high to low HP. Data inputs: source (any, default=None). Data output: result '
                               '(any). Settings: source. This is a pure data/query node; no white execution wire is '
                               'required.'},
 'flex_order_name': {'example': '1. Add ORDER BY Name from the Queries category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': 'Sort names alphabetically. Data inputs: source (any, default=None). Data output: result '
                            '(any). Settings: source. This is a pure data/query node; no white execution wire is '
                            'required.'},
 'flex_order_random': {'example': '1. Add ORDER Random from the Queries category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                              'default=None), a (any, default=None), b (any, default=None), value (number, '
                              "default=0), count (number, default=1), tag (string, default=''). Data output: result "
                              '(any). Settings: source, a, b, value, count, tag. This is a pure data/query node; no '
                              'white execution wire is required.'},
 'flex_order_speed': {'example': '1. Add ORDER BY Speed from the Queries category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                             'default=None), a (any, default=None), b (any, default=None), value (number, '
                             "default=0), count (number, default=1), tag (string, default=''). Data output: result "
                             '(any). Settings: source, a, b, value, count, tag. This is a pure data/query node; no '
                             'white execution wire is required.'},
 'flex_order_tag_count': {'example': '1. Add ORDER BY Tag Count from the Queries category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                 'default=None), a (any, default=None), b (any, default=None), value (number, '
                                 "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                 'result (any). Settings: source, a, b, value, count, tag. This is a pure data/query '
                                 'node; no white execution wire is required.'},
 'flex_order_x': {'example': '1. Add ORDER BY X from the Queries category.\n'
                             '2. Connect its compatible inputs.\n'
                             '3. Use its output or execution path in the next operation.',
                  'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                         'default=None), a (any, default=None), b (any, default=None), value (number, default=0), '
                         "count (number, default=1), tag (string, default=''). Data output: result (any). Settings: "
                         'source, a, b, value, count, tag. This is a pure data/query node; no white execution wire '
                         'is required.'},
 'flex_order_y': {'example': '1. Add ORDER BY Y from the Queries category.\n'
                             '2. Connect its compatible inputs.\n'
                             '3. Use its output or execution path in the next operation.',
                  'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                         'default=None), a (any, default=None), b (any, default=None), value (number, default=0), '
                         "count (number, default=1), tag (string, default=''). Data output: result (any). Settings: "
                         'source, a, b, value, count, tag. This is a pure data/query node; no white execution wire '
                         'is required.'},
 'flex_phase_touch_damage': {'example': '1. Add Phase Touch Damage Per Second from the Phase & Touch category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Deal explicit DPS while passing through characters; zero is harmless. Execution '
                                    'input: exec. Execution output: exec. Data inputs: target (object, '
                                    'default=None), damage (number, default=0), duration (number, default=0.3), tag '
                                    "(string, default=''). Settings: target, damage, duration, tag. Use the white "
                                    'execution path for ordering and colored pins for values.'},
 'flex_remove_tag': {'example': '1. Add ALTER Remove Tag from the Collection Effects category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': 'Remove tag from every selected result. Execution input: exec. Execution output: exec. '
                            "Data inputs: source (any, default=None), tag (string, default=''). Settings: source, "
                            'tag. Use the white execution path for ordering and colored pins for values.'},
 'flex_select_each': {'example': '1. Add SELECT Each from the Queries category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                             'default=None), a (any, default=None), b (any, default=None), value (number, '
                             "default=0), count (number, default=1), tag (string, default=''). Data output: result "
                             '(any). Settings: source, a, b, value, count, tag. This is a pure data/query node; no '
                             'white execution wire is required.'},
 'flex_select_farthest': {'example': '1. Add SELECT Farthest from the Queries category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Return farthest from a position. Data inputs: source (any, default=None), position '
                                 '(vector, default=(0, 0)). Data output: result (target). Settings: source, '
                                 'position. This is a pure data/query node; no white execution wire is required.'},
 'flex_select_first': {'example': '1. Add SELECT First from the Queries category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Return first item. Data inputs: source (any, default=None). Data output: result '
                              '(target). Settings: source. This is a pure data/query node; no white execution wire '
                              'is required.'},
 'flex_select_highest_hp': {'example': '1. Add SELECT Highest HP from the Queries category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                   'default=None), a (any, default=None), b (any, default=None), value (number, '
                                   "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                   'result (any). Settings: source, a, b, value, count, tag. This is a pure '
                                   'data/query node; no white execution wire is required.'},
 'flex_select_last': {'example': '1. Add SELECT Last from the Queries category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Return last item. Data inputs: source (any, default=None). Data output: result '
                             '(target). Settings: source. This is a pure data/query node; no white execution wire is '
                             'required.'},
 'flex_select_limit': {'example': '1. Add LIMIT from the Queries category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Limit number of results. Data inputs: source (any, default=None), count (number, '
                              'default=1). Data output: result (any). Settings: source, count. This is a pure '
                              'data/query node; no white execution wire is required.'},
 'flex_select_lowest_hp': {'example': '1. Add SELECT Lowest HP from the Queries category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                                  'default=None), a (any, default=None), b (any, default=None), value (number, '
                                  "default=0), count (number, default=1), tag (string, default=''). Data output: "
                                  'result (any). Settings: source, a, b, value, count, tag. This is a pure '
                                  'data/query node; no white execution wire is required.'},
 'flex_select_middle': {'example': '1. Add SELECT Middle from the Queries category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                               'default=None), a (any, default=None), b (any, default=None), value (number, '
                               "default=0), count (number, default=1), tag (string, default=''). Data output: result "
                               '(any). Settings: source, a, b, value, count, tag. This is a pure data/query node; no '
                               'white execution wire is required.'},
 'flex_select_nearest': {'example': '1. Add SELECT Nearest from the Queries category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Return nearest to a position. Data inputs: source (any, default=None), position '
                                '(vector, default=(0, 0)). Data output: result (target). Settings: source, position. '
                                'This is a pure data/query node; no white execution wire is required.'},
 'flex_select_offset': {'example': '1. Add OFFSET from the Queries category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Skip a number of results. Data inputs: source (any, default=None), count (number, '
                               'default=1). Data output: result (any). Settings: source, count. This is a pure '
                               'data/query node; no white execution wire is required.'},
 'flex_select_random': {'example': '1. Add SELECT Random from the Queries category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Return random item. Data inputs: source (any, default=None). Data output: result '
                               '(target). Settings: source. This is a pure data/query node; no white execution wire '
                               'is required.'},
 'flex_select_second': {'example': '1. Add SELECT Second from the Queries category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                               'default=None), a (any, default=None), b (any, default=None), value (number, '
                               "default=0), count (number, default=1), tag (string, default=''). Data output: result "
                               '(any). Settings: source, a, b, value, count, tag. This is a pure data/query node; no '
                               'white execution wire is required.'},
 'flex_shake_all': {'example': '1. Add Shake All Characters from the Collection Effects category.\n'
                               '2. Connect its compatible inputs.\n'
                               '3. Use its output or execution path in the next operation.',
                    'tip': 'Apply collection-wide shake. Execution input: exec. Execution output: exec. Data inputs: '
                           'strength (number, default=6), frequency (number, default=24), duration (number, '
                           "default=0.3), axis (string, default='both'). Settings: strength, frequency, duration, "
                           'axis. Use the white execution path for ordering and colored pins for values.'},
 'flex_shake_tag': {'example': '1. Add Shake Characters With Tag from the Collection Effects category.\n'
                               '2. Connect its compatible inputs.\n'
                               '3. Use its output or execution path in the next operation.',
                    'tip': 'Apply shake to all matching tags. Execution input: exec. Execution output: exec. Data '
                           "inputs: tag (string, default=''), strength (number, default=6), frequency (number, "
                           "default=24), duration (number, default=0.3), axis (string, default='both'). Settings: "
                           'tag, strength, frequency, duration, axis. Use the white execution path for ordering and '
                           'colored pins for values.'},
 'flex_shake_target': {'example': '1. Add Shake Target from the Collection Effects category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Shake one target with strength/frequency/axis. Execution input: exec. Execution '
                              'output: exec. Data inputs: target (object, default=None), strength (number, '
                              'default=6), frequency (number, default=24), duration (number, default=0.3), axis '
                              "(string, default='both'). Settings: target, strength, frequency, duration, axis. Use "
                              'the white execution path for ordering and colored pins for values.'},
 'flex_source_all': {'example': '1. Add FROM All Characters from the Queries category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': 'Collection source containing every living character. Data output: result (any). This is '
                            'a pure data/query node; no white execution wire is required.'},
 'flex_source_cone': {'example': '1. Add FROM Direction Cone from the Queries category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Characters in a position/angle/radius cone. Data inputs: position (vector, default=(0, '
                             '0)), radius (number, default=100), angle (number, default=0), arc (number, '
                             'default=90). Data output: result (any). Settings: position, radius, angle, arc. This '
                             'is a pure data/query node; no white execution wire is required.'},
 'flex_source_radius': {'example': '1. Add FROM Radius from the Queries category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Characters within radius of any position. Data inputs: position (vector, default=(0, '
                               '0)), radius (number, default=100). Data output: result (any). Settings: position, '
                               'radius. This is a pure data/query node; no white execution wire is required.'},
 'flex_source_tag': {'example': '1. Add FROM Characters With Tag from the Queries category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': "Collection source by arbitrary tag. Data inputs: tag (string, default=''). Data output: "
                            'result (any). Settings: tag. This is a pure data/query node; no white execution wire is '
                            'required.'},
 'flex_source_team': {'example': '1. Add FROM Team from the Queries category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': "Collection source by team/group name. Data inputs: team (string, default=''). Data "
                             'output: result (any). Settings: team. This is a pure data/query node; no white '
                             'execution wire is required.'},
 'flex_tint_tag': {'example': '1. Add Tint Characters With Tag from the Collection Effects category.\n'
                              '2. Connect its compatible inputs.\n'
                              '3. Use its output or execution path in the next operation.',
                   'tip': 'Tint every matching character. Execution input: exec. Execution output: exec. Data '
                          "inputs: tag (string, default=''), color (color, default=[255, 80, 80]), opacity (number, "
                          'default=140), duration (number, default=0.3), flash (boolean, default=False). Settings: '
                          'tag, color, opacity, duration, flash. Use the white execution path for ordering and '
                          'colored pins for values.'},
 'flex_tint_target': {'example': '1. Add Tint Target Collection from the Collection Effects category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Tint one target or supplied collection. Execution input: exec. Execution output: exec. '
                             'Data inputs: source (any, default=None), color (color, default=[255, 80, 80]), opacity '
                             '(number, default=140), duration (number, default=0.3), flash (boolean, default=False). '
                             'Settings: source, color, opacity, duration, flash. Use the white execution path for '
                             'ordering and colored pins for values.'},
 'flex_to': {'example': '1. Connect the destination value to TO.\n2. Feed FROM and TO into ALTER.',
             'tip': 'Declare any destination value for a reusable transition pipeline.'},
 'flex_transform_angle': {'example': '1. Add ALTER Angle from the Universal category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Universal FROM/TO interpolation specialization. Data inputs: a (any, '
                                 'default=None), b (any, default=None), value (number, default=0), easing (string, '
                                 "default='smoothstep'). Data output: result (any). Settings: a, b, value, easing. "
                                 'This is a pure data/query node; no white execution wire is required.'},
 'flex_transform_color': {'example': '1. Add ALTER Color from the Universal category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Universal FROM/TO interpolation specialization. Data inputs: a (any, '
                                 'default=None), b (any, default=None), value (number, default=0), easing (string, '
                                 "default='smoothstep'). Data output: result (any). Settings: a, b, value, easing. "
                                 'This is a pure data/query node; no white execution wire is required.'},
 'flex_transform_number': {'example': '1. Add ALTER Number from the Universal category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Universal FROM/TO interpolation specialization. Data inputs: a (any, '
                                  'default=None), b (any, default=None), value (number, default=0), easing (string, '
                                  "default='smoothstep'). Data output: result (any). Settings: a, b, value, easing. "
                                  'This is a pure data/query node; no white execution wire is required.'},
 'flex_transform_opacity': {'example': '1. Add ALTER Opacity from the Universal category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Universal FROM/TO interpolation specialization. Data inputs: a (any, '
                                   'default=None), b (any, default=None), value (number, default=0), easing (string, '
                                   "default='smoothstep'). Data output: result (any). Settings: a, b, value, easing. "
                                   'This is a pure data/query node; no white execution wire is required.'},
 'flex_transform_vector': {'example': '1. Add ALTER Vector from the Universal category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Universal FROM/TO interpolation specialization. Data inputs: a (any, '
                                  'default=None), b (any, default=None), value (number, default=0), easing (string, '
                                  "default='smoothstep'). Data output: result (any). Settings: a, b, value, easing. "
                                  'This is a pure data/query node; no white execution wire is required.'},
 'flex_weapon_if_above': {'example': '1. Add Thrust If Target Above from the Weapon Decisions category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Trigger configurable weapon motion only when the spatial condition matches. '
                                 'Execution input: exec. Execution output: exec. Data inputs: name (string, '
                                 "default='main'), target (object, default=None), radius (number, default=100), "
                                 "motion (string, default='rig_weapon_swing'), distance (number, default=35), angle "
                                 '(number, default=0), duration (number, default=0.3), afterimage (boolean, '
                                 'default=True). Settings: name, target, radius, motion, distance, angle, duration, '
                                 'afterimage. Use the white execution path for ordering and colored pins for '
                                 'values.'},
 'flex_weapon_if_below': {'example': '1. Add Stab If Target Below from the Weapon Decisions category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Trigger configurable weapon motion only when the spatial condition matches. '
                                 'Execution input: exec. Execution output: exec. Data inputs: name (string, '
                                 "default='main'), target (object, default=None), radius (number, default=100), "
                                 "motion (string, default='rig_weapon_swing'), distance (number, default=35), angle "
                                 '(number, default=0), duration (number, default=0.3), afterimage (boolean, '
                                 'default=True). Settings: name, target, radius, motion, distance, angle, duration, '
                                 'afterimage. Use the white execution path for ordering and colored pins for '
                                 'values.'},
 'flex_weapon_if_left': {'example': '1. Add Swing If Target Left from the Weapon Decisions category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Trigger configurable weapon motion only when the spatial condition matches. '
                                'Execution input: exec. Execution output: exec. Data inputs: name (string, '
                                "default='main'), target (object, default=None), radius (number, default=100), "
                                "motion (string, default='rig_weapon_swing'), distance (number, default=35), angle "
                                '(number, default=0), duration (number, default=0.3), afterimage (boolean, '
                                'default=True). Settings: name, target, radius, motion, distance, angle, duration, '
                                'afterimage. Use the white execution path for ordering and colored pins for values.'},
 'flex_weapon_if_range': {'example': '1. Add Swing If In Range from the Weapon Decisions category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Trigger configurable weapon motion only when the spatial condition matches. '
                                 'Execution input: exec. Execution output: exec. Data inputs: name (string, '
                                 "default='main'), target (object, default=None), radius (number, default=100), "
                                 "motion (string, default='rig_weapon_swing'), distance (number, default=35), angle "
                                 '(number, default=0), duration (number, default=0.3), afterimage (boolean, '
                                 'default=True). Settings: name, target, radius, motion, distance, angle, duration, '
                                 'afterimage. Use the white execution path for ordering and colored pins for '
                                 'values.'},
 'flex_weapon_if_right': {'example': '1. Add Swing If Target Right from the Weapon Decisions category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Trigger configurable weapon motion only when the spatial condition matches. '
                                 'Execution input: exec. Execution output: exec. Data inputs: name (string, '
                                 "default='main'), target (object, default=None), radius (number, default=100), "
                                 "motion (string, default='rig_weapon_swing'), distance (number, default=35), angle "
                                 '(number, default=0), duration (number, default=0.3), afterimage (boolean, '
                                 'default=True). Settings: name, target, radius, motion, distance, angle, duration, '
                                 'afterimage. Use the white execution path for ordering and colored pins for '
                                 'values.'},
 'flex_where': {'example': '1. FROM collection → WHERE.\n'
                           '2. Connect a Boolean condition and continue with SELECT/ORDER/LIMIT.',
                'tip': 'Filter a collection with a Boolean condition; compatible with any FROM collection.'},
 'flex_where_above': {'example': '1. Add WHERE Above Position from the Queries category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Keep targets above a position. Data inputs: source (any, default=None), position '
                             '(vector, default=(0, 0)). Data output: result (any). Settings: source, position. This '
                             'is a pure data/query node; no white execution wire is required.'},
 'flex_where_alive': {'example': '1. Add WHERE Alive from the Queries category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Keep living targets. Data inputs: source (any, default=None). Data output: result '
                             '(any). Settings: source. This is a pure data/query node; no white execution wire is '
                             'required.'},
 'flex_where_ally': {'example': '1. Add WHERE Ally from the Queries category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                            'default=None), a (any, default=None), b (any, default=None), value (number, default=0), '
                            "count (number, default=1), tag (string, default=''). Data output: result (any). "
                            'Settings: source, a, b, value, count, tag. This is a pure data/query node; no white '
                            'execution wire is required.'},
 'flex_where_below': {'example': '1. Add WHERE Below Position from the Queries category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Keep targets below a position. Data inputs: source (any, default=None), position '
                             '(vector, default=(0, 0)). Data output: result (any). Settings: source, position. This '
                             'is a pure data/query node; no white execution wire is required.'},
 'flex_where_distance': {'example': '1. Add WHERE Within Distance from the Queries category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Filter relative to any position. Data inputs: source (any, default=None), position '
                                '(vector, default=(0, 0)), radius (number, default=100). Data output: result (any). '
                                'Settings: source, position, radius. This is a pure data/query node; no white '
                                'execution wire is required.'},
 'flex_where_enemy': {'example': '1. Add WHERE Enemy from the Queries category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                             'default=None), a (any, default=None), b (any, default=None), value (number, '
                             "default=0), count (number, default=1), tag (string, default=''). Data output: result "
                             '(any). Settings: source, a, b, value, count, tag. This is a pure data/query node; no '
                             'white execution wire is required.'},
 'flex_where_hp_above': {'example': '1. Add WHERE HP Above Percent from the Queries category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Filter by current HP percentage. Data inputs: source (any, default=None), value '
                                '(number, default=0). Data output: result (any). Settings: source, value. This is a '
                                'pure data/query node; no white execution wire is required.'},
 'flex_where_hp_below': {'example': '1. Add WHERE HP Below Percent from the Queries category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Filter by current HP percentage. Data inputs: source (any, default=None), value '
                                '(number, default=0). Data output: result (any). Settings: source, value. This is a '
                                'pure data/query node; no white execution wire is required.'},
 'flex_where_left': {'example': '1. Add WHERE Left Of Position from the Queries category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': 'Keep targets left of a position. Data inputs: source (any, default=None), position '
                            '(vector, default=(0, 0)). Data output: result (any). Settings: source, position. This '
                            'is a pure data/query node; no white execution wire is required.'},
 'flex_where_name': {'example': '1. Add WHERE Name Contains from the Queries category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                            'default=None), a (any, default=None), b (any, default=None), value (number, default=0), '
                            "count (number, default=1), tag (string, default=''). Data output: result (any). "
                            'Settings: source, a, b, value, count, tag. This is a pure data/query node; no white '
                            'execution wire is required.'},
 'flex_where_not_self': {'example': '1. Add WHERE Not Self from the Queries category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Remove the graph owner. Data inputs: source (any, default=None). Data output: '
                                'result (any). Settings: source. This is a pure data/query node; no white execution '
                                'wire is required.'},
 'flex_where_not_tag': {'example': '1. Add WHERE Not Tag from the Queries category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Exclude a tag from a collection. Data inputs: source (any, default=None), tag '
                               "(string, default=''). Data output: result (any). Settings: source, tag. This is a "
                               'pure data/query node; no white execution wire is required.'},
 'flex_where_right': {'example': '1. Add WHERE Right Of Position from the Queries category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Keep targets right of a position. Data inputs: source (any, default=None), position '
                             '(vector, default=(0, 0)). Data output: result (any). Settings: source, position. This '
                             'is a pure data/query node; no white execution wire is required.'},
 'flex_where_tag': {'example': '1. Add WHERE Has Tag from the Queries category.\n'
                               '2. Connect its compatible inputs.\n'
                               '3. Use its output or execution path in the next operation.',
                    'tip': 'Filter a collection by tag. Data inputs: source (any, default=None), tag (string, '
                           "default=''). Data output: result (any). Settings: source, tag. This is a pure data/query "
                           'node; no white execution wire is required.'},
 'flex_where_tag_all': {'example': '1. Add WHERE All Tags from the Queries category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                               'default=None), a (any, default=None), b (any, default=None), value (number, '
                               "default=0), count (number, default=1), tag (string, default=''). Data output: result "
                               '(any). Settings: source, a, b, value, count, tag. This is a pure data/query node; no '
                               'white execution wire is required.'},
 'flex_where_tag_any': {'example': '1. Add WHERE Any Tag from the Queries category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Composable SQL-inspired collection/value operation. Data inputs: source (any, '
                               'default=None), a (any, default=None), b (any, default=None), value (number, '
                               "default=0), count (number, default=1), tag (string, default=''). Data output: result "
                               '(any). Settings: source, a, b, value, count, tag. This is a pure data/query node; no '
                               'white execution wire is required.'},
 'flex_where_team': {'example': '1. Add WHERE Team from the Queries category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': 'Filter collection by team. Data inputs: source (any, default=None), team (string, '
                            "default=''). Data output: result (any). Settings: source, team. This is a pure "
                            'data/query node; no white execution wire is required.'},
 'flow_defer': {'example': '1. Defer spawn after death to avoid removing from loop mid-tick\n'
                           '2. Defer state change to next frame',
                'tip': 'Queues execution to run at the START of the next on_tick call instead of right now. Prevents '
                       'mid-frame side effects. Like Godot call_deferred(). Execution input: exec. Execution output: '
                       'next_tick. Use the white execution path for ordering and the colored pins for values.'},
 'flow_disabled': {'example': '1. On Spawn -> [old logic] -> Disabled Block (keep but skip)\n'
                              '2. Bypass a DoT while testing',
                   'tip': "Any nodes wired INTO this node's exec input are skipped — execution stops here and the "
                          "output pin is never triggered. Wire it between two nodes you want to 'comment out' "
                          'without deleting the connections. Toggle by re-routing around it. Execution input: exec. '
                          'Execution output: bypassed. Use the white execution path for ordering and the colored '
                          'pins for values.'},
 'flow_gate': {'example': '1. Only allow attacks after a gate is opened by On Spawn\n'
                          '2. Close gate during invulnerability windows',
               'tip': "Execution only passes through when the gate is open. Wire a second exec into 'open' or "
                      "'close' to control it. Like a valve on a pipe. Execution input: exec, open, close, toggle. "
                      'Execution output: exec. Settings: start_open. Use the white execution path for ordering and '
                      'the colored pins for values.'},
 'flow_pass': {'example': '1. On Hit -> Pass -> (fill in later)\n2. Keep a chain wired up but do nothing yet',
               'tip': 'Does nothing and lets execution flow through unchanged. Use it as a placeholder to keep a '
                      "chain of nodes wired up while you work on the logic — like a Python 'pass' statement. "
                      'Execution input: exec. Execution output: exec. Use the white execution path for ordering and '
                      'the colored pins for values.'},
 'flow_return': {'example': '1. If HP > 50% -> Return (ignore weak attacks)\n2. If not valid target -> Return',
                 'tip': "Immediately stops execution of this hook (like Python 'return'). Anything wired after this "
                        "node is ignored. Great for early-exit conditions: 'If not valid -> Return'. Execution "
                        'input: exec. Use the white execution path for ordering and the colored pins for values.'},
 'flow_state_machine': {'example': '1. idle/patrol/attack/flee AI\n2. Boss phase 1/2/3 behaviour switching',
                        'tip': "A named-state controller. Set the 'state' input to switch between up to 4 states. "
                               'Each state fires its own exec output every tick. Like AnimationStateMachine or a '
                               'manual GDScript state machine. Execution input: exec. Execution output: state_a, '
                               'state_b, state_c, state_d. Data inputs: target (object), set_state (string, '
                               "default=''). Data outputs: current_state (string). Settings: state_a, state_b, "
                               'state_c, state_d, var_name. Use the white execution path for ordering and the '
                               'colored pins for values.'},
 'flow_switch_number': {'example': '1. Phase variable 0/1/2 -> Switch -> Phase0/Phase1/Phase2 behaviour\n'
                                   '2. Combo counter mod 3 -> Switch -> attack style',
                        'tip': 'Jumps to one of up to 5 output exec pins based on an integer value (0→Case0, 1→Case1 '
                               '… default if no match). Execution input: exec. Execution output: case_0, case_1, '
                               'case_2, case_3, case_4, default. Data inputs: value (number, default=0). Settings: '
                               'cases. Use the white execution path for ordering and the colored pins for values.'},
 'flow_switch_tag': {'example': '1. Has "elite" -> big damage, has "boss" -> camera shake\n'
                                '2. Route AI behaviour by faction tag',
                     'tip': "Checks a character's tags and fires the matching exec output. Like a string-based "
                            'switch statement. Execution input: exec. Execution output: tag_a, tag_b, tag_c, none. '
                            'Data inputs: target (object). Settings: tag_a, tag_b, tag_c. Use the white execution '
                            'path for ordering and the colored pins for values.'},
 'gameplay_add_shield': {'example': '1. Add Shield (50) on Spawn\n2. On Cast -> Add Shield (100)',
                         'tip': 'Adds temporary hit points that absorb damage before actual HP is reduced. Execution '
                                'input: exec. Execution output: exec. Data inputs: target (object), amount (number, '
                                'default=20). Settings: amount. Use the white execution path for ordering and the '
                                'colored pins for values.'},
 'gameplay_apply_status': {'example': '1. Apply "Stun" for 2.0s\n2. Apply "Silence" for 5.0s',
                           'tip': 'Applies an engine status effect (Stun, Root, Silence, Slow, Poison, Burn, Freeze) '
                                  'for a duration. Execution input: exec. Execution output: exec. Data inputs: '
                                  "target (object), status (string, default='poison'), duration (number, "
                                  'default=3.0). Settings: status, duration. Use the white execution path for '
                                  'ordering and the colored pins for values.'},
 'gameplay_armor_pierce': {'example': '1. Sniper bullet: 100% Armor Pierce ensures true damage\n'
                                      '2. Heavy swing -> 50% Armor Pierce',
                           'tip': "Deals damage that bypasses a percentage of the target's defense stat. Execution "
                                  'input: exec. Execution output: exec. Data inputs: target (object), damage '
                                  '(number, default=10), pierce_percent (number, default=50). Settings: damage, '
                                  'pierce_percent. Use the white execution path for ordering and the colored pins '
                                  'for values.'},
 'gameplay_camera_shake': {'example': '1. Camera Shake (Intensity 10, Duration 0.5s) on explosion\n'
                                      '2. On Boss Landing -> Camera Shake',
                           'tip': 'Shakes the arena camera for a given intensity and duration. Execution input: '
                                  'exec. Execution output: exec. Data inputs: intensity (number, default=5), '
                                  'duration (number, default=0.5). Settings: intensity, duration. Use the white '
                                  'execution path for ordering and the colored pins for values.'},
 'gameplay_cleanse': {'example': '1. On taking damage -> 20% chance cleanse\n'
                                 '2. Paladin ability: cleanse ally on heal',
                      'tip': 'Removes ALL debuff statuses from the target at once (stun, root, silence, slow, '
                             'poison, burn, freeze). Execution input: exec. Execution output: exec. Data inputs: '
                             'target (object). Use the white execution path for ordering and the colored pins for '
                             'values.'},
 'gameplay_collision_toggle': {'example': '1. Disable Collisions (2s) -> Ghost walk\n'
                                          '2. On Dash -> Disable Collisions',
                               'tip': 'Temporarily disables physics collision for a character -- ghost mode for '
                                      'dashes. Execution input: exec. Execution output: exec. Data inputs: target '
                                      '(object). Settings: duration. Use the white execution path for ordering and '
                                      'the colored pins for values.'},
 'gameplay_critical_hit_roll': {'example': '1. Crit Roll (20% chance, 2x mult) -> Deal Damage\n'
                                           '2. If Is Crit -> Play "crit.wav"',
                                'tip': 'Rolls for a critical hit based on chance and multiplier, returning a Boolean '
                                       'and the final damage. Data inputs: chance (number, default=0.2), multiplier '
                                       '(number, default=2.0), base_damage (number, default=10). Data outputs: '
                                       'is_crit (boolean), final_damage (number). Settings: chance, multiplier, '
                                       'base_damage.'},
 'gameplay_damage_multiplier_vs_tag': {'example': '1. Tag "undead" -> Multiplier 2.0\n'
                                                  '2. Tag "flying" -> Multiplier 1.5',
                                       'tip': 'Multiplies damage dealt against targets that carry a specific tag. '
                                              'Data inputs: target (object), tag (string), multiplier (number, '
                                              'default=1.5), base_damage (number, default=10). Data outputs: '
                                              'final_damage (number). Settings: tag, multiplier, base_damage.'},
 'gameplay_damage_over_time': {'example': '1. Apply DOT: 5 damage, 1s interval, 5s duration = 25 total damage\n'
                                          '2. Poison arrow -> Apply DOT',
                               'tip': 'Attaches a ticking damage effect to a target -- poison, burn, bleed. Engine '
                                      'handles ticks automatically. Execution input: exec. Execution output: exec. '
                                      'Data inputs: target (object), damage (number, default=5), interval (number, '
                                      'default=1.0), duration (number, default=5.0). Settings: damage, interval, '
                                      'duration. Use the white execution path for ordering and the colored pins for '
                                      'values.'},
 'gameplay_deal_damage': {'example': '1. Deal 15 damage to Event Other on hit\n2. Area Damage -> Deal Damage to List',
                          'tip': 'Deals damage to a target respecting shields, defense, and invulnerability frames. '
                                 'Execution input: exec. Execution output: exec. Data inputs: target (object), '
                                 'amount (number, default=10). Settings: amount. Use the white execution path for '
                                 'ordering and the colored pins for values.'},
 'gameplay_deal_damage_over_path': {'example': '1. Deal damage from Self to Target over 50 width\n'
                                               '2. Laser beam -> Deal Damage Over Path',
                                    'tip': 'Deals damage along a straight line from start to end -- laser beams, '
                                           'sword slashes. Execution input: exec. Execution output: exec. Data '
                                           'inputs: start (vector), end (vector), width (number, default=20), damage '
                                           '(number, default=10). Settings: damage, width. Use the white execution '
                                           'path for ordering and the colored pins for values.'},
 'gameplay_decrease_speed': {'example': '1. Decrease Speed by 20\n2. On Leg Hit -> Decrease Speed',
                             'tip': "Permanently subtracts from the character's movement speed stat. Execution "
                                    'input: exec. Execution output: exec. Data inputs: target (object), multiplier '
                                    '(number, default=0.7). Settings: multiplier. Use the white execution path for '
                                    'ordering and the colored pins for values.'},
 'gameplay_destroy_object': {'example': '1. Destroy Self on collision\n2. On Timer End -> Destroy Self',
                             'tip': 'Instantly removes a character from the scene without triggering death hooks. '
                                    'Execution input: exec. Execution output: exec. Data inputs: target (object). '
                                    'Use the white execution path for ordering and the colored pins for values.'},
 'gameplay_execute': {'example': '1. Executioner trait: 20% Threshold = massive damage to dying foes\n'
                                 '2. Execute Target if HP < 10%',
                      'tip': "Deals double damage if the target's HP is below a threshold percentage. Execution "
                             'input: exec. Execution output: exec. Data inputs: target (object), damage (number, '
                             'default=10), threshold_percent (number, default=20). Settings: damage, '
                             'threshold_percent. Use the white execution path for ordering and the colored pins for '
                             'values.'},
 'gameplay_flash_tint': {'example': '1. Flash White when hit\n2. Flash Red when low HP',
                         'tip': "Applies a blinking color overlay to a character's sprite. Execution input: exec. "
                                'Execution output: exec. Data inputs: target (object), color (color, default=[255, '
                                '90, 90]), duration (number, default=1.0), interval (number, default=0.15). '
                                'Settings: color, duration, interval. Use the white execution path for ordering and '
                                'the colored pins for values.'},
 'gameplay_get_name': {'example': '1. Get Name -> Compare == "Skeleton"\n2. Get Name -> Print To Screen',
                       'tip': "Returns the character's current name string. Data inputs: target (object). Data "
                              'outputs: name (string).'},
 'gameplay_get_tags': {'example': '1. Get Tags -> Print To Screen\n2. Get Tags -> Contains "fire"',
                       'tip': 'Returns all tags currently applied to a character as a list. Data inputs: target '
                              '(object). Data outputs: tags (object).'},
 'gameplay_get_team': {'example': '1. Get Team -> Compare == "red_team"\n2. Get Team -> Print To Screen',
                       'tip': "Returns the character's current team string. Data inputs: target (object). Data "
                              'outputs: team (string).'},
 'gameplay_has_tag': {'example': '1. Has Tag "boss" -> Branch\n2. Has Tag "undead" -> Double Damage',
                      'tip': 'Returns True if the character currently has the specified tag. Data inputs: target '
                             "(object), tag (string, default=''). Data outputs: result (boolean). Settings: tag."},
 'gameplay_heal': {'example': '1. Heal Self for 20\n2. On Item Pickup -> Heal Self',
                   'tip': "Restores HP up to the character's Max HP cap. Execution input: exec. Execution output: "
                          'exec. Data inputs: target (object), amount (number, default=10). Data outputs: healed '
                          '(number). Settings: amount. Use the white execution path for ordering and the colored '
                          'pins for values.'},
 'gameplay_hp_drain': {'example': '1. Vampire bite: drain 30 HP from nearest enemy\n2. Leech on every hit',
                       'tip': 'Deals damage to target AND heals source by the same amount (lifesteal without a '
                              'percentage — full 1:1 drain). Execution input: exec. Execution output: exec. Data '
                              'inputs: source (object), target (object), amount (number, default=20). Data outputs: '
                              'drained (number). Settings: amount. Use the white execution path for ordering and the '
                              'colored pins for values.'},
 'gameplay_increase_attack': {'example': '1. Increase Attack by 5\n2. On Rage -> Increase Attack by 50',
                              'tip': "Permanently adds to the character's base damage output. Execution input: exec. "
                                     'Execution output: exec. Data inputs: target (object), amount (number, '
                                     'default=5). Settings: amount. Use the white execution path for ordering and '
                                     'the colored pins for values.'},
 'gameplay_increase_crit_chance': {'example': '1. Increase Crit Chance by 10%\n2. On Focus -> Increase Crit Chance',
                                   'tip': "Adds a flat percentage to the character's critical strike chance. "
                                          'Execution input: exec. Execution output: exec. Data inputs: target '
                                          '(object), amount (number, default=0.05). Settings: amount. Use the white '
                                          'execution path for ordering and the colored pins for values.'},
 'gameplay_increase_crit_damage': {'example': '1. Increase Crit Damage by 0.5\n'
                                              '2. Assassin Trait -> Increase Crit Damage',
                                   'tip': "Adds to the character's critical strike damage multiplier. Execution "
                                          'input: exec. Execution output: exec. Data inputs: target (object), amount '
                                          '(number, default=0.2). Settings: amount. Use the white execution path for '
                                          'ordering and the colored pins for values.'},
 'gameplay_increase_defense': {'example': '1. Increase Defense by 2\n2. Equip Armor -> Increase Defense',
                               'tip': "Permanently adds to the character's defense (flat damage reduction). "
                                      'Execution input: exec. Execution output: exec. Data inputs: target (object), '
                                      'amount (number, default=5). Settings: amount. Use the white execution path '
                                      'for ordering and the colored pins for values.'},
 'gameplay_increase_speed': {'example': '1. Increase Speed by 50\n2. On Level Up -> Increase Speed',
                             'tip': "Permanently adds to the character's movement speed stat. Execution input: exec. "
                                    'Execution output: exec. Data inputs: target (object), multiplier (number, '
                                    'default=1.3). Settings: multiplier. Use the white execution path for ordering '
                                    'and the colored pins for values.'},
 'gameplay_knockback': {'example': '1. Knockback Target with Force 500\n2. Area Push/Pull -> Knockback List',
                        'tip': 'Applies a physics impulse in a direction to shove a character. Execution input: '
                               'exec. Execution output: exec. Data inputs: target (object), direction (vector), '
                               'force (number, default=300). Settings: force. Use the white execution path for '
                               'ordering and the colored pins for values.'},
 'gameplay_lifesteal': {'example': '1. Vampire trait: Lifesteal node on "On Attack"\n'
                                   '2. Lifesteal (50% of 100 damage) -> Heals 50',
                        'tip': 'Deals damage to a target and heals the attacker for a percentage of the damage '
                               'dealt. Execution input: exec. Execution output: exec. Data inputs: target (object), '
                               'damage (number, default=10), lifesteal_percent (number, default=50). Settings: '
                               'damage, lifesteal_percent. Use the white execution path for ordering and the colored '
                               'pins for values.'},
 'gameplay_parry_window': {'example': '1. "On Input" -> Parry Window (1.0s)\n'
                                      '2. AI: Distance < 50 -> Random Chance 30% -> Parry Window',
                           'tip': 'Grants brief invulnerability and stuns any attacker who hits during the window. '
                                  'Execution input: exec. Execution output: exec. Data inputs: target (object), '
                                  'duration (number, default=1.0). Settings: duration. Use the white execution path '
                                  'for ordering and the colored pins for values.'},
 'gameplay_phase_change': {'example': '1. Add Set Phase from the Gameplay category.\n'
                                      '2. Connect target, phase.\n'
                                      '3. Use phase in the next calculation or condition.',
                           'tip': 'Sets a numeric phase variable on a character and fires the on_phase_change event '
                                  'hook. Use to create classic boss phase transitions: Phase 1 → Phase 2 → Phase 3. '
                                  'Wire On Phase Change event to react to it. Execution input: exec. Execution '
                                  'output: exec. Data inputs: target (object), phase (number, default=2). Data '
                                  'outputs: phase (number). Settings: phase. Use the white execution path for '
                                  'ordering and the colored pins for values.'},
 'gameplay_reflect_damage': {'example': '1. Spike Armor: "On Damage Taken" -> Reflect Damage (50%)\n'
                                        '2. Reflect 100% while Shielded',
                             'tip': 'Returns a percentage of incoming damage back to whoever attacked this '
                                    'character. Execution input: exec. Execution output: exec. Data inputs: target '
                                    '(object), damage (number, default=10), reflect_percent (number, default=50). '
                                    'Settings: damage, reflect_percent. Use the white execution path for ordering '
                                    'and the colored pins for values.'},
 'gameplay_remove_shield': {'example': '1. On EMP Hit -> Remove Shield\n2. On Shield Break Anim -> Remove Shield',
                            'tip': 'Instantly strips all shield hit points from a character. Execution input: exec. '
                                   'Execution output: exec. Data inputs: target (object). Use the white execution '
                                   'path for ordering and the colored pins for values.'},
 'gameplay_remove_status': {'example': '1. Remove "Stun"\n2. Cleanse Potion -> Remove "Poison"',
                            'tip': 'Instantly clears a specific status effect from a character. Execution input: '
                                   'exec. Execution output: exec. Data inputs: target (object), status (string, '
                                   "default='poison'). Settings: status. Use the white execution path for ordering "
                                   'and the colored pins for values.'},
 'gameplay_remove_tag': {'example': '1. Remove Tag "shielded"\n2. Remove Tag "stealth" on attack',
                         'tip': 'Removes a specific tag string from a character. Execution input: exec. Execution '
                                "output: exec. Data inputs: target (object), tag (string, default=''). Settings: "
                                'tag. Use the white execution path for ordering and the colored pins for values.'},
 'gameplay_screen_effects': {'example': '1. Screen Flash (Red, 0.2s) on hit\n2. Screen Tint (Black, 1.0s) on death',
                             'tip': 'Applies full-screen visual overlays like flashes, tints, and shakes. Execution '
                                    'input: exec. Execution output: exec. Data inputs: color (color, default=(255, '
                                    '255, 255)), duration (number, default=0.3). Settings: effect, duration. Use the '
                                    'white execution path for ordering and the colored pins for values.'},
 'gameplay_set_hp': {'example': '1. Boss enters phase 2 -> Set HP = max_hp\n2. Tutorial: set dummy to exactly 1 HP',
                     'tip': "Directly sets a character's current HP to an exact value. Clamped to [0, max_hp]. Use "
                            'for scripted moments like boss intros. Execution input: exec. Execution output: exec. '
                            'Data inputs: target (object), amount (number, default=100). Settings: amount. Use the '
                            'white execution path for ordering and the colored pins for values.'},
 'gameplay_set_invulnerable': {'example': '1. Use alongside a visual "shield" animation\n'
                                          '2. Invulnerable (3s) on spawn',
                               'tip': 'Makes a character completely immune to all incoming HP damage for a set '
                                      'duration. Execution input: exec. Execution output: exec. Data inputs: target '
                                      '(object), duration (number, default=3.0). Settings: duration. Use the white '
                                      'execution path for ordering and the colored pins for values.'},
 'gameplay_set_name': {'example': '1. Set Name "Enraged Boss"\n2. Set Name "Minion 1"',
                       'tip': "Changes the character's displayed name in the arena. Execution input: exec. Execution "
                              "output: exec. Data inputs: target (object), name (string, default=''). Settings: "
                              'name. Use the white execution path for ordering and the colored pins for values.'},
 'gameplay_set_tag': {'example': '1. Set Tag "boss"\n2. Set Tag "poisoned" for 5s',
                      'tip': "Add a free-form tag (e.g. 'boss', 'neutral') to a character, independent of team. "
                             'Duration > 0 makes it auto-expire. Execution input: exec. Execution output: exec. Data '
                             "inputs: target (object), tag (string, default=''), duration (number, default=0). "
                             'Settings: tag, duration. Use the white execution path for ordering and the colored '
                             'pins for values.'},
 'gameplay_set_team': {'example': '1. Set Team to "red_team"\n2. Set Team to "neutral"',
                       'tip': "Assign this character's team so 'enemy'/'ally' filters work correctly. Call on_spawn. "
                              'Execution input: exec. Execution output: exec. Data inputs: target (object), team '
                              "(string, default='enemy'). Settings: team. Use the white execution path for ordering "
                              'and the colored pins for values.'},
 'gameplay_spawn_library_character': {'example': '1. Spawn "Skeleton" at Random Point In Radius\n'
                                                 '2. On Death -> Spawn "Ghost"',
                                      'tip': 'Choose any saved character and spawn it at an exact wired world '
                                             'position. Execution input: exec. Execution output: exec. Data inputs: '
                                             "position (vector), character (string, default=''). Data outputs: "
                                             'spawned (object). Settings: character. Use the white execution path '
                                             'for ordering and the colored pins for values.'},
 'gameplay_spawn_object': {'example': '1. Spawn Object at Position\n2. Spawn Object -> Set Sprite',
                           'tip': 'Spawns a generic character into the scene at a position. Execution input: exec. '
                                  'Execution output: exec. Data inputs: position (vector). Data outputs: spawned '
                                  '(object). Settings: template_name. Use the white execution path for ordering and '
                                  'the colored pins for values.'},
 'gameplay_teleport': {'example': '1. Teleport to Target Position\n2. Teleport to Random Point In Radius',
                       'tip': 'Instantly moves a character to a new world position. Execution input: exec. Execution '
                              'output: exec. Data inputs: target (object), position (vector). Use the white '
                              'execution path for ordering and the colored pins for values.'},
 'gameplay_tint_character': {'example': '1. Tint Red when enraged\n2. Tint Blue when frozen',
                             'tip': "Applies a solid color overlay tint to a character's sprite for a duration. "
                                    'Execution input: exec. Execution output: exec. Data inputs: target (object), '
                                    'color (color, default=[90, 255, 90]), duration (number, default=1.0). Settings: '
                                    'color, duration. Use the white execution path for ordering and the colored pins '
                                    'for values.'},
 'gate_and': {'example': '1. If A and B -> Explode',
              'tip': 'Returns True if both A and B are True. Data inputs: A (boolean), B (boolean). Data outputs: '
                     'Out (boolean).'},
 'gate_implies': {'example': '1. Formal logic flow',
                  'tip': 'Returns False if A is True and B is False, else True. Data inputs: A (boolean), B '
                         '(boolean). Data outputs: Out (boolean).'},
 'gate_nand': {'example': '1. Universal logic gate base',
               'tip': 'Returns False only if both A and B are True. Data inputs: A (boolean), B (boolean). Data '
                      'outputs: Out (boolean).'},
 'gate_nor': {'example': '1. If neither -> Do Action',
              'tip': 'Returns True only if both A and B are False. Data inputs: A (boolean), B (boolean). Data '
                     'outputs: Out (boolean).'},
 'gate_not': {'example': '1. If Not Stunned -> Move',
              'tip': 'Inverts the boolean value. Data inputs: In (boolean). Data outputs: Out (boolean).'},
 'gate_or': {'example': '1. If A or B -> Jump',
             'tip': 'Returns True if either A or B is True. Data inputs: A (boolean), B (boolean). Data outputs: Out '
                    '(boolean).'},
 'gate_xnor': {'example': '1. State matcher',
               'tip': 'Returns True if A and B are the same. Data inputs: A (boolean), B (boolean). Data outputs: '
                      'Out (boolean).'},
 'gate_xor': {'example': '1. Flashing light toggle',
              'tip': 'Returns True if A and B are different. Data inputs: A (boolean), B (boolean). Data outputs: '
                     'Out (boolean).'},
 'godot_apply_floor_snap': {'example': '1. Add Apply Floor Snap from the Godot 2D category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Snap a body down to a nearby floor.'},
 'godot_clear_slide_collisions': {'example': '1. Add Clear Slide Collisions from the Godot 2D category.\n'
                                             '2. Connect the available inputs.\n'
                                             '3. Use the output in the next calculation or condition.',
                                  'tip': 'Clear stored slide results.'},
 'godot_floor_velocity': {'example': '1. Add Get Floor Velocity from the Godot 2D category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Read supporting floor movement.'},
 'godot_force_floor_state': {'example': '1. Add Force Floor State from the Godot 2D category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Override grounded state for scripted movement.'},
 'godot_force_wall_state': {'example': '1. Add Force Wall State from the Godot 2D category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Override wall contact state.'},
 'godot_get_floor_normal': {'example': '1. Add Get Floor Normal from the Godot 2D category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Read the current floor normal.'},
 'godot_get_last_motion': {'example': '1. Add Get Last Motion from the Godot 2D category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Read the motion applied last frame.'},
 'godot_get_position_delta': {'example': '1. Add Get Position Delta from the Godot 2D category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Read movement since last frame.'},
 'godot_get_real_velocity': {'example': '1. Add Get Real Velocity from the Godot 2D category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Read velocity after sliding.'},
 'godot_get_slide_collision': {'example': '1. Add Get Slide Collision from the Godot 2D category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Read one slide collision result.'},
 'godot_get_slide_count': {'example': '1. Add Get Slide Count from the Godot 2D category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Count slide collisions from the latest move.'},
 'godot_get_wall_normal': {'example': '1. Add Get Wall Normal from the Godot 2D category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Read the latest wall normal.'},
 'godot_is_on_ceiling': {'example': '1. Add Is On Ceiling from the Godot 2D category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Check whether the body touches the ceiling.'},
 'godot_is_on_floor': {'example': '1. Add Is On Floor from the Godot 2D category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Check whether the body is grounded.'},
 'godot_is_on_wall': {'example': '1. Add Is On Wall from the Godot 2D category.\n'
                                 '2. Connect the available inputs.\n'
                                 '3. Use the output in the next calculation or condition.',
                      'tip': 'Check whether the body touches a wall.'},
 'godot_move_and_collide': {'example': '1. Add Move And Collide from the Godot 2D category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Move once and return collision information.'},
 'godot_move_and_slide': {'example': '1. Add Move And Slide from the Godot 2D category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Kinematic movement with floor and wall sliding.'},
 'godot_move_local': {'example': '1. Add Move Local from the Godot 2D category.\n'
                                 '2. Connect the available inputs.\n'
                                 '3. Use the output in the next calculation or condition.',
                      'tip': "Move in the body's local axes."},
 'godot_platform_angular_velocity': {'example': '1. Add Get Platform Angular Velocity from the Godot 2D category.\n'
                                                '2. Connect the available inputs.\n'
                                                '3. Use the output in the next calculation or condition.',
                                     'tip': 'Read platform rotation speed.'},
 'godot_platform_velocity': {'example': '1. Add Get Platform Velocity from the Godot 2D category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Read the current platform velocity.'},
 'godot_reset_motion': {'example': '1. Add Reset Motion from the Godot 2D category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Clear kinematic motion state.'},
 'godot_rotate_toward': {'example': '1. Add Rotate Toward from the Godot 2D category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Turn toward an angle by a limited step.'},
 'godot_set_ceiling_bounce': {'example': '1. Add Set Ceiling Bounce from the Godot 2D category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Tune ceiling response.'},
 'godot_set_downhill_control': {'example': '1. Add Set Downhill Control from the Godot 2D category.\n'
                                           '2. Connect the available inputs.\n'
                                           '3. Use the output in the next calculation or condition.',
                                'tip': 'Adjust downhill acceleration.'},
 'godot_set_floor_bounce': {'example': '1. Add Set Floor Bounce from the Godot 2D category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Tune floor response.'},
 'godot_set_floor_friction': {'example': '1. Add Set Floor Friction from the Godot 2D category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Tune stopping on floors.'},
 'godot_set_floor_max_angle': {'example': '1. Add Set Floor Max Angle from the Godot 2D category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Choose the steepest walkable slope.'},
 'godot_set_floor_stop': {'example': '1. Add Set Floor Stop from the Godot 2D category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Stop sliding when floor velocity is zero.'},
 'godot_set_max_slides': {'example': '1. Add Set Max Slides from the Godot 2D category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Limit collision slide iterations.'},
 'godot_set_motion_mode': {'example': '1. Add Set Motion Mode from the Godot 2D category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Choose grounded or floating character motion.'},
 'godot_set_platform_floor_layers': {'example': '1. Add Set Platform Layers from the Godot 2D category.\n'
                                                '2. Connect the available inputs.\n'
                                                '3. Use the output in the next calculation or condition.',
                                     'tip': 'Choose which platforms count as floors.'},
 'godot_set_platform_on_leave': {'example': '1. Add Set Platform On Leave from the Godot 2D category.\n'
                                            '2. Connect the available inputs.\n'
                                            '3. Use the output in the next calculation or condition.',
                                 'tip': 'Choose behavior when leaving moving platforms.'},
 'godot_set_platform_wall_layers': {'example': '1. Add Set Platform Wall Layers from the Godot 2D category.\n'
                                               '2. Connect the available inputs.\n'
                                               '3. Use the output in the next calculation or condition.',
                                    'tip': 'Choose platform wall inheritance.'},
 'godot_set_position_smoothing': {'example': '1. Add Set Position Smoothing from the Godot 2D category.\n'
                                             '2. Connect the available inputs.\n'
                                             '3. Use the output in the next calculation or condition.',
                                  'tip': 'Tune kinematic movement smoothing.'},
 'godot_set_rotation_smoothing': {'example': '1. Add Set Rotation Smoothing from the Godot 2D category.\n'
                                             '2. Connect the available inputs.\n'
                                             '3. Use the output in the next calculation or condition.',
                                  'tip': 'Tune angular movement smoothing.'},
 'godot_set_safe_margin': {'example': '1. Add Set Kinematic Safe Margin from the Godot 2D category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Tune recovery from overlaps.'},
 'godot_set_up_direction': {'example': '1. Add Set Up Direction from the Godot 2D category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Define floor/ceiling orientation.'},
 'godot_set_uphill_control': {'example': '1. Add Set Uphill Control from the Godot 2D category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Adjust movement on slopes.'},
 'godot_set_wall_friction': {'example': '1. Add Set Wall Friction from the Godot 2D category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Tune sliding along walls.'},
 'godot_snap_to_floor': {'example': '1. Add Snap To Floor from the Godot 2D category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Perform an immediate floor snap.'},
 'godot_test_move': {'example': '1. Add Test Move from the Godot 2D category.\n'
                                '2. Connect the available inputs.\n'
                                '3. Use the output in the next calculation or condition.',
                     'tip': 'Check a proposed motion without applying it.'},
 'graph_group_disable': {'example': '1. Add Disable Graph Group from the Graph Groups category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Ignore execution for every node inside a named Smart Group.'},
 'graph_group_enable': {'example': '1. Add Enable Graph Group from the Graph Groups category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Allow nodes inside a named Smart Group to execute.'},
 'graph_group_enabled': {'example': '1. Add Graph Group Enabled? from the Graph Groups category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Query a named Smart Group execution state.'},
 'graph_group_if_enabled': {'example': '1. Add IF Graph Group Enabled from the Graph Groups category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'True-only execution gate for a Smart Group flag.'},
 'graph_group_members': {'example': '1. Add Graph Group Member IDs from the Graph Groups category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Output design-time node IDs contained by a Smart Group.'},
 'graph_group_toggle': {'example': '1. Add Toggle Graph Group from the Graph Groups category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Toggle whether a named Smart Group executes.'},
 'input_add_input_vector': {'example': '1. Add Add Input Vector from the Input category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': "Add an input vector to the character's current manual vector."},
 'input_any_key': {'example': '1. Add Any Key from the Input category.\n'
                              '2. Connect the available inputs.\n'
                              '3. Use the output in the next calculation or condition.',
                   'tip': 'Fires for any keyboard key or mouse input. Use the key output to inspect which input '
                          'arrived.'},
 'input_axis_to_vector': {'example': '1. Add Axis To Vector from the Input category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Turn one horizontal axis into a vector.'},
 'input_bind_key': {'example': '1. Add Bind Key from the Input category.\n'
                               '2. Connect the available inputs.\n'
                               '3. Use the output in the next calculation or condition.',
                    'tip': 'Store a key-to-action binding for this character.'},
 'input_clamp_vector': {'example': '1. Add Clamp Input Vector from the Input category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Clamp vector magnitude.'},
 'input_clear_input_vector': {'example': '1. Add Clear Input Vector from the Input category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Clear manual input without changing velocity.'},
 'input_cursor_lock': {'example': '1. Add Lock Cursor from the Input category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Capture the mouse cursor to the game window.'},
 'input_cursor_visible': {'example': '1. Add Set Cursor Visible from the Input category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Show or hide the system mouse cursor.'},
 'input_disable_action_map': {'example': '1. Add Disable Action Map from the Input category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Disable a named group of input commands.'},
 'input_edge': {'example': '1. Add Input Edge from the Control category.\n'
                           '2. Connect the available inputs.\n'
                           '3. Use the output in the next calculation or condition.',
                'tip': 'Record a rising or falling edge state.'},
 'input_enable_action_map': {'example': '1. Add Enable Action Map from the Input category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Enable a named group of input commands.'},
 'input_fire_action': {'example': '1. Add Fire Action from the Input category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Manually emit a stored action command.'},
 'input_gate': {'example': '1. Add Input Gate from the Control category.\n'
                           '2. Connect the available inputs.\n'
                           '3. Use the output in the next calculation or condition.',
                'tip': 'Allow input through only while Enabled is true.'},
 'input_get_control_mode': {'example': '1. Add Get Control Mode from the Input category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': "Read the character's control mode."},
 'input_get_input_priority': {'example': '1. Add Get Input Priority from the Input category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Read scene input priority.'},
 'input_get_manual_input': {'example': '1. Add Get Manual Input Enabled from the Input category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Read whether manual input is enabled.'},
 'input_get_mouse_delta': {'example': '1. Add Get Mouse Delta from the Input category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Read relative mouse movement.'},
 'input_get_mouse_position': {'example': '1. Add Get Mouse Position from the Input category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Read current mouse screen position.'},
 'input_get_mouse_wheel': {'example': '1. Add Get Mouse Wheel from the Input category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Read the latest mouse wheel amount.'},
 'input_key': {'example': '1. Add Key Input from the Input category.\n'
                          '2. Connect event_key.\n'
                          '3. Use is_down, key in the next calculation or condition.',
               'tip': 'Matches a key string from On Input. It exposes separate pressed, released, and held execution '
                      'outputs. Execution input: exec. Execution output: pressed, released, held. Data inputs: '
                      "event_key (string, default=''). Data outputs: is_down (boolean), key (string). Settings: key. "
                      'Use the white execution path for ordering and the colored pins for values.'},
 'input_key_combo': {'example': '1. Add Key Combination from the Input category.\n'
                                '2. Connect the available inputs.\n'
                                '3. Use the output in the next calculation or condition.',
                     'tip': 'Matches modifier combinations such as ctrl+w, shift+space, or alt+mouse_left. Settings: '
                            'key.'},
 'input_latch': {'example': '1. Add Input Latch from the Control category.\n'
                            '2. Connect the available inputs.\n'
                            '3. Use the output in the next calculation or condition.',
                 'tip': 'Latch a boolean input until explicitly reset.'},
 'input_lock_manual': {'example': '1. Add Lock Manual Input from the Input category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Stop raw keyboard/mouse input from reaching this character.'},
 'input_lock_scene_controls': {'example': '1. Add Lock Scene Controls from the Input category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': "Disable the arena camera's normal WASD/arrow controls."},
 'input_mouse_button': {'example': '1. Add Mouse Button from the Input category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Treats mouse_left, mouse_right, or mouse_middle as an input key. Settings: key.'},
 'input_normalize_vector': {'example': '1. Add Normalize Input Vector from the Input category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Normalize a vector safely.'},
 'input_pause_input': {'example': '1. Add Pause Input from the Input category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Temporarily ignore manual input while preserving current movement.'},
 'input_release_mouse_capture': {'example': '1. Add Release Mouse Capture from the Input category.\n'
                                            '2. Connect the available inputs.\n'
                                            '3. Use the output in the next calculation or condition.',
                                 'tip': 'Release captured mouse input.'},
 'input_reset_action_state': {'example': '1. Add Reset Action State from the Input category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Clear a named action state.'},
 'input_resume_input': {'example': '1. Add Resume Input from the Input category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Allow manual input after an input pause.'},
 'input_scale_vector': {'example': '1. Add Scale Input Vector from the Input category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Multiply a vector by a sensitivity scale.'},
 'input_set_action_state': {'example': '1. Add Set Action State from the Input category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Set a named action state on or off.'},
 'input_set_controller_deadzone': {'example': '1. Add Set Controller Deadzone from the Input category.\n'
                                              '2. Connect the available inputs.\n'
                                              '3. Use the output in the next calculation or condition.',
                                   'tip': 'Store an analog controller deadzone.'},
 'input_set_deadzone': {'example': '1. Add Set Input Deadzone from the Input category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Set a stored analog input deadzone.'},
 'input_set_input_priority': {'example': '1. Add Set Input Priority from the Input category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Store which system owns input priority: player, scene, UI, or custom.'},
 'input_set_input_vector': {'example': '1. Add Set Input Vector from the Input category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': "Set the character's manual input vector."},
 'input_set_manual_enabled': {'example': '1. Add Set Manual Input Enabled from the Input category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Enable or disable character manual input from a boolean pin.'},
 'input_set_mouse_capture': {'example': '1. Add Set Mouse Capture from the Input category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Capture or release mouse input for gameplay controls.'},
 'input_set_mouse_sensitivity': {'example': '1. Add Set Mouse Sensitivity from the Input category.\n'
                                            '2. Connect the available inputs.\n'
                                            '3. Use the output in the next calculation or condition.',
                                 'tip': 'Store mouse look sensitivity.'},
 'input_set_repeat_rate': {'example': '1. Add Set Key Repeat Rate from the Input category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Store a repeat interval for held input commands.'},
 'input_set_sensitivity': {'example': '1. Add Set Input Sensitivity from the Input category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Set a stored manual input sensitivity multiplier.'},
 'input_set_touch_mode': {'example': '1. Add Set Touch Mode from the Input category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Store a touch input mode name.'},
 'input_smooth_vector': {'example': '1. Add Smooth Input Vector from the Input category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Blend current input toward a target vector.'},
 'input_unbind_key': {'example': '1. Add Unbind Key from the Input category.\n'
                                 '2. Connect the available inputs.\n'
                                 '3. Use the output in the next calculation or condition.',
                      'tip': 'Remove a named key binding.'},
 'input_unlock_manual': {'example': '1. Add Unlock Manual Input from the Input category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Allow raw keyboard/mouse input to reach this character again.'},
 'input_unlock_scene_controls': {'example': '1. Add Unlock Scene Controls from the Input category.\n'
                                            '2. Connect the available inputs.\n'
                                            '3. Use the output in the next calculation or condition.',
                                 'tip': "Restore the arena camera's normal keyboard controls."},
 'input_vector_to_direction': {'example': '1. Add Vector To Direction from the Input category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Normalize an input vector.'},
 'lifecycle_clone_with_stats': {'example': '1. Clone boss but set Scale = 0.5 and Speed = 300 for a fast '
                                           'mini-version\n'
                                           '2. Clone self on hit',
                                'tip': 'Duplicates a character but overrides specific stats on the new copy. '
                                       'Execution input: exec. Execution output: exec. Data inputs: target (object), '
                                       'hp (number, default=0), damage_min (number, default=0), damage_max (number, '
                                       'default=0), speed (number, default=0), scale (number, default=0.0). Data '
                                       'outputs: clone (object). Settings: hp, damage_min, damage_max, speed, scale. '
                                       'Use the white execution path for ordering and the colored pins for values.'},
 'lifecycle_despawn': {'example': '1. Despawn projectiles after 2 seconds\n2. On Animation Finished -> Despawn',
                       'tip': 'Removes the character from the scene without triggering on_death hooks. Execution '
                              'input: exec. Execution output: exec. Data inputs: target (object). Use the white '
                              'execution path for ordering and the colored pins for values.'},
 'lifecycle_revive': {'example': '1. Necromancer trait: On Ally Died -> Revive Ally (50% HP)\n'
                                 '2. On Death -> Once -> Revive Self (100% HP)',
                      'tip': 'Brings a dead (0 HP) character back to life with a set percentage of their max HP. '
                             'Execution input: exec. Execution output: exec. Data inputs: target (object), '
                             'hp_percent (number, default=100). Settings: hp_percent. Use the white execution path '
                             'for ordering and the colored pins for values.'},
 'lifecycle_set_max_hp': {'example': '1. Boss Phase 2: Set Max HP to 5000\n2. Level Up -> Set Max HP + 100',
                          'tip': "Changes the character's HP ceiling. Can optionally scale current HP "
                                 'proportionally. Execution input: exec. Execution output: exec. Data inputs: target '
                                 '(object), max_hp (number, default=100). Settings: max_hp, scale_current. Use the '
                                 'white execution path for ordering and the colored pins for values.'},
 'logic_is_alive': {'example': '1. If Is Alive -> Play Anim\n2. Prevent tracking dead bodies',
                    'tip': 'Returns True if the character is not dead. Data inputs: Character (object). Data '
                           'outputs: Alive (boolean).'},
 'loop_break': {'example': '1. If Target Found -> Break\n2. If HP < 0 -> Break',
                'tip': 'Immediately aborts the enclosing loop. Execution input: exec. Use the white execution path '
                       'for ordering and the colored pins for values.'},
 'loop_continue': {'example': '1. If Ally -> Continue (skip damage logic)\n2. If Dead -> Continue',
                   'tip': 'Skips the rest of this loop iteration and moves to the next one. Execution input: exec. '
                          'Use the white execution path for ordering and the colored pins for values.'},
 'loop_countdown_until': {'example': '1. Add Countdown Until Equal from the Loops category.\n'
                                     '2. Connect start, step, target.\n'
                                     '3. Use current, done in the next calculation or condition.',
                          'tip': 'Starts at Start, subtracts Step repeatedly, and runs the Loop body until Current '
                                 'equals Target. Use Current or Done as colored data, Loop for each subtraction, and '
                                 'Completed after the target is reached. Execution input: exec. Execution output: '
                                 'loop, completed. Data inputs: start (number, default=3), step (number, default=1), '
                                 'target (number, default=0). Data outputs: current (number), done (boolean). '
                                 'Settings: start, step, target. Use the white execution path for ordering and the '
                                 'colored pins for values.'},
 'loop_for': {'example': '1. For 1 to 5 -> Spawn Particle\n2. For 1 to 3 -> Spawn Minion',
              'tip': 'A standard counted For loop from Start to End, firing its body each iteration. Execution '
                     'input: exec. Execution output: exec, completed. Data inputs: count (number, default=3). Data '
                     'outputs: index (number). Settings: count. Use the white execution path for ordering and the '
                     'colored pins for values.'},
 'loop_for_each': {'example': '1. Get Characters In Radius -> For Each -> Deal Damage\n2. For Each Ally -> Heal',
                   'tip': 'Iterates over a list of characters, firing the body once per item in the list. Execution '
                          'input: exec. Execution output: exec, completed. Data inputs: list (object). Data outputs: '
                          'item (object), index (number). Use the white execution path for ordering and the colored '
                          'pins for values.'},
 'loop_repeat_while': {'example': '1. Keep generating "Random Point" until it\'s a safe distance away\n'
                                  '2. Safe iteration over array',
                       'tip': 'A safe While loop capped at 1000 iterations -- repeats until the condition is False. '
                              'Execution input: exec. Execution output: exec, completed. Data inputs: condition '
                              '(boolean, default=True). Data outputs: index (number). Settings: max_iterations. Use '
                              'the white execution path for ordering and the colored pins for values.'},
 'loop_trigger_n_times': {'example': '1. Trigger 5 times -> Spawn Particle\n2. Trigger 3 times -> Dash in triangle',
                          'tip': 'Fires its execution body exactly N times in a single frame. Execution input: exec. '
                                 'Execution output: exec, completed. Data inputs: count (number, default=3). Data '
                                 'outputs: index (number). Settings: count. Use the white execution path for '
                                 'ordering and the colored pins for values.'},
 'loop_while': {'example': '1. While HP < 100 -> Heal (Will freeze if no delay!)\n'
                           '2. Use "Repeat While" instead for safety',
                'tip': 'A raw While loop -- will crash the game if the condition never becomes False. Use Repeat '
                       'While instead. Execution input: exec. Execution output: exec, completed. Data inputs: '
                       'condition (boolean, default=True). Use the white execution path for ordering and the colored '
                       'pins for values.'},
 'math_abs': {'example': '1. Abs(Velocity X) -> Speed X\n2. Abs(-50) -> 50',
              'tip': 'Returns the absolute (positive) value of a number. -50 becomes 50. Data inputs: value (number, '
                     'default=0). Data outputs: result (number). This is a pure data node: wire its colored output '
                     'directly into another input; no white execution wire is required.'},
 'math_add': {'example': '1. Base Damage + Bonus Damage -> Deal Damage\n2. Variable + 1 -> Set Variable',
              'tip': 'Adds two numbers together. A + B. Data inputs: a (number, default=0), b (number, default=0). '
                     'Data outputs: result (number). This is a pure data node: wire its colored output directly into '
                     'another input; no white execution wire is required.'},
 'math_angle_between': {'example': '1. Angle from self to target → rotate a cone\n'
                                   '2. Check if target is to the left or right',
                        'tip': 'Returns the angle in degrees from position A to position B. Wire two character '
                               'positions to get a facing direction as a number. Data inputs: from_pos (vector, '
                               'default=(0, 0)), to_pos (vector, default=(1, 0)). Data outputs: degrees (number). '
                               'This is a pure data node: wire its colored output directly into another input; no '
                               'white execution wire is required.'},
 'math_atan2': {'example': '1. Add Atan2 from the Math category.\n'
                           '2. Connect y, x.\n'
                           '3. Use result in the next calculation or condition.',
                'tip': 'Returns the angle in radians from X and Y. Data inputs: y (number, default=0), x (number, '
                       'default=1). Data outputs: result (number). This is a pure data node: wire its colored output '
                       'directly into another input; no white execution wire is required.'},
 'math_average': {'example': '1. Add Average from the Math category.\n'
                             '2. Connect a, b.\n'
                             '3. Use result in the next calculation or condition.',
                  'tip': 'Returns the arithmetic mean of A and B. Data inputs: a (number, default=0), b (number, '
                         'default=0). Data outputs: result (number). This is a pure data node: wire its colored '
                         'output directly into another input; no white execution wire is required.'},
 'math_bezier_scalar': {'example': '1. Add Bezier Scalar from the Math category.\n'
                                   '2. Connect a, control, b.\n'
                                   '3. Use result in the next calculation or condition.',
                        'tip': 'Quadratic Bezier interpolation of A, Control, and B. Data inputs: a (number, '
                               'default=0), control (number, default=0.5), b (number, default=1), t (number, '
                               'default=0.5). Data outputs: result (number). This is a pure data node: wire its '
                               'colored output directly into another input; no white execution wire is required.'},
 'math_cbrt': {'example': '1. Add Cube Root from the Math category.\n'
                          '2. Connect value.\n'
                          '3. Use result in the next calculation or condition.',
               'tip': 'Returns the real cube root, including for negative values. Data inputs: value (number, '
                      'default=0). Data outputs: result (number). This is a pure data node: wire its colored output '
                      'directly into another input; no white execution wire is required.'},
 'math_ceil': {'example': '1. Ceil(2.1) -> 3\n2. Ceil(Damage) -> Minimum 1 Damage',
               'tip': 'Rounds a number UP to the nearest whole integer. 2.1 becomes 3. Data inputs: value (number, '
                      'default=0). Data outputs: result (number). This is a pure data node: wire its colored output '
                      'directly into another input; no white execution wire is required.'},
 'math_clamp': {'example': '1. Clamp HP between 0 and Max HP\n2. Clamp Speed between 0 and 500',
                'tip': 'Forces a number to stay between Min and Max. Prevents values from going out of range. Data '
                       'inputs: value (number, default=0), min (number, default=0), max (number, default=1). Data '
                       'outputs: result (number). This is a pure data node: wire its colored output directly into '
                       'another input; no white execution wire is required.'},
 'math_closest': {'example': '1. Add Closest Number from the Math category.\n'
                             '2. Connect a, b, target.\n'
                             '3. Use value in the next calculation or condition.',
                  'tip': 'Returns whichever candidate is closer to Target. Data inputs: a (number, default=0), b '
                         '(number, default=1), target (number, default=0). Data outputs: value (number). This is a '
                         'pure data node: wire its colored output directly into another input; no white execution '
                         'wire is required.'},
 'math_color_lerp': {'example': '1. Interpolate -> eased_t -> Color Lerp (white→transparent) -> Tint Character\n'
                                '2. HP Percent -> Color Lerp (green→red) -> Tint Character (live health colour)',
                     'tip': 'Smoothly blends between two RGB colors based on a 0→1 T value. Wire an Ease or '
                            "Interpolate 'eased_t' output here to get smooth color transitions. The result is a "
                            'Color you can plug directly into Tint Character, Flash Tint, Constant Color, particle '
                            'color, etc. Data inputs: t (number, default=0.5), from_color (color, default=[255, 90, '
                            '90]), to_color (color, default=[90, 90, 255]). Data outputs: color (color). Settings: '
                            'from_color, to_color. This is a pure data node: wire its colored output directly into '
                            'another input; no white execution wire is required.'},
 'math_compare_range': {'example': '1. Add Compare Range from the Math category.\n'
                                   '2. Connect value, min, max.\n'
                                   '3. Use inside in the next calculation or condition.',
                        'tip': 'Returns True when Value is between Min and Max, inclusive. Data inputs: value '
                               '(number, default=0), min (number, default=0), max (number, default=1). Data outputs: '
                               'inside (number). This is a pure data node: wire its colored output directly into '
                               'another input; no white execution wire is required.'},
 'math_constant': {'example': '1. Constant(100) -> HP\n2. Constant(3.14) -> Pi',
                   'tip': 'Provides a fixed hardcoded number. Drag to wire it to any numeric input. Data outputs: '
                          'value (number). Settings: value. This is a pure data node: wire its colored output '
                          'directly into another input; no white execution wire is required.'},
 'math_cos': {'example': '1. Circular movement X component\n2. Oscillations',
              'tip': 'Returns the cosine of A (in radians).'},
 'math_cosine': {'example': '1. Cosine(Time) -> Swaying Motion\n2. Cosine(Angle) -> X Vector',
                 'tip': 'Returns the cosine of an angle in degrees. Use with Sine for circular motion. Data inputs: '
                        'value (number, default=0). Data outputs: result (number). This is a pure data node: wire '
                        'its colored output directly into another input; no white execution wire is required.'},
 'math_cube': {'example': '1. Add Cube from the Math category.\n'
                          '2. Connect value.\n'
                          '3. Use result in the next calculation or condition.',
               'tip': 'Returns Value cubed. Data inputs: value (number, default=0). Data outputs: result (number). '
                      'This is a pure data node: wire its colored output directly into another input; no white '
                      'execution wire is required.'},
 'math_cubic_bezier': {'example': '1. Add Cubic Bezier from the Math category.\n'
                                  '2. Connect a, b, c.\n'
                                  '3. Use result in the next calculation or condition.',
                       'tip': 'Cubic Bezier interpolation through A, B, C, and D. Data inputs: a (number, '
                              'default=0), b (number, default=0), c (number, default=1), d (number, default=1), t '
                              '(number, default=0.5). Data outputs: result (number). This is a pure data node: wire '
                              'its colored output directly into another input; no white execution wire is required.'},
 'math_deadzone': {'example': '1. Add Deadzone from the Math category.\n'
                              '2. Connect value, zone.\n'
                              '3. Use value in the next calculation or condition.',
                   'tip': 'Removes small input noise and rescales the remaining range. Data inputs: value (number, '
                          'default=0), zone (number, default=0.1). Data outputs: value (number). This is a pure data '
                          'node: wire its colored output directly into another input; no white execution wire is '
                          'required.'},
 'math_degrees': {'example': '1. Add Radians To Degrees from the Math category.\n'
                             '2. Connect radians.\n'
                             '3. Use result in the next calculation or condition.',
                  'tip': 'Converts radians into degrees. Data inputs: radians (number, default=0). Data outputs: '
                         'result (number). This is a pure data node: wire its colored output directly into another '
                         'input; no white execution wire is required.'},
 'math_direction_1d': {'example': '1. Add Direction 1D from the Math category.\n'
                                  '2. Connect origin, target.\n'
                                  '3. Use direction in the next calculation or condition.',
                       'tip': 'Returns -1, 0, or 1 from Origin toward Target. Data inputs: origin (number, '
                              'default=0), target (number, default=0). Data outputs: direction (number). This is a '
                              'pure data node: wire its colored output directly into another input; no white '
                              'execution wire is required.'},
 'math_distance_1d': {'example': '1. Add Distance 1D from the Math category.\n'
                                 '2. Connect a, b.\n'
                                 '3. Use distance in the next calculation or condition.',
                      'tip': 'Absolute distance between A and B on a number line. Data inputs: a (number, '
                             'default=0), b (number, default=0). Data outputs: distance (number). This is a pure '
                             'data node: wire its colored output directly into another input; no white execution '
                             'wire is required.'},
 'math_divide': {'example': '1. Current HP / Max HP -> HP Percent\n2. Distance / Speed -> Time to Arrive',
                 'tip': 'Divides A by B. Returns 0 safely if B is zero. Data inputs: a (number, default=1), b '
                        '(number, default=1). Data outputs: result (number). This is a pure data node: wire its '
                        'colored output directly into another input; no white execution wire is required.'},
 'math_ease': {'example': '1. Tween Value -> t -> Ease (sine_out) -> eased_t -> Color Lerp\n'
                          '2. Normalize Range -> Ease (bounce_out) -> Lerp -> Set Speed',
               'tip': 'Applies an easing curve to a 0→1 progress value. Wire a Normalize Range or Tween Value '
                      'progress into this, then pipe the result into a Lerp or Color Lerp. Covers all standard '
                      'curves: linear, quad, cubic, quart, quint, sine, expo, circ, back, elastic, bounce — each '
                      'with in/out/inout variants. Data inputs: t (number, default=0.5). Data outputs: eased '
                      '(number). Settings: curve. This is a pure data node: wire its colored output directly into '
                      'another input; no white execution wire is required.'},
 'math_ease_in': {'example': '1. Add Ease In from the Math category.\n'
                             '2. Connect t.\n'
                             '3. Use value in the next calculation or condition.',
                  'tip': 'Quadratic ease-in for T. Data inputs: t (number, default=0.5). Data outputs: value '
                         '(number). This is a pure data node: wire its colored output directly into another input; '
                         'no white execution wire is required.'},
 'math_ease_in_out': {'example': '1. Add Ease In Out from the Math category.\n'
                                 '2. Connect t.\n'
                                 '3. Use value in the next calculation or condition.',
                      'tip': 'Smooth sine ease-in/out for T. Data inputs: t (number, default=0.5). Data outputs: '
                             'value (number). This is a pure data node: wire its colored output directly into '
                             'another input; no white execution wire is required.'},
 'math_ease_out': {'example': '1. Add Ease Out from the Math category.\n'
                              '2. Connect t.\n'
                              '3. Use value in the next calculation or condition.',
                   'tip': 'Quadratic ease-out for T. Data inputs: t (number, default=0.5). Data outputs: value '
                          '(number). This is a pure data node: wire its colored output directly into another input; '
                          'no white execution wire is required.'},
 'math_exp': {'example': '1. Add Exponential from the Math category.\n'
                         '2. Connect value.\n'
                         '3. Use result in the next calculation or condition.',
              'tip': 'Returns e to the power of Value. Data inputs: value (number, default=0). Data outputs: result '
                     '(number). This is a pure data node: wire its colored output directly into another input; no '
                     'white execution wire is required.'},
 'math_factorial': {'example': '1. Add Factorial from the Math category.\n'
                               '2. Connect n.\n'
                               '3. Use value in the next calculation or condition.',
                    'tip': 'Returns N factorial for a non-negative integer. Data inputs: n (number, default=1). Data '
                           'outputs: value (number). This is a pure data node: wire its colored output directly into '
                           'another input; no white execution wire is required.'},
 'math_fibonacci': {'example': '1. Add Fibonacci from the Math category.\n'
                               '2. Connect n.\n'
                               '3. Use value in the next calculation or condition.',
                    'tip': 'Returns the Nth Fibonacci number, safely capped. Data inputs: n (number, default=0). '
                           'Data outputs: value (number). This is a pure data node: wire its colored output directly '
                           'into another input; no white execution wire is required.'},
 'math_floor': {'example': '1. Floor(2.9) -> 2\n2. Floor(HP) -> Integer HP',
                'tip': 'Rounds a number DOWN to the nearest whole integer. 2.9 becomes 2. Data inputs: value '
                       '(number, default=0). Data outputs: result (number). This is a pure data node: wire its '
                       'colored output directly into another input; no white execution wire is required.'},
 'math_fraction': {'example': '1. Add Fractional Part from the Math category.\n'
                              '2. Connect value.\n'
                              '3. Use result in the next calculation or condition.',
                   'tip': 'Returns the fractional part of Value. Data inputs: value (number, default=0). Data '
                          'outputs: result (number). This is a pure data node: wire its colored output directly into '
                          'another input; no white execution wire is required.'},
 'math_gcd': {'example': '1. Add Greatest Common Divisor from the Math category.\n'
                         '2. Connect a, b.\n'
                         '3. Use gcd in the next calculation or condition.',
              'tip': 'Returns the greatest common divisor of A and B. Data inputs: a (number, default=0), b (number, '
                     'default=0). Data outputs: gcd (number). This is a pure data node: wire its colored output '
                     'directly into another input; no white execution wire is required.'},
 'math_geometric_mean': {'example': '1. Add Geometric Mean from the Math category.\n'
                                    '2. Connect a, b.\n'
                                    '3. Use result in the next calculation or condition.',
                         'tip': 'Returns the geometric mean of two non-negative values. Data inputs: a (number, '
                                'default=1), b (number, default=1). Data outputs: result (number). This is a pure '
                                'data node: wire its colored output directly into another input; no white execution '
                                'wire is required.'},
 'math_harmonic_mean': {'example': '1. Add Harmonic Mean from the Math category.\n'
                                   '2. Connect a, b.\n'
                                   '3. Use result in the next calculation or condition.',
                        'tip': 'Returns 2AB divided by A+B, safely handling zero. Data inputs: a (number, '
                               'default=1), b (number, default=1). Data outputs: result (number). This is a pure '
                               'data node: wire its colored output directly into another input; no white execution '
                               'wire is required.'},
 'math_hypot': {'example': '1. Add Hypotenuse from the Math category.\n'
                           '2. Connect x, y.\n'
                           '3. Use result in the next calculation or condition.',
                'tip': 'Returns sqrt(X squared + Y squared). Data inputs: x (number, default=0), y (number, '
                       'default=0). Data outputs: result (number). This is a pure data node: wire its colored output '
                       'directly into another input; no white execution wire is required.'},
 'math_in_range': {'example': '1. Add In Range from the Math category.\n'
                              '2. Connect value, min, max.\n'
                              '3. Use inside in the next calculation or condition.',
                   'tip': 'Returns 1 when Value is inside the range, otherwise 0. Data inputs: value (number, '
                          'default=0), min (number, default=0), max (number, default=1). Data outputs: inside '
                          '(number). This is a pure data node: wire its colored output directly into another input; '
                          'no white execution wire is required.'},
 'math_interpolate': {'example': '1. On Spawn -> Interpolate (0→300, 2s, sine_inout) -> value -> Set Speed '
                                 '(ramp-up)\n'
                                 '2. Interpolate (1→0, 0.5s, expo_out) -> alpha -> Opacity Fade',
                      'tip': 'Blends from value A to value B using a 0→1 progress input and an optional easing '
                             'curve. This is the all-in-one version: set duration, pick your curve, and it drives '
                             "itself each frame using an internal timer stored on the character. Wire the 'value' "
                             'output into anything — speed, damage, opacity, color channels, etc. Execution input: '
                             'exec. Execution output: exec, done. Data inputs: target (object), from_val (number, '
                             'default=0.0), to_val (number, default=1.0), duration (number, default=1.0). Data '
                             'outputs: value (number), t (number), eased_t (number). Settings: curve, duration, '
                             'loop, pingpong. Use the white execution path for ordering and the colored pins for '
                             'values.'},
 'math_inverse_lerp': {'example': '1. Add Inverse Lerp from the Math category.\n'
                                  '2. Connect a, b, value.\n'
                                  '3. Use t in the next calculation or condition.',
                       'tip': 'Returns where Value lies between A and B as a 0-to-1 fraction. Data inputs: a '
                              '(number, default=0), b (number, default=1), value (number, default=0). Data outputs: '
                              't (number). This is a pure data node: wire its colored output directly into another '
                              'input; no white execution wire is required.'},
 'math_is_even': {'example': '1. Add Is Even from the Math category.\n'
                             '2. Connect value.\n'
                             '3. Use even in the next calculation or condition.',
                  'tip': 'Returns True when the integer part of Value is even. Data inputs: value (number, '
                         'default=0). Data outputs: even (number). This is a pure data node: wire its colored output '
                         'directly into another input; no white execution wire is required.'},
 'math_is_integer': {'example': '1. Add Is Integer from the Math category.\n'
                                '2. Connect value.\n'
                                '3. Use integer in the next calculation or condition.',
                     'tip': 'Returns True when Value has no fractional part. Data inputs: value (number, default=0). '
                            'Data outputs: integer (number). This is a pure data node: wire its colored output '
                            'directly into another input; no white execution wire is required.'},
 'math_is_near': {'example': '1. Add Is Near from the Math category.\n'
                             '2. Connect a, b, tolerance.\n'
                             '3. Use near in the next calculation or condition.',
                  'tip': 'Returns True when A and B are within Tolerance. Data inputs: a (number, default=0), b '
                         '(number, default=0), tolerance (number, default=0.001). Data outputs: near (number). This '
                         'is a pure data node: wire its colored output directly into another input; no white '
                         'execution wire is required.'},
 'math_is_odd': {'example': '1. Add Is Odd from the Math category.\n'
                            '2. Connect value.\n'
                            '3. Use odd in the next calculation or condition.',
                 'tip': 'Returns True when the integer part of Value is odd. Data inputs: value (number, default=0). '
                        'Data outputs: odd (number). This is a pure data node: wire its colored output directly into '
                        'another input; no white execution wire is required.'},
 'math_is_positive': {'example': '1. Add Is Positive from the Math category.\n'
                                 '2. Connect value.\n'
                                 '3. Use positive in the next calculation or condition.',
                      'tip': 'Returns True when Value is greater than zero. Data inputs: value (number, default=0). '
                             'Data outputs: positive (number). This is a pure data node: wire its colored output '
                             'directly into another input; no white execution wire is required.'},
 'math_lcm': {'example': '1. Add Least Common Multiple from the Math category.\n'
                         '2. Connect a, b.\n'
                         '3. Use lcm in the next calculation or condition.',
              'tip': 'Returns the least common multiple of A and B. Data inputs: a (number, default=0), b (number, '
                     'default=0). Data outputs: lcm (number). This is a pure data node: wire its colored output '
                     'directly into another input; no white execution wire is required.'},
 'math_lerp': {'example': '1. Timeline -> Lerp(0, 255) -> Alpha\n2. Lerp(Scale 1.0, Scale 2.0) -> Set Scale',
               'tip': 'Smoothly blends from A to B based on T (0.0 = A, 1.0 = B). Essential for animations, fades, '
                      'and easing. Data inputs: a (number, default=0), b (number, default=1), t (number, '
                      'default=0.5). Data outputs: result (number). This is a pure data node: wire its colored '
                      'output directly into another input; no white execution wire is required.'},
 'math_lerp_angle': {'example': '1. Smoothly rotate a facing direction toward target\n2. Lerp a turret aim angle',
                     'tip': 'Interpolates between two angles (degrees) without wrap-around jitter. Always takes the '
                            'shortest path around the circle. Data inputs: from_deg (number, default=0), to_deg '
                            '(number, default=180), t (number, default=0.5). Data outputs: angle (number). This is a '
                            'pure data node: wire its colored output directly into another input; no white execution '
                            'wire is required.'},
 'math_log': {'example': '1. Add Logarithm from the Math category.\n'
                         '2. Connect value, base.\n'
                         '3. Use result in the next calculation or condition.',
              'tip': 'Logarithm of Value using the selected Base. Data inputs: value (number, default=1), base '
                     '(number, default=2). Data outputs: result (number). This is a pure data node: wire its colored '
                     'output directly into another input; no white execution wire is required.'},
 'math_log10': {'example': '1. Add Log 10 from the Math category.\n'
                           '2. Connect value.\n'
                           '3. Use result in the next calculation or condition.',
                'tip': 'Base-10 logarithm of Value. Data inputs: value (number, default=1). Data outputs: result '
                       '(number). This is a pure data node: wire its colored output directly into another input; no '
                       'white execution wire is required.'},
 'math_map_range2': {'example': '1. Map HP (0 to Max HP) into Bar Width (0 to 200)\n2. Scale speed based on distance',
                     'tip': 'Remaps a value from one range to another. Data inputs: Value (number), InMin (number), '
                            'InMax (number), OutMin (number), OutMax (number). Data outputs: Result (number). This '
                            'is a pure data node: wire its colored output directly into another input; no white '
                            'execution wire is required.'},
 'math_max': {'example': '1. Max(0, Damage - Defense) -> Actual Damage\n2. Max(Speed, 100) -> Minimum Speed',
              'tip': 'Returns whichever of A or B is larger. Data inputs: a (number, default=0), b (number, '
                     'default=0). Data outputs: result (number). This is a pure data node: wire its colored output '
                     'directly into another input; no white execution wire is required.'},
 'math_median_three': {'example': '1. Add Median Three from the Math category.\n'
                                  '2. Connect a, b, c.\n'
                                  '3. Use result in the next calculation or condition.',
                       'tip': 'Returns the middle value of A, B, and C. Data inputs: a (number, default=0), b '
                              '(number, default=0), c (number, default=0). Data outputs: result (number). This is a '
                              'pure data node: wire its colored output directly into another input; no white '
                              'execution wire is required.'},
 'math_min': {'example': '1. Min(HP, 100) -> Cap heal amount\n2. Min(Damage, Shield) -> Absorbed Damage',
              'tip': 'Returns whichever of A or B is smaller. Data inputs: a (number, default=0), b (number, '
                     'default=0). Data outputs: result (number). This is a pure data node: wire its colored output '
                     'directly into another input; no white execution wire is required.'},
 'math_modulo': {'example': '1. hit_count mod 3 == 0 -> spawn clone\n'
                            '2. frame_count mod 60 == 0 -> every second pulse',
                 'tip': 'Returns A mod B (the remainder after dividing A by B). Essential for every-Nth-hit '
                        'patterns, cycling through states, or wrapping values. Data inputs: a (number, default=0), b '
                        '(number, default=2). Data outputs: result (number). This is a pure data node: wire its '
                        'colored output directly into another input; no white execution wire is required.'},
 'math_multiply': {'example': '1. Base Damage * 2.0 (Crit) -> Deal Damage\n2. Speed * 0.5 (Slow) -> Set Speed',
                   'tip': 'Multiplies two numbers. A * B. Use for damage scaling, speed multipliers, percentages. '
                          'Data inputs: a (number, default=1), b (number, default=1). Data outputs: result (number). '
                          'This is a pure data node: wire its colored output directly into another input; no white '
                          'execution wire is required.'},
 'math_negate': {'example': '1. Add Negate from the Math category.\n'
                            '2. Connect value.\n'
                            '3. Use result in the next calculation or condition.',
                 'tip': 'Changes the sign of Value. Data inputs: value (number, default=0). Data outputs: result '
                        '(number). This is a pure data node: wire its colored output directly into another input; no '
                        'white execution wire is required.'},
 'math_normalize_range': {'example': '1. HP / max_hp -> normalize -> lerp colour\n'
                                     '2. Distance 0-300 -> normalize -> volume fade',
                          'tip': 'Maps a value from [min, max] to [0.0, 1.0]. Useful for HP percent, distance fade, '
                                 'intensity curves. Data inputs: value (number, default=0), min (number, default=0), '
                                 'max (number, default=100). Data outputs: normalized (number). Settings: min_val, '
                                 'max_val. This is a pure data node: wire its colored output directly into another '
                                 'input; no white execution wire is required.'},
 'math_percent_change': {'example': '1. Add Percent Change from the Math category.\n'
                                    '2. Connect old, new.\n'
                                    '3. Use result in the next calculation or condition.',
                         'tip': 'Returns percentage change from Old to New. Data inputs: old (number, default=0), '
                                'new (number, default=0). Data outputs: result (number). This is a pure data node: '
                                'wire its colored output directly into another input; no white execution wire is '
                                'required.'},
 'math_percent_of': {'example': '1. Add Percent Of from the Math category.\n'
                                '2. Connect base, percent.\n'
                                '3. Use result in the next calculation or condition.',
                     'tip': 'Returns Percent percent of Base. Data inputs: base (number, default=100), percent '
                            '(number, default=50). Data outputs: result (number). This is a pure data node: wire its '
                            'colored output directly into another input; no white execution wire is required.'},
 'math_ping_pong': {'example': '1. Add Ping Pong from the Math category.\n'
                               '2. Connect value, min, max.\n'
                               '3. Use result in the next calculation or condition.',
                    'tip': 'Bounces Value between Min and Max like a repeating triangle wave. Data inputs: value '
                           '(number, default=0), min (number, default=0), max (number, default=1). Data outputs: '
                           'result (number). This is a pure data node: wire its colored output directly into another '
                           'input; no white execution wire is required.'},
 'math_pow': {'example': '1. Pow(2, 3) -> 8\n2. Calculate exponential growth',
              'tip': 'Returns A raised to the power of B.'},
 'math_power': {'example': '1. Distance ^ 2 -> Squared Distance\n2. 2 ^ 3 -> 8',
                'tip': 'Raises A to the power of B. Data inputs: base (number, default=1), exponent (number, '
                       'default=2). Data outputs: result (number). This is a pure data node: wire its colored output '
                       'directly into another input; no white execution wire is required.'},
 'math_product_three': {'example': '1. Add Product Three from the Math category.\n'
                                   '2. Connect a, b, c.\n'
                                   '3. Use result in the next calculation or condition.',
                        'tip': 'Multiplies A, B, and C. Data inputs: a (number, default=1), b (number, default=1), c '
                               '(number, default=1). Data outputs: result (number). This is a pure data node: wire '
                               'its colored output directly into another input; no white execution wire is '
                               'required.'},
 'math_quadratic_discriminant': {'example': '1. Add Quadratic Discriminant from the Math category.\n'
                                            '2. Connect a, b, c.\n'
                                            '3. Use discriminant in the next calculation or condition.',
                                 'tip': 'Returns B squared minus 4AC for a quadratic equation. Data inputs: a '
                                        '(number, default=1), b (number, default=0), c (number, default=0). Data '
                                        'outputs: discriminant (number). This is a pure data node: wire its colored '
                                        'output directly into another input; no white execution wire is required.'},
 'math_quadratic_root_minus': {'example': '1. Add Quadratic Root - from the Math category.\n'
                                          '2. Connect a, b, c.\n'
                                          '3. Use root in the next calculation or condition.',
                               'tip': 'Returns the negative quadratic root using A, B, and C. Data inputs: a '
                                      '(number, default=1), b (number, default=0), c (number, default=0). Data '
                                      'outputs: root (number). This is a pure data node: wire its colored output '
                                      'directly into another input; no white execution wire is required.'},
 'math_quadratic_root_plus': {'example': '1. Add Quadratic Root + from the Math category.\n'
                                         '2. Connect a, b, c.\n'
                                         '3. Use root in the next calculation or condition.',
                              'tip': 'Returns the positive quadratic root using A, B, and C. Data inputs: a (number, '
                                     'default=1), b (number, default=0), c (number, default=0). Data outputs: root '
                                     '(number). This is a pure data node: wire its colored output directly into '
                                     'another input; no white execution wire is required.'},
 'math_quantize': {'example': '1. Add Quantize from the Math category.\n'
                              '2. Connect value, step.\n'
                              '3. Use result in the next calculation or condition.',
                   'tip': 'Rounds Value to the nearest Step. Data inputs: value (number, default=0), step (number, '
                          'default=1). Data outputs: result (number). This is a pure data node: wire its colored '
                          'output directly into another input; no white execution wire is required.'},
 'math_radians': {'example': '1. Add Degrees To Radians from the Math category.\n'
                             '2. Connect degrees.\n'
                             '3. Use result in the next calculation or condition.',
                  'tip': 'Converts degrees into radians. Data inputs: degrees (number, default=0). Data outputs: '
                         'result (number). This is a pure data node: wire its colored output directly into another '
                         'input; no white execution wire is required.'},
 'math_random_float': {'example': '1. Random Float -> Check < 0.5 for 50% chance\n'
                                  '2. Random Float * 360 -> Random Angle',
                       'tip': 'Returns a random decimal number between 0.0 and 1.0 each time it is evaluated. Data '
                              'inputs: min (number, default=0), max (number, default=1). Data outputs: value '
                              '(number). This is a pure data node: wire its colored output directly into another '
                              'input; no white execution wire is required.'},
 'math_random_int': {'example': '1. Random Int(1, 10) -> Loot Drop Table\n2. Random Int(10, 20) -> Base Damage',
                     'tip': 'Returns a random whole number between Min and Max (inclusive). Data inputs: min '
                            '(number, default=0), max (number, default=10). Data outputs: value (number). This is a '
                            'pure data node: wire its colored output directly into another input; no white execution '
                            'wire is required.'},
 'math_reciprocal': {'example': '1. Add Reciprocal from the Math category.\n'
                                '2. Connect value.\n'
                                '3. Use result in the next calculation or condition.',
                     'tip': 'Returns 1 divided by Value, safely returning 0 for zero. Data inputs: value (number, '
                            'default=1). Data outputs: result (number). This is a pure data node: wire its colored '
                            'output directly into another input; no white execution wire is required.'},
 'math_remap': {'example': '1. HP 0-100 → scale 0.5-2.0\n2. Distance 50-200 → opacity 1.0-0.0',
                'tip': 'Maps a value from one range [in_min, in_max] to another [out_min, out_max]. Like Godot '
                       'remap() — e.g. distance 0-300 -> volume 1.0-0.0. Data inputs: value (number, default=0), '
                       'in_min (number, default=0), in_max (number, default=100), out_min (number, default=0), '
                       'out_max (number, default=1). Data outputs: result (number). Settings: in_min, in_max, '
                       'out_min, out_max. This is a pure data node: wire its colored output directly into another '
                       'input; no white execution wire is required.'},
 'math_remap_clamped': {'example': '1. Add Remap Clamped from the Math category.\n'
                                   '2. Connect value, in_min, in_max.\n'
                                   '3. Use result in the next calculation or condition.',
                        'tip': 'Maps Value from one range to another and clamps the result. Data inputs: value '
                               '(number, default=0), in_min (number, default=0), in_max (number, default=1), out_min '
                               '(number, default=0), out_max (number, default=1). Data outputs: result (number). '
                               'This is a pure data node: wire its colored output directly into another input; no '
                               'white execution wire is required.'},
 'math_rotate_vector': {'example': '1. Forward + rotate 45° → diagonal slash\n'
                                   '2. Loop 0-360 step 30° → ring of projectiles',
                        'tip': 'Rotates a direction vector by N degrees clockwise. Use to offset aim, create spiral '
                               'patterns, or rotate a cone direction. Data inputs: vector (vector, default=(1, 0)), '
                               'degrees (number, default=45). Data outputs: rotated (vector). Settings: degrees. '
                               'This is a pure data node: wire its colored output directly into another input; no '
                               'white execution wire is required.'},
 'math_round': {'example': '1. Round(2.5) -> 3\n2. Round(Damage) -> Clean Combat Text',
                'tip': 'Rounds to the nearest whole integer. 2.5 becomes 3. Data inputs: value (number, default=0). '
                       'Data outputs: result (number). This is a pure data node: wire its colored output directly '
                       'into another input; no white execution wire is required.'},
 'math_round_digits': {'example': '1. Add Round Digits from the Math category.\n'
                                  '2. Connect value, digits.\n'
                                  '3. Use result in the next calculation or condition.',
                       'tip': 'Rounds Value to a chosen number of decimal Digits. Data inputs: value (number, '
                              'default=0), digits (number, default=2). Data outputs: result (number). This is a pure '
                              'data node: wire its colored output directly into another input; no white execution '
                              'wire is required.'},
 'math_select_number': {'example': '1. Add Select Number from the Math category.\n'
                                   '2. Connect condition, a, b.\n'
                                   '3. Use value in the next calculation or condition.',
                        'tip': 'Returns A when Condition is true, otherwise B. Data inputs: condition (boolean, '
                               'default=True), a (number, default=1), b (number, default=0). Data outputs: value '
                               '(number). This is a pure data node: wire its colored output directly into another '
                               'input; no white execution wire is required.'},
 'math_sign': {'example': '1. Sign of velocity.x -> face left or right\n2. Sign of HP delta -> gained or lost HP',
               'tip': 'Returns 1 if the number is positive, -1 if negative, 0 if zero. Data inputs: value (number, '
                      'default=0). Data outputs: sign (number). This is a pure data node: wire its colored output '
                      'directly into another input; no white execution wire is required.'},
 'math_sign_match': {'example': '1. Add Sign Match from the Math category.\n'
                                '2. Connect a, b.\n'
                                '3. Use match in the next calculation or condition.',
                     'tip': 'Returns 1 when A and B share a sign, otherwise -1. Data inputs: a (number, default=1), '
                            'b (number, default=1). Data outputs: match (number). This is a pure data node: wire its '
                            'colored output directly into another input; no white execution wire is required.'},
 'math_sin': {'example': '1. Hovering effects\n2. Circular movement', 'tip': 'Returns the sine of A (in radians).'},
 'math_sine': {'example': '1. Sine(Time) -> Bobbing Motion\n2. Sine(Angle) -> Y Vector',
               'tip': 'Returns the sine of an angle in degrees. Great for wave motion, bobbing, oscillation. Data '
                      'inputs: value (number, default=0). Data outputs: result (number). This is a pure data node: '
                      'wire its colored output directly into another input; no white execution wire is required.'},
 'math_slope': {'example': '1. Add Slope from the Math category.\n'
                           '2. Connect x1, y1, x2.\n'
                           '3. Use slope in the next calculation or condition.',
                'tip': 'Solves rise over run: (Y2 - Y1) / (X2 - X1). Data inputs: x1 (number, default=0), y1 '
                       '(number, default=0), x2 (number, default=1), y2 (number, default=1). Data outputs: slope '
                       '(number). This is a pure data node: wire its colored output directly into another input; no '
                       'white execution wire is required.'},
 'math_smoothstep': {'example': '1. Smoothstep time 0-1 → scale for spawn pop\n2. Smooth HP bar fill animation',
                     'tip': 'Returns a smooth ease curve between 0 and 1, given an edge0, edge1, and input value. '
                            'Faster than lerp for natural-feeling transitions. Data inputs: value (number, '
                            'default=0.5), edge0 (number, default=0), edge1 (number, default=1). Data outputs: '
                            'result (number). Settings: edge0, edge1. This is a pure data node: wire its colored '
                            'output directly into another input; no white execution wire is required.'},
 'math_snap': {'example': '1. Add Snap With Offset from the Math category.\n'
                          '2. Connect value, step, offset.\n'
                          '3. Use result in the next calculation or condition.',
               'tip': 'Snaps Value to Step intervals starting at Offset. Data inputs: value (number, default=0), '
                      'step (number, default=1), offset (number, default=0). Data outputs: result (number). This is '
                      'a pure data node: wire its colored output directly into another input; no white execution '
                      'wire is required.'},
 'math_solve_linear': {'example': '1. Add Solve Linear from the Math category.\n'
                                  '2. Connect a, b, c.\n'
                                  '3. Use x in the next calculation or condition.',
                       'tip': 'Solves A times X plus B equals C for X. Data inputs: a (number, default=1), b '
                              '(number, default=0), c (number, default=1). Data outputs: x (number). This is a pure '
                              'data node: wire its colored output directly into another input; no white execution '
                              'wire is required.'},
 'math_solve_proportion': {'example': '1. Add Solve Proportion from the Math category.\n'
                                      '2. Connect a, b, c.\n'
                                      '3. Use x in the next calculation or condition.',
                           'tip': 'Solves A / B equals C / X for X. Data inputs: a (number, default=1), b (number, '
                                  'default=1), c (number, default=1). Data outputs: x (number). This is a pure data '
                                  'node: wire its colored output directly into another input; no white execution '
                                  'wire is required.'},
 'math_spring_damper': {'example': '1. Add Spring Damper from the Math category.\n'
                                   '2. Connect current, target, damping.\n'
                                   '3. Use value in the next calculation or condition.',
                        'tip': 'Moves Current toward Target using Damping over dt. Data inputs: current (number, '
                               'default=0), target (number, default=1), damping (number, default=5), dt (number, '
                               'default=0.016). Data outputs: value (number). This is a pure data node: wire its '
                               'colored output directly into another input; no white execution wire is required.'},
 'math_sqrt': {'example': '1. Sqrt(Squared Distance) -> Actual Distance\n2. Sqrt(9) -> 3',
               'tip': 'Returns the square root of a number. Data inputs: value (number, default=1). Data outputs: '
                      'result (number). This is a pure data node: wire its colored output directly into another '
                      'input; no white execution wire is required.'},
 'math_square': {'example': '1. Add Square from the Math category.\n'
                            '2. Connect value.\n'
                            '3. Use result in the next calculation or condition.',
                 'tip': 'Returns Value squared. Data inputs: value (number, default=0). Data outputs: result '
                        '(number). This is a pure data node: wire its colored output directly into another input; no '
                        'white execution wire is required.'},
 'math_stddev_two': {'example': '1. Add Std Dev Two from the Math category.\n'
                                '2. Connect a, b.\n'
                                '3. Use stddev in the next calculation or condition.',
                     'tip': 'Population standard deviation for two samples. Data inputs: a (number, default=0), b '
                            '(number, default=0). Data outputs: stddev (number). This is a pure data node: wire its '
                            'colored output directly into another input; no white execution wire is required.'},
 'math_step': {'example': '1. Add Step from the Math category.\n'
                          '2. Connect value, edge.\n'
                          '3. Use result in the next calculation or condition.',
               'tip': 'Returns 1 when Value is at least Edge, otherwise 0. Data inputs: value (number, default=0), '
                      'edge (number, default=0). Data outputs: result (number). This is a pure data node: wire its '
                      'colored output directly into another input; no white execution wire is required.'},
 'math_subtract': {'example': '1. Max HP - Current HP -> Healing Needed\n2. Variable - 1 -> Set Variable',
                   'tip': 'Subtracts B from A. A - B. Data inputs: a (number, default=0), b (number, default=0). '
                          'Data outputs: result (number). This is a pure data node: wire its colored output directly '
                          'into another input; no white execution wire is required.'},
 'math_sum_three': {'example': '1. Add Sum Three from the Math category.\n'
                               '2. Connect a, b, c.\n'
                               '3. Use result in the next calculation or condition.',
                    'tip': 'Adds A, B, and C. Data inputs: a (number, default=0), b (number, default=0), c (number, '
                           'default=0). Data outputs: result (number). This is a pure data node: wire its colored '
                           'output directly into another input; no white execution wire is required.'},
 'math_tan': {'example': '1. Mathematical waves\n2. Advanced geometry',
              'tip': 'Returns the tangent of A (in radians).'},
 'math_tangent': {'example': '1. Add Tangent from the Math category.\n'
                             '2. Connect angle.\n'
                             '3. Use result in the next calculation or condition.',
                  'tip': 'Tangent of Angle in radians. Data inputs: angle (number, default=0). Data outputs: result '
                         '(number). This is a pure data node: wire its colored output directly into another input; '
                         'no white execution wire is required.'},
 'math_to_boolean': {'example': '1. 0 -> False. 1 -> True\n2. String "True" -> Boolean True',
                     'tip': 'Converts a number or string to True/False. 0, empty string, and "false"/"no"/"off" all '
                            'become False; anything else becomes True. Data inputs: value (any). Data outputs: '
                            'boolean (boolean). This is a pure data node: wire its colored output directly into '
                            'another input; no white execution wire is required.'},
 'math_to_integer': {'example': '1. Add To Integer from the Math category.\n'
                                '2. Connect value.\n'
                                '3. Use integer in the next calculation or condition.',
                     'tip': "Converts a string, float, or boolean to a whole number (rounded). '12.7' becomes 13. "
                            'Data inputs: value (any). Data outputs: integer (number). This is a pure data node: '
                            'wire its colored output directly into another input; no white execution wire is '
                            'required.'},
 'math_to_number': {'example': '1. "True" -> 1.0. "False" -> 0.0. "50" -> 50.0\n2. String "100" -> Number 100',
                    'tip': "Converts a string or boolean to a number. '50' becomes 50, True becomes 1. Data inputs: "
                           'value (any). Data outputs: number (number). This is a pure data node: wire its colored '
                           'output directly into another input; no white execution wire is required.'},
 'math_to_number_default': {'example': '1. Add To Number (With Default) from the Math category.\n'
                                       '2. Connect value.\n'
                                       '3. Use number in the next calculation or condition.',
                            'tip': 'Same as To Number, but you choose what fallback value to use when the input '
                                   "can't be converted, instead of always falling back to 0. Data inputs: value "
                                   '(any). Data outputs: number (number). Settings: default. This is a pure data '
                                   'node: wire its colored output directly into another input; no white execution '
                                   'wire is required.'},
 'math_to_percent': {'example': '1. Add To Percent from the Math category.\n'
                                '2. Connect value, whole.\n'
                                '3. Use result in the next calculation or condition.',
                     'tip': 'Converts Value / Whole into a percentage. Data inputs: value (number, default=0), whole '
                            '(number, default=100). Data outputs: result (number). This is a pure data node: wire '
                            'its colored output directly into another input; no white execution wire is required.'},
 'math_to_string': {'example': '1. 50.5 -> "50.5"\n2. HP -> To String -> Print To Screen',
                    'tip': "Converts a number or boolean to a text string. 50 becomes '50'. Data inputs: value "
                           '(any). Data outputs: string (string). This is a pure data node: wire its colored output '
                           'directly into another input; no white execution wire is required.'},
 'math_truncate': {'example': '1. Add Truncate from the Math category.\n'
                              '2. Connect value.\n'
                              '3. Use result in the next calculation or condition.',
                   'tip': 'Drops the decimal portion of Value toward zero. Data inputs: value (number, default=0). '
                          'Data outputs: result (number). This is a pure data node: wire its colored output directly '
                          'into another input; no white execution wire is required.'},
 'math_variance_two': {'example': '1. Add Variance Two from the Math category.\n'
                                  '2. Connect a, b.\n'
                                  '3. Use variance in the next calculation or condition.',
                       'tip': 'Population variance for two samples. Data inputs: a (number, default=0), b (number, '
                              'default=0). Data outputs: variance (number). This is a pure data node: wire its '
                              'colored output directly into another input; no white execution wire is required.'},
 'math_vector_dot': {'example': '1. Check if facing target (Dot > 0)\n2. Physics reflection',
                     'tip': 'Returns the dot product of two vectors. Data inputs: A (vector), B (vector). Data '
                            'outputs: Dot (number). This is a pure data node: wire its colored output directly into '
                            'another input; no white execution wire is required.'},
 'math_vector_length': {'example': '1. Velocity -> Vector Length -> Speed (Number)\n2. Check exact distance',
                        'tip': 'Returns the magnitude of the vector. Data inputs: Vector (vector). Data outputs: '
                               'Length (number). This is a pure data node: wire its colored output directly into '
                               'another input; no white execution wire is required.'},
 'math_vector_normalize': {'example': '1. Velocity -> Normalize -> Move Direction\n2. Calculate look direction',
                           'tip': 'Returns the vector with length 1. Data inputs: Vector (vector). Data outputs: '
                                  'Normal (vector). This is a pure data node: wire its colored output directly into '
                                  'another input; no white execution wire is required.'},
 'math_vector_rotate': {'example': '1. Rotate Velocity by 90 deg -> Orbit motion\n2. Spread projectiles',
                        'tip': 'Rotates a vector by degrees.'},
 'math_weighted_average': {'example': '1. Add Weighted Average from the Math category.\n'
                                      '2. Connect a, b, weight.\n'
                                      '3. Use result in the next calculation or condition.',
                           'tip': 'Blends A toward B by Weight: 0 = A, 1 = B. Data inputs: a (number, default=0), b '
                                  '(number, default=1), weight (number, default=0.5). Data outputs: result (number). '
                                  'This is a pure data node: wire its colored output directly into another input; no '
                                  'white execution wire is required.'},
 'math_wrap': {'example': '1. Add Wrap from the Math category.\n'
                          '2. Connect value, min, max.\n'
                          '3. Use result in the next calculation or condition.',
               'tip': 'Wraps Value into the inclusive Min/Max range. Data inputs: value (number, default=0), min '
                      '(number, default=0), max (number, default=1). Data outputs: result (number). This is a pure '
                      'data node: wire its colored output directly into another input; no white execution wire is '
                      'required.'},
 'mem_8bit_reg': {'example': '1. Byte-level memory',
                  'tip': 'Stores an 8-bit integer. Execution input: exec. Execution output: exec. Data inputs: Data '
                         '(number), Load (boolean). Data outputs: Out (number). Use the white execution path for '
                         'ordering and the colored pins for values.'},
 'mem_clear': {'example': '1. Reset system',
               'tip': 'Wipes the entire global memory dictionary. Execution input: exec. Execution output: exec. Use '
                      'the white execution path for ordering and the colored pins for values.'},
 'mem_d_latch': {'example': '1. Sample position when attacked',
                 'tip': 'Data Latch. Stores data when Enable is True. Execution input: exec. Execution output: exec. '
                        'Data inputs: Data (any), Enable (boolean). Data outputs: Q (any). Use the white execution '
                        'path for ordering and the colored pins for values.'},
 'mem_jk_flipflop': {'example': '1. Complex toggling logic',
                     'tip': 'JK Flip-Flop state machine. Execution input: exec. Execution output: exec. Data inputs: '
                            'J (boolean), K (boolean). Data outputs: Q (boolean). Use the white execution path for '
                            'ordering and the colored pins for values.'},
 'mem_read': {'example': '1. Read High Score',
              'tip': 'Reads a value from a global memory address. Data inputs: Address (string). Data outputs: Value '
                     '(any).'},
 'mem_sr_latch': {'example': '1. Toggle boss mode permanently',
                  'tip': 'Set-Reset Latch. Stores a boolean state. Execution input: exec. Execution output: exec. '
                         'Data inputs: Set (boolean), Reset (boolean). Data outputs: Q (boolean). Use the white '
                         'execution path for ordering and the colored pins for values.'},
 'mem_t_flipflop': {'example': '1. Toggle light on/off',
                    'tip': 'Toggle Flip-Flop. Flips state on execution if T is True. Execution input: exec. '
                           'Execution output: exec. Data inputs: T (boolean). Data outputs: Q (boolean). Use the '
                           'white execution path for ordering and the colored pins for values.'},
 'mem_write': {'example': '1. Write High Score',
               'tip': 'Writes a value to a global memory address. Execution input: exec. Execution output: exec. '
                      'Data inputs: Address (string), Value (any). Use the white execution path for ordering and the '
                      'colored pins for values.'},
 'movement_clamp_position': {'example': '1. Keep a boss locked in the center 500x500 area\n'
                                        '2. Clamp Position to Arena Bounds',
                             'tip': 'Prevents a character from leaving a defined rectangular boundary area. '
                                    'Execution input: exec. Execution output: exec. Data inputs: min (vector), max '
                                    '(vector). Use the white execution path for ordering and the colored pins for '
                                    'values.'},
 'movement_dash_to_position': {'example': '1. Evade attacks by dashing to "Random Point In Radius"\n'
                                          '2. Dash To Target (0.2s) -> Melee Attack',
                               'tip': 'High-speed instant translation to a position, bypassing normal speed limits. '
                                      'Execution input: exec. Execution output: exec. Data inputs: target (vector), '
                                      'duration (number, default=0.3). Settings: duration. Use the white execution '
                                      'path for ordering and the colored pins for values.'},
 'movement_face_target': {'example': '1. Useful before firing a directional projectile\n'
                                     '2. Face Target -> Damage Cone',
                          'tip': "Snaps the character's movement direction toward a target without actually moving "
                                 'forward. Execution input: exec. Execution output: exec. Data inputs: target '
                                 '(vector). Use the white execution path for ordering and the colored pins for '
                                 'values.'},
 'movement_follow_path': {'example': '1. Patrol routing: Follow Path [Point A, Point B]\n'
                                     '2. Follow Path (Loop = True)',
                          'tip': 'Walks the character through an ordered list of world positions in sequence. '
                                 'Execution input: exec. Execution output: exec. Data inputs: path (any), speed '
                                 '(number, default=150). Settings: speed, loop. Use the white execution path for '
                                 'ordering and the colored pins for values.'},
 'movement_freeze': {'example': '1. Ice spike hit -> Freeze for 2s\n2. Boss stomp -> Freeze all nearby for 1s',
                     'tip': "Instantly zeroes this character's velocity and applies a root status for the given "
                            'duration, preventing all movement. Execution input: exec. Execution output: exec. Data '
                            'inputs: target (object), duration (number, default=1.5). Settings: duration. Use the '
                            'white execution path for ordering and the colored pins for values.'},
 'movement_get_speed': {'example': '1. Get Speed -> current_speed -> Compare > 300 -> Branch\n'
                                   '2. Get Speed -> max_speed -> Format String -> Print',
                        'tip': "Returns the character's current movement speed as a number, plus separate max_speed "
                               'and min_speed caps. Use with Compare Number to react when a character is going too '
                               'fast or too slow. Data inputs: target (object). Data outputs: current_speed '
                               '(number), max_speed (number), min_speed (number).'},
 'movement_move_away': {'example': '1. Flee behavior: Move Away From Target (Speed 300)\n2. HP < 20% -> Move Away',
                        'tip': 'Applies a steering force moving the character away from a target position. Execution '
                               'input: exec. Execution output: exec. Data inputs: target (vector), speed (number, '
                               'default=150). Settings: speed. Use the white execution path for ordering and the '
                               'colored pins for values.'},
 'movement_move_toward': {'example': '1. Move Toward -> Target Position (Speed 200)\n2. Move Toward -> Nearest Enemy',
                          'tip': 'Applies a steering force moving the character toward a target position at a set '
                                 'speed. Execution input: exec. Execution output: exec. Data inputs: target '
                                 '(vector), speed (number, default=150). Settings: speed. Use the white execution '
                                 'path for ordering and the colored pins for values.'},
 'movement_orbit': {'example': '1. Swarm behavior: Orbit summoner at 100 range\n2. Orbit Boss (Speed 150)',
                    'tip': 'Forces the character to circle around a point at a given radius and speed. Execution '
                           'input: exec. Execution output: exec. Data inputs: target (vector), radius (number, '
                           'default=100), speed (number, default=150). Settings: radius, speed, clockwise. Use the '
                           'white execution path for ordering and the colored pins for values.'},
 'movement_pathfind_to': {'example': '1. Pathfind to boss position while avoiding allies\n'
                                     '2. Zombie horde steering toward nearest player',
                          'tip': 'Moves toward a target while avoiding other characters (simple steering: moves '
                                 'toward goal, steers around blockers within avoidance_radius). Not full A* but '
                                 'effective for arena crowds. Execution input: exec. Execution output: exec, '
                                 'arrived. Data inputs: source (object), goal (object), speed (number, default=150), '
                                 'avoidance_radius (number, default=40). Settings: speed, avoidance_radius. Use the '
                                 'white execution path for ordering and the colored pins for values.'},
 'movement_random_wander': {'example': '1. Idle behavior: Random Wander (radius 200)\n2. If Is Idle -> Random Wander',
                            'tip': 'Smoothly wanders around randomly within a radius. Good for idle and patrol '
                                   'behavior. Execution input: exec. Execution output: exec. Data inputs: center '
                                   '(vector), radius (number, default=200), speed (number, default=100). Settings: '
                                   'radius, speed. Use the white execution path for ordering and the colored pins '
                                   'for values.'},
 'movement_set_speed_limits': {'example': '1. On Spawn -> Set Speed Limits (max=250, min=80) — always moving, never '
                                          'too fast\n'
                                          '2. On Rage -> Set Speed Limits (max=500) — unlock higher speed for boss '
                                          'phase',
                               'tip': 'Sets a per-character minimum and maximum speed cap. The engine enforces these '
                                      'every frame — no script can push the character faster than max_speed or '
                                      'slower than min_speed (unless it is completely stopped). Call on On Spawn to '
                                      "lock a character's speed range permanently, or at any time to change it "
                                      'mid-fight. Execution input: exec. Execution output: exec. Data inputs: target '
                                      '(object), max_speed (number, default=300), min_speed (number, default=0). '
                                      'Settings: max_speed, min_speed. Use the white execution path for ordering and '
                                      'the colored pins for values.'},
 'net_dec_b64': {'example': '1. Fake packet decode',
                 'tip': 'Simulates base64 decoding (string reversal). Data inputs: Encoded (string). Data outputs: '
                        'String (string).'},
 'net_dec_str': {'example': '1. Read secure text',
                 'tip': 'Simulates simple Caesar cipher decryption. Data inputs: Cipher (string), Key (number). Data '
                        'outputs: String (string).'},
 'net_demux': {'example': '1. Value splitter',
               'tip': 'Routes one input to two outputs. Non-selected is None. Data inputs: In (any), Select B '
                      '(boolean). Data outputs: Out A (any), Out B (any).'},
 'net_enc_b64': {'example': '1. Fake packet encode',
                 'tip': 'Simulates base64 encoding (string reversal). Data inputs: String (string). Data outputs: '
                        'Encoded (string).'},
 'net_enc_str': {'example': '1. Secure text',
                 'tip': 'Simulates simple Caesar cipher encryption. Data inputs: String (string), Key (number). Data '
                        'outputs: Cipher (string).'},
 'net_hash': {'example': '1. Checksums',
              'tip': 'Returns a fast hash integer of a string. Data inputs: Payload (string). Data outputs: Hash '
                     '(number).'},
 'net_mux': {'example': '1. Conditional routing',
             'tip': 'Selects between two inputs based on a boolean. Data inputs: A (any), B (any), Select B '
                    '(boolean). Data outputs: Out (any).'},
 'net_pack': {'example': '1. Byte construction',
              'tip': 'Packs 8 booleans into a single 8-bit integer. Data inputs: b0 (boolean), b1 (boolean), b2 '
                     '(boolean), b3 (boolean), b4 (boolean), b5 (boolean), b6 (boolean), b7 (boolean). Data outputs: '
                     'Byte (number).'},
 'net_router': {'example': '1. Switch statement',
                'tip': 'Routes execution to 1 of 4 paths based on an index. Execution input: exec. Execution output: '
                       'Port 0, Port 1, Port 2, Port 3. Data inputs: Port (number). Use the white execution path for '
                       'ordering and the colored pins for values.'},
 'net_unpack': {'example': '1. Bit reading',
                'tip': 'Unpacks an 8-bit integer into 8 booleans. Data inputs: Byte (number).'},
 'node_cluster_formation': {'example': '1. Add Node Cluster Formation from the Blueprint Tools category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Type a plain-language idea, then build an editable mockup cluster below this '
                                   'node.  The local parser recognizes conditions, comparisons, constants, print/log '
                                   'actions,  else branches, assignments, damage/heal, waits, and multi-step '
                                   'statements; unknown  parts become Comment nodes instead of silently '
                                   'disappearing.'},
 'nuc_coolant_pump': {'example': '1. Chill reactor',
                      'tip': 'Sets coolant flow rate. Execution input: exec. Execution output: exec. Data inputs: '
                             'Flow Rate (number). Use the white execution path for ordering and the colored pins for '
                             'values.'},
 'nuc_core_temp': {'example': '1. Drive turbines',
                   'tip': 'Calculates reactor temp based on rods and coolant. Data outputs: Temp (C) (number).'},
 'nuc_isotope': {'example': '1. Radiation source',
                 'tip': 'Simulates radioactive half-life. Execution input: exec. Execution output: exec. Data '
                        'outputs: Mass (number). Use the white execution path for ordering and the colored pins for '
                        'values.'},
 'nuc_meltdown': {'example': '1. Explosion',
                  'tip': 'Triggers catastrophic destruction if integrity is 0. Execution input: exec. Execution '
                         'output: Normal, BOOM. Data inputs: Integrity % (number). Use the white execution path for '
                         'ordering and the colored pins for values.'},
 'nuc_radiation': {'example': '1. Damage aura',
                   'tip': 'Outputs lethal damage over time based on Shield Integrity. Data inputs: Integrity % '
                          '(number). Data outputs: Rad Damage (number).'},
 'nuc_rod_actuator': {'example': '1. Throttle reactor',
                      'tip': 'Sets insertion depth of rods (0-100%). Execution input: exec. Execution output: exec. '
                             'Data inputs: Insertion % (number). Use the white execution path for ordering and the '
                             'colored pins for values.'},
 'nuc_scram': {'example': '1. Panic button',
               'tip': 'Emergency shutdown, fully inserts rods. Execution input: exec. Execution output: exec. Use '
                      'the white execution path for ordering and the colored pins for values.'},
 'nuc_shield': {'example': '1. Health check',
                'tip': 'Integrity drops if Temp > 1000C. Execution input: exec. Execution output: exec. Data inputs: '
                       'Temp (C) (number). Data outputs: Integrity % (number). Use the white execution path for '
                       'ordering and the colored pins for values.'},
 'nuc_stabilize': {'example': '1. Engineering team',
                   'tip': 'Repairs the shield slowly. Execution input: exec. Execution output: exec. Use the white '
                          'execution path for ordering and the colored pins for values.'},
 'nuc_turbine': {'example': '1. Megawatts out',
                 'tip': 'Generates electricity from reactor temp. Data inputs: Temp (C) (number). Data outputs: '
                        'Megawatts (number).'},
 'parameter_animation': {'example': '1. Create "AttackAnim" param -> Play Animation\n'
                                    '2. Allows one script for multiple classes',
                         'tip': 'Exposes an Animation Library picker in the character Traits section. Data outputs: '
                                'value (string). Settings: name, default.'},
 'parameter_boolean': {'example': '1. Create "IsFire" param -> Branch\n2. Create "CanFly"',
                       'tip': 'Exposes a True/False checkbox in the Character Traits panel. Data outputs: value '
                              '(boolean). Settings: name, default.'},
 'parameter_color': {'example': '1. Create "AuraColor" -> Tint Character\n2. Custom particle color',
                     'tip': 'Exposes a color picker in the Character Traits panel. Data outputs: value (color). '
                            'Settings: name, color.'},
 'parameter_number': {'example': '1. Create "DashSpeed" param -> Plug into Dash node\n2. Custom "DamageMult"',
                      'tip': 'Exposes a numeric slider in the Character Traits panel so you can tune it '
                             'per-character without editing the script. Data outputs: value (number). Settings: '
                             'name, default.'},
 'parameter_text': {'example': '1. Create "MinionName" param -> Spawn Swarm\n2. Custom Tag Name',
                    'tip': 'Exposes a text field in the Character Traits panel. Data outputs: value (string). '
                           'Settings: name, default.'},
 'perf_every_n_ticks': {'example': '1. Add Every N Ticks Gate from the Performance category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Performance gate: only continue once every N executions. Great for expensive checks '
                               'on Tick.'},
 'perf_random_chance_gate': {'example': '1. Add Random Chance Gate from the Performance category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Performance/randomness gate: run a branch only with a percentage chance.'},
 'phys_get_velocity_dir': {'example': '1. Get Velocity Dir -> Spawn Trail Particles behind\n'
                                      '2. Rotate sprite to match',
                           'tip': 'Returns the normalized direction of movement. Data inputs: Character (object). '
                                  'Data outputs: Direction (vector).'},
 'phys_set_max_speed': {'example': '1. On Sprint -> Set Speed (400)\n2. On Stun -> Set Speed (50)',
                        'tip': "Changes the character's base speed stat. Execution input: exec. Execution output: "
                               'exec. Data inputs: Character (object), Speed (number). Use the white execution path '
                               'for ordering and the colored pins for values.'},
 'phys_teleport': {'example': '1. On Hit -> Teleport to Random Range\n2. Teleport to Portal node',
                   'tip': 'Instantly moves a character to a position. Execution input: exec. Execution output: exec. '
                          'Data inputs: Character (object), Position (vector). Use the white execution path for '
                          'ordering and the colored pins for values.'},
 'physics_accelerate': {'example': '1. Add Accelerate from the Physics category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Add acceleration over a supplied time step.'},
 'physics_add_position': {'example': '1. Add Add Position from the Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Move the character by an X,Y offset.'},
 'physics_add_velocity': {'example': '1. Add Add Velocity from the Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Add X and Y to current velocity.'},
 'physics_apply_force': {'example': '1. Add Apply Force from the Physics category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Add a force vector to velocity.'},
 'physics_apply_gravity': {'example': '1. Add Apply Gravity Once from the Physics category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Apply an immediate vertical gravity impulse.'},
 'physics_apply_impulse': {'example': '1. Add Apply Impulse from the Physics category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Add an instantaneous mass-aware impulse.'},
 'physics_apply_traction': {'example': '1. Add Apply Traction from the Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Reduce sliding with friction-like traction.'},
 'physics_apply_wind': {'example': '1. Add Apply Wind from the Physics category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Apply a persistent-style wind impulse.'},
 'physics_body_add_central_force': {'example': '1. Add Add Central Force from the Physics category.\n'
                                               '2. Connect the available inputs.\n'
                                               '3. Use the output in the next calculation or condition.',
                                    'tip': 'Apply force through the center of mass.'},
 'physics_body_add_force_at_position': {'example': '1. Add Add Force At Position from the Physics category.\n'
                                                   '2. Connect the available inputs.\n'
                                                   '3. Use the output in the next calculation or condition.',
                                        'tip': 'Apply force at an offset to create rotation.'},
 'physics_body_add_torque': {'example': '1. Add Add Torque from the Physics category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Apply rotational force.'},
 'physics_body_apply_torque_impulse': {'example': '1. Add Apply Torque Impulse from the Physics category.\n'
                                                  '2. Connect the available inputs.\n'
                                                  '3. Use the output in the next calculation or condition.',
                                       'tip': 'Instantly spin the body.'},
 'physics_body_force_awake': {'example': '1. Add Force Awake from the Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Wake a body before applying a force.'},
 'physics_body_freeze_all': {'example': '1. Add Freeze All Axes from the Physics category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Freeze translation and rotation.'},
 'physics_body_freeze_position_x': {'example': '1. Add Freeze X Position from the Physics category.\n'
                                               '2. Connect the available inputs.\n'
                                               '3. Use the output in the next calculation or condition.',
                                    'tip': 'Lock horizontal translation.'},
 'physics_body_freeze_position_y': {'example': '1. Add Freeze Y Position from the Physics category.\n'
                                               '2. Connect the available inputs.\n'
                                               '3. Use the output in the next calculation or condition.',
                                    'tip': 'Lock vertical translation.'},
 'physics_body_freeze_rotation': {'example': '1. Add Freeze Rotation from the Physics category.\n'
                                             '2. Connect the available inputs.\n'
                                             '3. Use the output in the next calculation or condition.',
                                  'tip': 'Prevent rotation while preserving translation.'},
 'physics_body_get_material': {'example': '1. Add Get Physics Material from the Physics category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Read active material settings.'},
 'physics_body_limit_angular_speed': {'example': '1. Add Limit Angular Speed from the Physics category.\n'
                                                 '2. Connect the available inputs.\n'
                                                 '3. Use the output in the next calculation or condition.',
                                      'tip': 'Clamp rotational speed.'},
 'physics_body_limit_speed': {'example': '1. Add Limit Speed from the Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Clamp total linear speed.'},
 'physics_body_pull_to_point': {'example': '1. Add Pull To Point from the Physics category.\n'
                                           '2. Connect the available inputs.\n'
                                           '3. Use the output in the next calculation or condition.',
                                'tip': 'Apply radial force toward a point.'},
 'physics_body_push_from_point': {'example': '1. Add Push From Point from the Physics category.\n'
                                             '2. Connect the available inputs.\n'
                                             '3. Use the output in the next calculation or condition.',
                                  'tip': 'Apply radial force away from a point.'},
 'physics_body_reset_forces': {'example': '1. Add Reset Forces from the Physics category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Clear accumulated forces and torque.'},
 'physics_body_reset_physics_state': {'example': '1. Add Reset Physics State from the Physics category.\n'
                                                 '2. Connect the available inputs.\n'
                                                 '3. Use the output in the next calculation or condition.',
                                      'tip': 'Restore velocity, forces, and grounded flags.'},
 'physics_body_set_angular_damp_mode': {'example': '1. Add Set Angular Damp Mode from the Physics category.\n'
                                                   '2. Connect the available inputs.\n'
                                                   '3. Use the output in the next calculation or condition.',
                                        'tip': 'Choose body/world angular damping.'},
 'physics_body_set_angular_velocity': {'example': '1. Add Set Angular Velocity from the Physics category.\n'
                                                  '2. Connect the available inputs.\n'
                                                  '3. Use the output in the next calculation or condition.',
                                       'tip': 'Set rotational velocity.'},
 'physics_body_set_axis_lock': {'example': '1. Add Set Axis Lock from the Physics category.\n'
                                           '2. Connect the available inputs.\n'
                                           '3. Use the output in the next calculation or condition.',
                                'tip': 'Set a named translation/rotation axis lock.'},
 'physics_body_set_axis_lock_mask': {'example': '1. Add Set Axis Lock Mask from the Physics category.\n'
                                                '2. Connect the available inputs.\n'
                                                '3. Use the output in the next calculation or condition.',
                                     'tip': 'Set multiple axis locks from a mask.'},
 'physics_body_set_axis_velocity': {'example': '1. Add Set Axis Velocity from the Physics category.\n'
                                               '2. Connect the available inputs.\n'
                                               '3. Use the output in the next calculation or condition.',
                                    'tip': 'Replace velocity along one axis.'},
 'physics_body_set_body_priority': {'example': '1. Add Set Body Priority from the Physics category.\n'
                                               '2. Connect the available inputs.\n'
                                               '3. Use the output in the next calculation or condition.',
                                    'tip': 'Set body interaction priority.'},
 'physics_body_set_box_size': {'example': '1. Add Set Body Box Size from the Physics category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Set rectangular collision width/height.'},
 'physics_body_set_can_sleep': {'example': '1. Add Set Can Sleep from the Physics category.\n'
                                           '2. Connect the available inputs.\n'
                                           '3. Use the output in the next calculation or condition.',
                                'tip': 'Allow or prevent automatic sleeping.'},
 'physics_body_set_capsule_size': {'example': '1. Add Set Capsule Size from the Physics category.\n'
                                              '2. Connect the available inputs.\n'
                                              '3. Use the output in the next calculation or condition.',
                                   'tip': 'Set capsule radius and height.'},
 'physics_body_set_constant_force': {'example': '1. Add Set Constant Force from the Physics category.\n'
                                                '2. Connect the available inputs.\n'
                                                '3. Use the output in the next calculation or condition.',
                                     'tip': 'Apply a force continuously.'},
 'physics_body_set_constant_torque': {'example': '1. Add Set Constant Torque from the Physics category.\n'
                                                 '2. Connect the available inputs.\n'
                                                 '3. Use the output in the next calculation or condition.',
                                      'tip': 'Apply torque continuously.'},
 'physics_body_set_contact_monitor': {'example': '1. Add Set Contact Monitor from the Physics category.\n'
                                                 '2. Connect the available inputs.\n'
                                                 '3. Use the output in the next calculation or condition.',
                                      'tip': 'Enable contact tracking.'},
 'physics_body_set_custom_integrator': {'example': '1. Add Set Custom Integrator from the Physics category.\n'
                                                   '2. Connect the available inputs.\n'
                                                   '3. Use the output in the next calculation or condition.',
                                        'tip': 'Mark body for custom integration logic.'},
 'physics_body_set_density': {'example': '1. Add Set Density from the Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Set density used to derive mass.'},
 'physics_body_set_gravity_direction': {'example': '1. Add Set Gravity Direction from the Physics category.\n'
                                                   '2. Connect the available inputs.\n'
                                                   '3. Use the output in the next calculation or condition.',
                                        'tip': 'Use a custom gravity vector.'},
 'physics_body_set_gravity_override': {'example': '1. Add Set Gravity Override from the Physics category.\n'
                                                  '2. Connect the available inputs.\n'
                                                  '3. Use the output in the next calculation or condition.',
                                       'tip': 'Override world gravity for this body.'},
 'physics_body_set_inertia': {'example': '1. Add Set Inertia from the Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Set rotational inertia.'},
 'physics_body_set_linear_damp_mode': {'example': '1. Add Set Linear Damp Mode from the Physics category.\n'
                                                  '2. Connect the available inputs.\n'
                                                  '3. Use the output in the next calculation or condition.',
                                       'tip': 'Choose body/world linear damping.'},
 'physics_body_set_material': {'example': '1. Add Set Physics Material from the Physics category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Assign friction/bounce material values.'},
 'physics_body_set_max_contacts': {'example': '1. Add Set Max Contacts from the Physics category.\n'
                                              '2. Connect the available inputs.\n'
                                              '3. Use the output in the next calculation or condition.',
                                   'tip': 'Limit stored contact results.'},
 'physics_body_set_max_slope_speed': {'example': '1. Add Set Slope Speed from the Physics category.\n'
                                                 '2. Connect the available inputs.\n'
                                                 '3. Use the output in the next calculation or condition.',
                                      'tip': 'Set speed while climbing slopes.'},
 'physics_body_set_platform_inheritance': {'example': '1. Add Set Platform Inheritance from the Physics category.\n'
                                                      '2. Connect the available inputs.\n'
                                                      '3. Use the output in the next calculation or condition.',
                                           'tip': 'Inherit moving platform velocity.'},
 'physics_body_set_polygon': {'example': '1. Add Set Polygon Shape from the Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Assign polygon collision points.'},
 'physics_body_set_radius': {'example': '1. Add Set Body Radius from the Physics category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Set circular collision radius.'},
 'physics_body_set_shape': {'example': '1. Add Set Body Shape from the Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': "Set the body's collision shape type."},
 'physics_body_set_sleeping': {'example': '1. Add Set Sleeping from the Physics category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Put a body to sleep or wake it.'},
 'physics_body_set_slope_limit': {'example': '1. Add Set Slope Limit from the Physics category.\n'
                                             '2. Connect the available inputs.\n'
                                             '3. Use the output in the next calculation or condition.',
                                  'tip': 'Limit walkable slope angle.'},
 'physics_body_set_snap_length': {'example': '1. Add Set Snap Length from the Physics category.\n'
                                             '2. Connect the available inputs.\n'
                                             '3. Use the output in the next calculation or condition.',
                                  'tip': 'Keep the body attached to nearby floors.'},
 'physics_body_set_solver_priority': {'example': '1. Add Set Solver Priority from the Physics category.\n'
                                                 '2. Connect the available inputs.\n'
                                                 '3. Use the output in the next calculation or condition.',
                                      'tip': 'Set collision solver ordering.'},
 'physics_body_set_step_height': {'example': '1. Add Set Step Height from the Physics category.\n'
                                             '2. Connect the available inputs.\n'
                                             '3. Use the output in the next calculation or condition.',
                                  'tip': 'Allow a body to climb small steps.'},
 'physics_body_set_torque': {'example': '1. Add Set Torque from the Physics category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Set a rotational force accumulator.'},
 'physics_body_set_up_axis': {'example': '1. Add Set Up Axis from the Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Define which direction counts as up.'},
 'physics_body_unfreeze_all': {'example': '1. Add Unfreeze All from the Physics category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Release all freeze constraints.'},
 'physics_character_body': {'example': '1. Add Character Body 2D from the Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Preset for player-like movement: kinematic mode, manual input enabled, and '
                                   'floor-friendly motion. Execution input: exec. Execution output: exec. Settings: '
                                   'gravity, speed, jump. Use the white execution path for ordering and the colored '
                                   'pins for values.'},
 'physics_decelerate': {'example': '1. Add Decelerate from the Physics category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Reduce current speed by a fixed amount.'},
 'physics_disable_gravity': {'example': '1. Add Disable Gravity from the Physics category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Disable gravity without clearing its configured value.'},
 'physics_drag': {'example': '1. Add Drag from the Physics category.\n'
                             '2. Connect the available inputs.\n'
                             '3. Use the output in the next calculation or condition.',
                  'tip': 'Apply a drag multiplier to movement.'},
 'physics_earth_gravity': {'example': '1. Add Earth Gravity Body from the Physics category.\n'
                                      '2. Connect gravity, bounce.\n'
                                      '3. Use grounded in the next calculation or condition.',
                           'tip': 'Prebuilt Earth-like gravity: 980 units/s² downward, terminal velocity, modest '
                                  'restitution, floor friction, and sleeping at rest. Execution input: exec. '
                                  'Execution output: exec. Data inputs: gravity (number, default=980.0), bounce '
                                  '(number, default=0.15). Data outputs: grounded (boolean). Settings: gravity, '
                                  'bounce, floor_friction, terminal_velocity. Use the white execution path for '
                                  'ordering and the colored pins for values.'},
 'physics_enable_gravity': {'example': '1. Add Enable Gravity from the Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': "Enable the character's configured gravity."},
 'physics_friction': {'example': '1. Add Friction from the Physics category.\n'
                                 '2. Connect the available inputs.\n'
                                 '3. Use the output in the next calculation or condition.',
                      'tip': 'Multiply velocity by one minus friction.'},
 'physics_get_gravity': {'example': '1. Add Get Gravity from the Physics category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Read configured gravity.'},
 'physics_get_position': {'example': '1. Add Get Position from the Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Read world position vector.'},
 'physics_get_position_x': {'example': '1. Add Get Position X from the Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Read world X position.'},
 'physics_get_position_y': {'example': '1. Add Get Position Y from the Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Read world Y position.'},
 'physics_get_velocity': {'example': '1. Add Get Velocity from the Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Read current velocity vector.'},
 'physics_get_velocity_x': {'example': '1. Add Get Velocity X from the Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Read horizontal velocity.'},
 'physics_get_velocity_y': {'example': '1. Add Get Velocity Y from the Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Read vertical velocity.'},
 'physics_is_grounded': {'example': '1. Add Is Grounded from the Physics category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Read whether the gravity body touched the lower arena boundary.'},
 'physics_jump': {'example': '1. Add Jump from the Physics category.\n'
                             '2. Connect the available inputs.\n'
                             '3. Use the output in the next calculation or condition.',
                  'tip': 'Apply an upward velocity impulse.'},
 'physics_kinematic_body': {'example': '1. Add Kinematic Body 2D from the Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Preset for a manually moved character body that is not pushed by gravity unless '
                                   'you enable it. Execution input: exec. Execution output: exec. Use the white '
                                   'execution path for ordering and the colored pins for values.'},
 'physics_lock_movement': {'example': '1. Add Lock Movement from the Physics category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Prevent normal movement while preserving velocity.'},
 'physics_moon_gravity': {'example': '1. Add Moon Gravity Body from the Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Prebuilt low-gravity body using approximately 162 units/s². Settings: gravity, '
                                 'bounce, floor_friction, terminal_velocity.'},
 'physics_move_axis': {'example': '1. Add Move Axis from the Physics category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Move along one chosen axis using an input value.'},
 'physics_move_input': {'example': '1. Add Move From Input Vector from the Physics category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': "Apply the character's stored manual input vector at Speed."},
 'physics_reset_velocity': {'example': '1. Add Reset Velocity from the Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Zero velocity without changing position.'},
 'physics_rigid_body': {'example': '1. Add Rigid Body 2D from the Physics category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Preset for a dynamic body affected by gravity, forces, impulses, collision bounce, '
                               'and damping. Execution input: exec. Execution output: exec. Settings: mass, bounce, '
                               'damping. Use the white execution path for ordering and the colored pins for values.'},
 'physics_rotate_input': {'example': '1. Add Rotate Input from the Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Store an input rotation angle for custom movement scripts.'},
 'physics_set_air_control': {'example': '1. Add Set Air Control from the Physics category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Store air-control multiplier.'},
 'physics_set_bounce': {'example': '1. Add Set Bounce from the Physics category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Set bounce restitution from 0 to 1.'},
 'physics_set_collision_mode': {'example': '1. Add Set Collision Mode from the Physics category.\n'
                                           '2. Connect the available inputs.\n'
                                           '3. Use the output in the next calculation or condition.',
                                'tip': 'Store solid, ghost, or trigger collision mode.'},
 'physics_set_facing': {'example': '1. Add Set Facing from the Physics category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Store a facing vector for manual movement and attacks.'},
 'physics_set_gravity': {'example': '1. Add Set Gravity from the Physics category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Set downward acceleration for this character and enable gravity.'},
 'physics_set_gravity_scale': {'example': '1. Add Set Gravity Scale from the Physics category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Multiply configured gravity by a scale factor.'},
 'physics_set_grounded': {'example': '1. Add Set Grounded from the Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Manually set grounded state.'},
 'physics_set_input_acceleration': {'example': '1. Add Set Input Acceleration from the Physics category.\n'
                                               '2. Connect the available inputs.\n'
                                               '3. Use the output in the next calculation or condition.',
                                    'tip': 'Store acceleration used by custom input movement.'},
 'physics_set_mass': {'example': '1. Add Set Mass from the Physics category.\n'
                                 '2. Connect the available inputs.\n'
                                 '3. Use the output in the next calculation or condition.',
                      'tip': 'Set mass used by impulses.'},
 'physics_set_position': {'example': '1. Add Set Position from the Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Teleport the character to X,Y.'},
 'physics_set_terminal_velocity': {'example': '1. Add Set Terminal Velocity from the Physics category.\n'
                                              '2. Connect the available inputs.\n'
                                              '3. Use the output in the next calculation or condition.',
                                   'tip': 'Cap vertical gravity speed.'},
 'physics_set_velocity': {'example': '1. Add Set Velocity from the Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Replace velocity with X and Y.'},
 'physics_set_velocity_x': {'example': '1. Add Set Velocity X from the Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Set horizontal velocity only.'},
 'physics_set_velocity_y': {'example': '1. Add Set Velocity Y from the Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Set vertical velocity only.'},
 'physics_static_body': {'example': '1. Add Static Body 2D from the Physics category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Preset for an unmoving collision body. Execution input: exec. Execution output: '
                                'exec. Use the white execution path for ordering and the colored pins for values.'},
 'physics_stop': {'example': '1. Add Stop Movement from the Physics category.\n'
                             '2. Connect the available inputs.\n'
                             '3. Use the output in the next calculation or condition.',
                  'tip': 'Zero all velocity.'},
 'physics_stop_bounce': {'example': '1. Add Stop Bouncing from the Physics category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Immediately removes vertical bounce, marks the body grounded, and applies floor '
                                'friction. Execution input: exec. Execution output: exec. Use the white execution '
                                'path for ordering and the colored pins for values.'},
 'physics_unlock_movement': {'example': '1. Add Unlock Movement from the Physics category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Allow normal movement again.'},
 'physics_zero_gravity': {'example': '1. Add Zero Gravity Body from the Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Disables gravity and bounce for a floating body. Execution input: exec. Execution '
                                 'output: exec. Use the white execution path for ordering and the colored pins for '
                                 'values.'},
 'pwr_battery': {'example': '1. Match power',
                 'tip': 'Provides a steady voltage number, depleting over time. Data inputs: Voltage (number). Data '
                        'outputs: Power (number).'},
 'pwr_capacitor': {'example': '1. Laser charge up',
                   'tip': 'Stores and slowly releases power. Execution input: exec. Execution output: exec. Data '
                          'inputs: Charge (number). Data outputs: Output (number). Use the white execution path for '
                          'ordering and the colored pins for values.'},
 'pwr_diode': {'example': '1. One-way flow',
               'tip': 'Allows power only if positive. Data inputs: Voltage (number). Data outputs: Output V '
                      '(number).'},
 'pwr_fuse': {'example': '1. Protection',
              'tip': 'Permanently breaks if voltage exceeds maximum. Execution input: exec. Execution output: Power, '
                     'Broken. Data inputs: Voltage (number), Max V (number). Use the white execution path for '
                     'ordering and the colored pins for values.'},
 'pwr_monitor': {'example': '1. Grid check',
                 'tip': 'Returns True if power grid is supplying electricity. Data inputs: In V (number). Data '
                        'outputs: Has Power (boolean).'},
 'pwr_regulator': {'example': '1. Steady 5V',
                   'tip': 'Clamps voltage to a strict target. Data inputs: In V (number), Target V (number). Data '
                          'outputs: Out V (number).'},
 'pwr_resistor': {'example': '1. Heat generation',
                  'tip': 'Divides voltage by resistance. Data inputs: Voltage (number), Ohms (number). Data outputs: '
                         'Output V (number).'},
 'pwr_switch': {'example': '1. On/Off toggle',
                'tip': 'Toggles power flow manually. Data inputs: In V (number), On (boolean). Data outputs: Out V '
                       '(number).'},
 'pwr_transformer': {'example': '1. Step up/down',
                     'tip': 'Multiplies voltage by a winding ratio. Data inputs: Voltage (number), Ratio (number). '
                            'Data outputs: Output V (number).'},
 'pwr_transistor': {'example': '1. Switch',
                    'tip': 'Allows Collector power to Emitter only if Base is True. Data inputs: Collector (number), '
                           'Base (boolean). Data outputs: Emitter (number).'},
 'random_angle': {'example': '1. Add Random Angle from the Utility category.\n'
                             '2. Connect min, max.\n'
                             '3. Use angle in the next calculation or condition.',
                  'tip': 'Returns a random angle in degrees or radians for projectile spread and random facing. Data '
                         'inputs: min (number, default=0), max (number, default=360). Data outputs: angle (number). '
                         'Settings: radians.'},
 'random_coin_flip': {'example': '1. Add Random Coin Flip from the Utility category.\n'
                                 '2. Connect heads_chance.\n'
                                 '3. Use result in the next calculation or condition.',
                      'tip': 'Pure boolean random source. Every evaluation returns True or False with an optional '
                             'bias percentage. Data inputs: heads_chance (number, default=50.0). Data outputs: '
                             'result (boolean). Settings: heads_chance.'},
 'random_gaussian': {'example': '1. Add Random Gaussian from the Utility category.\n'
                                '2. Connect mean, deviation.\n'
                                '3. Use value in the next calculation or condition.',
                     'tip': 'Returns a bell-curve random number centered on Mean with the chosen Standard Deviation. '
                            'Data inputs: mean (number, default=0), deviation (number, default=1). Data outputs: '
                            'value (number).'},
 'random_jitter': {'example': '1. Add Random Jitter from the Utility category.\n'
                              '2. Connect value, amount.\n'
                              '3. Use value in the next calculation or condition.',
                   'tip': 'Adds a uniformly random offset from -Amount to +Amount to a value. Data inputs: value '
                          '(number, default=0), amount (number, default=1). Data outputs: value (number).'},
 'random_once_chance': {'example': '1. Add Random Once Chance from the Utility category.\n'
                                   '2. Connect chance.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Allows a random event through at most once per character. Reset its latch with the '
                               'Reset input. Execution input: exec, reset. Execution output: pass, fail. Data '
                               'inputs: chance (number, default=50). Use the white execution path for ordering and '
                               'the colored pins for values.'},
 'random_pick_range': {'example': '1. Add Random Pick Range from the Utility category.\n'
                                  '2. Connect min, max.\n'
                                  '3. Use value in the next calculation or condition.',
                       'tip': 'Returns a random integer or decimal between Min and Max. Choose integer mode for '
                              'dice-like values. Data inputs: min (number, default=0), max (number, default=1). Data '
                              'outputs: value (number). Settings: integer.'},
 'random_probability_gate': {'example': '1. Add Random Probability Gate from the Utility category.\n'
                                        '2. Connect chance.\n'
                                        '3. Use roll in the next calculation or condition.',
                             'tip': 'Rolls a percentage every time it receives execution, sending the signal to Pass '
                                    'or Fail. Use Pass to trigger a Utility Button or action only when the random '
                                    'roll succeeds. Execution input: exec. Execution output: pass, fail. Data '
                                    'inputs: chance (number, default=50.0). Data outputs: roll (number). Settings: '
                                    'chance. Use the white execution path for ordering and the colored pins for '
                                    'values.'},
 'random_retrigger_gate': {'example': '1. Add Random Retrigger Gate from the Utility category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Rolls a chance on every trigger and provides explicit Pass/Fail execution paths. '
                                  'Unlike Once Chance it never latches.'},
 'random_seed': {'example': '1. Add Random Seed from the Utility category.\n'
                            '2. Connect seed.\n'
                            '3. Use seed in the next calculation or condition.',
                 'tip': 'Seeds the random stream for repeatable tests. The same seed produces the same random '
                        'sequence. Execution input: exec. Execution output: exec. Data inputs: seed (number, '
                        'default=1). Data outputs: seed (number). Use the white execution path for ordering and the '
                        'colored pins for values.'},
 'random_shuffle_index': {'example': '1. Add Random Shuffle Index from the Utility category.\n'
                                     '2. Connect count.\n'
                                     '3. Use index in the next calculation or condition.',
                          'tip': 'Produces a shuffled index from 0 to Count-1. It cycles through every index before '
                                 'repeating. Execution input: exec. Execution output: exec, finished. Data inputs: '
                                 'count (number, default=3). Data outputs: index (number). Settings: count. Use the '
                                 'white execution path for ordering and the colored pins for values.'},
 'random_weighted_choice': {'example': '1. Add Random Weighted Choice from the Utility category.\n'
                                       '2. Connect a, b, weight.\n'
                                       '3. Use value, picked_b in the next calculation or condition.',
                            'tip': 'Chooses A or B. Weight is the percentage chance of choosing B, so 0 always '
                                   'chooses A and 100 always chooses B. Data inputs: a (any), b (any), weight '
                                   '(number, default=50.0). Data outputs: value (any), picked_b (boolean).'},
 'rig_ammo_add': {'example': '1. Add Add Ammo from the Weapon Inventory category.\n'
                             '2. Connect its compatible inputs.\n'
                             '3. Use its output or execution path in the next operation.',
                  'tip': 'Add ammo without imposing a weapon type. Execution input: exec. Execution output: exec. '
                         "Data inputs: name (string, default='main'), amount (number, default=1). Settings: name, "
                         'amount. Use the white execution path for ordering and colored pins for values.'},
 'rig_ammo_consume': {'example': '1. Add Consume Ammo from the Weapon Inventory category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Consume ammo for custom fire logic. Execution input: exec. Execution output: exec. '
                             "Data inputs: name (string, default='main'), amount (number, default=1). Settings: "
                             'name, amount. Use the white execution path for ordering and colored pins for values.'},
 'rig_ammo_get': {'example': '1. Add Get Ammo from the Weapon Inventory category.\n'
                             '2. Connect its compatible inputs.\n'
                             '3. Use its output or execution path in the next operation.',
                  'tip': "Output current ammo for branches/conditions. Data inputs: name (string, default='main'). "
                         'Data output: result (number). Settings: name. This is a pure data/query node; no white '
                         'execution wire is required.'},
 'rig_ammo_reload': {'example': '1. Add Reload Ammo from the Weapon Inventory category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': 'Restore a named ammo pool to capacity. Execution input: exec. Execution output: exec. '
                            "Data inputs: name (string, default='main'), capacity (number, default=10). Settings: "
                            'name, capacity. Use the white execution path for ordering and colored pins for values.'},
 'rig_ammo_set': {'example': '1. Add Set Ammo from the Weapon Inventory category.\n'
                             '2. Connect its compatible inputs.\n'
                             '3. Use its output or execution path in the next operation.',
                  'tip': 'Set ammo for any named weapon/resource. Execution input: exec. Execution output: exec. '
                         "Data inputs: name (string, default='main'), amount (number, default=1). Settings: name, "
                         'amount. Use the white execution path for ordering and colored pins for values.'},
 'rig_collider_angle': {'example': '1. Add Rotate Collider from the Rig Collisions category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Rotate shape independently from its artwork. Execution input: exec. Execution '
                               "output: exec. Data inputs: name (string, default='main'), angle (number, "
                               'default=0.0). Settings: name, angle. Use the white execution path for ordering and '
                               'colored pins for values.'},
 'rig_collider_attach': {'example': '1. Add Attach Collider To Position from the Rig Collisions category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Re-anchor a collider to any named position event. Execution input: exec. Execution '
                                "output: exec. Data inputs: name (string, default='main'), anchor (string, "
                                "default='main'). Settings: name, anchor. Use the white execution path for ordering "
                                'and colored pins for values.'},
 'rig_collider_capsule': {'example': '1. Add Create Capsule Collider from the Rig Collisions category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Create a disabled capsule shape for blades/beams. Execution input: exec. Execution '
                                 "output: exec. Data inputs: name (string, default='main'), anchor (string, "
                                 "default='main'), radius (number, default=12.0), length (number, default=40.0). "
                                 'Settings: name, anchor, radius, length. Use the white execution path for ordering '
                                 'and colored pins for values.'},
 'rig_collider_circle': {'example': '1. Add Create Circle Collider from the Rig Collisions category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Create a disabled circle collider attached to a position. Execution input: exec. '
                                "Execution output: exec. Data inputs: name (string, default='main'), anchor (string, "
                                "default='main'), radius (number, default=12.0). Settings: name, anchor, radius. Use "
                                'the white execution path for ordering and colored pins for values.'},
 'rig_collider_damage': {'example': '1. Add Set Collider Damage from the Rig Collisions category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Assign optional shape damage; default is zero. Execution input: exec. Execution '
                                "output: exec. Data inputs: name (string, default='main'), damage (number, "
                                'default=0.0). Settings: name, damage. Use the white execution path for ordering and '
                                'colored pins for values.'},
 'rig_collider_debug': {'example': '1. Add Toggle Collision Drawing from the Rig Collisions category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Show/hide the editor collision outline. Execution input: exec. Execution output: '
                               "exec. Data inputs: name (string, default='main'), enabled (boolean, default=True). "
                               'Settings: name, enabled. Use the white execution path for ordering and colored pins '
                               'for values.'},
 'rig_collider_destroy': {'example': '1. Add Destroy Collider from the Rig Collisions category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Remove a named collider while retaining visuals. Execution input: exec. Execution '
                                 "output: exec. Data inputs: name (string, default='main'). Settings: name. Use the "
                                 'white execution path for ordering and colored pins for values.'},
 'rig_collider_enabled': {'example': '1. Add Toggle Collider from the Rig Collisions category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Explicitly enable/disable a shape. Execution input: exec. Execution output: exec. '
                                 "Data inputs: name (string, default='main'), enabled (boolean, default=True). "
                                 'Settings: name, enabled. Use the white execution path for ordering and colored '
                                 'pins for values.'},
 'rig_collider_ignore_tag': {'example': '1. Add Ignore Target Tag from the Rig Collisions category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Ignore targets carrying a chosen tag. Execution input: exec. Execution output: '
                                    "exec. Data inputs: name (string, default='main'), tag (string, default=''). "
                                    'Settings: name, tag. Use the white execution path for ordering and colored pins '
                                    'for values.'},
 'rig_collider_knockback': {'example': '1. Add Set Collider Knockback from the Rig Collisions category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Assign optional force independently from damage. Execution input: exec. '
                                   "Execution output: exec. Data inputs: name (string, default='main'), force "
                                   '(number, default=0.0). Settings: name, force. Use the white execution path for '
                                   'ordering and colored pins for values.'},
 'rig_collider_last': {'example': '1. Add Get Last Collider from the Rig Collisions category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Output the latest collider object. Data output: result (target). This is a pure '
                              'data/query node; no white execution wire is required.'},
 'rig_collider_line': {'example': '1. Add Create Line Collider from the Rig Collisions category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Create a disabled line shape for swords/rays. Execution input: exec. Execution '
                              "output: exec. Data inputs: name (string, default='main'), anchor (string, "
                              "default='main'), length (number, default=40.0), width (number, default=40.0). "
                              'Settings: name, anchor, length, width. Use the white execution path for ordering and '
                              'colored pins for values.'},
 'rig_collider_offset': {'example': '1. Add Offset Collider from the Rig Collisions category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Offset shape relative to its origin. Execution input: exec. Execution output: exec. '
                                "Data inputs: name (string, default='main'), x (number, default=0.0), y (number, "
                                'default=0.0). Settings: name, x, y. Use the white execution path for ordering and '
                                'colored pins for values.'},
 'rig_collider_polygon': {'example': '1. Add Create Polygon Collider from the Rig Collisions category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Create a free-form polygon configuration. Execution input: exec. Execution output: '
                                 "exec. Data inputs: name (string, default='main'), anchor (string, default='main'), "
                                 'value (number, default=0.0). Settings: name, anchor, value. Use the white '
                                 'execution path for ordering and colored pins for values.'},
 'rig_collider_rect': {'example': '1. Add Create Rectangle Collider from the Rig Collisions category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Create a disabled visible rectangle collision shape. Execution input: exec. Execution '
                              "output: exec. Data inputs: name (string, default='main'), anchor (string, "
                              "default='main'), width (number, default=40.0), height (number, default=24.0). "
                              'Settings: name, anchor, width, height. Use the white execution path for ordering and '
                              'colored pins for values.'},
 'rig_collider_require_tag': {'example': '1. Add Require Target Tag from the Rig Collisions category.\n'
                                         '2. Connect its compatible inputs.\n'
                                         '3. Use its output or execution path in the next operation.',
                              'tip': 'Only react to targets carrying a chosen tag. Execution input: exec. Execution '
                                     "output: exec. Data inputs: name (string, default='main'), tag (string, "
                                     "default=''). Settings: name, tag. Use the white execution path for ordering "
                                     'and colored pins for values.'},
 'rig_collider_scale': {'example': '1. Add Scale Collider from the Rig Collisions category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Scale a shape without scaling its sprite. Execution input: exec. Execution output: '
                               "exec. Data inputs: name (string, default='main'), scale (number, default=1.0). "
                               'Settings: name, scale. Use the white execution path for ordering and colored pins '
                               'for values.'},
 'rig_collider_sensor': {'example': '1. Add Set Collider Sensor from the Rig Collisions category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Choose overlap-only sensor behavior. Execution input: exec. Execution output: exec. '
                                "Data inputs: name (string, default='main'), enabled (boolean, default=True). "
                                'Settings: name, enabled. Use the white execution path for ordering and colored pins '
                                'for values.'},
 'rig_collider_tag': {'example': '1. Add Tag Collider from the Rig Collisions category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Tag a hitbox, hurtbox, pickup, or custom sensor. Execution input: exec. Execution '
                             "output: exec. Data inputs: name (string, default='main'), tag (string, default=''). "
                             'Settings: name, tag. Use the white execution path for ordering and colored pins for '
                             'values.'},
 'rig_collider_team_filter': {'example': '1. Add Set Collider Team Filter from the Rig Collisions category.\n'
                                         '2. Connect its compatible inputs.\n'
                                         '3. Use its output or execution path in the next operation.',
                              'tip': 'Choose enemy, ally, any, or custom filtering. Execution input: exec. Execution '
                                     "output: exec. Data inputs: name (string, default='main'), filter (string, "
                                     "default='enemy'). Settings: name, filter. Use the white execution path for "
                                     'ordering and colored pins for values.'},
 'rig_event_attack': {'example': '1. Add Attack Event from the Weapon Events category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Register a free-form attack event and tag. Execution input: exec. Execution output: '
                             "exec. Data inputs: name (string, default='main'), tag (string, default=''). Settings: "
                             'name, tag. Use the white execution path for ordering and colored pins for values.'},
 'rig_event_collision': {'example': '1. Add Rig Collision Event from the Weapon Events category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Register a collider event without forcing damage. Execution input: exec. Execution '
                                "output: exec. Data inputs: name (string, default='main'), tag (string, default=''). "
                                'Settings: name, tag. Use the white execution path for ordering and colored pins for '
                                'values.'},
 'rig_event_muzzle': {'example': '1. Add Muzzle Event from the Weapon Events category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Register a muzzle event at any position anchor. Execution input: exec. Execution '
                             "output: exec. Data inputs: name (string, default='main'), anchor (string, "
                             "default='main'), tag (string, default=''). Settings: name, anchor, tag. Use the white "
                             'execution path for ordering and colored pins for values.'},
 'rig_event_projectile_hit': {'example': '1. Add Projectile Hit Event from the Weapon Events category.\n'
                                         '2. Connect its compatible inputs.\n'
                                         '3. Use its output or execution path in the next operation.',
                              'tip': 'Register projectile-hit metadata for custom logic. Execution input: exec. '
                                     "Execution output: exec. Data inputs: name (string, default='main'), tag "
                                     "(string, default=''). Settings: name, tag. Use the white execution path for "
                                     'ordering and colored pins for values.'},
 'rig_event_visual_swap': {'example': '1. Add Timed Visual Swap Event from the Weapon Events category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Register a sprite/animation swap duration. Execution input: exec. Execution '
                                  "output: exec. Data inputs: name (string, default='main'), sprite (string, "
                                  "default=''), animation (string, default=''), duration (number, default=0.25). "
                                  'Settings: name, sprite, animation, duration. Use the white execution path for '
                                  'ordering and colored pins for values.'},
 'rig_item_detach': {'example': '1. Add Detach Rig Item from the Weapon Inventory category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': 'Detach an item while retaining its world state. Execution input: exec. Execution '
                            "output: exec. Data inputs: name (string, default='main'). Settings: name. Use the white "
                            'execution path for ordering and colored pins for values.'},
 'rig_item_drop': {'example': '1. Add Drop Rig Item from the Weapon Inventory category.\n'
                              '2. Connect its compatible inputs.\n'
                              '3. Use its output or execution path in the next operation.',
                   'tip': 'Record a dropped item event with arbitrary tag. Execution input: exec. Execution output: '
                          "exec. Data inputs: name (string, default='main'), tag (string, default=''). Settings: "
                          'name, tag. Use the white execution path for ordering and colored pins for values.'},
 'rig_item_pickup_event': {'example': '1. Add Register Pickup Event from the Weapon Inventory category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Record a tagged pickup event for custom flow. Execution input: exec. Execution '
                                  "output: exec. Data inputs: name (string, default='main'), tag (string, "
                                  "default=''), radius (number, default=12.0). Settings: name, tag, radius. Use the "
                                  'white execution path for ordering and colored pins for values.'},
 'rig_item_recall': {'example': '1. Add Recall Rig Item from the Weapon Inventory category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': 'Configure return-to-owner behavior. Execution input: exec. Execution output: exec. Data '
                            "inputs: name (string, default='main'), speed (number, default=250.0). Settings: name, "
                            'speed. Use the white execution path for ordering and colored pins for values.'},
 'rig_item_stick': {'example': '1. Add Stick Item To Target from the Weapon Inventory category.\n'
                               '2. Connect its compatible inputs.\n'
                               '3. Use its output or execution path in the next operation.',
                    'tip': 'Configure an item/projectile attachment event. Execution input: exec. Execution output: '
                           "exec. Data inputs: name (string, default='main'), target (object, default=None). "
                           'Settings: name, target. Use the white execution path for ordering and colored pins for '
                           'values.'},
 'rig_position_add_offset': {'example': '1. Add Add Position Offset from the Position Rig category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Add to an anchor offset without replacing it. Execution input: exec. Execution '
                                    "output: exec. Data inputs: name (string, default='main'), x (number, "
                                    'default=0.0), y (number, default=0.0). Settings: name, x, y. Use the white '
                                    'execution path for ordering and colored pins for values.'},
 'rig_position_aim_nearest': {'example': '1. Add Aim At Nearest Enemy from the Position Rig category.\n'
                                         '2. Connect its compatible inputs.\n'
                                         '3. Use its output or execution path in the next operation.',
                              'tip': 'Continuously rotate an anchor toward the nearest matching enemy. Execution '
                                     'input: exec. Execution output: exec. Data inputs: name (string, '
                                     "default='main'), tag (string, default=''). Settings: name, tag. Use the white "
                                     'execution path for ordering and colored pins for values.'},
 'rig_position_aim_target': {'example': '1. Add Aim At Target from the Position Rig category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Continuously rotate an anchor toward any target input. Execution input: exec. '
                                    "Execution output: exec. Data inputs: name (string, default='main'), target "
                                    '(object, default=None). Settings: name, target. Use the white execution path '
                                    'for ordering and colored pins for values.'},
 'rig_position_angle': {'example': '1. Add Get Position Event Angle from the Position Rig category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': "Output a named anchor's current world-facing angle. Data inputs: name (string, "
                               "default='main'). Data output: result (number). Settings: name. This is a pure "
                               'data/query node; no white execution wire is required.'},
 'rig_position_copy': {'example': '1. Add Copy Position Event from the Position Rig category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Copy one anchor into a separately editable anchor. Execution input: exec. Execution '
                              "output: exec. Data inputs: name (string, default='main'), source (string, "
                              "default='main'). Settings: name, source. Use the white execution path for ordering "
                              'and colored pins for values.'},
 'rig_position_create': {'example': '1. Add Create Position Event from the Position Rig category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Create a tagged editor-visible anchor; defaults to Self origin. Execution input: '
                                "exec. Execution output: exec. Data inputs: name (string, default='main'), tag "
                                "(string, default=''), origin (string, default='self'), parent (string, default=''), "
                                'x (number, default=0.0), y (number, default=0.0), angle (number, default=0.0), '
                                "layer (string, default='front'), scale (number, default=1.0), visible (boolean, "
                                'default=True), show_gizmo (boolean, default=True). Settings: name, tag, origin, '
                                'parent, x, y, angle, layer, scale, visible, show_gizmo. Use the white execution '
                                'path for ordering and colored pins for values.'},
 'rig_position_gizmo': {'example': '1. Add Toggle Position Gizmo from the Position Rig category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Toggle the editor-only circle/cross marker. Execution input: exec. Execution output: '
                               "exec. Data inputs: name (string, default='main'), enabled (boolean, default=True). "
                               'Settings: name, enabled. Use the white execution path for ordering and colored pins '
                               'for values.'},
 'rig_position_layer': {'example': '1. Add Set Position Layer from the Position Rig category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Place attached visuals in front of or behind the character. Execution input: exec. '
                               "Execution output: exec. Data inputs: name (string, default='main'), layer (string, "
                               "default='front'). Settings: name, layer. Use the white execution path for ordering "
                               'and colored pins for values.'},
 'rig_position_lock_angle': {'example': '1. Add Lock Position Rotation from the Position Rig category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Stop automatic aiming and keep the current angle. Execution input: exec. '
                                    "Execution output: exec. Data inputs: name (string, default='main'). Settings: "
                                    'name. Use the white execution path for ordering and colored pins for values.'},
 'rig_position_mirror_x': {'example': '1. Add Mirror Position X from the Position Rig category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Mirror the local offset horizontally. Execution input: exec. Execution output: '
                                  "exec. Data inputs: name (string, default='main'). Settings: name. Use the white "
                                  'execution path for ordering and colored pins for values.'},
 'rig_position_mirror_y': {'example': '1. Add Mirror Position Y from the Position Rig category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Mirror the local offset vertically. Execution input: exec. Execution output: '
                                  "exec. Data inputs: name (string, default='main'). Settings: name. Use the white "
                                  'execution path for ordering and colored pins for values.'},
 'rig_position_offset': {'example': '1. Add Get Position Event Offset from the Position Rig category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': "Output a position event's local offset as a vector for FROM/TO/ALTER pipelines."},
 'rig_position_rotate': {'example': '1. Add Rotate Position By from the Position Rig category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Add an angle to the current anchor orientation. Execution input: exec. Execution '
                                "output: exec. Data inputs: name (string, default='main'), angle (number, "
                                'default=0.0). Settings: name, angle. Use the white execution path for ordering and '
                                'colored pins for values.'},
 'rig_position_scale': {'example': '1. Add Set Position Scale from the Position Rig category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Set inherited scale for attached content. Execution input: exec. Execution output: '
                               "exec. Data inputs: name (string, default='main'), scale (number, default=1.0). "
                               'Settings: name, scale. Use the white execution path for ordering and colored pins '
                               'for values.'},
 'rig_position_set_angle': {'example': '1. Add Set Position Angle from the Position Rig category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Set absolute orientation; zero points east and -90 points north. Execution '
                                   "input: exec. Execution output: exec. Data inputs: name (string, default='main'), "
                                   'angle (number, default=0.0). Settings: name, angle. Use the white execution path '
                                   'for ordering and colored pins for values.'},
 'rig_position_set_offset': {'example': '1. Add Set Position Offset from the Position Rig category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Set local X/Y offset from the chosen origin. Execution input: exec. Execution '
                                    "output: exec. Data inputs: name (string, default='main'), x (number, "
                                    'default=0.0), y (number, default=0.0). Settings: name, x, y. Use the white '
                                    'execution path for ordering and colored pins for values.'},
 'rig_position_set_offset_vector': {'example': '1. Add Set Position Offset Vector from the Position Rig category.\n'
                                               '2. Connect its compatible inputs.\n'
                                               '3. Use its output or execution path in the next operation.',
                                    'tip': 'Apply a vector result from ALTER directly to a position event.'},
 'rig_position_set_origin': {'example': '1. Add Set Position Origin from the Position Rig category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Use Self or another named anchor/sprite position as origin. Execution input: '
                                    "exec. Execution output: exec. Data inputs: name (string, default='main'), "
                                    "origin (string, default='self'), parent (string, default=''). Settings: name, "
                                    'origin, parent. Use the white execution path for ordering and colored pins for '
                                    'values.'},
 'rig_position_tag': {'example': '1. Add Set Position Tag from the Position Rig category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Assign an arbitrary lookup/gameplay tag to an anchor. Execution input: exec. Execution '
                             "output: exec. Data inputs: name (string, default='main'), tag (string, default=''). "
                             'Settings: name, tag. Use the white execution path for ordering and colored pins for '
                             'values.'},
 'rig_position_tip': {'example': '1. Add Create Tip Position from the Position Rig category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Create a child anchor at a length along a parent orientation. Execution input: exec. '
                             "Execution output: exec. Data inputs: name (string, default='main'), parent (string, "
                             "default=''), length (number, default=40.0), angle (number, default=0.0), tag (string, "
                             "default=''). Settings: name, parent, length, angle, tag. Use the white execution path "
                             'for ordering and colored pins for values.'},
 'rig_position_visible': {'example': '1. Add Set Position Visibility from the Position Rig category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Show or hide content attached to this position. Execution input: exec. Execution '
                                 "output: exec. Data inputs: name (string, default='main'), enabled (boolean, "
                                 'default=True). Settings: name, enabled. Use the white execution path for ordering '
                                 'and colored pins for values.'},
 'rig_position_world': {'example': '1. Add Get Position Event World Position from the Position Rig category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Output the live world position of a named anchor. Data inputs: name (string, '
                               "default='main'). Data output: result (position). Settings: name. This is a pure "
                               'data/query node; no white execution wire is required.'},
 'rig_projectile_angle': {'example': '1. Add Set Projectile Angle from the Projectiles category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Set travel direction in degrees. Execution input: exec. Execution output: exec. '
                                 'Data inputs: angle (number, default=0.0). Settings: angle. Use the white execution '
                                 'path for ordering and colored pins for values.'},
 'rig_projectile_animation': {'example': '1. Add Set Projectile Animation from the Projectiles category.\n'
                                         '2. Connect its compatible inputs.\n'
                                         '3. Use its output or execution path in the next operation.',
                              'tip': 'Assign a reusable animation to projectile art. Execution input: exec. '
                                     "Execution output: exec. Data inputs: animation (string, default=''). Settings: "
                                     'animation. Use the white execution path for ordering and colored pins for '
                                     'values.'},
 'rig_projectile_bounces': {'example': '1. Add Set Projectile Bounces from the Projectiles category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Set allowed environment/target bounces. Execution input: exec. Execution output: '
                                   'exec. Data inputs: bounces (number, default=0). Settings: bounces. Use the white '
                                   'execution path for ordering and colored pins for values.'},
 'rig_projectile_collision': {'example': '1. Add Set Projectile Collidable from the Projectiles category.\n'
                                         '2. Connect its compatible inputs.\n'
                                         '3. Use its output or execution path in the next operation.',
                              'tip': 'Explicitly enable collision; default is off. Execution input: exec. Execution '
                                     'output: exec. Data inputs: enabled (boolean, default=True). Settings: enabled. '
                                     'Use the white execution path for ordering and colored pins for values.'},
 'rig_projectile_damage': {'example': '1. Add Set Projectile Damage from the Projectiles category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Assign optional hit damage; default is zero. Execution input: exec. Execution '
                                  'output: exec. Data inputs: damage (number, default=0.0). Settings: damage. Use '
                                  'the white execution path for ordering and colored pins for values.'},
 'rig_projectile_destroy': {'example': '1. Add Destroy Last Projectile from the Projectiles category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Explicitly despawn the most recently created projectile. Execution input: exec. '
                                   'Execution output: exec. Use the white execution path for ordering and colored '
                                   'pins for values.'},
 'rig_projectile_drag': {'example': '1. Add Set Projectile Drag from the Projectiles category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Apply configurable air/water resistance. Execution input: exec. Execution output: '
                                'exec. Data inputs: drag (number, default=0.0). Settings: drag. Use the white '
                                'execution path for ordering and colored pins for values.'},
 'rig_projectile_gravity': {'example': '1. Add Set Projectile Gravity from the Projectiles category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Apply vertical acceleration; zero gives straight travel. Execution input: exec. '
                                   'Execution output: exec. Data inputs: gravity (number, default=0.0). Settings: '
                                   'gravity. Use the white execution path for ordering and colored pins for values.'},
 'rig_projectile_homing': {'example': '1. Add Set Projectile Homing from the Projectiles category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Steer toward nearest enemy with unrestricted strength. Execution input: exec. '
                                  'Execution output: exec. Data inputs: homing (number, default=0.0). Settings: '
                                  'homing. Use the white execution path for ordering and colored pins for values.'},
 'rig_projectile_last': {'example': '1. Add Get Last Projectile from the Projectiles category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Output the latest projectile object for advanced chaining. Data output: result '
                                '(target). This is a pure data/query node; no white execution wire is required.'},
 'rig_projectile_lifetime': {'example': '1. Add Set Projectile Lifetime from the Projectiles category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Set automatic despawn time. Execution input: exec. Execution output: exec. Data '
                                    'inputs: lifetime (number, default=3.0). Settings: lifetime. Use the white '
                                    'execution path for ordering and colored pins for values.'},
 'rig_projectile_opacity': {'example': '1. Add Set Projectile Opacity from the Projectiles category.\n'
                                       '2. Connect its compatible inputs.\n'
                                       '3. Use its output or execution path in the next operation.',
                            'tip': 'Set projectile transparency. Execution input: exec. Execution output: exec. Data '
                                   'inputs: opacity (number, default=255). Settings: opacity. Use the white '
                                   'execution path for ordering and colored pins for values.'},
 'rig_projectile_owner_ignore': {'example': '1. Add Ignore Owner Temporarily from the Projectiles category.\n'
                                            '2. Connect its compatible inputs.\n'
                                            '3. Use its output or execution path in the next operation.',
                                 'tip': 'Prevent immediate collision with the thrower. Execution input: exec. '
                                        'Execution output: exec. Data inputs: duration (number, default=0.25). '
                                        'Settings: duration. Use the white execution path for ordering and colored '
                                        'pins for values.'},
 'rig_projectile_pickup': {'example': '1. Add Set Projectile Pickup from the Projectiles category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Allow a projectile/item to be picked up in a radius. Execution input: exec. '
                                  'Execution output: exec. Data inputs: enabled (boolean, default=True), radius '
                                  '(number, default=12.0). Settings: enabled, radius. Use the white execution path '
                                  'for ordering and colored pins for values.'},
 'rig_projectile_pierce': {'example': '1. Add Set Projectile Pierce from the Projectiles category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Set number of extra targets it can cross. Execution input: exec. Execution '
                                  'output: exec. Data inputs: pierce (number, default=0). Settings: pierce. Use the '
                                  'white execution path for ordering and colored pins for values.'},
 'rig_projectile_radius': {'example': '1. Add Set Projectile Radius from the Projectiles category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Set collision radius independently from sprite size. Execution input: exec. '
                                  'Execution output: exec. Data inputs: radius (number, default=12.0). Settings: '
                                  'radius. Use the white execution path for ordering and colored pins for values.'},
 'rig_projectile_scale': {'example': '1. Add Set Projectile Scale from the Projectiles category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Scale projectile visuals. Execution input: exec. Execution output: exec. Data '
                                 'inputs: scale (number, default=1.0). Settings: scale. Use the white execution path '
                                 'for ordering and colored pins for values.'},
 'rig_projectile_spawn': {'example': '1. Add Spawn Projectile From Position from the Projectiles category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Spawn an inert projectile from a named position event. Execution input: exec. '
                                 "Execution output: exec. Data inputs: name (string, default='main'), anchor "
                                 "(string, default='main'), speed (number, default=250.0), lifetime (number, "
                                 "default=3.0), sprite (string, default=''), animation (string, default=''), scale "
                                 '(number, default=1.0), opacity (number, default=255), radius (number, '
                                 "default=12.0), tags (string, default=''). Settings: name, anchor, speed, lifetime, "
                                 'sprite, animation, scale, opacity, radius, tags. Use the white execution path for '
                                 'ordering and colored pins for values.'},
 'rig_projectile_speed': {'example': '1. Add Set Projectile Speed from the Projectiles category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Change speed while preserving direction. Execution input: exec. Execution output: '
                                 'exec. Data inputs: speed (number, default=250.0). Settings: speed. Use the white '
                                 'execution path for ordering and colored pins for values.'},
 'rig_projectile_sprite': {'example': '1. Add Set Projectile Sprite from the Projectiles category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Assign projectile art without enabling collision. Execution input: exec. '
                                  "Execution output: exec. Data inputs: sprite (string, default=''). Settings: "
                                  'sprite. Use the white execution path for ordering and colored pins for values.'},
 'rig_projectile_tag': {'example': '1. Add Tag Projectile from the Projectiles category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Add type tags such as acid, water, bullet, or grass. Execution input: exec. '
                               "Execution output: exec. Data inputs: tag (string, default=''). Settings: tag. Use "
                               'the white execution path for ordering and colored pins for values.'},
 'rig_projectile_tag_multiplier': {'example': '1. Add Projectile Multiplier Vs Tag from the Projectiles category.\n'
                                              '2. Connect its compatible inputs.\n'
                                              '3. Use its output or execution path in the next operation.',
                                   'tip': 'Scale damage against targets with a chosen tag. Execution input: exec. '
                                          "Execution output: exec. Data inputs: tag (string, default=''), multiplier "
                                          '(number, default=1.0). Settings: tag, multiplier. Use the white execution '
                                          'path for ordering and colored pins for values.'},
 'rig_projectile_tint': {'example': '1. Add Tint Projectile from the Projectiles category.\n'
                                    '2. Connect its compatible inputs.\n'
                                    '3. Use its output or execution path in the next operation.',
                         'tip': 'Apply projectile color configuration. Execution input: exec. Execution output: '
                                'exec. Data inputs: color (color, default=[255, 255, 255]). Settings: color. Use the '
                                'white execution path for ordering and colored pins for values.'},
 'rig_projectile_trail': {'example': '1. Add Configure Projectile Trail from the Projectiles category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Store trail color, scale, and duration settings. Execution input: exec. Execution '
                                 'output: exec. Data inputs: color (color, default=[255, 255, 255]), scale (number, '
                                 'default=1.0), duration (number, default=0.25). Settings: color, scale, duration. '
                                 'Use the white execution path for ordering and colored pins for values.'},
 'rig_projectile_velocity': {'example': '1. Add Set Projectile Velocity from the Projectiles category.\n'
                                        '2. Connect its compatible inputs.\n'
                                        '3. Use its output or execution path in the next operation.',
                             'tip': 'Set independent X/Y velocity. Execution input: exec. Execution output: exec. '
                                    'Data inputs: x (number, default=0.0), y (number, default=0.0). Settings: x, y. '
                                    'Use the white execution path for ordering and colored pins for values.'},
 'rig_visual_afterimage': {'example': '1. Add Configure Afterimage from the Weapon Visuals category.\n'
                                      '2. Connect its compatible inputs.\n'
                                      '3. Use its output or execution path in the next operation.',
                           'tip': 'Enable transparent motion ghosts for fast attacks. Execution input: exec. '
                                  "Execution output: exec. Data inputs: name (string, default='main'), enabled "
                                  '(boolean, default=True), opacity (number, default=255), duration (number, '
                                  'default=0.25). Settings: name, enabled, opacity, duration. Use the white '
                                  'execution path for ordering and colored pins for values.'},
 'rig_visual_angle': {'example': '1. Add Set Rig Visual Angle from the Weapon Visuals category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Rotate artwork relative to its position-event direction. Execution input: exec. '
                             "Execution output: exec. Data inputs: name (string, default='main'), angle (number, "
                             'default=0.0). Settings: name, angle. Use the white execution path for ordering and '
                             'colored pins for values.'},
 'rig_visual_animation': {'example': '1. Add Set Rig Animation from the Weapon Visuals category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Assign an Animation Library clip to a rig visual. Execution input: exec. Execution '
                                 "output: exec. Data inputs: name (string, default='main'), animation (string, "
                                 "default=''). Settings: name, animation. Use the white execution path for ordering "
                                 'and colored pins for values.'},
 'rig_visual_attach': {'example': '1. Add Attach Visual To Position from the Weapon Visuals category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Attach any sprite/animation visual to a named anchor. Execution input: exec. '
                              "Execution output: exec. Data inputs: name (string, default='main'), anchor (string, "
                              "default='main'). Settings: name, anchor. Use the white execution path for ordering "
                              'and colored pins for values.'},
 'rig_visual_flash': {'example': '1. Add Temporary Sprite Flash from the Weapon Visuals category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Temporarily swap to a muzzle-flash/attack sprite. Execution input: exec. Execution '
                             "output: exec. Data inputs: name (string, default='main'), sprite (string, default=''), "
                             'duration (number, default=0.25). Settings: name, sprite, duration. Use the white '
                             'execution path for ordering and colored pins for values.'},
 'rig_visual_layer': {'example': '1. Add Set Rig Visual Layer from the Weapon Visuals category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Draw a weapon visual in front of or behind its owner. Execution input: exec. Execution '
                             "output: exec. Data inputs: name (string, default='main'), layer (string, "
                             "default='front'). Settings: name, layer. Use the white execution path for ordering and "
                             'colored pins for values.'},
 'rig_visual_opacity': {'example': '1. Add Set Rig Visual Opacity from the Weapon Visuals category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Set visual alpha independently from collision. Execution input: exec. Execution '
                               "output: exec. Data inputs: name (string, default='main'), opacity (number, "
                               'default=255). Settings: name, opacity. Use the white execution path for ordering and '
                               'colored pins for values.'},
 'rig_visual_random_animation': {'example': '1. Add Random Rig Animation from the Weapon Visuals category.\n'
                                            '2. Connect its compatible inputs.\n'
                                            '3. Use its output or execution path in the next operation.',
                                 'tip': 'Choose one animation from a comma-separated group. Execution input: exec. '
                                        "Execution output: exec. Data inputs: name (string, default='main'), "
                                        "animations (string, default=''). Settings: name, animations. Use the white "
                                        'execution path for ordering and colored pins for values.'},
 'rig_visual_scale': {'example': '1. Add Set Rig Visual Scale from the Weapon Visuals category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Scale only the attached visual. Execution input: exec. Execution output: exec. Data '
                             "inputs: name (string, default='main'), scale (number, default=1.0). Settings: name, "
                             'scale. Use the white execution path for ordering and colored pins for values.'},
 'rig_visual_sprite': {'example': '1. Add Set Rig Sprite from the Weapon Visuals category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Assign a sprite path without changing collisions. Execution input: exec. Execution '
                              "output: exec. Data inputs: name (string, default='main'), sprite (string, "
                              "default=''). Settings: name, sprite. Use the white execution path for ordering and "
                              'colored pins for values.'},
 'rig_visual_tint': {'example': '1. Add Tint Rig Visual from the Weapon Visuals category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': 'Apply a visual color tint configuration. Execution input: exec. Execution output: exec. '
                            "Data inputs: name (string, default='main'), color (color, default=[255, 255, 255]). "
                            'Settings: name, color. Use the white execution path for ordering and colored pins for '
                            'values.'},
 'rig_visual_visible': {'example': '1. Add Toggle Rig Visual from the Weapon Visuals category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Show/hide a visual without deleting its anchor. Execution input: exec. Execution '
                               "output: exec. Data inputs: name (string, default='main'), enabled (boolean, "
                               'default=True). Settings: name, enabled. Use the white execution path for ordering '
                               'and colored pins for values.'},
 'rig_weapon_collision': {'example': '1. Add Set Weapon Collidable from the Weapons category.\n'
                                     '2. Connect its compatible inputs.\n'
                                     '3. Use its output or execution path in the next operation.',
                          'tip': 'Explicitly enable/disable weapon collision; default is off. Execution input: exec. '
                                 "Execution output: exec. Data inputs: name (string, default='main'), enabled "
                                 '(boolean, default=True). Settings: name, enabled. Use the white execution path for '
                                 'ordering and colored pins for values.'},
 'rig_weapon_create': {'example': '1. Add Create Weapon from the Weapons category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Create a harmless weapon definition attached to an anchor. Execution input: exec. '
                              "Execution output: exec. Data inputs: name (string, default='main'), anchor (string, "
                              "default='main'), kind (string, default='weapon'). Settings: name, anchor, kind. Use "
                              'the white execution path for ordering and colored pins for values.'},
 'rig_weapon_damage': {'example': '1. Add Set Weapon Contact Damage from the Weapons category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Assign optional contact damage; default remains zero. Execution input: exec. '
                              "Execution output: exec. Data inputs: name (string, default='main'), damage (number, "
                              'default=0.0). Settings: name, damage. Use the white execution path for ordering and '
                              'colored pins for values.'},
 'rig_weapon_destroy': {'example': '1. Add Destroy Weapon Rig from the Weapons category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Remove a named weapon and its visual. Execution input: exec. Execution output: exec. '
                               "Data inputs: name (string, default='main'). Settings: name. Use the white execution "
                               'path for ordering and colored pins for values.'},
 'rig_weapon_equip': {'example': '1. Add Equip Weapon from the Weapons category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Enable a named weapon without forcing damage or collision. Execution input: exec. '
                             "Execution output: exec. Data inputs: name (string, default='main'). Settings: name. "
                             'Use the white execution path for ordering and colored pins for values.'},
 'rig_weapon_jab': {'example': '1. Add Jab Weapon from the Weapons category.\n'
                               '2. Connect its compatible inputs.\n'
                               '3. Use its output or execution path in the next operation.',
                    'tip': 'Fast forward/back jab with optional afterimage. Execution input: exec. Execution output: '
                           "exec. Data inputs: name (string, default='main'), distance (number, default=35.0), "
                           'duration (number, default=0.25), speed (number, default=250.0), afterimage (boolean, '
                           'default=True). Settings: name, distance, duration, speed, afterimage. Use the white '
                           'execution path for ordering and colored pins for values.'},
 'rig_weapon_recoil': {'example': '1. Add Weapon Recoil from the Weapons category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Kick a visual backward and recover. Execution input: exec. Execution output: exec. '
                              "Data inputs: name (string, default='main'), distance (number, default=35.0), duration "
                              '(number, default=0.25), speed (number, default=250.0). Settings: name, distance, '
                              'duration, speed. Use the white execution path for ordering and colored pins for '
                              'values.'},
 'rig_weapon_spin': {'example': '1. Add Spin Weapon from the Weapons category.\n'
                                '2. Connect its compatible inputs.\n'
                                '3. Use its output or execution path in the next operation.',
                     'tip': 'Rotate a weapon through a configurable spin. Execution input: exec. Execution output: '
                            "exec. Data inputs: name (string, default='main'), duration (number, default=0.25), "
                            'speed (number, default=250.0), afterimage (boolean, default=True). Settings: name, '
                            'duration, speed, afterimage. Use the white execution path for ordering and colored pins '
                            'for values.'},
 'rig_weapon_swing': {'example': '1. Add Swing Weapon from the Weapons category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Animate an arc without automatically dealing damage. Execution input: exec. Execution '
                             "output: exec. Data inputs: name (string, default='main'), angle (number, default=0.0), "
                             'duration (number, default=0.25), speed (number, default=250.0), afterimage (boolean, '
                             'default=True). Settings: name, angle, duration, speed, afterimage. Use the white '
                             'execution path for ordering and colored pins for values.'},
 'rig_weapon_tag': {'example': '1. Add Tag Weapon from the Weapons category.\n'
                               '2. Connect its compatible inputs.\n'
                               '3. Use its output or execution path in the next operation.',
                    'tip': 'Add a free-form tag such as steel, fire, knife, or water. Execution input: exec. '
                           "Execution output: exec. Data inputs: name (string, default='main'), tag (string, "
                           "default=''). Settings: name, tag. Use the white execution path for ordering and colored "
                           'pins for values.'},
 'rig_weapon_throw': {'example': '1. Add Throw Weapon from the Weapons category.\n'
                                 '2. Connect its compatible inputs.\n'
                                 '3. Use its output or execution path in the next operation.',
                      'tip': 'Turn the current weapon visual into an inert projectile. Execution input: exec. '
                             "Execution output: exec. Data inputs: name (string, default='main'), speed (number, "
                             'default=250.0). Settings: name, speed. Use the white execution path for ordering and '
                             'colored pins for values.'},
 'rig_weapon_thrust': {'example': '1. Add Thrust Weapon from the Weapons category.\n'
                                  '2. Connect its compatible inputs.\n'
                                  '3. Use its output or execution path in the next operation.',
                       'tip': 'Long thrust motion with speed and ghosting controls. Execution input: exec. Execution '
                              "output: exec. Data inputs: name (string, default='main'), distance (number, "
                              'default=35.0), duration (number, default=0.25), speed (number, default=250.0), '
                              'afterimage (boolean, default=True). Settings: name, distance, duration, speed, '
                              'afterimage. Use the white execution path for ordering and colored pins for values.'},
 'rig_weapon_unequip': {'example': '1. Add Unequip Weapon from the Weapons category.\n'
                                   '2. Connect its compatible inputs.\n'
                                   '3. Use its output or execution path in the next operation.',
                        'tip': 'Disable a named weapon while retaining its setup. Execution input: exec. Execution '
                               "output: exec. Data inputs: name (string, default='main'). Settings: name. Use the "
                               'white execution path for ordering and colored pins for values.'},
 'scene_camera_follow': {'example': '1. Add Camera Follow from the Camera category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Follow a character with the scene camera.'},
 'scene_camera_pan': {'example': '1. Add Pan Camera from the Camera category.\n'
                                 '2. Connect the available inputs.\n'
                                 '3. Use the output in the next calculation or condition.',
                      'tip': 'Offset the scene camera by X,Y.'},
 'scene_camera_set_deadzone': {'example': '1. Add Set Camera Deadzone from the Camera category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Store a camera follow deadzone.'},
 'scene_camera_set_smoothing': {'example': '1. Add Set Camera Smoothing from the Camera category.\n'
                                           '2. Connect the available inputs.\n'
                                           '3. Use the output in the next calculation or condition.',
                                'tip': 'Store camera follow smoothing.'},
 'scene_camera_stop_follow': {'example': '1. Add Stop Camera Follow from the Camera category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Clear the scene camera target.'},
 'scene_camera_zoom': {'example': '1. Add Set Camera Zoom from the Camera category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Set the scene camera zoom target.'},
 'scene_clear_camera_target': {'example': '1. Add Clear Camera Target from the Camera category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Clear the scene camera target.'},
 'scene_disable_manual_input': {'example': '1. Add Disable Manual Input from the Control category.\n'
                                           '2. Connect the available inputs.\n'
                                           '3. Use the output in the next calculation or condition.',
                                'tip': 'Disable character manual input.'},
 'scene_enable_manual_input': {'example': '1. Add Enable Manual Input from the Control category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Allow character manual input.'},
 'scene_generate_walls': {'example': '1. On Spawn → Generate Arena Walls (thickness=12)\n'
                                     '2. On Phase Change → thicker walls',
                          'tip': 'Auto-generate four collision walls around the arena boundary. Walls are tagged '
                                 "'auto_wall' and 'arena_wall'. Existing auto-walls are replaced; custom walls are "
                                 'untouched. Execution input: exec. Execution output: exec. Data inputs: thickness '
                                 '(number, default=8), color (color, default=[60, 60, 80]). Settings: thickness, '
                                 'color. Use the white execution path for ordering and the colored pins for values.'},
 'scene_get_box_scale': {'example': '1. Get Arena Size → Compare < 100 → end condition\n'
                                    '2. Feed size into Set Node Value for a minimap',
                         'tip': 'Returns the current arena box scale and thickness. Data outputs: size (number), '
                                'thickness (number).'},
 'scene_get_camera_locked': {'example': '1. Add Is Camera Locked from the Camera category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Read scene camera lock state.'},
 'scene_get_camera_zoom': {'example': '1. Add Get Camera Zoom from the Camera category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Read current camera zoom target.'},
 'scene_lock_camera': {'example': '1. Add Lock Camera Controls from the Camera category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': "Stop the arena's normal WASD/arrow camera movement."},
 'scene_lock_controls': {'example': '1. Add Lock Scene Controls from the Camera category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Disable manual camera controls without affecting character input.'},
 'scene_lock_cursor': {'example': '1. Add Lock Cursor from the Camera category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Capture the cursor.'},
 'scene_pause_input': {'example': '1. Add Pause Scene Input from the Control category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': "Pause the character's input processing."},
 'scene_resume_input': {'example': '1. Add Resume Scene Input from the Control category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Resume character input processing.'},
 'scene_set_arena_input_mode': {'example': '1. Add Set Arena Input Mode from the Control category.\n'
                                           '2. Connect the available inputs.\n'
                                           '3. Use the output in the next calculation or condition.',
                                'tip': 'Store player, editor, cinematic, or locked scene mode.'},
 'scene_set_box_scale': {'example': '1. Every 10s → Set Arena Size (current - 20) — shrinking zone\n'
                                    '2. Boss Phase 2 → bigger arena',
                         'tip': 'Change the arena box size at runtime. Combine with a Tween or Countdown for '
                                'animated scaling effects. Execution input: exec. Execution output: exec. Data '
                                'inputs: size (number, default=260). Data outputs: old_size (number). Settings: '
                                'size. Use the white execution path for ordering and the colored pins for values.'},
 'scene_set_box_thickness': {'example': '1. On Phase Change → thicker border\n2. Pulse thickness with Sine wave',
                             'tip': 'Change the visible border thickness of the arena box. Execution input: exec. '
                                    'Execution output: exec. Data inputs: thickness (number, default=5). Settings: '
                                    'thickness. Use the white execution path for ordering and the colored pins for '
                                    'values.'},
 'scene_set_camera_bounds': {'example': '1. Add Set Camera Bounds from the Camera category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Store camera movement bounds.'},
 'scene_set_camera_drag': {'example': '1. Add Set Camera Drag from the Camera category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Set normal scene camera drag.'},
 'scene_set_camera_speed': {'example': '1. Add Set Camera Speed from the Camera category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Set normal scene camera speed.'},
 'scene_set_camera_target': {'example': '1. Add Set Camera Target from the Camera category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Set the scene camera target character.'},
 'scene_set_camera_zoom': {'example': '1. Set Camera Zoom (2.0) -> Close up\n2. Set Camera Zoom (0.5) -> Wide view',
                           'tip': 'Forces the camera zoom level. Execution input: exec. Execution output: exec. Data '
                                  'inputs: Zoom (number). Use the white execution path for ordering and the colored '
                                  'pins for values.'},
 'scene_set_control_mode': {'example': '1. Add Set Control Mode from the Control category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Store manual, AI, cinematic, or disabled control mode.'},
 'scene_set_cursor_visible': {'example': '1. Add Set Cursor Visible from the Camera category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Show or hide the cursor.'},
 'scene_set_global_light': {'example': '1. Set Light (0.1) -> Spawns a creepy dark mood\n2. Day/Night cycle',
                            'tip': 'Darkens the arena (0.0=Pitch Black, 1.0=Bright). Execution input: exec. '
                                   'Execution output: exec. Data inputs: Level (number). Use the white execution '
                                   'path for ordering and the colored pins for values.'},
 'scene_set_input_priority': {'example': '1. Add Set Scene Input Priority from the Control category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Set scene/player/UI priority label.'},
 'scene_set_time_scale': {'example': '1. On Death -> Time Scale (0.2) for 2 seconds\n'
                                     '2. Boss enrage -> Time Scale (1.2)',
                          'tip': 'Slows down or speeds up the simulation. Execution input: exec. Execution output: '
                                 'exec. Data inputs: Scale (number). Use the white execution path for ordering and '
                                 'the colored pins for values.'},
 'scene_unlock_camera': {'example': '1. Add Unlock Camera Controls from the Camera category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Allow normal arena camera movement again.'},
 'scene_unlock_controls': {'example': '1. Add Unlock Scene Controls from the Camera category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Restore manual camera controls.'},
 'scene_unlock_cursor': {'example': '1. Add Unlock Cursor from the Camera category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Release the cursor.'},
 'sens_broadcast': {'example': '1. Siren',
                    'tip': 'Fires a global event alert to all characters. Execution input: exec. Execution output: '
                           'exec. Data inputs: Alert Message (string). Use the white execution path for ordering and '
                           'the colored pins for values.'},
 'sens_geiger': {'example': '1. Audio clicking',
                 'tip': 'Simulates radiation ticks. Data outputs: Radiation (number).'},
 'sens_monitor': {'example': '1. Display on HUD',
                  'tip': 'Returns a string representing system health. Data inputs: Health (number). Data outputs: '
                         'Status (string).'},
 'sens_motion': {'example': '1. Turret detection',
                 'tip': 'Triggers if velocity magnitude > threshold. Data inputs: Character (object), Threshold '
                        '(number). Data outputs: Triggered (boolean).'},
 'sens_overload': {'example': '1. Circuit breaker',
                   'tip': 'Triggers an execution if a value exceeds a maximum. Execution input: exec. Execution '
                          'output: Safe, Overload. Data inputs: Value (number), Max (number). Use the white '
                          'execution path for ordering and the colored pins for values.'},
 'sens_pressure': {'example': '1. Screen Shake on high pressure',
                   'tip': 'Outputs pressure based on collisions. Data outputs: Pressure (number).'},
 'sens_smoke': {'example': '1. Fire alarm',
                'tip': 'Triggers if particles are nearby. Data inputs: Position (vector). Data outputs: Alarm '
                       '(boolean).'},
 'sens_temp': {'example': '1. If Temp > 100 -> Fan On',
               'tip': 'Outputs simulated heat based on action density. Data outputs: Temp (C) (number).'},
 'sig_amp': {'example': '1. Boost signal',
             'tip': 'Multiplies a numeric signal. Data inputs: In (number), Gain (number). Data outputs: Out '
                    '(number).'},
 'sig_emitter': {'example': '1. Wireless event',
                 'tip': 'Emits a signal string locally. Execution input: exec. Execution output: exec. Data inputs: '
                        'Signal (string). Use the white execution path for ordering and the colored pins for '
                        'values.'},
 'sig_highpass': {'example': '1. Motion detection',
                  'tip': 'Only outputs sudden changes in a signal. Execution input: exec. Execution output: exec. '
                         'Data inputs: In (number). Data outputs: Out (number). Use the white execution path for '
                         'ordering and the colored pins for values.'},
 'sig_lowpass': {'example': '1. Sensor smoothing',
                 'tip': 'Smooths out sudden spikes in a signal. Execution input: exec. Execution output: exec. Data '
                        'inputs: In (number), Smooth (number). Data outputs: Out (number). Use the white execution '
                        'path for ordering and the colored pins for values.'},
 'sig_noise': {'example': '1. Interference',
               'tip': 'Adds random noise to a signal. Data inputs: In (number), Amount (number). Data outputs: Out '
                      '(number).'},
 'sig_osc_saw': {'example': '1. Fast reset',
                 'tip': 'Outputs a sawtooth wave -1 to 1. Data inputs: Freq (number). Data outputs: Out (number).'},
 'sig_osc_sine': {'example': '1. Siren pitch',
                  'tip': 'Outputs a sine wave -1 to 1 based on time. Data inputs: Freq (number). Data outputs: Out '
                         '(number).'},
 'sig_osc_sq': {'example': '1. Blinking light',
                'tip': 'Outputs a square wave -1 or 1. Data inputs: Freq (number). Data outputs: Out (number).'},
 'sig_osc_tri': {'example': '1. Ramp up/down',
                 'tip': 'Outputs a triangle wave -1 to 1. Data inputs: Freq (number). Data outputs: Out (number).'},
 'sig_receiver': {'example': '1. Wireless trigger',
                  'tip': 'Returns True if signal emitted recently. Data inputs: Signal (string). Data outputs: '
                         'Active (boolean).'},
 'stat_add_max_hp': {'example': '1. On Level Up -> Add Max HP (50)\n2. Permanent debuffs',
                     'tip': 'Increases or decreases max HP. Execution input: exec. Execution output: exec. Data '
                            'inputs: Character (object), Amount (number). Use the white execution path for ordering '
                            'and the colored pins for values.'},
 'status_cleanse': {'example': '1. On Heal -> Cleanse\n2. On Transform -> Cleanse',
                    'tip': 'Removes ALL negative engine status effects at once (Stun, Root, Silence, Slow, Poison, '
                           'Burn, Freeze). Execution input: exec. Execution output: exec. Data inputs: target '
                           '(object). Use the white execution path for ordering and the colored pins for values.'},
 'status_copy_tags': {'example': '1. When a boss spawns a clone, copy tags so the clone inherits "boss" rules\n'
                                 '2. Copy Tags from Target to Self',
                      'tip': 'Copies all tag strings from one character to another. Execution input: exec. Execution '
                             'output: exec. Data inputs: source (object), target (object). Use the white execution '
                             'path for ordering and the colored pins for values.'},
 'status_count_tag': {'example': '1. Count "zombie" > 10 -> Spawn Holy Nova\n2. Count "ally" < 2 -> Flee',
                      'tip': 'Counts how many characters in an area carry a specific tag string. Data inputs: center '
                             '(vector), radius (number, default=0), tag (string). Data outputs: count (number). '
                             'Settings: tag.'},
 'status_has_all_tags': {'example': '1. Has All "stunned, poisoned" -> Execute\n'
                                    '2. Has All "buff1, buff2" -> Transform',
                         'tip': 'Returns True only if the character has every one of the comma-separated tags. Data '
                                'inputs: target (object), tags (string). Data outputs: result (boolean). Settings: '
                                'tags.'},
 'status_has_any': {'example': '1. Has Any Status -> True -> Cleanse\n2. Has Any Status -> False -> Move',
                    'tip': 'Returns True if the character has any active engine status effect at all. Data inputs: '
                           'target (object). Data outputs: result (boolean). Settings: statuses.'},
 'status_has_any_tag': {'example': '1. Has Any "boss, elite" -> True\n2. Has Any "poison, burn" -> Heal',
                        'tip': 'Returns True if the character has at least one of the comma-separated tags. Data '
                               'inputs: target (object), tags (string). Data outputs: result (boolean). Settings: '
                               'tags.'},
 'status_tag_count': {'example': '1. Tag Count > 3 -> Cleanse\n2. Tag Count -> Multiply Damage',
                      'tip': 'Returns the total number of tags currently applied to a character. Data inputs: target '
                             '(object). Data outputs: count (number).'},
 'status_timed_modifier': {'example': '1. Timed Modifier (Speed, +50, 3s)\n2. Timed Modifier (Damage, *2.0, 5s)',
                           'tip': 'Applies a temporary stat boost or penalty that automatically reverts after the '
                                  'duration. Execution input: exec. Execution output: exec. Data inputs: target '
                                  '(object). Settings: stat, amount, duration, multiply. Use the white execution '
                                  'path for ordering and the colored pins for values.'},
 'status_toggle_tag': {'example': '1. Toggle a "shielded" tag every time a cooldown finishes\n2. Toggle "aggro"',
                       'tip': 'Adds a tag if it is absent, removes it if it is present -- a flip-flop tag. Execution '
                              'input: exec. Execution output: exec. Data inputs: target (object), tag (string). '
                              'Settings: tag. Use the white execution path for ordering and the colored pins for '
                              'values.'},
 'swarm_count_allies': {'example': '1. Count Allies < 3 -> Spawn Swarm\n2. Count Allies > 10 -> Boss Enrage',
                        'tip': 'Returns the number of allied characters within a radius. Data outputs: count '
                               '(number). Settings: radius.'},
 'swarm_count_by_team': {'example': '1. If Enemy Count > 5 -> Trigger AoE blast\n2. Ally Count < 2 -> Flee',
                         'tip': 'Counts how many allies or enemies are within a radius without building a full list. '
                                'Data inputs: center (vector), radius (number, default=0). Data outputs: count '
                                '(number). Settings: team_filter.'},
 'swarm_pheromone': {'example': '1. Pheromone (Target Pos) -> Minions Move Toward Pheromone\n2. Leave Trail',
                     'tip': 'Drops an invisible trail marker that swarm allies can track and move toward. Execution '
                            'input: exec. Execution output: exec. Data inputs: position (vector). Settings: tag, '
                            'duration. Use the white execution path for ordering and the colored pins for values.'},
 'swarm_regroup': {'example': '1. HP < 30% -> Swarm Regroup\n2. Boss Shield phase -> Regroup',
                   'tip': 'Commands all swarm members to move back toward their summoner. Execution input: exec. '
                          'Execution output: exec. Settings: radius, force. Use the white execution path for '
                          'ordering and the colored pins for values.'},
 'swarm_share_target': {'example': '1. Share Target (Nearest Enemy) -> Minions attack together\n'
                                   '2. Boss -> Share Target',
                        'tip': 'Forces all swarm members with the same team to attack the same target. Execution '
                               'input: exec. Execution output: exec. Data inputs: target (object). Use the white '
                               'execution path for ordering and the colored pins for values.'},
 'swarm_spawn': {'example': '1. Mitosis: On Death -> Spawn Swarm (2)\n2. Split into smaller slimes',
                 'tip': 'Spawns N clones of this character nearby. Each clone runs the same script independently. '
                        'Execution input: exec. Execution output: exec. Data inputs: count (number, default=5), '
                        'radius (number, default=50). Data outputs: spawned (any). Settings: count, radius. Use the '
                        'white execution path for ordering and the colored pins for values.'},
 'swarm_spawn_library': {'example': '1. Queen: Spawn Library Character ("Ant Minion", count=5)\n'
                                    '2. Necromancer -> Spawn "Skeleton" (3)',
                         'tip': 'Spawns multiple copies of a named library character nearby. Execution input: exec. '
                                "Execution output: exec. Data inputs: character (string, default=''), count (number, "
                                'default=5), radius (number, default=50). Data outputs: spawned (any). Settings: '
                                'character, count, radius. Use the white execution path for ordering and the colored '
                                'pins for values.'},
 'swarm_split_death': {'example': '1. On Death -> Split Death (2, scale 0.5)\n2. Slime split mechanic',
                       'tip': 'Spawns smaller scaled copies of this character when it dies.'},
 'sys_cpu_temp': {'example': '1. System heat', 'tip': 'Alias for Temp Sensor. Data outputs: Temp (number).'},
 'sys_dump_mem': {'example': '1. Check leaks',
                  'tip': 'Prints the global memory dictionary length. Execution input: exec. Execution output: exec. '
                         'Use the white execution path for ordering and the colored pins for values.'},
 'sys_kill_proc': {'example': '1. Delete enemy',
                   'tip': 'Instantly sets character HP to 0. Execution input: exec. Execution output: exec. Data '
                          'inputs: Character (object). Use the white execution path for ordering and the colored '
                          'pins for values.'},
 'sys_load_disk': {'example': '1. Read save file',
                   'tip': 'Loads integer from simulated disk. Data inputs: Slot (number). Data outputs: Value '
                          '(number).'},
 'sys_ping': {'example': '1. Check alive',
              'tip': 'Checks if a character exists. Returns bool. Data inputs: Character (object). Data outputs: '
                     'Exists (boolean).'},
 'sys_reboot': {'example': '1. Hard reset',
                'tip': 'Heals all characters to max HP instantly. Execution input: exec. Execution output: exec. Use '
                       'the white execution path for ordering and the colored pins for values.'},
 'sys_save_disk': {'example': '1. Write save file',
                   'tip': 'Saves integer to simulated disk. Execution input: exec. Execution output: exec. Data '
                          'inputs: Slot (number), Value (number). Use the white execution path for ordering and the '
                          'colored pins for values.'},
 'sys_stack_trace': {'example': '1. Error reading',
                     'tip': 'Returns current character state dump. Data inputs: Character (object). Data outputs: '
                            'Trace (string).'},
 'sys_syslog': {'example': '1. Print debug',
                'tip': 'Logs a message to the debug toast with system prefix. Execution input: exec. Execution '
                       'output: exec. Data inputs: Message (string). Use the white execution path for ordering and '
                       'the colored pins for values.'},
 'sys_watchdog': {'example': '1. System crash protection',
                  'tip': 'If not fed for 5s, triggers Reset. Execution input: exec. Execution output: Normal, Reset. '
                         'Data inputs: Feed (boolean). Use the white execution path for ordering and the colored '
                         'pins for values.'},
 'tag_wait_until_removed': {'example': '1. Wait Until "shielded" removed -> Deal Damage\n'
                                       '2. Wait Until "stun" removed -> Attack',
                            'tip': 'Pauses this execution branch until the target loses the specified tag. Execution '
                                   'input: exec. Execution output: exec. Data inputs: target (object), tag (string). '
                                   'Settings: tag. Use the white execution path for ordering and the colored pins '
                                   'for values.'},
 'tag_wait_until_set': {'example': '1. Wait Until "enraged" -> then trigger massive explosion\n'
                                   '2. Wait Until "healed" -> Move Away',
                        'tip': 'Pauses this execution branch until the target gains the specified tag. Execution '
                               'input: exec. Execution output: exec. Data inputs: target (object), tag (string). '
                               'Settings: tag. Use the white execution path for ordering and the colored pins for '
                               'values.'},
 'target_all_in_range': {'example': '1. All Enemies in 200 -> For Each -> Deal Damage\n'
                                    '2. All Allies in 500 -> For Each -> Add Shield',
                         'tip': 'Get a list for For Each. Max distance 0 means the whole arena. Data inputs: origin '
                                '(object), min_distance (number, default=0.0), max_distance (number, default=0.0). '
                                'Data outputs: characters (object). Settings: min_distance, max_distance, '
                                'include_self.'},
 'target_character_position': {'example': '1. Character Position -> Move Toward\n'
                                          '2. Character Position -> Spawn Particle',
                               'tip': "Get a character's world position for particles, teleporting, or distance "
                                      'logic. Data inputs: character (object). Data outputs: position (vector).'},
 'target_event_other': {'example': '1. On Hit -> Deal Damage to Event Other\n'
                                   '2. On Collision -> Knockback Event Other',
                        'tip': 'The other character supplied by On Hit, Damage, Kill, or Collision. Data outputs: '
                               'character (object).'},
 'target_facing_me': {'example': '1. Use to trigger block/parry logic only when attacked from the front\n'
                                 '2. Enemies Facing Me -> Deal Damage (Frontal cone logic)',
                      'tip': 'Returns characters that are actively moving toward or looking at this character. Data '
                             'inputs: radius (number, default=0). Data outputs: characters (any). Settings: '
                             'team_filter.'},
 'target_filter_list': {'example': '1. Filter List: HP < 50. Use "filtered_list" in a For Each loop\n'
                                   '2. Filter List: Tag has "poisoned" -> First Match -> Execute',
                        'tip': 'Takes a list of characters and filters it down based on a condition. Data inputs: '
                               'list (any). Data outputs: filtered_list (any), first_match (object). Settings: '
                               'property, operation, value_num, value_str.'},
 'target_find_random_opponent': {'example': '1. Find Random Opponent -> Found -> Move Toward\n'
                                            '2. Not Found -> Random Wander',
                                 'tip': 'Execution search with Found/Not Found branches, target, position, distance, '
                                        'and candidate count. Execution input: exec. Execution output: found, '
                                        'not_found. Data inputs: origin (object), min_distance (number, '
                                        "default=0.0), max_distance (number, default=0.0), tag (string, default=''), "
                                        "name (string, default=''). Data outputs: target (object), position "
                                        '(vector), distance (number), candidate_count (number). Settings: '
                                        'min_distance, max_distance, identify_by, team_filter, tag, name, '
                                        'fallback_any, include_self. Use the white execution path for ordering and '
                                        'the colored pins for values.'},
 'target_highest_threat': {'example': '1. Tanks: Highest Threat Enemy -> Taunt\n'
                                      '2. Highest Threat Enemy -> Focus Fire',
                           'tip': 'Returns the character with the highest threat score in the search radius. Data '
                                  'inputs: center (vector), radius (number, default=0). Data outputs: character '
                                  '(object). Settings: team_filter.'},
 'target_hp_percent': {'example': '1. Use "< 50%" to find wounded enemies, then plug the list into a For Each loop\n'
                                  '2. Allies < 20% -> For Each -> Heal',
                       'tip': 'Filters or finds targets based on their remaining HP as a percentage of maximum. Data '
                              'inputs: center (vector), radius (number, default=0), percent (number, default=50). '
                              'Data outputs: characters (any). Settings: operation, percent, team_filter.'},
 'target_line_of_sight': {'example': '1. Line of Sight (Me, Target) -> True -> Ranged Attack\n'
                                     '2. False -> Move Toward Target',
                          'tip': 'Returns True if there is a clear unobstructed path between two characters. Data '
                                 'inputs: a (object), b (object). Data outputs: visible (boolean).'},
 'target_lowest_hp': {'example': '1. Healers: "Lowest HP Ally" -> Heal\n'
                                 '2. Assassins: "Lowest HP Enemy" -> Move Toward',
                      'tip': 'Returns the character with the least HP in the search radius. Data inputs: center '
                             '(vector), radius (number, default=0). Data outputs: character (object). Settings: '
                             'team_filter.'},
 'target_my_last_attacker': {'example': '1. Link "On Damage Taken" -> "Get Last Attacker" -> "Deal Damage" to '
                                        'counter-attack\n'
                                        '2. Get Last Attacker -> Move Toward',
                             'tip': 'Returns the character that most recently dealt damage to this one. Data '
                                    'outputs: attacker (object).'},
 'target_my_summoner': {'example': '1. Minions can use "Move Toward" -> "My Summoner" to stay close to their boss\n'
                                   '2. My Summoner -> Heal',
                        'tip': 'Returns the character that spawned this one via Swarm or Clone. Data outputs: '
                               'summoner (object).'},
 'target_nearest_in_range': {'example': '1. Nearest Enemy -> Move Toward\n2. Nearest Ally -> Heal',
                             'tip': 'Find the nearest living character in a distance range. Max 0 is unlimited. Data '
                                    'inputs: origin (object), min_distance (number, default=0.0), max_distance '
                                    '(number, default=0.0). Data outputs: character (object). Settings: '
                                    'min_distance, max_distance, include_self.'},
 'target_not_facing_me': {'example': '1. Synergizes perfectly with "Backstab" damage multipliers\n'
                                     '2. Enemies Not Facing Me -> For Each -> Execute',
                          'tip': 'Returns characters that are moving away from or ignoring this character. Data '
                                 'inputs: radius (number, default=0). Data outputs: characters (any). Settings: '
                                 'team_filter.'},
 'target_random_in_range': {'example': '1. Random In Range (500) -> Move Toward\n2. Random In Range -> Deal Damage',
                            'tip': 'Pick a random living character between min and max distance from origin. Max 0 '
                                   'is unlimited. Data inputs: origin (object), min_distance (number, default=0.0), '
                                   'max_distance (number, default=0.0). Data outputs: character (object). Settings: '
                                   'min_distance, max_distance, team_filter, fallback_any, include_self.'},
 'target_random_point': {'example': '1. Feed this into "Dash To Position" or "Move Toward" to wander randomly\n'
                                    '2. Random Point -> Spawn Explosion',
                         'tip': 'Returns a random X,Y world position within a given radius of a center. Data inputs: '
                                'center (vector), radius (number, default=100). Data outputs: point (vector). '
                                'Settings: radius.'},
 'target_self': {'example': '1. Heal -> Self\n2. Get Position -> Self',
                 'tip': 'The character that owns and is running this blueprint. Data outputs: character (object).'},
 'target_validate': {'example': '1. Validate Target -> Valid -> Deal Damage\n2. Invalid -> Find New Target',
                     'tip': 'Gate any target-based action through Valid/Invalid execution branches. Execution input: '
                            'exec. Execution output: valid, invalid. Data inputs: target (object). Data outputs: '
                            'target (object), position (vector). Use the white execution path for ordering and the '
                            'colored pins for values.'},
 'timing_cooldown': {'example': '1. On Hit -> Cooldown (1s) -> Play Sound (prevents sound spam)\n'
                                '2. Every Frame -> Cooldown (3s) -> Spawn Swarm',
                     'tip': 'Lets execution through once, then blocks all retriggers for the duration. Prevents '
                            'ability spam. Execution input: exec. Execution output: exec. Data inputs: duration '
                            '(number, default=1.0). Data outputs: ready (boolean). Settings: duration. Use the white '
                            'execution path for ordering and the colored pins for values.'},
 'timing_countdown': {'example': '1. On Spawn -> Countdown (10s) -> Despawn\n'
                                 '2. Read "Progress" (0.0 to 1.0) into a Lerp node to fade a color',
                      'tip': 'A timer that counts down from a duration and fires when it hits zero. Outputs '
                             'Remaining and Progress (0-1). Execution input: exec. Execution output: exec. Data '
                             'inputs: duration (number, default=5.0). Data outputs: remaining (number), progress '
                             '(number). Settings: duration. Use the white execution path for ordering and the '
                             'colored pins for values.'},
 'timing_debounce': {'example': '1. Prevent 10 bullets hitting at once from triggering 10 "On Hit" sounds\n'
                                '2. On Collision -> Debounce (0.5s) -> Knockback',
                     'tip': 'Ignores retriggers that happen faster than the cooldown -- prevents event flooding. '
                            'Execution input: exec. Execution output: exec. Data inputs: duration (number, '
                            'default=1.0). Settings: duration. Use the white execution path for ordering and the '
                            'colored pins for values.'},
 'timing_elapsed_match_time': {'example': '1. Scale boss damage up by elapsed time\n'
                                          '2. If Elapsed Time > 60s -> Spawn Enraged Clones',
                               'tip': 'Returns the total seconds the current simulation has been running. Data '
                                      'outputs: time (number).'},
 'timing_every_frame': {'example': '1. Every Frame -> Move Toward (Target)\n2. Every Frame -> Face Target',
                        'tip': 'Fires its execution pin every single simulation frame (~60/s). Use for continuous '
                               'movement, facing, and real-time checks. Execution output: exec. Use the white '
                               'execution path for ordering and the colored pins for values.'},
 'timing_every_second': {'example': '1. Every Second -> Deal Damage (Target=Self, amount=5) for a basic DoT\n'
                                    '2. Every Second -> Increment Variable ("time_survived")',
                         'tip': 'Executes exactly once per real-time second. Good for DoT ticks, score counters, and '
                                'slow repeating logic. Execution input: exec. Execution output: exec. Settings: '
                                'interval. Use the white execution path for ordering and the colored pins for '
                                'values.'},
 'timing_every_x_seconds': {'example': '1. Every 2.5s -> Spawn Particle\n2. Every 5s -> Random Wander',
                            'tip': 'Fires at a custom interval you set. The go-to node for standard repeating '
                                   'abilities. Execution input: exec. Execution output: exec. Data inputs: interval '
                                   '(number, default=2.0). Settings: interval, variation. Use the white execution '
                                   'path for ordering and the colored pins for values.'},
 'timing_fuse': {'example': '1. On Spawn -> Fuse Timer (3s) -> Spawn Explosion\n'
                            '2. On Death -> Fuse Timer (1.5s) -> Despawn Character',
                 'tip': 'Wait for a fuse duration, then continue into an explosion or any other node. Settings: '
                        'duration.'},
 'timing_loop_while_active': {'example': '1. While moving -> Loop While Active -> Spawn "dust" particles\n'
                                         '2. Loop While Active -> Move Toward Target',
                              'tip': 'Runs its body every frame as long as it has been started and not stopped. '
                                     'Persistent looping effects. Execution input: exec. Execution output: exec, '
                                     'inactive. Data inputs: active (boolean, default=True). Settings: '
                                     'active_on_start. Use the white execution path for ordering and the colored '
                                     'pins for values.'},
 'timing_once': {'example': '1. Phase transitions (e.g. 50% HP -> Transform into Phase 2)\n'
                            '2. On Spawn -> Once -> Broadcast "Boss Appeared"',
                 'tip': 'Only allows execution to pass through one single time per character lifetime. Execution '
                        'input: exec, reset. Execution output: exec. Use the white execution path for ordering and '
                        'the colored pins for values.'},
 'timing_random_chance_gate': {'example': '1. On Kill -> 20% chance to drop health pack\n'
                                          '2. On Hit -> 5% chance to instantly Execute',
                               'tip': 'Splits execution into Success or Failure based on a random percentage roll. '
                                      'Execution input: exec. Execution output: success, failure. Data inputs: '
                                      'chance (number, default=50). Settings: chance. Use the white execution path '
                                      'for ordering and the colored pins for values.'},
 'timing_repeat': {'example': '1. Repeat (5) -> Spawn Particle (burst of 5 particles)\n'
                              '2. Repeat (3) -> Spawn Library Character',
                   'tip': 'Fires its body N times instantly -- equivalent to a For loop. Spawns, burst attacks, '
                          'multi-hit combos. Execution input: exec. Execution output: exec, completed. Data inputs: '
                          'count (number, default=3). Data outputs: index (number). Settings: count. Use the white '
                          'execution path for ordering and the colored pins for values.'},
 'timing_repeat_for_duration': {'example': '1. Machine Gun attack: Repeat 0.1s for 2.0s -> Deal Damage\n'
                                           '2. Healing beam: Repeat 0.5s for 5.0s -> Heal Ally',
                                'tip': 'Fires its body at an interval for a set total duration, then stops. '
                                       'Machine-gun attacks, healing beams. Execution input: exec. Execution output: '
                                       'tick, finished. Data inputs: interval (number, default=3.0), duration '
                                       '(number, default=60.0). Settings: interval, duration. Use the white '
                                       'execution path for ordering and the colored pins for values.'},
 'timing_round_robin_sequence': {'example': '1. Three-hit combo: Swing Left, Swing Right, Heavy Slam\n'
                                            '2. On Hit -> Round Robin -> Play "hit1.wav", "hit2.wav", "hit3.wav"',
                                 'tip': 'Cycles through outputs in order each time triggered -- 1st call fires 0, '
                                        '2nd fires 1, then loops. Execution input: exec. Settings: count. Use the '
                                        'white execution path for ordering and the colored pins for values.'},
 'timing_sequence': {'example': '1. On Spawn -> Sequence. [0] -> Set HP. [1] -> Play Sound. [2] -> Set Sprite\n'
                                '2. On Kill -> Sequence [0] -> Lifesteal. [1] -> Broadcast Event',
                     'tip': "Fires multiple execution outputs sequentially in one frame -- like Unreal's Sequence "
                            'node. Execution input: exec. Settings: count. Use the white execution path for ordering '
                            'and the colored pins for values.'},
 'timing_stopwatch': {'example': '1. On Hit -> Start. On Idle -> Stop. Use "Elapsed" to see combat time\n'
                                 '2. Stopwatch -> Compare Number -> Deal Damage',
                      'tip': 'A toggleable elapsed-time counter. Wire Start/Stop pins to control it, read Elapsed '
                             'for the result. Execution input: exec, start, stop. Data outputs: elapsed (number), '
                             'running (boolean). Settings: autostart. Use the white execution path for ordering and '
                             'the colored pins for values.'},
 'timing_timeline': {'example': '1. Timeline (2s) -> Math Lerp (10 to 50) -> Scale\n'
                                '2. Timeline (1s) -> Math Lerp Color -> Tint Character',
                     'tip': 'Outputs a smooth 0.0-1.0 value over a duration. Feed it into Lerp for animations, '
                            'fades, and scaling. Execution input: exec. Execution output: completed. Data inputs: '
                            'duration (number, default=2.0). Data outputs: progress (number). Settings: duration. '
                            'Use the white execution path for ordering and the colored pins for values.'},
 'tween_value': {'example': '1. Tween scale 1.0→2.0 over 0.3s for spawn pop\n'
                            '2. Tween opacity 255→0 for fade-out death',
                 'tip': 'Animates a local variable from A to B over a duration using an easing curve. Every frame '
                        'the variable gets closer to the target — like Godot Tween.tween_property(). Execution '
                        'input: exec. Execution output: exec, done. Data inputs: target (object), from_val (number, '
                        'default=0), to_val (number, default=1), duration (number, default=1.0). Data outputs: value '
                        '(number). Settings: var_name, duration, easing. Use the white execution path for ordering '
                        'and the colored pins for values.'},
 'unity_add_force': {'example': '1. Add Unity Add Force from the Unity Physics category.\n'
                                '2. Connect the available inputs.\n'
                                '3. Use the output in the next calculation or condition.',
                     'tip': 'Apply a force using ForceMode semantics.'},
 'unity_add_relative_force': {'example': '1. Add Unity Add Relative Force from the Unity Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Apply force in local body axes.'},
 'unity_add_relative_torque': {'example': '1. Add Unity Add Relative Torque from the Unity Physics category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Apply local-space torque.'},
 'unity_add_torque': {'example': '1. Add Unity Add Torque from the Unity Physics category.\n'
                                 '2. Connect the available inputs.\n'
                                 '3. Use the output in the next calculation or condition.',
                      'tip': 'Apply rotational torque.'},
 'unity_auto_sync_transforms': {'example': '1. Add Unity Auto Sync Transforms from the Unity Physics category.\n'
                                           '2. Connect the available inputs.\n'
                                           '3. Use the output in the next calculation or condition.',
                                'tip': 'Toggle transform synchronization.'},
 'unity_box_cast': {'example': '1. Add Unity Box Cast from the Unity Physics category.\n'
                               '2. Connect the available inputs.\n'
                               '3. Use the output in the next calculation or condition.',
                    'tip': 'Cast a swept box.'},
 'unity_capsule_cast': {'example': '1. Add Unity Capsule Cast from the Unity Physics category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Cast a swept capsule.'},
 'unity_closest_point': {'example': '1. Add Unity Closest Point from the Unity Physics category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Find the closest point on a collider.'},
 'unity_collision_enter': {'example': '1. Add Unity Collision Enter from the Unity Physics category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Gate when collision begins.'},
 'unity_collision_exit': {'example': '1. Add Unity Collision Exit from the Unity Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Gate when collision ends.'},
 'unity_collision_stay': {'example': '1. Add Unity Collision Stay from the Unity Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Gate while collision continues.'},
 'unity_compute_penetration': {'example': '1. Add Unity Compute Penetration from the Unity Physics category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Calculate separation direction/depth.'},
 'unity_get_contacts': {'example': '1. Add Unity Get Contacts from the Unity Physics category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Read current contact list.'},
 'unity_get_point_velocity': {'example': '1. Add Unity Get Point Velocity from the Unity Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Read velocity at a world point.'},
 'unity_get_relative_point_velocity': {'example': '1. Add Unity Get Relative Point Velocity from the Unity Physics '
                                                  'category.\n'
                                                  '2. Connect the available inputs.\n'
                                                  '3. Use the output in the next calculation or condition.',
                                       'tip': 'Read local point velocity.'},
 'unity_ignore_collision': {'example': '1. Add Unity Ignore Collision from the Unity Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Ignore a collider pair.'},
 'unity_is_sleeping': {'example': '1. Add Unity Is Sleeping from the Unity Physics category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Read rigidbody sleep state.'},
 'unity_material_bounce': {'example': '1. Add Unity Material Bounce from the Unity Physics category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Set bounciness.'},
 'unity_material_friction': {'example': '1. Add Unity Material Friction from the Unity Physics category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Set static/dynamic friction.'},
 'unity_move_position': {'example': '1. Add Unity Move Position from the Unity Physics category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Move the rigidbody for kinematic motion.'},
 'unity_move_rotation': {'example': '1. Add Unity Move Rotation from the Unity Physics category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Move rotation for kinematic motion.'},
 'unity_overlap_box': {'example': '1. Add Unity Overlap Box from the Unity Physics category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Return colliders inside a box.'},
 'unity_overlap_sphere': {'example': '1. Add Unity Overlap Sphere from the Unity Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Return colliders inside a sphere.'},
 'unity_raycast': {'example': '1. Add Unity Raycast from the Unity Physics category.\n'
                              '2. Connect the available inputs.\n'
                              '3. Use the output in the next calculation or condition.',
                   'tip': 'Cast a physics ray.'},
 'unity_set_angular_drag': {'example': '1. Add Unity Set Angular Drag from the Unity Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Set angular drag.'},
 'unity_set_center_of_mass': {'example': '1. Add Unity Set Center Of Mass from the Unity Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Offset the center of mass.'},
 'unity_set_collision_detection': {'example': '1. Add Unity Set Collision Detection from the Unity Physics '
                                              'category.\n'
                                              '2. Connect the available inputs.\n'
                                              '3. Use the output in the next calculation or condition.',
                                   'tip': 'Choose discrete/continuous detection.'},
 'unity_set_constraints': {'example': '1. Add Unity Set Constraints from the Unity Physics category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Freeze selected position or rotation axes.'},
 'unity_set_drag': {'example': '1. Add Unity Set Drag from the Unity Physics category.\n'
                               '2. Connect the available inputs.\n'
                               '3. Use the output in the next calculation or condition.',
                    'tip': 'Set linear drag.'},
 'unity_set_interpolation': {'example': '1. Add Unity Set Interpolation from the Unity Physics category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Choose none/interpolate/extrapolate.'},
 'unity_set_is_kinematic': {'example': '1. Add Unity Set Is Kinematic from the Unity Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Switch dynamic/kinematic behavior.'},
 'unity_set_layer_collision': {'example': '1. Add Unity Set Layer Collision from the Unity Physics category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Enable/disable layer pair collisions.'},
 'unity_set_mass': {'example': '1. Add Unity Set Mass from the Unity Physics category.\n'
                               '2. Connect the available inputs.\n'
                               '3. Use the output in the next calculation or condition.',
                    'tip': 'Set rigidbody mass.'},
 'unity_set_max_angular_velocity': {'example': '1. Add Unity Set Max Angular Velocity from the Unity Physics '
                                               'category.\n'
                                               '2. Connect the available inputs.\n'
                                               '3. Use the output in the next calculation or condition.',
                                    'tip': 'Cap spin speed.'},
 'unity_set_use_gravity': {'example': '1. Add Unity Set Use Gravity from the Unity Physics category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Enable or disable gravity.'},
 'unity_sleep': {'example': '1. Add Unity Sleep from the Unity Physics category.\n'
                            '2. Connect the available inputs.\n'
                            '3. Use the output in the next calculation or condition.',
                 'tip': 'Put the rigidbody to sleep.'},
 'unity_sphere_cast': {'example': '1. Add Unity Sphere Cast from the Unity Physics category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Cast a swept sphere.'},
 'unity_sync_transforms': {'example': '1. Add Unity Sync Transforms from the Unity Physics category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Force physics transform sync.'},
 'unity_trigger_enter': {'example': '1. Add Unity Trigger Enter from the Unity Physics category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Gate when entering a trigger.'},
 'unity_trigger_exit': {'example': '1. Add Unity Trigger Exit from the Unity Physics category.\n'
                                   '2. Connect the available inputs.\n'
                                   '3. Use the output in the next calculation or condition.',
                        'tip': 'Gate when leaving a trigger.'},
 'unity_wake_up': {'example': '1. Add Unity Wake Up from the Unity Physics category.\n'
                              '2. Connect the available inputs.\n'
                              '3. Use the output in the next calculation or condition.',
                   'tip': 'Wake the rigidbody.'},
 'unreal_add_controller_pitch': {'example': '1. Add Unreal Add Controller Pitch from the Unreal Physics category.\n'
                                            '2. Connect the available inputs.\n'
                                            '3. Use the output in the next calculation or condition.',
                                 'tip': 'Apply pitch input.'},
 'unreal_add_controller_yaw': {'example': '1. Add Unreal Add Controller Yaw from the Unreal Physics category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Apply yaw input.'},
 'unreal_add_movement_input': {'example': '1. Add Unreal Add Movement Input from the Unreal Physics category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Add movement input in a direction.'},
 'unreal_box_trace': {'example': '1. Add Unreal Box Trace from the Unreal Physics category.\n'
                                 '2. Connect the available inputs.\n'
                                 '3. Use the output in the next calculation or condition.',
                      'tip': 'Trace a swept box.'},
 'unreal_can_crouch': {'example': '1. Add Unreal Can Crouch from the Unreal Physics category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Check crouch availability.'},
 'unreal_capsule_trace': {'example': '1. Add Unreal Capsule Trace from the Unreal Physics category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use the output in the next calculation or condition.',
                          'tip': 'Trace a swept capsule.'},
 'unreal_crouch': {'example': '1. Add Unreal Crouch from the Unreal Physics category.\n'
                              '2. Connect the available inputs.\n'
                              '3. Use the output in the next calculation or condition.',
                   'tip': 'Enter crouched movement.'},
 'unreal_get_current_acceleration': {'example': '1. Add Unreal Get Acceleration from the Unreal Physics category.\n'
                                                '2. Connect the available inputs.\n'
                                                '3. Use the output in the next calculation or condition.',
                                     'tip': 'Read current acceleration.'},
 'unreal_get_floor_result': {'example': '1. Add Unreal Get Floor Result from the Unreal Physics category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Read floor hit information.'},
 'unreal_get_last_input_vector': {'example': '1. Add Unreal Get Last Input Vector from the Unreal Physics category.\n'
                                             '2. Connect the available inputs.\n'
                                             '3. Use the output in the next calculation or condition.',
                                  'tip': 'Read previous movement input.'},
 'unreal_get_movement_base': {'example': '1. Add Unreal Get Movement Base from the Unreal Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Read supporting platform.'},
 'unreal_get_velocity': {'example': '1. Add Unreal Get Velocity from the Unreal Physics category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Read character velocity.'},
 'unreal_is_falling': {'example': '1. Add Unreal Is Falling from the Unreal Physics category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Read falling state.'},
 'unreal_is_flying': {'example': '1. Add Unreal Is Flying from the Unreal Physics category.\n'
                                 '2. Connect the available inputs.\n'
                                 '3. Use the output in the next calculation or condition.',
                      'tip': 'Read flying state.'},
 'unreal_is_moving_on_ground': {'example': '1. Add Unreal Is Moving On Ground from the Unreal Physics category.\n'
                                           '2. Connect the available inputs.\n'
                                           '3. Use the output in the next calculation or condition.',
                                'tip': 'Read grounded movement state.'},
 'unreal_jump': {'example': '1. Add Unreal Jump from the Unreal Physics category.\n'
                            '2. Connect the available inputs.\n'
                            '3. Use the output in the next calculation or condition.',
                 'tip': 'Trigger a character jump.'},
 'unreal_launch_character': {'example': '1. Add Unreal Launch Character from the Unreal Physics category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Launch with velocity and override flags.'},
 'unreal_line_trace': {'example': '1. Add Unreal Line Trace from the Unreal Physics category.\n'
                                  '2. Connect the available inputs.\n'
                                  '3. Use the output in the next calculation or condition.',
                       'tip': 'Trace a line and return hit data.'},
 'unreal_multisphere_trace': {'example': '1. Add Unreal Multi Sphere Trace from the Unreal Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Return every hit in a sphere sweep.'},
 'unreal_ragdoll': {'example': '1. Add Unreal Ragdoll from the Unreal Physics category.\n'
                               '2. Connect the available inputs.\n'
                               '3. Use the output in the next calculation or condition.',
                    'tip': 'Switch body to ragdoll-like dynamic motion.'},
 'unreal_set_air_control': {'example': '1. Add Unreal Air Control from the Unreal Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Set midair steering.'},
 'unreal_set_braking_deceleration': {'example': '1. Add Unreal Braking Deceleration from the Unreal Physics '
                                                'category.\n'
                                                '2. Connect the available inputs.\n'
                                                '3. Use the output in the next calculation or condition.',
                                     'tip': 'Set braking force.'},
 'unreal_set_capsule_half_height': {'example': '1. Add Unreal Capsule Height from the Unreal Physics category.\n'
                                               '2. Connect the available inputs.\n'
                                               '3. Use the output in the next calculation or condition.',
                                    'tip': 'Resize character capsule.'},
 'unreal_set_gravity_scale': {'example': '1. Add Unreal Gravity Scale from the Unreal Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Scale character gravity.'},
 'unreal_set_jump_velocity': {'example': '1. Add Unreal Jump Velocity from the Unreal Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Set jump launch velocity.'},
 'unreal_set_max_acceleration': {'example': '1. Add Unreal Max Acceleration from the Unreal Physics category.\n'
                                            '2. Connect the available inputs.\n'
                                            '3. Use the output in the next calculation or condition.',
                                 'tip': 'Set acceleration cap.'},
 'unreal_set_max_walk_speed': {'example': '1. Add Unreal Max Walk Speed from the Unreal Physics category.\n'
                                          '2. Connect the available inputs.\n'
                                          '3. Use the output in the next calculation or condition.',
                               'tip': 'Set walk speed.'},
 'unreal_set_movement_base': {'example': '1. Add Unreal Set Movement Base from the Unreal Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Assign supporting platform.'},
 'unreal_set_movement_mode': {'example': '1. Add Unreal Set Movement Mode from the Unreal Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Set walking/falling/flying/swimming mode.'},
 'unreal_set_network_smoothing': {'example': '1. Add Unreal Network Smoothing from the Unreal Physics category.\n'
                                             '2. Connect the available inputs.\n'
                                             '3. Use the output in the next calculation or condition.',
                                  'tip': 'Tune movement smoothing.'},
 'unreal_set_orient_rotation': {'example': '1. Add Unreal Orient Rotation from the Unreal Physics category.\n'
                                           '2. Connect the available inputs.\n'
                                           '3. Use the output in the next calculation or condition.',
                                'tip': 'Toggle facing from movement.'},
 'unreal_set_physics_blend': {'example': '1. Add Unreal Physics Blend from the Unreal Physics category.\n'
                                         '2. Connect the available inputs.\n'
                                         '3. Use the output in the next calculation or condition.',
                              'tip': 'Blend animation and physics control.'},
 'unreal_set_root_motion': {'example': '1. Add Unreal Root Motion from the Unreal Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Toggle animation root motion.'},
 'unreal_set_use_controller_rotation': {'example': '1. Add Unreal Controller Rotation from the Unreal Physics '
                                                   'category.\n'
                                                   '2. Connect the available inputs.\n'
                                                   '3. Use the output in the next calculation or condition.',
                                        'tip': 'Toggle controller-driven rotation.'},
 'unreal_set_walkable_floor_angle': {'example': '1. Add Unreal Walkable Floor Angle from the Unreal Physics '
                                                'category.\n'
                                                '2. Connect the available inputs.\n'
                                                '3. Use the output in the next calculation or condition.',
                                     'tip': 'Set slope angle.'},
 'unreal_sleep_all_bodies': {'example': '1. Add Unreal Sleep All Bodies from the Unreal Physics category.\n'
                                        '2. Connect the available inputs.\n'
                                        '3. Use the output in the next calculation or condition.',
                             'tip': 'Sleep a body hierarchy.'},
 'unreal_sphere_trace': {'example': '1. Add Unreal Sphere Trace from the Unreal Physics category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Trace a swept sphere.'},
 'unreal_stop_jumping': {'example': '1. Add Unreal Stop Jumping from the Unreal Physics category.\n'
                                    '2. Connect the available inputs.\n'
                                    '3. Use the output in the next calculation or condition.',
                         'tip': 'Stop a held jump.'},
 'unreal_sweep_movement': {'example': '1. Add Unreal Sweep Movement from the Unreal Physics category.\n'
                                      '2. Connect the available inputs.\n'
                                      '3. Use the output in the next calculation or condition.',
                           'tip': 'Move with collision sweep.'},
 'unreal_uncrouch': {'example': '1. Add Unreal Uncrouch from the Unreal Physics category.\n'
                                '2. Connect the available inputs.\n'
                                '3. Use the output in the next calculation or condition.',
                     'tip': 'Leave crouched movement.'},
 'unreal_wake_all_bodies': {'example': '1. Add Unreal Wake All Bodies from the Unreal Physics category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use the output in the next calculation or condition.',
                            'tip': 'Wake a ragdoll/body hierarchy.'},
 'utility_assert': {'example': '1. Assert target != None before damage\n2. Assert hp > 0 at start of on_tick',
                    'tip': 'If the condition is False, raises an error and prints a message. Use during development '
                           'to catch logic bugs fast — remove before final use. Execution input: exec. Execution '
                           'output: exec. Data inputs: condition (boolean, default=True). Settings: message. Use the '
                           'white execution path for ordering and the colored pins for values.'},
 'utility_bool_to_string': {'example': "1. Has Tag -> Bool to String ('Has it'/'Nope') -> Print Value\n"
                                       '2. Is Moving -> Bool to String -> Format String',
                            'tip': "Converts True/False to a readable string. Outputs 'True'/'False' by default, or "
                                   "custom labels you set in the inspector (e.g. 'Yes'/'No', 'On'/'Off'). Data "
                                   'inputs: value (boolean, default=False). Data outputs: text (string). Settings: '
                                   'true_label, false_label.'},
 'utility_broadcast_event': {'example': '1. Queen broadcasts "focus_target". Minions use "On Broadcast" to attack\n'
                                        '2. Broadcast "retreat"',
                             'tip': 'Fires a named custom event to all nearby team members so they can react via On '
                                    'Broadcast. Execution input: exec. Execution output: exec. Data inputs: center '
                                    "(vector), radius (number, default=0), event_name (string, default='signal'), "
                                    'payload (any). Settings: event_name, team_filter. Use the white execution path '
                                    'for ordering and the colored pins for values.'},
 'utility_button': {'example': '1. Add Utility Button from the Utility category.\n'
                               '2. Connect value.\n'
                               '3. Use value, active in the next calculation or condition.',
                    'tip': 'A normal manual/procedural button source. Click it in Canvas Debug, or connect a white '
                           'trigger and a number value. Its Pressed output can run any action while Value carries '
                           'the number supplied to the button. Execution input: trigger. Execution output: pressed. '
                           'Data inputs: value (number, default=1.0). Data outputs: value (number), active '
                           '(boolean). Settings: label, mode, default_value. Use the white execution path for '
                           'ordering and the colored pins for values.'},
 'utility_clamp_damage': {'example': '1. Clamp Damage (Max 50) -> Boss mitigation\n2. Clamp Damage (Min 10)',
                          'tip': 'Caps incoming or outgoing damage to a min/max range. Data inputs: damage (number, '
                                 'default=0), min (number, default=0), max (number, default=9999). Data outputs: '
                                 'damage (number).'},
 'utility_comment': {'example': '1. Comment: "Movement Logic"\n2. Comment: "DO NOT EDIT"',
                     'tip': 'A visual sticky note on the graph. Does nothing at runtime. Use to label and organize '
                            'sections. Execution input: exec. Execution output: exec. Settings: text. Use the white '
                            'execution path for ordering and the colored pins for values.'},
 'utility_constant_boolean': {'example': '1. Constant(True) -> Enable Loop\n2. Constant(False)',
                              'tip': 'A hardcoded True or False value. Data outputs: value (boolean). Settings: '
                                     'value.'},
 'utility_constant_color': {'example': '1. Constant(Red) -> Tint\n2. Constant(Blue) -> Particle',
                            'tip': 'A hardcoded RGB color with an inline color-picker in the inspector. Data '
                                   'outputs: value (color). Settings: r, g, b.'},
 'utility_constant_float': {'example': '1. Add Constant Float from the Utility category.\n'
                                       '2. Connect the available inputs.\n'
                                       '3. Use value in the next calculation or condition.',
                            'tip': 'A hardcoded decimal number — always generates a float (e.g. 3.0, not 3). Use '
                                   'where a fractional value matters, like speed multipliers or scale. Data outputs: '
                                   'value (number). Settings: value.'},
 'utility_constant_int': {'example': '1. Add Constant Int from the Utility category.\n'
                                     '2. Connect the available inputs.\n'
                                     '3. Use value in the next calculation or condition.',
                          'tip': 'A hardcoded whole number — always generates an int (rounded, no decimal). Use '
                                 'where a value must be a count or index, like stack size or frame number. Data '
                                 'outputs: value (number). Settings: value.'},
 'utility_constant_number': {'example': '1. Constant(50) -> Radius\n2. Constant(1.5) -> Duration',
                             'tip': 'A hardcoded number you type in. Drag the output wire to any numeric input. Data '
                                    'outputs: value (number). Settings: value.'},
 'utility_constant_string': {'example': '1. Constant("boss") -> Tag\n2. Constant("enemy") -> Team',
                             'tip': 'A hardcoded text string. Drag the output wire to any text input. Data outputs: '
                                    'value (string). Settings: value.'},
 'utility_constant_vector': {'example': '1. Constant(0,0) -> Center of arena\n2. Target position',
                             'tip': 'A hardcoded X,Y world coordinate. Data outputs: value (vector). Settings: x, '
                                    'y.'},
 'utility_format_string': {'example': '1. "HP: {0} / {1}" -> Print to screen\n'
                                      '2. "Phase {0} activated" -> debug toast',
                           'tip': "Builds a string from a template. Use {0}, {1}, {2} as placeholders: e.g. 'HP: {0} "
                                  "/ {1}'. Data inputs: a (any, default=0), b (any, default=0), c (any, default=0). "
                                  'Data outputs: text (string). Settings: template.'},
 'utility_get_hp': {'example': '1. Get HP -> percent -> Color Lerp (green→red) -> Tint Character\n'
                               "2. Get HP -> hp -> Format String 'HP: {0}' -> Print Value",
                    'tip': "Returns a character's current HP, max HP, and HP as a 0→1 percentage. Pure node — no "
                           'exec wire needed. Wire into Compare, Format String, Print, Color Lerp, etc. Data inputs: '
                           'target (object). Data outputs: hp (number), max_hp (number), percent (number).'},
 'utility_get_name': {'example': "1. Self -> Get Name -> Print Value (label='I am')\n"
                                 '2. Event Other -> Get Name -> Concat -> Print',
                      'tip': "Returns a character's name as a string. Pure node — wire directly into Print Value or "
                             'Format String. Data inputs: target (object). Data outputs: name (string).'},
 'utility_get_position': {'example': "1. Self -> Get Position -> x -> Print Value (label='X')\n"
                                     '2. Get Position -> Make Vector offset -> Move Toward',
                          'tip': "Returns a character's world position as X and Y number outputs separately, or as a "
                                 'combined vector. Useful for feeding into Format String, math, or movement nodes. '
                                 'Data inputs: target (object). Data outputs: position (vector), x (number), y '
                                 '(number).'},
 'utility_library_character': {'example': '1. Choose "Zombie" -> Spawn Swarm Library\n'
                                          '2. Choose "Boss" -> Spawn Library Character',
                               'tip': 'A dropdown that outputs the name of a library character as a string. Wire '
                                      'into Spawn nodes. Data outputs: name (string). Settings: character.'},
 'utility_make_color': {'example': '1. Add Make Color from the Utility category.\n'
                                   '2. Connect r, g, b.\n'
                                   '3. Use color in the next calculation or condition.',
                        'tip': 'Combines R, G, B numbers (0-255) into a single Color you can wire into any color '
                               'input. Data inputs: r (number, default=255), g (number, default=255), b (number, '
                               'default=255). Data outputs: color (color). Settings: r, g, b.'},
 'utility_make_vector': {'example': '1. (0, -100) -> Make Vector -> Offset from character\n'
                                    '2. Math -> X, Math -> Y -> Make Vector -> Teleport',
                         'tip': 'Combines an X and Y number into a single Vector2 that you can wire into movement '
                                'nodes, direction nodes, or spawn positions. Data inputs: x (number, default=0), y '
                                '(number, default=0). Data outputs: vector (vector). Settings: x, y.'},
 'utility_number_to_string': {'example': '1. Get HP -> Number to String -> Format String\n'
                                         '2. Get Speed -> Number to String (decimals=0) -> Print Value',
                              'tip': 'Converts any number to a text string so you can wire it into Print or Format '
                                     'String. Optionally rounds to N decimal places. Wire a number out from any math '
                                     'node straight in here. Data inputs: value (number, default=0). Data outputs: '
                                     'text (string). Settings: decimals.'},
 'utility_percent_max_hp': {'example': '1. 20% of Max HP -> Heal amount\n2. 50% of Max HP -> Execute threshold',
                            'tip': "Calculates an absolute HP amount as a percentage of a character's maximum HP. "
                                   'Data inputs: target (object), percent (number, default=10). Data outputs: amount '
                                   '(number). Settings: percent.'},
 'utility_print': {'example': '1. Print "Triggered Phase 2"\n2. Debug variable values',
                   'tip': 'Print to terminal and optionally show an on-screen toast. Execution input: exec. '
                          "Execution output: exec. Data inputs: message (any, default=''). Settings: message, "
                          'show_on_screen. Use the white execution path for ordering and the colored pins for '
                          'values.'},
 'utility_print_target': {'example': '1. Debug Target -> Console\n2. Check who is attacking',
                          'tip': 'Print target name, position, HP, and distance from Self. Execution input: exec. '
                                 'Execution output: exec. Data inputs: target (object). Settings: prefix, '
                                 'show_on_screen. Use the white execution path for ordering and the colored pins for '
                                 'values.'},
 'utility_print_to_screen': {'example': '1. Print "BUFFED!" when gaining a tag\n2. Print "DODGE" on miss',
                             'tip': 'Displays floating combat text above a character -- visible in the arena to '
                                    'players. Execution input: exec. Execution output: exec. Data inputs: target '
                                    "(object), text (string, default='Hello'), color (color, default=[255, 255, "
                                    '255]). Settings: text, color. Use the white execution path for ordering and the '
                                    'colored pins for values.'},
 'utility_print_value': {'example': "1. Get HP -> Print Value (label='HP')\n"
                                    "2. Get Speed -> Print Value (label='Speed', show_on_screen=True)",
                         'tip': 'The simplest debug node. Wire ANY output — number, string, boolean, color, vector — '
                                'directly into here and it prints it formatted as a toast + terminal line. '
                                "Optionally add a label prefix so you know what you're looking at. No conversion "
                                'node needed — it auto-converts everything. Execution input: exec. Execution output: '
                                "exec. Data inputs: value (any), label (string, default=''). Settings: label, "
                                'show_on_screen, duration. Use the white execution path for ordering and the colored '
                                'pins for values.'},
 'utility_random_direction': {'example': '1. Random Direction -> Dash\n2. Random Direction -> Spawn Projectile',
                              'tip': 'Returns a random normalized direction vector. Data outputs: direction '
                                     '(vector).'},
 'utility_random_position_radius': {'example': '1. Random Position -> Teleport\n2. Random Position -> Meteor',
                                    'tip': 'Returns a random world coordinate within a circle around a center point. '
                                           'Data inputs: center (vector). Data outputs: position (vector). Settings: '
                                           'radius.'},
 'utility_split_color': {'example': '1. Add Split Color from the Utility category.\n'
                                    '2. Connect color.\n'
                                    '3. Use r, g, b in the next calculation or condition.',
                         'tip': 'Breaks an RGB Color into separate R, G, B number outputs (0-255 each). Data inputs: '
                                'color (color). Data outputs: r (number), g (number), b (number).'},
 'utility_split_vector': {'example': '1. Get Position -> Split Vector -> x -> Compare < 0 -> facing left\n'
                                     '2. Get Velocity -> Split -> y -> Abs -> vertical speed',
                          'tip': 'Breaks a Vector2 into separate X and Y number outputs. Use when you need to read '
                                 'or compare individual axis values. Data inputs: vector (vector). Data outputs: x '
                                 '(number), y (number).'},
 'utility_string_concat': {'example': "1. Concat('HP:' + Get HP + '/' + Max HP, sep='') -> Print Value\n"
                                      "2. Concat(Name, ':', Speed, sep=' ') -> toast",
                           'tip': 'Joins up to 4 strings/values together in order with an optional separator between '
                                  'them. Wire numbers, booleans, or text into any slot — everything gets converted '
                                  "automatically. Data inputs: a (any, default=''), b (any, default=''), c (any, "
                                  "default=''), d (any, default=''). Data outputs: text (string). Settings: "
                                  'separator.'},
 'utility_string_to_vector': {'example': '1. Add String To Vector from the Utility category.\n'
                                         '2. Connect string.\n'
                                         '3. Use vector in the next calculation or condition.',
                              'tip': "Parses text like '120,40' or '120, 40' into a Vector2. Falls back to (0,0) if "
                                     "it can't be parsed. Data inputs: string (string, default='0,0'). Data outputs: "
                                     'vector (vector).'},
 'utility_team_filter': {'example': '1. Team Filter (Ally) -> Heal\n2. Team Filter (Enemy) -> Attack',
                         'tip': 'Checks whether a target is an Ally, Enemy, or Neutral relative to the source. Data '
                                'inputs: characters (object). Data outputs: characters (object). Settings: filter.'},
 'utility_vector_get_x': {'example': '1. Add Get Vector X from the Utility category.\n'
                                     '2. Connect vector.\n'
                                     '3. Use x in the next calculation or condition.',
                          'tip': 'Pulls just the X component out of a Vector2. Handy shortcut when you only need one '
                                 "axis and don't want to wire up a full Split Vector. Data inputs: vector (vector). "
                                 'Data outputs: x (number).'},
 'utility_vector_get_y': {'example': '1. Add Get Vector Y from the Utility category.\n'
                                     '2. Connect vector.\n'
                                     '3. Use y in the next calculation or condition.',
                          'tip': 'Pulls just the Y component out of a Vector2. Handy shortcut when you only need one '
                                 "axis and don't want to wire up a full Split Vector. Data inputs: vector (vector). "
                                 'Data outputs: y (number).'},
 'utility_vector_to_string': {'example': '1. Add Vector To String from the Utility category.\n'
                                         '2. Connect vector.\n'
                                         '3. Use string in the next calculation or condition.',
                              'tip': "Turns a Vector2 into readable text, e.g. '(120, 40)'. Useful for debug labels. "
                                     'Data inputs: vector (vector). Data outputs: string (string).'},
 'utility_watch': {'example': "1. Every Frame -> Watch (label='speed', value=Get Speed)\n"
                              "2. Every Frame -> Watch (label='hp%', value=HP Percent)",
                   'tip': 'Continuously displays a live value above the character every frame — like a floating '
                          'debug overlay. Shows label + value as combat text. Use inside Every Frame to monitor a '
                          'variable in real-time without spamming toasts. Does NOT print to the terminal. Execution '
                          'input: exec. Execution output: exec. Data inputs: target (object), value (any, '
                          'default=0). Settings: label. Use the white execution path for ordering and the colored '
                          'pins for values.'},
 'variable_decrement': {'example': '1. Decrement "lives_remaining" by 1\n2. Decrement "timer" by 1',
                        'tip': 'Subtracts a value from a global variable. Execution input: exec. Execution output: '
                               'exec. Data inputs: amount (number, default=1). Settings: name, amount. Use the white '
                               'execution path for ordering and the colored pins for values.'},
 'variable_exists': {'example': '1. If "charge_stacks" exists -> read it, else start at 0\n'
                                '2. Guard against first-frame crashes',
                     'tip': 'Returns True if the named local variable has been set on this character, False if it is '
                            'still None/unset. Data inputs: target (object). Data outputs: exists (boolean). '
                            'Settings: name.'},
 'variable_get': {'example': '1. Get "boss_dead" -> If True -> Win\n2. Get "match_score" -> Compare > 10',
                  'tip': 'Reads a project-wide global variable. Data outputs: value (any). Settings: name, type.'},
 'variable_global_get': {'example': '1. Get Global "kills" -> Compare -> 10 -> win condition\n'
                                    '2. Get Global "boss_alive" -> branch minion AI',
                         'tip': 'Reads a project-wide variable. Returns the default if it has never been set. Data '
                                'outputs: value (any). Settings: name, type, default_num.'},
 'variable_global_set': {'example': '1. On Kill -> Set Global "kills" = kills + 1\n'
                                    '2. On Spawn -> Set Global "boss_alive" = True',
                         'tip': 'Writes a value into a project-wide variable accessible by every character. Good for '
                                'kill counts, round numbers, shared flags. Execution input: exec. Execution output: '
                                'exec. Data inputs: value (any). Settings: name, type. Use the white execution path '
                                'for ordering and the colored pins for values.'},
 'variable_increment': {'example': '1. Increment "red_team_score" by 1\n2. Increment "boss_hits" by 1',
                        'tip': 'Adds a value to a global variable. Execution input: exec. Execution output: exec. '
                               'Data inputs: amount (number, default=1). Settings: name, amount. Use the white '
                               'execution path for ordering and the colored pins for values.'},
 'variable_local_get': {'example': '1. Get Local "hits_taken" -> Compare > 5\n'
                                   '2. Get Local "combo_count" -> Deal Damage * Count',
                        'tip': 'Reads a private variable stored on this character. Returns a default if never set. '
                               'Data inputs: target (object). Data outputs: value (any). Settings: name, type, '
                               'default_num.'},
 'variable_local_set': {'example': '1. Set Local "hits_taken" = 0\n2. Set Local "my_target" = Target ID',
                        'tip': 'Stores a private variable on this specific character -- not shared with others. '
                               'Execution input: exec. Execution output: exec. Data inputs: target (object), value '
                               '(any). Settings: name, type. Use the white execution path for ordering and the '
                               'colored pins for values.'},
 'variable_reset': {'example': '1. On Death -> Reset "hits_left"\n2. On Respawn -> Reset all counters',
                    'tip': 'Deletes the named local variable from the character so the next Get returns its default. '
                           'Execution input: exec. Execution output: exec. Data inputs: target (object). Settings: '
                           'name. Use the white execution path for ordering and the colored pins for values.'},
 'variable_set': {'example': '1. Set "boss_dead" = True\n2. Set "match_score" = 0',
                  'tip': 'Sets a project-wide global variable accessible by every character in the scene. Execution '
                         'input: exec. Execution output: exec. Data inputs: value (any). Settings: name, type. Use '
                         'the white execution path for ordering and the colored pins for values.'},
 'variable_toggle': {'example': '1. Toggle "doors_open"\n2. Toggle "hard_mode"',
                     'tip': 'Flips a global Boolean variable between True and False. Execution input: exec. '
                            'Execution output: exec. Settings: name. Use the white execution path for ordering and '
                            'the colored pins for values.'},
 'vfx_camera_shake': {'example': '1. Shake (Intensity 5) on hit\n2. Shake (Intensity 20) on death',
                      'tip': 'Shakes the camera. Quick shorthand for the Camera Shake node. Execution input: exec. '
                             'Execution output: exec. Data inputs: intensity (number, default=5), duration (number, '
                             'default=0.5). Settings: intensity, duration. Use the white execution path for ordering '
                             'and the colored pins for values.'},
 'vfx_opacity_fade': {'example': '1. On Death -> Opacity Fade (from=1, to=0, 1.5s, sine_inout) -> done -> Despawn\n'
                                 '2. On Spawn -> Opacity Fade (from=0, to=1, 0.5s, quad_out) — fade in',
                      'tip': "Fades a character's tint from fully opaque to fully transparent (or vice-versa) over a "
                             'duration with an easing curve. Works by animating the tint overlay alpha — at '
                             'opacity=0 the sprite is invisible, at opacity=1 the tint is fully applied. Use for '
                             'spawn pop-in, death fade-out, stealth effects, etc. Execution input: exec. Execution '
                             'output: exec, done. Data inputs: target (object), from_opacity (number, default=1.0), '
                             'to_opacity (number, default=0.0), duration (number, default=1.0), color (color, '
                             'default=[255, 255, 255]). Data outputs: alpha (number). Settings: curve, from_opacity, '
                             'to_opacity, color, duration, loop. Use the white execution path for ordering and the '
                             'colored pins for values.'},
 'vfx_play_sound': {'example': '1. Play "hit.wav"\n2. Play "jump.wav"',
                    'tip': 'Plays a sound by cue name. Legacy shorthand for the full Audio Play node. Execution '
                           'input: exec. Execution output: exec. Data inputs: target (object), volume (number, '
                           'default=1.0). Settings: cue, volume. Use the white execution path for ordering and the '
                           'colored pins for values.'},
 'vfx_screen_flash': {'example': '1. Flash White on spawn\n2. Flash Red on damage',
                      'tip': 'Flashes the screen with a color. Quick shorthand for the Screen Effects node. '
                             'Execution input: exec. Execution output: exec. Data inputs: color (color, '
                             'default=[255, 255, 255]), duration (number, default=0.3). Settings: color, duration. '
                             'Use the white execution path for ordering and the colored pins for values.'},
 'vfx_spawn_particle': {'example': '1. Spawn 10 Red Particles on Hit\n2. Spawn Blue Particles on Heal',
                        'tip': 'Generates small visual dot particles at a location. Purely cosmetic, no collision. '
                               'Execution input: exec. Execution output: exec. Data inputs: position (vector), color '
                               '(color, default=[255, 200, 70]), count (number, default=5). Settings: color, count. '
                               'Use the white execution path for ordering and the colored pins for values.'},
 'vfx_spawn_trail': {'example': '1. From self to target → sword slash trail\n'
                                '2. From start to end of dash → speed trail',
                     'tip': 'Emits a burst of particles along a line between two world positions — creates a trail, '
                            'slash, or beam effect. Execution input: exec. Execution output: exec. Data inputs: '
                            'from_pos (vector, default=(0, 0)), to_pos (vector, default=(100, 0)), count (number, '
                            'default=12), color (color, default=[255, 200, 80]). Settings: count, width, lifetime, '
                            'color. Use the white execution path for ordering and the colored pins for values.'},
 'vfx_tint_ease': {'example': '1. On Hit -> Tint Ease (white→transparent, 0.4s, sine_out)\n'
                              '2. On Spawn -> Tint Ease (yellow→transparent, 0.8s, expo_out) — spawn glow',
                   'tip': 'Applies an eased color tint to a character that fades from one color to another over a '
                          'duration using your chosen easing curve. This is the all-in-one version of: Interpolate → '
                          'Color Lerp → Tint Character. Example: on hit, ease from white to transparent over 0.4s '
                          'with sine_out. Execution input: exec. Execution output: exec, done. Data inputs: target '
                          '(object), from_color (color, default=[255, 255, 255]), to_color (color, default=[0, 0, '
                          '0]), duration (number, default=0.5). Settings: curve, from_color, to_color, duration. Use '
                          'the white execution path for ordering and the colored pins for values.'},
 'weather_chain_lightning': {'example': '1. Chain Lightning (Target, Jumps 3, Decay 0.8)\n2. Arc Lightning spell',
                             'tip': 'Strikes a target then jumps to the N nearest enemies with optional damage decay '
                                    'per jump. Execution input: exec. Execution output: exec. Data inputs: target '
                                    '(object). Settings: animation, damage, jumps, range, decay, allow_self. Use the '
                                    'white execution path for ordering and the colored pins for values.'},
 'weather_fire_zone': {'example': '1. Create Fire Zone (Radius 100, 5s duration)\n2. Dragon Breath -> Fire Zone',
                       'tip': 'Creates a persistent fire puddle that deals damage over time to anyone inside. '
                              'Execution input: exec. Execution output: exec. Data inputs: position (vector). Data '
                              'outputs: zone (object). Settings: animation, radius, duration, interval, damage, '
                              'allow_self. Use the white execution path for ordering and the colored pins for '
                              'values.'},
 'weather_lightning': {'example': '1. Every 5s -> Lightning Strike (Random Enemy)\n2. Smite -> Lightning Strike',
                       'tip': 'Custom animation + impact damage + optional chain. No collision contact required. '
                              'Execution input: exec. Execution output: exec, failed. Data inputs: target (object), '
                              "position (vector), animation (string, default='lightning'), damage (number, "
                              'default=35), radius (number, default=45), jumps (number, default=0), jump_range '
                              '(number, default=100), decay (number, default=0.8), allow_self (boolean, '
                              'default=False). Data outputs: target (object). Settings: animation, damage, radius, '
                              'jumps, jump_range, decay, team_filter, allow_self. Use the white execution path for '
                              'ordering and the colored pins for values.'},
 'weather_meteor': {'example': '1. Meteor (Warning 2s, Radius 200, Damage 150)\n2. Boss ultimate -> Meteor',
                    'tip': 'Shows a telegraph warning zone then strikes for massive damage after a delay. Execution '
                           'input: exec. Execution output: exec. Data inputs: position (vector). Settings: '
                           'animation, warning_time, radius, damage, allow_self. Use the white execution path for '
                           'ordering and the colored pins for values.'},
 'weather_slow_field': {'example': '1. Create Freeze Field (Radius 150, 4s)\n2. Ice trap -> Slow Field',
                        'tip': 'Creates a persistent slow field that reduces movement speed of anyone inside. '
                               'Execution input: exec. Execution output: exec. Data inputs: position (vector). '
                               'Settings: animation, radius, duration, slow, team_filter. Use the white execution '
                               'path for ordering and the colored pins for values.'}}

# Dynamic catalog registrations synchronised from box_game.py
NODE_TIPS.update({'camera_follow_live': {'example': '1. Add Follow Live Camera Target from the Camera category.\n'
                                   '2. Wire the visible inputs for your setup.\n'
                                   '3. Use its value or execution output in the next graph step.',
                        'tip': 'Link the virtual camera to the character/position selected by the actual scene '
                               'camera. Use its visible pins to supply data and continue the white execution path '
                               'when the node exposes one.'},
 'camera_pan_virtual': {'example': '1. Add Pan Virtual Camera from the Camera category.\n'
                                   '2. Wire the visible inputs for your setup.\n'
                                   '3. Use its value or execution output in the next graph step.',
                        'tip': 'Offset the virtual crop without breaking its character follow target. Use its '
                               'visible pins to supply data and continue the white execution path when the node '
                               'exposes one.'},
 'camera_reset_virtual_pan': {'example': '1. Add Reset Virtual Camera Pan from the Camera category.\n'
                                         '2. Wire the visible inputs for your setup.\n'
                                         '3. Use its value or execution output in the next graph step.',
                              'tip': 'Return the virtual crop to the center of its follow point. Use its visible '
                                     'pins to supply data and continue the white execution path when the node '
                                     'exposes one.'},
 'camera_set_frame_visible': {'example': '1. Add Show Virtual Camera Frame from the Camera category.\n'
                                         '2. Wire the visible inputs for your setup.\n'
                                         '3. Use its value or execution output in the next graph step.',
                              'tip': 'Show or hide the editor-only virtual camera bounds. Use its visible pins to '
                                     'supply data and continue the white execution path when the node exposes one.'},
 'camera_set_swap_on_death': {'example': '1. Add Virtual Camera Swap On Death from the Camera category.\n'
                                         '2. Wire the visible inputs for your setup.\n'
                                         '3. Use its value or execution output in the next graph step.',
                              'tip': 'Enable or disable automatic target switching when the followed character dies. '
                                     'Use its visible pins to supply data and continue the white execution path when '
                                     'the node exposes one.'},
 'camera_set_virtual_pan': {'example': '1. Add Set Virtual Camera Pan from the Camera category.\n'
                                       '2. Wire the visible inputs for your setup.\n'
                                       '3. Use its value or execution output in the next graph step.',
                            'tip': 'Set the virtual crop offset from its follow point. Use its visible pins to '
                                   'supply data and continue the white execution path when the node exposes one.'},
 'ext_array_node': {'example': '1. Add Array External Node from the Scene category.\n'
                               '2. Wire the visible inputs for your setup.\n'
                               '3. Use its value or execution output in the next graph step.',
                    'tip': 'Repeat a node N times with a step offset -- fences, tick marks, backgrounds. Use its '
                           'visible pins to supply data and continue the white execution path when the node exposes '
                           'one.'},
 'motion_get_key_ease': {'example': '1. Add Get Keyframe Ease from the Motion Clips category.\n'
                                    '2. Wire the visible inputs for your setup.\n'
                                    '3. Use its value or execution output in the next graph step.',
                         'tip': 'Easing name on the outgoing segment of the keyframe nearest Frame. Use its visible '
                                'pins to supply data and continue the white execution path when the node exposes '
                                'one.'},
 'motion_set_key_ease': {'example': '1. Add Set Keyframe Ease from the Motion Clips category.\n'
                                    '2. Wire the visible inputs for your setup.\n'
                                    '3. Use its value or execution output in the next graph step.',
                         'tip': 'Set the outgoing interpolation of the keyframe nearest Frame on Layer of Clip. Any '
                                'engine easing name (linear, discrete, sine_out, bounce_out, ...) or a custom F8 '
                                'curve (curve:name) - same as the F9 studio ease cycler. Persistent clip edit. Use '
                                'its visible pins to supply data and continue the white execution path when the node '
                                'exposes one.'},
 'pe_attach': {'example': '1. Add Attach Emitter To Character from the Particles category.\n'
                          '2. Wire the visible inputs for your setup.\n'
                          '3. Use its value or execution output in the next graph step.',
               'tip': 'Make an emitter follow a character every frame. Use its visible pins to supply data and '
                      'continue the white execution path when the node exposes one.'},
 'pe_burst_at': {'example': '1. Add Particle Burst At from the Particles category.\n'
                            '2. Wire the visible inputs for your setup.\n'
                            '3. Use its value or execution output in the next graph step.',
                 'tip': 'One-off burst of a preset at a position — hits, impacts, pickups. Use its visible pins to '
                        'supply data and continue the white execution path when the node exposes one.'},
 'pe_count': {'example': '1. Add Emitter Particle Count from the Particles category.\n'
                         '2. Wire the visible inputs for your setup.\n'
                         '3. Use its value or execution output in the next graph step.',
              'tip': 'How many particles a named emitter currently has alive. Use its visible pins to supply data '
                     'and continue the white execution path when the node exposes one.'},
 'pe_kill': {'example': '1. Add Destroy Emitter from the Particles category.\n'
                        '2. Wire the visible inputs for your setup.\n'
                        '3. Use its value or execution output in the next graph step.',
             'tip': 'Remove a named emitter from the scene. Use its visible pins to supply data and continue the '
                    'white execution path when the node exposes one.'},
 'pe_move': {'example': '1. Add Move Emitter To from the Particles category.\n'
                        '2. Wire the visible inputs for your setup.\n'
                        '3. Use its value or execution output in the next graph step.',
             'tip': 'Reposition a named emitter in world space. Use its visible pins to supply data and continue the '
                    'white execution path when the node exposes one.'},
 'pe_set_emitting': {'example': '1. Add Set Emitter Emitting from the Particles category.\n'
                                '2. Wire the visible inputs for your setup.\n'
                                '3. Use its value or execution output in the next graph step.',
                     'tip': 'Turn a named emitter on or off. Use its visible pins to supply data and continue the '
                            'white execution path when the node exposes one.'},
 'pe_set_prop': {'example': '1. Add Set Emitter Property from the Particles category.\n'
                            '2. Wire the visible inputs for your setup.\n'
                            '3. Use its value or execution output in the next graph step.',
                 'tip': 'Set any emitter field by name (rate, direction, wind_gust, ...). Use its visible pins to '
                        'supply data and continue the white execution path when the node exposes one.'},
 'pe_spawn': {'example': '1. Add Spawn Particle Emitter from the Particles category.\n'
                         '2. Wire the visible inputs for your setup.\n'
                         '3. Use its value or execution output in the next graph step.',
              'tip': 'Create an emitter at a position from a preset (fire, smoke, sparks, rain, ...). Use its '
                     'visible pins to supply data and continue the white execution path when the node exposes one.'},
 'scene_anim_busy': {'example': '1. Add Scene Item Is Animating from the Scene Animation category.\n'
                                '2. Wire the visible inputs for your setup.\n'
                                '3. Use its value or execution output in the next graph step.',
                     'tip': 'True while any tween is still running on this item. Use its visible pins to supply data '
                            'and continue the white execution path when the node exposes one.'},
 'scene_anim_move': {'example': '1. Add Animate Scene Item Move from the Scene Animation category.\n'
                                '2. Wire the visible inputs for your setup.\n'
                                '3. Use its value or execution output in the next graph step.',
                     'tip': 'Tween a scene item to a world position over time. Use its visible pins to supply data '
                            'and continue the white execution path when the node exposes one.'},
 'scene_anim_stop': {'example': '1. Add Stop Scene Animations from the Scene Animation category.\n'
                                '2. Wire the visible inputs for your setup.\n'
                                '3. Use its value or execution output in the next graph step.',
                     'tip': 'Cancel every running tween on a scene item. Use its visible pins to supply data and '
                            'continue the white execution path when the node exposes one.'},
 'scene_anim_to': {'example': '1. Add Animate Scene Item To from the Scene Animation category.\n'
                              '2. Wire the visible inputs for your setup.\n'
                              '3. Use its value or execution output in the next graph step.',
                   'tip': "Tween a scene item's property to a value over time (position, opacity, scale, rotation, "
                          'parallax). Use its visible pins to supply data and continue the white execution path when '
                          'the node exposes one.'},
 'scene_item_get_pos': {'example': '1. Add Get Scene Item Position from the Scene Text category.\n'
                                   '2. Wire the visible inputs for your setup.\n'
                                   '3. Use its value or execution output in the next graph step.',
                        'tip': 'World position of a scene text or image. Use its visible pins to supply data and '
                               'continue the white execution path when the node exposes one.'},
 'scene_item_get_prop': {'example': '1. Add Get Scene Item Property from the Scene Text category.\n'
                                    '2. Wire the visible inputs for your setup.\n'
                                    '3. Use its value or execution output in the next graph step.',
                         'tip': 'Read any field from a scene text or image. Use its visible pins to supply data and '
                                'continue the white execution path when the node exposes one.'},
 'scene_item_set_opacity': {'example': '1. Add Set Scene Item Opacity from the Scene Text category.\n'
                                       '2. Wire the visible inputs for your setup.\n'
                                       '3. Use its value or execution output in the next graph step.',
                            'tip': 'Fade a scene text or image. Accepts 0..1 or 0..255. Use its visible pins to '
                                   'supply data and continue the white execution path when the node exposes one.'},
 'scene_item_set_parallax': {'example': '1. Add Set Scene Item Parallax from the Scene Text category.\n'
                                        '2. Wire the visible inputs for your setup.\n'
                                        '3. Use its value or execution output in the next graph step.',
                             'tip': '0 = locked to screen (background plate), 1 = normal world, >1 = foreground. Use '
                                    'its visible pins to supply data and continue the white execution path when the '
                                    'node exposes one.'},
 'scene_item_set_pos': {'example': '1. Add Set Scene Item Position from the Scene Text category.\n'
                                   '2. Wire the visible inputs for your setup.\n'
                                   '3. Use its value or execution output in the next graph step.',
                        'tip': 'Move a scene text or image to a world position. Use its visible pins to supply data '
                               'and continue the white execution path when the node exposes one.'},
 'scene_item_set_prop': {'example': '1. Add Set Scene Item Property from the Scene Text category.\n'
                                    '2. Wire the visible inputs for your setup.\n'
                                    '3. Use its value or execution output in the next graph step.',
                         'tip': 'Set ANY field on a scene text or image by name -- the generic escape hatch. Use its '
                                'visible pins to supply data and continue the white execution path when the node '
                                'exposes one.'},
 'scene_item_set_rotation': {'example': '1. Add Set Scene Item Rotation from the Scene Text category.\n'
                                        '2. Wire the visible inputs for your setup.\n'
                                        '3. Use its value or execution output in the next graph step.',
                             'tip': 'Rotate a scene text or image, in degrees. Use its visible pins to supply data '
                                    'and continue the white execution path when the node exposes one.'},
 'scene_item_set_scale': {'example': '1. Add Set Scene Item Scale from the Scene Text category.\n'
                                     '2. Wire the visible inputs for your setup.\n'
                                     '3. Use its value or execution output in the next graph step.',
                          'tip': 'Resize a scene item (font size for text, scale for images). Use its visible pins '
                                 'to supply data and continue the white execution path when the node exposes one.'},
 'scene_item_set_visible': {'example': '1. Add Set Scene Item Visible from the Scene Text category.\n'
                                       '2. Wire the visible inputs for your setup.\n'
                                       '3. Use its value or execution output in the next graph step.',
                            'tip': 'Show or hide a scene text or image. Use its visible pins to supply data and '
                                   'continue the white execution path when the node exposes one.'},
 'scene_text_set': {'example': '1. Add Set Scene Text from the Scene Text category.\n'
                               '2. Wire the visible inputs for your setup.\n'
                               '3. Use its value or execution output in the next graph step.',
                    'tip': 'Change the words shown by a scene text. Reference it by its sid number or current text. '
                           'Use its visible pins to supply data and continue the white execution path when the node '
                           'exposes one.'},
 'scene_text_set_color': {'example': '1. Add Set Scene Text Colour from the Scene Text category.\n'
                                     '2. Wire the visible inputs for your setup.\n'
                                     '3. Use its value or execution output in the next graph step.',
                          'tip': 'Recolour a scene text. Use its visible pins to supply data and continue the white '
                                 'execution path when the node exposes one.'},
 'status_root': {'example': '1. Add root from the Root category.\n'
                            '2. Wire the visible inputs for your setup.\n'
                            '3. Use its value or execution output in the next graph step.',
                 'tip': 'root is a Root node. Use its visible pins to supply data and continue the white execution '
                        'path when the node exposes one.'},
 'status_silence': {'example': '1. Add silence from the Silence category.\n'
                               '2. Wire the visible inputs for your setup.\n'
                               '3. Use its value or execution output in the next graph step.',
                    'tip': 'silence is a Silence node. Use its visible pins to supply data and continue the white '
                           'execution path when the node exposes one.'},
 'status_stun': {'example': '1. Add stun from the Stun category.\n'
                            '2. Wire the visible inputs for your setup.\n'
                            '3. Use its value or execution output in the next graph step.',
                 'tip': 'stun is a Stun node. Use its visible pins to supply data and continue the white execution '
                        'path when the node exposes one.'}})

# Event factories synchronised from the dynamic registrations in box_game.py
NODE_TIPS.update({
    'event_on_scene_damage': {'example': '1. Add Scene: Any Damage Taken from Events.\n2. Connect its exec output to a Scene Director action.\n3. Use subject and damage to react globally.', 'tip': 'Global scene event. Fires whenever any character takes damage. Outputs the affected subject and event data; use it for arena-wide reactions, camera effects, or directors.'},
    'event_on_scene_death': {'example': '1. Add Scene: Any Death from Events.\n2. Connect to weather, score, or cleanup logic.\n3. Use subject or killer_name in the next node.', 'tip': 'Global scene event. Fires whenever a character dies and exposes the dead subject and killer information.'},
    'event_on_scene_debug_button': {'example': '1. Add Scene Debug Button event.\n2. Connect it to a test action.\n3. Press the matching debug button in the arena.', 'tip': 'Global scene event fired by a configured Scene Debug Button. Use it to test director logic without changing combat flow.'},
    'event_on_scene_heal': {'example': '1. Add Scene: Any Heal from Events.\n2. Connect to a glow or score action.\n3. Use subject and amount downstream.', 'tip': 'Global scene event. Fires whenever any character receives healing.'},
    'event_on_scene_wall_bounce': {'example': '1. Add Scene: Any Wall Bounce from Events.\n2. Connect to sparks or knockback logic.\n3. Use subject in the next node.', 'tip': 'Global scene event. Fires whenever any character bounces against the arena wall.'},
})
NODE_TIPS.update({
    **{f'audio_event_{event}': {
        'example': f'1. Add Audio On {event.replace("_", " ").title()}.\n2. Connect its exec output to Play Audio or audio logic.\n3. Use damage, crit, or hp_pct outputs when relevant.',
        'tip': f'Audio event node for {event.replace("_", " ")}. Fires an execution signal with event context (character, other, damage, critical flag, and HP percent when available).'
    } for event in ('spawn','attack','hit','death','wall_bounce','kill','heal','crit','combo','dash','low_hp','status_applied','status_removed','custom')}
})
# Corrected dynamic status factory documentation.
NODE_TIPS.update({
    'status_stun': {'example':'1. On Hit → Stun Target for 1.0s\n2. Connect a duration value for a boss slam.', 'tip':'Applies the Stun control status to a target for a duration. Execution input: exec. Execution output: exec. Data inputs: target (object). Settings: duration.'},
    'status_root': {'example':'1. Root Target for 2.0s before a meteor strike\n2. On Trap → Root Event Other.', 'tip':'Applies the Root control status to a target for a duration, preventing normal movement. Execution input: exec. Execution output: exec. Data inputs: target (object). Settings: duration.'},
    'status_silence': {'example':'1. Silence Target before a spell combo\n2. On Hit → Silence for 1.5s.', 'tip':'Applies the Silence control status to a target for a duration. Execution input: exec. Execution output: exec. Data inputs: target (object). Settings: duration.'},
})
