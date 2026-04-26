import glfw
import sys
import numpy as np
import pyrr
from OpenGL.GL import *

from camera import Camera
from shaders import compile_all_shaders
from scene import Scene
from renderer import Renderer

def main():
    if not glfw.init():
        print("Failed to initialize GLFW")
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(1280, 720, "Pelari Kalcer 3D", None, None)
    if not window:
        glfw.terminate()
        print("Failed to create GLFW window")
        sys.exit(1)

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, lambda w, width, height: glViewport(0, 0, width, height))
    glfw.swap_interval(1)

    glEnable(GL_DEPTH_TEST)

    scene_shader, depth_shader = compile_all_shaders()
    scene = Scene()
    renderer = Renderer()
    cam = Camera()
    
    def key_callback(window, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key == glfw.KEY_1: cam.mode = 1
            elif key == glfw.KEY_2: cam.mode = 2
            elif key == glfw.KEY_3: cam.mode = 3
    glfw.set_key_callback(window, key_callback)

    # Lighting setup
    light_pos = np.array([0.0, 30.0, -21.0], dtype=np.float32)
    light_proj = pyrr.matrix44.create_perspective_projection(100.0, 1.0, 1.0, 100.0, dtype=np.float32)
    light_view = pyrr.matrix44.create_look_at(light_pos, [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], dtype=np.float32)
    light_space_matrix = light_view @ light_proj
    
    moon_dir = np.array([0.8, -1.0, -0.2], dtype=np.float32)
    moon_pos = -moon_dir * 50.0
    moon_proj = pyrr.matrix44.create_orthogonal_projection(-60.0, 60.0, -60.0, 60.0, 0.1, 150.0, dtype=np.float32)
    moon_view = pyrr.matrix44.create_look_at(moon_pos, [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], dtype=np.float32)
    moon_space_matrix = moon_view @ moon_proj

    last_frame = glfw.get_time()

    while not glfw.window_should_close(window):
        current_frame = glfw.get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame
        time = current_frame
        
        cam.process_input(window, delta_time, time)

        # 1. Render Spotlight Depth Map
        renderer.bind_shadow_map(renderer.depth_map_fbo)
        glUseProgram(depth_shader)
        glUniformMatrix4fv(glGetUniformLocation(depth_shader, "lightSpaceMatrix"), 1, GL_FALSE, light_space_matrix)
        scene.render(depth_shader, scene_shader, time, is_shadow=True, is_moon=False)
        renderer.unbind_shadow_map()
        
        # 1b. Render Moon Depth Map
        renderer.bind_shadow_map(renderer.moon_depth_map_fbo)
        glUseProgram(depth_shader)
        glUniformMatrix4fv(glGetUniformLocation(depth_shader, "lightSpaceMatrix"), 1, GL_FALSE, moon_space_matrix)
        scene.render(depth_shader, scene_shader, time, is_shadow=True, is_moon=True)
        renderer.unbind_shadow_map()

        # 2. Render Scene Normally
        width, height = glfw.get_framebuffer_size(window)
        glViewport(0, 0, width, height)
        glClearColor(0.05, 0.05, 0.1, 1.0) # Night sky
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(scene_shader)
        
        view = cam.get_view_matrix()
        projection = pyrr.matrix44.create_perspective_projection(45.0, width / height, 0.1, 100.0, dtype=np.float32)

        glUniformMatrix4fv(glGetUniformLocation(scene_shader, "view"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(scene_shader, "projection"), 1, GL_FALSE, projection)
        glUniformMatrix4fv(glGetUniformLocation(scene_shader, "lightSpaceMatrix"), 1, GL_FALSE, light_space_matrix)
        glUniformMatrix4fv(glGetUniformLocation(scene_shader, "moonSpaceMatrix"), 1, GL_FALSE, moon_space_matrix)
        glUniform3fv(glGetUniformLocation(scene_shader, "lightPos"), 1, light_pos)
        glUniform3fv(glGetUniformLocation(scene_shader, "viewPos"), 1, cam.get_view_pos())
        glUniform3fv(glGetUniformLocation(scene_shader, "lightColor"), 1, np.array([1.0, 1.0, 0.8], dtype=np.float32))
        glUniform3fv(glGetUniformLocation(scene_shader, "moonDir"), 1, moon_dir)
        glUniform3fv(glGetUniformLocation(scene_shader, "moonColor"), 1, np.array([0.2, 0.25, 0.4], dtype=np.float32))

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, renderer.depth_map)
        glUniform1i(glGetUniformLocation(scene_shader, "shadowMap"), 0)
        
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, renderer.moon_depth_map)
        glUniform1i(glGetUniformLocation(scene_shader, "moonShadowMap"), 1)

        scene.render(scene_shader, scene_shader, time)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
