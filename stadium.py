import glm
from OpenGL.GL import *
from geometry import draw_vao

tree_positions = [
    (15.0, 12.0, 2.5), (-16.0, 4.0, 2.2), (0.0, -14.0, 2.8), (-14.0, 12.0, 2.0), (10.0, 14.0, 2.6)
]
lamp_positions = [
    (10.0, 9.0, 135), (-10.0, 9.0, 45), (10.0, -9.0, 225), (-10.0, -9.0, -45)
]

def draw_small_leaf_tree(shader, x, z, size):
    base_model = glm.translate(glm.mat4(1.0), glm.vec3(x, 0.0, z))
    
    m_trunk = glm.scale(base_model, glm.vec3(size * 0.08, size * 1.5, size * 0.08))
    draw_vao("cylinder", shader, m_trunk, [0.4, 0.25, 0.1])
    
    m_leaf1 = glm.translate(base_model, glm.vec3(0.0, size * 1.3, 0.0))
    m_leaf1 = glm.scale(m_leaf1, glm.vec3(size * 0.4, size * 0.8, size * 0.4))
    draw_vao("cone", shader, m_leaf1, [0.2, 0.5, 0.2])
    
    m_leaf2 = glm.translate(base_model, glm.vec3(0.0, size * 1.3, 0.0))
    m_leaf2 = glm.translate(m_leaf2, glm.vec3(size * 0.2, -size * 0.1, 0.0))
    m_leaf2 = glm.scale(m_leaf2, glm.vec3(size * 0.3, size * 0.6, size * 0.3))
    draw_vao("cone", shader, m_leaf2, [0.18, 0.55, 0.18])
    
    m_leaf3 = glm.translate(base_model, glm.vec3(0.0, size * 1.3, 0.0))
    m_leaf3 = glm.translate(m_leaf3, glm.vec3(-size * 0.2, -size * 0.1, 0.0))
    m_leaf3 = glm.scale(m_leaf3, glm.vec3(size * 0.3, size * 0.6, size * 0.3))
    draw_vao("cone", shader, m_leaf3, [0.22, 0.45, 0.22])

def draw_lamp_post(shader, x, z, angle_y):
    base_model = glm.translate(glm.mat4(1.0), glm.vec3(x, 0.0, z))
    base_model = glm.rotate(base_model, glm.radians(angle_y), glm.vec3(0, 1, 0))
    
    m_post = glm.scale(base_model, glm.vec3(0.12, 6.0, 0.12))
    draw_vao("cylinder", shader, m_post, [0.3, 0.3, 0.3])
    
    m_head_base = glm.translate(base_model, glm.vec3(0.5, 6.0, 0.0))
    m_head1 = glm.scale(m_head_base, glm.vec3(0.5, 0.1, 0.1))
    draw_vao("box", shader, m_head1, [0.2, 0.2, 0.2])
    
    m_head2 = glm.translate(base_model, glm.vec3(1.0, 5.8, 0.0))
    m_head2_s = glm.scale(m_head2, glm.vec3(0.3, 0.3, 0.4))
    draw_vao("box", shader, m_head2_s, [0.15, 0.15, 0.15])
    
    m_light = glm.translate(m_head2, glm.vec3(0.0, -0.31, 0.0))
    m_light_s = glm.scale(m_light, glm.vec3(0.25, 0.05, 0.35))
    draw_vao("box", shader, m_light_s, [1.0, 1.0, 0.8], use_light=False)

def draw_stadium_ground(shader):
    ident = glm.mat4(1.0)
    draw_vao("oval1", shader, ident, [0.3, 0.6, 0.3])
    draw_vao("oval2", shader, ident, [0.4, 0.8, 0.4])
    draw_vao("oval3", shader, ident, [0.8, 0.3, 0.2])
    draw_vao("oval4", shader, ident, [0.4, 0.8, 0.4])
    
    glLineWidth(2.0)
    draw_vao("lanes", shader, ident, [0.9, 0.9, 0.9], use_light=False)

def draw_fence(shader, fence_poles):
    draw_vao("fence_base", shader, glm.mat4(1.0), [1.0, 1.0, 1.0])
    glLineWidth(1.0)
    draw_vao("fence_lines", shader, glm.mat4(1.0), [1.0, 1.0, 1.0])
    for p in fence_poles:
        m_pole = glm.translate(glm.mat4(1.0), glm.vec3(p[0], p[1], p[2]))
        m_pole = glm.scale(m_pole, glm.vec3(0.05, 2.0, 0.05))
        draw_vao("cylinder", shader, m_pole, [1.0, 1.0, 1.0])
