import glfw
import glm
from OpenGL.GL import *
from shaders import compile_shaders
from geometry import init_vaos
from camera import CameraManager
from stadium import lamp_positions, draw_stadium_ground, draw_fence, draw_lamp_post, draw_small_leaf_tree, tree_positions
from runner import render_runner_with_shadows

def main():
    if not glfw.init(): return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.SAMPLES, 4)
    
    window = glfw.create_window(800, 600, "Stadion UAS Grafkom - Modern OpenGL", None, None)
    if not window: glfw.terminate(); return
    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    
    shader = compile_shaders()
    fence_poles = init_vaos()
    
    glUseProgram(shader)
    
    for i, pos in enumerate(lamp_positions):
        glUniform3f(glGetUniformLocation(shader, f"spotLights[{i}].position"), pos[0], 6.0, pos[1])
        glUniform3f(glGetUniformLocation(shader, f"spotLights[{i}].direction"), -pos[0], -6.0, -pos[1])
        glUniform3f(glGetUniformLocation(shader, f"spotLights[{i}].diffuse"), 0.9, 0.8, 0.5)
        glUniform3f(glGetUniformLocation(shader, f"spotLights[{i}].specular"), 0.3, 0.3, 0.3)

    glUniform3f(glGetUniformLocation(shader, "materialSpecular"), 0.2, 0.2, 0.2)
    glUniform1f(glGetUniformLocation(shader, "materialShininess"), 8.0)
    
    def framebuffer_size_callback(win, width, height):
        if height == 0: height = 1
        glViewport(0, 0, width, height)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    
    cam_manager = CameraManager()
    
    is_paused = False
    
    def key_callback_wrapper(win, key, scancode, action, mods):
        nonlocal is_paused
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            is_paused = not is_paused
        cam_manager.key_callback(win, key, scancode, action, mods)
        
    glfw.set_key_callback(window, key_callback_wrapper)
    glfw.set_cursor_pos_callback(window, cam_manager.mouse_callback)
    
    last_time = glfw.get_time()
    waktu = 0.0
    
    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        delta_time = current_time - last_time
        last_time = current_time
        
        if not is_paused:
            waktu += delta_time
            
        cam_manager.update_time(current_time)
        cam_manager.process_input(window)

        glfw.poll_events()
        glClearColor(0.25, 0.35, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        
        width, height = glfw.get_framebuffer_size(window)
        if height == 0: height = 1
        
        projection = glm.perspective(glm.radians(45.0), width / height, 0.1, 100.0)
        
        view, cam_pos = cam_manager.get_view_matrix_and_pos(waktu)
        
        glUniform3f(glGetUniformLocation(shader, "viewPos"), cam_pos.x, cam_pos.y, cam_pos.z)
        glUniformMatrix4fv(glGetUniformLocation(shader, "projection"), 1, GL_FALSE, glm.value_ptr(projection))
        glUniformMatrix4fv(glGetUniformLocation(shader, "view"), 1, GL_FALSE, glm.value_ptr(view))
        
        draw_stadium_ground(shader)
        draw_fence(shader, fence_poles)
        
        for pos in lamp_positions:
            draw_lamp_post(shader, pos[0], pos[1], pos[2])

        for pos in tree_positions: 
            draw_small_leaf_tree(shader, pos[0], pos[1], pos[2])

        # Runner 1 (Biru)
        render_runner_with_shadows(shader, waktu, 12.0, 4.4, [0.2, 0.4, 0.8], [0.8, 0.2, 0.2], 0)
        # Runner 2 (Kuning)
        render_runner_with_shadows(shader, waktu, 14.0, 6.0, [0.9, 0.8, 0.2], [0.2, 0.3, 0.7], 6.0)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()