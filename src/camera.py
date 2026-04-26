import numpy as np
import pyrr
import glfw
import math

class Camera:
    def __init__(self):
        self.mode = 1
        self.pos = np.array([0.0, 15.0, 35.0], dtype=np.float32)
        self.front = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.yaw = -90.0
        self.pitch = 0.0
        
        self.view_pos = self.pos
        self.view_matrix = pyrr.matrix44.create_identity(dtype=np.float32)

    def process_input(self, window, delta_time, time):
        if self.mode == 2:
            speed = 35.0 * delta_time
            if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
                self.pos += speed * self.front
            if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
                self.pos -= speed * self.front
            if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
                self.pos -= pyrr.vector.normalize(np.cross(self.front, self.up)) * speed
            if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
                self.pos += pyrr.vector.normalize(np.cross(self.front, self.up)) * speed
            if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
                self.pos -= speed * self.up
            if glfw.get_key(window, glfw.KEY_E) == glfw.PRESS:
                self.pos += speed * self.up
                
            look_speed = 90.0 * delta_time
            if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
                self.yaw -= look_speed
            if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
                self.yaw += look_speed
            if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
                self.pitch += look_speed
            if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
                self.pitch -= look_speed
                
            if self.pitch > 89.0: self.pitch = 89.0
            if self.pitch < -89.0: self.pitch = -89.0
            
            front = np.array([
                math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
                math.sin(math.radians(self.pitch)),
                math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
            ], dtype=np.float32)
            self.front = pyrr.vector.normalize(front)

        # Compute view matrix based on mode
        if self.mode == 1:
            cam_x = math.sin(time * 0.2) * 55.0
            cam_z = math.cos(time * 0.2) * 55.0
            self.view_pos = np.array([cam_x, 30.0, cam_z], dtype=np.float32)
            self.view_matrix = pyrr.matrix44.create_look_at(self.view_pos, [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], dtype=np.float32)
        elif self.mode == 2:
            self.view_pos = self.pos
            self.view_matrix = pyrr.matrix44.create_look_at(self.view_pos, self.view_pos + self.front, self.up, dtype=np.float32)
        elif self.mode == 3:
            # Runner POV logic
            val_lane = 0.85 + (0.5 / 4.0) * 0.3
            a = 25.0 * val_lane
            b = 15.0 * val_lane
            
            speed = 4.0 * 0.25 # Speed for lane 0
            
            runner_x = a * math.cos(time * speed)
            runner_z = b * math.sin(time * speed)
            
            dx = -a * speed * math.sin(time * speed)
            dz = b * speed * math.cos(time * speed)
            
            mag = math.sqrt(dx*dx + dz*dz)
            dir_x = dx / mag
            dir_z = dz / mag
            
            swing_angle = math.sin(time * speed * 7.0) * 1.0
            runner_y = 0.75 + 1.2 * math.cos(swing_angle) + 2.0 # Head height
            
            self.view_pos = np.array([runner_x, runner_y, runner_z], dtype=np.float32)
            look_target = self.view_pos + np.array([dir_x * 5.0, -0.5, dir_z * 5.0], dtype=np.float32)
            self.view_matrix = pyrr.matrix44.create_look_at(self.view_pos, look_target, [0.0, 1.0, 0.0], dtype=np.float32)

    def get_view_matrix(self):
        return self.view_matrix

    def get_view_pos(self):
        return self.view_pos
