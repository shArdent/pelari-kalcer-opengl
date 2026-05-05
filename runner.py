import math
import glm
from OpenGL.GL import *
from geometry import draw_vao
from stadium import lamp_positions

def get_runner_pos_multi(t, length_straight, radius):
    offset_x = length_straight / 2.0
    perimeter = 2 * length_straight + 2 * math.pi * radius
    speed = 8.0
    dist = (t * speed) % perimeter
    
    if dist < length_straight:
        x = -offset_x + dist
        z = radius
    elif dist < length_straight + math.pi * radius:
        arc_dist = dist - length_straight
        angle = arc_dist / radius
        x = offset_x + radius * math.sin(angle)
        z = radius * math.cos(angle)
    elif dist < 2 * length_straight + math.pi * radius:
        straight_dist = dist - (length_straight + math.pi * radius)
        x = offset_x - straight_dist
        z = -radius
    else:
        arc_dist = dist - (2 * length_straight + math.pi * radius)
        angle = arc_dist / radius
        x = -offset_x - radius * math.sin(angle)
        z = -radius * math.cos(angle)
    return x, z

def draw_realistic_runner(shader, waktu, anim_speed_input, color_shirt, color_shorts, base_model, is_shadow=False, shadow_alpha=0.7):
    phase = waktu * anim_speed_input
    
    model = glm.scale(base_model, glm.vec3(0.6, 0.6, 0.6))
    model = glm.translate(model, glm.vec3(0.0, 0.3, 0.0))
    
    color_skin = [0.9, 0.7, 0.5]
    swing_ang = math.sin(phase) * 35.0 
    leg_swing_ang = math.sin(phase) * 30.0 
    
    if is_shadow:
        glUniform1i(glGetUniformLocation(shader, "isShadow"), 1)
        glUniform1f(glGetUniformLocation(shader, "shadowAlpha"), shadow_alpha)
    
    m_head = glm.translate(model, glm.vec3(0.0, 3.1, 0.0))
    m_head = glm.scale(m_head, glm.vec3(0.22, 0.25, 0.22))
    draw_vao("box", shader, m_head, color_skin)
    
    m_torso = glm.translate(model, glm.vec3(0.0, 2.2, 0.0))
    m_torso = glm.scale(m_torso, glm.vec3(0.3, 0.6, 0.18))
    draw_vao("box", shader, m_torso, color_shirt)
    
    m_hip = glm.translate(model, glm.vec3(0.0, 1.4, 0.0))
    m_hip = glm.scale(m_hip, glm.vec3(0.3, 0.2, 0.18))
    draw_vao("box", shader, m_hip, color_shorts)
    
    def draw_limb(angle, c1, c2, x_off, y_pos, is_leg):
        m_limb = glm.translate(model, glm.vec3(x_off, y_pos, 0.0))
        m_limb = glm.rotate(m_limb, glm.radians(angle), glm.vec3(1, 0, 0))
        
        m_up = glm.translate(m_limb, glm.vec3(0.0, -0.3, 0.0))
        m_up_s = glm.scale(m_up, glm.vec3(0.12, 0.35, 0.12))
        draw_vao("box", shader, m_up_s, c1)
        
        m_low = glm.translate(m_limb, glm.vec3(0.0, -0.65, 0.0))
        m_low = glm.rotate(m_low, glm.radians(abs(angle)), glm.vec3(1 if is_leg else -1, 0, 0))
        
        m_low_p = glm.translate(m_low, glm.vec3(0.0, -0.3, 0.0))
        m_low_s = glm.scale(m_low_p, glm.vec3(0.1, 0.35, 0.1))
        draw_vao("box", shader, m_low_s, c2)
        
        if is_leg:
            m_foot = glm.translate(m_low, glm.vec3(0.0, -0.65, 0.1))
            m_foot = glm.scale(m_foot, glm.vec3(0.12, 0.1, 0.2))
            draw_vao("box", shader, m_foot, [0.2, 0.2, 0.2])
        else:
            m_hand = glm.translate(m_low, glm.vec3(0.0, -0.65, 0.0))
            m_hand = glm.scale(m_hand, glm.vec3(0.1, 0.1, 0.1))
            draw_vao("box", shader, m_hand, color_skin)

    draw_limb(swing_ang, color_shirt, color_skin, -0.4, 2.6, False)
    draw_limb(-swing_ang, color_shirt, color_skin, 0.4, 2.6, False)
    draw_limb(-leg_swing_ang, color_shorts, color_skin, -0.18, 1.3, True)
    draw_limb(leg_swing_ang, color_shorts, color_skin, 0.18, 1.3, True)

    if is_shadow:
        glUniform1i(glGetUniformLocation(shader, "isShadow"), 0)

def get_shadow_matrix(Lx, Ly, Lz):
    P = glm.vec4(0.0, 1.0, 0.0, -0.02)
    L = glm.vec4(Lx, Ly, Lz, 1.0)
    dot = glm.dot(P, L)
    mat = glm.mat4(
        dot - P.x*L.x, -P.x*L.y, -P.x*L.z, -P.x*L.w,
        -P.y*L.x, dot - P.y*L.y, -P.y*L.z, -P.y*L.w,
        -P.z*L.x, -P.z*L.y, dot - P.z*L.z, -P.z*L.w,
        -P.w*L.x, -P.w*L.y, -P.w*L.z, dot - P.w*L.w
    )
    return mat

def render_runner_with_shadows(shader, waktu, t_put, R, c1, c2, off):
    x, z = get_runner_pos_multi(waktu + off, t_put, R)
    next_x, next_z = get_runner_pos_multi(waktu + off + 0.1, t_put, R)
    rot_angle = math.atan2(next_x - x, next_z - z)
    
    base_model = glm.translate(glm.mat4(1.0), glm.vec3(x, 0.0, z))
    base_model = glm.rotate(base_model, rot_angle, glm.vec3(0, 1, 0))
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)
    glEnable(GL_STENCIL_TEST)
    
    for pos in lamp_positions:
        dist = math.sqrt((pos[0] - x)**2 + (pos[1] - z)**2)
        max_dist = 18.0
        if dist < max_dist:
            alpha = 0.65 * (1.0 - (dist / max_dist))
            glClear(GL_STENCIL_BUFFER_BIT)
            glStencilFunc(GL_EQUAL, 0, 0xFF)
            glStencilOp(GL_KEEP, GL_KEEP, GL_INCR)
            
            shadow_mat = get_shadow_matrix(pos[0], 6.0, pos[1])
            final_model = shadow_mat * base_model
            draw_realistic_runner(shader, waktu, 15.0, c1, c2, final_model, True, alpha)
    
    glDisable(GL_STENCIL_TEST)
    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)

    draw_realistic_runner(shader, waktu, 15.0, c1, c2, base_model)
