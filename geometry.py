import math
import ctypes
import numpy as np
import glm
from OpenGL.GL import *

# Global dictionary to hold VAO configurations
VAOs = {}

def create_vao(vertices, draw_mode=GL_TRIANGLES):
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    # Position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    # Normal
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)
    vertex_count = len(vertices) // 6
    return vao, vbo, vertex_count, draw_mode

def draw_vao(name, shader, model_mat, color, use_light=True):
    glUniformMatrix4fv(glGetUniformLocation(shader, "model"), 1, GL_FALSE, glm.value_ptr(model_mat))
    glUniform3fv(glGetUniformLocation(shader, "overrideColor"), 1, color)
    glUniform1i(glGetUniformLocation(shader, "useLighting"), 1 if use_light else 0)
    
    vao, vbo, count, mode = VAOs[name]
    glBindVertexArray(vao)
    glDrawArrays(mode, 0, count)
    glBindVertexArray(0)

def init_vaos():
    VAOs["cone"] = create_vao(gen_unit_cone())
    VAOs["cylinder"] = create_vao(gen_unit_cylinder())
    VAOs["box"] = create_vao(gen_unit_box())
    VAOs["oval1"] = create_vao(gen_oval_surface(-0.5, 8.0, 30.0), GL_TRIANGLE_FAN)
    VAOs["oval2"] = create_vao(gen_oval_surface(-0.02, 6.0, 12.0), GL_TRIANGLE_FAN)
    VAOs["oval3"] = create_vao(gen_oval_surface(-0.01, 6.0, 7.2), GL_TRIANGLE_FAN)
    VAOs["oval4"] = create_vao(gen_oval_surface(0.0, 6.0, 4.0), GL_TRIANGLE_FAN)
    VAOs["lanes"] = create_vao(gen_lane_lines(0.01, 6.0, 4.0, 0.8, 4), GL_LINES)
    
    fence_base, fence_lines, fence_poles = gen_fence_base_and_poles()
    VAOs["fence_base"] = create_vao(fence_base)
    VAOs["fence_lines"] = create_vao(fence_lines, GL_LINES)
    return fence_poles

# --- GEOMETRY GENERATORS ---
def gen_unit_cone(segments=16):
    vertices = []
    for i in range(segments):
        theta1 = 2.0 * math.pi * i / segments
        theta2 = 2.0 * math.pi * (i + 1) / segments
        nx1, ny1, nz1 = math.cos(theta1), 0.5, math.sin(theta1)
        nx2, ny2, nz2 = math.cos(theta2), 0.5, math.sin(theta2)
        n0x, n0y, n0z = 0.0, 1.0, 0.0
        vertices.extend([0.0, 1.0, 0.0, n0x, n0y, n0z])
        vertices.extend([math.cos(theta1), 0.0, math.sin(theta1), nx1, ny1, nz1])
        vertices.extend([math.cos(theta2), 0.0, math.sin(theta2), nx2, ny2, nz2])
    return np.array(vertices, dtype=np.float32)

def gen_unit_cylinder(segments=16):
    vertices = []
    for i in range(segments):
        theta1 = 2.0 * math.pi * i / segments
        theta2 = 2.0 * math.pi * (i + 1) / segments
        x1, z1 = math.cos(theta1), math.sin(theta1)
        x2, z2 = math.cos(theta2), math.sin(theta2)
        vertices.extend([x1, 0.0, z1, x1, 0.0, z1])
        vertices.extend([x2, 0.0, z2, x2, 0.0, z2])
        vertices.extend([x1, 1.0, z1, x1, 0.0, z1])
        vertices.extend([x2, 0.0, z2, x2, 0.0, z2])
        vertices.extend([x2, 1.0, z2, x2, 0.0, z2])
        vertices.extend([x1, 1.0, z1, x1, 0.0, z1])
    return np.array(vertices, dtype=np.float32)

def gen_unit_box():
    vertices = [
        -1.0,-1.0,-1.0,  0.0, 0.0,-1.0,
         1.0,-1.0,-1.0,  0.0, 0.0,-1.0,
         1.0, 1.0,-1.0,  0.0, 0.0,-1.0,
         1.0, 1.0,-1.0,  0.0, 0.0,-1.0,
        -1.0, 1.0,-1.0,  0.0, 0.0,-1.0,
        -1.0,-1.0,-1.0,  0.0, 0.0,-1.0,

        -1.0,-1.0, 1.0,  0.0, 0.0, 1.0,
         1.0,-1.0, 1.0,  0.0, 0.0, 1.0,
         1.0, 1.0, 1.0,  0.0, 0.0, 1.0,
         1.0, 1.0, 1.0,  0.0, 0.0, 1.0,
        -1.0, 1.0, 1.0,  0.0, 0.0, 1.0,
        -1.0,-1.0, 1.0,  0.0, 0.0, 1.0,

        -1.0, 1.0, 1.0, -1.0, 0.0, 0.0,
        -1.0, 1.0,-1.0, -1.0, 0.0, 0.0,
        -1.0,-1.0,-1.0, -1.0, 0.0, 0.0,
        -1.0,-1.0,-1.0, -1.0, 0.0, 0.0,
        -1.0,-1.0, 1.0, -1.0, 0.0, 0.0,
        -1.0, 1.0, 1.0, -1.0, 0.0, 0.0,

         1.0, 1.0, 1.0,  1.0, 0.0, 0.0,
         1.0, 1.0,-1.0,  1.0, 0.0, 0.0,
         1.0,-1.0,-1.0,  1.0, 0.0, 0.0,
         1.0,-1.0,-1.0,  1.0, 0.0, 0.0,
         1.0,-1.0, 1.0,  1.0, 0.0, 0.0,
         1.0, 1.0, 1.0,  1.0, 0.0, 0.0,

        -1.0,-1.0,-1.0,  0.0,-1.0, 0.0,
         1.0,-1.0,-1.0,  0.0,-1.0, 0.0,
         1.0,-1.0, 1.0,  0.0,-1.0, 0.0,
         1.0,-1.0, 1.0,  0.0,-1.0, 0.0,
        -1.0,-1.0, 1.0,  0.0,-1.0, 0.0,
        -1.0,-1.0,-1.0,  0.0,-1.0, 0.0,

        -1.0, 1.0,-1.0,  0.0, 1.0, 0.0,
         1.0, 1.0,-1.0,  0.0, 1.0, 0.0,
         1.0, 1.0, 1.0,  0.0, 1.0, 0.0,
         1.0, 1.0, 1.0,  0.0, 1.0, 0.0,
        -1.0, 1.0, 1.0,  0.0, 1.0, 0.0,
        -1.0, 1.0,-1.0,  0.0, 1.0, 0.0
    ]
    return np.array(vertices, dtype=np.float32)

def gen_oval_surface(y, x_offset, radius):
    vertices = []
    vertices.extend([0.0, y, 0.0, 0.0, 1.0, 0.0])
    segments = 25 
    for i in range(segments + 1):
        theta = math.pi / 2 - (math.pi * i / segments)
        vertices.extend([x_offset + radius * math.cos(theta), y, radius * math.sin(theta), 0.0, 1.0, 0.0])
    for i in range(segments + 1):
        theta = -math.pi / 2 - (math.pi * i / segments)
        vertices.extend([-x_offset + radius * math.cos(theta), y, radius * math.sin(theta), 0.0, 1.0, 0.0])
    theta = math.pi / 2
    vertices.extend([x_offset + radius * math.cos(theta), y, radius * math.sin(theta), 0.0, 1.0, 0.0])
    return np.array(vertices, dtype=np.float32)

def gen_lane_lines(y, x_offset, start_radius, lane_width, total_lanes):
    vertices = []
    segments = 25
    for lane in range(total_lanes + 1):
        current_radius = start_radius + (lane * lane_width)
        lane_verts = []
        for i in range(segments + 1):
            theta = math.pi / 2 - (math.pi * i / segments)
            lane_verts.extend([x_offset + current_radius * math.cos(theta), y, current_radius * math.sin(theta), 0.0, 1.0, 0.0])
        for i in range(segments + 1):
            theta = -math.pi / 2 - (math.pi * i / segments)
            lane_verts.extend([-x_offset + current_radius * math.cos(theta), y, current_radius * math.sin(theta), 0.0, 1.0, 0.0])
        theta = math.pi / 2
        lane_verts.extend([x_offset + current_radius * math.cos(theta), y, current_radius * math.sin(theta), 0.0, 1.0, 0.0])
        
        num_pts = len(lane_verts) // 6
        for j in range(num_pts - 1):
            vertices.extend(lane_verts[j*6 : j*6+6])
            vertices.extend(lane_verts[(j+1)*6 : (j+1)*6+6])
    return np.array(vertices, dtype=np.float32)

def gen_fence_base_and_poles():
    x_off = 6.0
    R = 8.5 
    height = 2.0
    segments = 30
    
    base_verts = []
    line_verts = []
    pole_positions = []
    
    for i in range(segments):
        theta1 = 2.0 * math.pi * i / segments
        theta2 = 2.0 * math.pi * (i + 1) / segments
        px1 = x_off if math.cos(theta1) >= 0 else -x_off
        px2 = x_off if math.cos(theta2) >= 0 else -x_off
        
        n1 = [math.cos(theta1), 0.0, math.sin(theta1)]
        n2 = [math.cos(theta2), 0.0, math.sin(theta2)]
        
        p1 = [px1 + R * math.cos(theta1), 0.0, R * math.sin(theta1)]
        p2 = [px1 + R * math.cos(theta1), height * 0.4, R * math.sin(theta1)]
        p3 = [px2 + R * math.cos(theta2), 0.0, R * math.sin(theta2)]
        p4 = [px2 + R * math.cos(theta2), height * 0.4, R * math.sin(theta2)]
        
        base_verts.extend([*p1, *n1, *p3, *n2, *p2, *n1])
        base_verts.extend([*p3, *n2, *p4, *n2, *p2, *n1])
        
    for i in range(segments + 1):
        theta = 2.0 * math.pi * i / segments
        px = x_off if math.cos(theta) >= 0 else -x_off
        pole_pos = [px + R * math.cos(theta), 0.0, R * math.sin(theta)]
        pole_positions.append(pole_pos)
        
        if i % 2 == 0 and i < segments:
            next_theta = 2.0 * math.pi * (i + 1) / segments
            npx = x_off if math.cos(next_theta) >= 0 else -x_off
            np_pos = [npx + R * math.cos(next_theta), 0.0, R * math.sin(next_theta)]
            
            line_verts.extend([pole_pos[0], height * 0.6, pole_pos[2], 0.0, 1.0, 0.0])
            line_verts.extend([np_pos[0], height * 0.9, np_pos[2], 0.0, 1.0, 0.0])
            line_verts.extend([pole_pos[0], height * 0.4, pole_pos[2], 0.0, 1.0, 0.0])
            line_verts.extend([np_pos[0], height * 0.6, np_pos[2], 0.0, 1.0, 0.0])
            
    return np.array(base_verts, dtype=np.float32), np.array(line_verts, dtype=np.float32), pole_positions
