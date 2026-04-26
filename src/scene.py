import pyrr
import math
import numpy as np
from OpenGL.GL import *
from models import create_cube, create_plane

class Scene:
    def __init__(self):
        self.cube_vao = create_cube()
        self.plane_vao = create_plane()

        self.shirt_colors = [
            [0.2, 0.4, 0.8], # Blue
            [0.8, 0.2, 0.2], # Red
            [0.2, 0.8, 0.2], # Green
            [0.8, 0.8, 0.2]  # Yellow
        ]
        self.speed_ratios = [4.0, 1.0, 3.0, 2.0]
        self.base_speed = 0.25
        self.num_lanes = 4
        self.base_a = 25.0
        self.base_b = 15.0

    def draw_cube(self, shader, scene_shader, model_mat, color, is_ground=0):
        glUniformMatrix4fv(glGetUniformLocation(shader, "model"), 1, GL_FALSE, model_mat)
        if shader == scene_shader:
            glUniform3fv(glGetUniformLocation(shader, "objectColor"), 1, color)
            glUniform1i(glGetUniformLocation(shader, "isGround"), is_ground)
        glBindVertexArray(self.cube_vao)
        glDrawArrays(GL_TRIANGLES, 0, 36)

    def draw_plane(self, shader, scene_shader, model_mat):
        glUniformMatrix4fv(glGetUniformLocation(shader, "model"), 1, GL_FALSE, model_mat)
        if shader == scene_shader:
            glUniform3fv(glGetUniformLocation(shader, "objectColor"), 1, [1.0, 1.0, 1.0])
            glUniform1i(glGetUniformLocation(shader, "isGround"), 1)
        glBindVertexArray(self.plane_vao)
        glDrawArrays(GL_TRIANGLES, 0, 6)

    def render(self, shader, scene_shader, time, is_shadow=False, is_moon=False):
        # 1. Draw Ground
        if not is_shadow:
            ground_model = pyrr.matrix44.create_identity(dtype=np.float32)
            self.draw_plane(shader, scene_shader, ground_model)
            
        if not is_shadow or is_moon:
            # 2. Draw Floodlamp Structure
            # Base Block
            base_scale = pyrr.matrix44.create_from_scale([2.0, 2.0, 2.0], dtype=np.float32)
            base_trans = pyrr.matrix44.create_from_translation([0.0, 1.0, -22.0], dtype=np.float32)
            base_model = base_scale @ base_trans
            self.draw_cube(shader, scene_shader, base_model, [0.3, 0.3, 0.3], is_ground=0)
            
            # Main Vertical Pole
            pole_scale = pyrr.matrix44.create_from_scale([0.5, 28.0, 0.5], dtype=np.float32)
            pole_trans = pyrr.matrix44.create_from_translation([0.0, 16.0, -22.0], dtype=np.float32)
            pole_model = pole_scale @ pole_trans
            self.draw_cube(shader, scene_shader, pole_model, [0.5, 0.5, 0.5], is_ground=0)
            
            # Horizontal Support Arm
            arm_scale = pyrr.matrix44.create_from_scale([4.0, 0.4, 0.4], dtype=np.float32)
            arm_trans = pyrr.matrix44.create_from_translation([0.0, 29.8, -21.5], dtype=np.float32)
            arm_model = arm_scale @ arm_trans
            self.draw_cube(shader, scene_shader, arm_model, [0.4, 0.4, 0.4], is_ground=0)
            
            # Draw Floodlamp Array (Multiple lamp panels angled down)
            panel_scale = pyrr.matrix44.create_from_scale([3.5, 1.5, 0.2], dtype=np.float32)
            panel_rot = pyrr.matrix44.create_from_x_rotation(math.radians(-25.0), dtype=np.float32)
            panel_trans = pyrr.matrix44.create_from_translation([0.0, 30.0, -21.0], dtype=np.float32)
            panel_model = panel_scale @ panel_rot @ panel_trans
            self.draw_cube(shader, scene_shader, panel_model, [0.2, 0.2, 0.2], is_ground=0)
            
            # Draw bulbs
            for i in range(-1, 2):
                for j in range(-1, 2, 2):
                    bulb_scale = pyrr.matrix44.create_from_scale([0.8, 0.5, 0.2], dtype=np.float32)
                    bulb_shift = pyrr.matrix44.create_from_translation([i * 1.0, j * 0.4, 0.15], dtype=np.float32)
                    bulb_model = bulb_scale @ bulb_shift @ panel_rot @ panel_trans
                    self.draw_cube(shader, scene_shader, bulb_model, [1.0, 1.0, 0.8], is_ground=0)

        # 3. Draw Runners
        for lane in range(self.num_lanes):
            val_lane = 0.85 + ((lane + 0.5) / self.num_lanes) * 0.3
            a = self.base_a * val_lane
            b = self.base_b * val_lane
            
            speed = self.speed_ratios[lane] * self.base_speed
            
            runner_x = a * math.cos(time * speed)
            runner_z = b * math.sin(time * speed)
            
            dx = -a * speed * math.sin(time * speed)
            dz = b * speed * math.cos(time * speed)
            angle = math.atan2(-dx, dz)
            
            runner_rot = pyrr.matrix44.create_from_y_rotation(angle, dtype=np.float32)
            
            swing_angle = math.sin(time * speed * 7.0) * 1.0
            runner_y = 0.75 + 1.2 * math.cos(swing_angle)
            
            runner_base = runner_rot @ pyrr.matrix44.create_from_translation([runner_x, runner_y, runner_z], dtype=np.float32)

            skin_color = [0.8, 0.6, 0.4]
            shirt_color = self.shirt_colors[lane % len(self.shirt_colors)]
            pants_color = [0.15, 0.15, 0.15]

            # Torso
            torso_scale = pyrr.matrix44.create_from_scale([0.8, 1.5, 0.4], dtype=np.float32)
            torso_model = torso_scale @ runner_base
            self.draw_cube(shader, scene_shader, torso_model, shirt_color)

            # Head
            head_scale = pyrr.matrix44.create_from_scale([0.5, 0.5, 0.5], dtype=np.float32)
            head_trans = pyrr.matrix44.create_from_translation([0.0, 1.0, 0.0], dtype=np.float32)
            head_model = head_scale @ head_trans @ runner_base
            self.draw_cube(shader, scene_shader, head_model, skin_color)
            
            # Left Arm
            arm_scale = pyrr.matrix44.create_from_scale([0.2, 1.0, 0.2], dtype=np.float32)
            l_arm_shift = pyrr.matrix44.create_from_translation([0.0, -0.5, 0.0], dtype=np.float32)
            l_arm_rot = pyrr.matrix44.create_from_x_rotation(swing_angle, dtype=np.float32)
            l_arm_pivot = pyrr.matrix44.create_from_translation([0.5, 0.75, 0.0], dtype=np.float32)
            l_arm_model = arm_scale @ l_arm_shift @ l_arm_rot @ l_arm_pivot @ runner_base
            self.draw_cube(shader, scene_shader, l_arm_model, skin_color)

            # Right Arm
            r_arm_shift = pyrr.matrix44.create_from_translation([0.0, -0.5, 0.0], dtype=np.float32)
            r_arm_rot = pyrr.matrix44.create_from_x_rotation(-swing_angle, dtype=np.float32)
            r_arm_pivot = pyrr.matrix44.create_from_translation([-0.5, 0.75, 0.0], dtype=np.float32)
            r_arm_model = arm_scale @ r_arm_shift @ r_arm_rot @ r_arm_pivot @ runner_base
            self.draw_cube(shader, scene_shader, r_arm_model, skin_color)

            # Left Leg
            leg_scale = pyrr.matrix44.create_from_scale([0.3, 1.2, 0.3], dtype=np.float32)
            l_leg_shift = pyrr.matrix44.create_from_translation([0.0, -0.6, 0.0], dtype=np.float32)
            l_leg_rot = pyrr.matrix44.create_from_x_rotation(-swing_angle, dtype=np.float32)
            l_leg_pivot = pyrr.matrix44.create_from_translation([0.25, -0.75, 0.0], dtype=np.float32)
            l_leg_model = leg_scale @ l_leg_shift @ l_leg_rot @ l_leg_pivot @ runner_base
            self.draw_cube(shader, scene_shader, l_leg_model, pants_color)

            # Right Leg
            r_leg_shift = pyrr.matrix44.create_from_translation([0.0, -0.6, 0.0], dtype=np.float32)
            r_leg_rot = pyrr.matrix44.create_from_x_rotation(swing_angle, dtype=np.float32)
            r_leg_pivot = pyrr.matrix44.create_from_translation([-0.25, -0.75, 0.0], dtype=np.float32)
            r_leg_model = leg_scale @ r_leg_shift @ r_leg_rot @ r_leg_pivot @ runner_base
            self.draw_cube(shader, scene_shader, r_leg_model, pants_color)