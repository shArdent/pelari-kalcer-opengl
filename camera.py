import math
import glfw
import glm
from runner import get_runner_pos_multi

class CameraManager:
    def __init__(self):
        self.mode = 1
        self.free_cam_pos = glm.vec3(0.0, 10.0, 20.0)
        self.free_cam_front = glm.vec3(0.0, 0.0, -1.0)
        self.free_cam_up = glm.vec3(0.0, 1.0, 0.0)
        self.yaw = -90.0
        self.pitch = -20.0
        self.last_x = 400.0
        self.last_y = 300.0
        self.first_mouse = True
        self.delta_time = 0.0
        self.last_frame = 0.0

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key == glfw.KEY_1:
                self.mode = 1
                glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
            elif key == glfw.KEY_2:
                self.mode = 2
                glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
                self.first_mouse = True
            elif key == glfw.KEY_3:
                self.mode = 3
                glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)

    def mouse_callback(self, window, xpos, ypos):
        if self.mode != 2: return
        
        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos 
        self.last_x = xpos
        self.last_y = ypos

        sensitivity = 0.1
        xoffset *= sensitivity
        yoffset *= sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if self.pitch > 89.0: self.pitch = 89.0
        if self.pitch < -89.0: self.pitch = -89.0

        front = glm.vec3()
        front.x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        front.y = math.sin(glm.radians(self.pitch))
        front.z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        self.free_cam_front = glm.normalize(front)

    def process_input(self, window):
        if self.mode != 2: return
        camera_speed = 10.0 * self.delta_time
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.free_cam_pos += camera_speed * self.free_cam_front
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.free_cam_pos -= camera_speed * self.free_cam_front
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.free_cam_pos -= glm.normalize(glm.cross(self.free_cam_front, self.free_cam_up)) * camera_speed
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.free_cam_pos += glm.normalize(glm.cross(self.free_cam_front, self.free_cam_up)) * camera_speed

    def update_time(self, current_frame):
        self.delta_time = current_frame - self.last_frame
        self.last_frame = current_frame

    def get_view_matrix_and_pos(self, waktu):
        if self.mode == 1:
            camX = math.sin(waktu*0.4)*28.0
            camZ = math.cos(waktu*0.4)*28.0
            view = glm.lookAt(glm.vec3(camX, 14.0, camZ), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))
            return view, glm.vec3(camX, 14.0, camZ)
        
        elif self.mode == 2:
            view = glm.lookAt(self.free_cam_pos, self.free_cam_pos + self.free_cam_front, self.free_cam_up)
            return view, self.free_cam_pos
            
        elif self.mode == 3:
            rx, rz = get_runner_pos_multi(waktu, 12.0, 4.4)
            r_next_x, r_next_z = get_runner_pos_multi(waktu + 0.1, 12.0, 4.4)
            rot_angle = math.atan2(r_next_x - rx, r_next_z - rz)
            
            dir_x = math.sin(rot_angle)
            dir_z = math.cos(rot_angle)
            
            cam_pos = glm.vec3(rx + dir_x * 0.4, 2.2, rz + dir_z * 0.4)
            cam_front = glm.vec3(dir_x, -0.1, dir_z)
            view = glm.lookAt(cam_pos, cam_pos + cam_front, glm.vec3(0.0, 1.0, 0.0))
            return view, cam_pos
