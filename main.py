import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# --- FUNGSI PEMBANTU BENTUK DASAR ---
def draw_cone(radius, height, segments, r, g, b):
    glColor3f(r, g, b)
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, height, 0.0) 
    for i in range(segments + 1):
        theta = 2.0 * math.pi * i / segments
        glNormal3f(math.cos(theta), 0.5, math.sin(theta))
        glVertex3f(radius * math.cos(theta), 0.0, radius * math.sin(theta))
    glEnd()

def draw_cylinder(radius, height, segments, r, g, b):
    glColor3f(r, g, b)
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        theta = 2.0 * math.pi * i / segments
        glNormal3f(math.cos(theta), 0.0, math.sin(theta)) 
        glVertex3f(radius * math.cos(theta), 0.0, radius * math.sin(theta))
        glVertex3f(radius * math.cos(theta), height, radius * math.sin(theta))
    glEnd()

def draw_box(dx, dy, dz):
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-dx, dy, -dz); glVertex3f( dx, dy, -dz); glVertex3f( dx, dy,  dz); glVertex3f(-dx, dy,  dz)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-dx, -dy, -dz); glVertex3f( dx, -dy, -dz); glVertex3f( dx, -dy,  dz); glVertex3f(-dx, -dy,  dz)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-dx, -dy, dz); glVertex3f( dx, -dy, dz); glVertex3f( dx, dy, dz); glVertex3f(-dx, dy, dz)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-dx, -dy, -dz); glVertex3f( dx, -dy, -dz); glVertex3f( dx, dy, -dz); glVertex3f(-dx, dy, -dz)
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(dx, -dy, -dz); glVertex3f(dx, dy, -dz); glVertex3f(dx, dy, dz); glVertex3f(dx, -dy, dz)
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-dx, -dy, -dz); glVertex3f(-dx, dy, -dz); glVertex3f(-dx, dy, dz); glVertex3f(-dx, -dy, dz)
    glEnd()

# --- FUNGSI ENVIRONMENT STADION ---
def draw_small_leaf_tree(x, z, size):
    glPushMatrix()
    glTranslatef(x, 0.0, z)
    draw_cylinder(size * 0.08, size * 1.5, 6, 0.4, 0.25, 0.1) 
    glTranslatef(0.0, size * 1.3, 0.0) 
    glPushMatrix()
    draw_cone(size * 0.4, size * 0.8, 5, 0.2, 0.5, 0.2)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(size * 0.2, -size * 0.1, 0.0)
    draw_cone(size * 0.3, size * 0.6, 5, 0.18, 0.55, 0.18)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-size * 0.2, -size * 0.1, 0.0)
    draw_cone(size * 0.3, size * 0.6, 5, 0.22, 0.45, 0.22)
    glPopMatrix()
    glPopMatrix()

def draw_lamp_post(x, z, angle_y):
    glPushMatrix()
    glTranslatef(x, 0.0, z)
    glRotatef(angle_y, 0.0, 1.0, 0.0) 
    draw_cylinder(0.12, 6.0, 8, 0.3, 0.3, 0.3)
    glTranslatef(0.0, 6.0, 0.0)
    glPushMatrix()
    glTranslatef(0.5, 0.0, 0.0)
    glColor3f(0.2, 0.2, 0.2)
    draw_box(0.5, 0.1, 0.1) 
    glPopMatrix()
    glPushMatrix()
    glTranslatef(1.0, -0.2, 0.0)
    glColor3f(0.15, 0.15, 0.15)
    draw_box(0.3, 0.3, 0.4) 
    glTranslatef(0.0, -0.31, 0.0)
    glColor3f(1.0, 1.0, 0.8) 
    draw_box(0.25, 0.05, 0.35)
    glPopMatrix()
    glPopMatrix()

def draw_oval_surface(y, x_offset, radius, r, g, b):
    glColor3f(r, g, b)
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 1.0, 0.0)
    segments = 25 
    for i in range(segments + 1):
        theta = math.pi / 2 - (math.pi * i / segments)
        glVertex3f(x_offset + radius * math.cos(theta), y, radius * math.sin(theta))
    for i in range(segments + 1):
        theta = -math.pi / 2 - (math.pi * i / segments)
        glVertex3f(-x_offset + radius * math.cos(theta), y, radius * math.sin(theta))
    glEnd()

def draw_lane_lines(y, x_offset, start_radius, lane_width, total_lanes):
    glDisable(GL_LIGHTING)
    glColor3f(0.9, 0.9, 0.9) 
    glLineWidth(2.0)         
    segments = 25
    for lane in range(total_lanes + 1):
        current_radius = start_radius + (lane * lane_width)
        glBegin(GL_LINE_LOOP)
        for i in range(segments + 1):
            theta = math.pi / 2 - (math.pi * i / segments)
            glVertex3f(x_offset + current_radius * math.cos(theta), y, current_radius * math.sin(theta))
        for i in range(segments + 1):
            theta = -math.pi / 2 - (math.pi * i / segments)
            glVertex3f(-x_offset + current_radius * math.cos(theta), y, current_radius * math.sin(theta))
        glEnd()
    glEnable(GL_LIGHTING)

# --- PERUBAHAN DI SINI ---
def draw_stadium_ground():
    # 1. Hamparan Rumput Luar (Batas Luar, Merata ke bawah Pagar)
    # Area ini dibuat hijau tua agar ada kedalaman visual
    draw_oval_surface(-0.5, 8.0, 30.0, 0.3, 0.6, 0.3)
    
    # 2. Area Luaran Lintasan (SEKARANG RUMPUT)
    # Sebelumnya abu-abu (0.6, 0.6, 0.6), sekarang hijau rumput (0.4, 0.8, 0.4)
    draw_oval_surface(-0.02, 6.0, 12.0, 0.4, 0.8, 0.4)
    
    # 3. Lapangan Inti
    draw_oval_surface(-0.01, 6.0, 7.2, 0.8, 0.3, 0.2) # Trek Merah Bata
    draw_oval_surface(0.0, 6.0, 4.0, 0.4, 0.8, 0.4)   # Rumput Hijau Inti
    draw_lane_lines(0.01, 6.0, 4.0, 0.8, 4)           # Garis
# --------------------------

def draw_fence():
    glDisable(GL_COLOR_MATERIAL) 
    x_off = 6.0
    R = 8.5 
    height = 2.0
    segments = 30
    
    # 1. Dasar Beton Pagar
    glColor3f(0.5, 0.5, 0.5) 
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        theta = 2.0 * math.pi * i / segments
        glNormal3f(math.cos(theta), 0.0, math.sin(theta))
        px = x_off if math.cos(theta) >= 0 else -x_off
        glVertex3f(px + R * math.cos(theta), 0.0, R * math.sin(theta))
        glVertex3f(px + R * math.cos(theta), height * 0.4, R * math.sin(theta))
    glEnd()
    
    # 2. Tiang Pagar
    glLineWidth(1.0)
    for i in range(segments + 1):
        theta = 2.0 * math.pi * i / segments
        px = x_off if math.cos(theta) >= 0 else -x_off
        
        glPushMatrix()
        glTranslatef(px + R * math.cos(theta), 0.0, R * math.sin(theta))
        draw_cylinder(0.05, height, 6, 0.2, 0.2, 0.2)
        
        # Kawat
        if i % 2 == 0 and i < segments:
            glColor3f(0.1, 0.1, 0.1)
            glBegin(GL_LINES)
            glVertex3f(0.0, height * 0.6, 0.0)
            next_theta = 2.0 * math.pi * (i + 1) / segments
            npx = x_off if math.cos(next_theta) >= 0 else -x_off
            dx = (npx + R * math.cos(next_theta)) - (px + R * math.cos(theta))
            dz = R * math.sin(next_theta) - R * math.sin(theta)
            glVertex3f(dx, height * 0.9, dz)
            glVertex3f(0.0, height * 0.4, 0.0)
            glVertex3f(dx, height * 0.6, dz)
            glEnd()
        glPopMatrix()
    glEnable(GL_COLOR_MATERIAL)

# --- LOGIKA ANIMASI & PELARI ---
def get_runner_pos_multi(waktu, waktu_putaran, R_lajur):
    t = (waktu % waktu_putaran) / waktu_putaran 
    x_off = 6.0
    L = x_off * 2
    C = math.pi * R_lajur
    total_jarak = 2 * L + 2 * C
    jarak_tempuh = t * total_jarak
    
    if jarak_tempuh < L: # Lurus Atas
        return x_off - jarak_tempuh, -R_lajur
    elif jarak_tempuh < L + C: # Tikungan Kiri
        arc = jarak_tempuh - L
        theta = -math.pi/2 - (arc / R_lajur) 
        return -x_off + R_lajur * math.cos(theta), R_lajur * math.sin(theta)
    elif jarak_tempuh < 2*L + C: # Lurus Bawah
        return -x_off + (jarak_tempuh - (L + C)), R_lajur
    else: # Tikungan Kanan
        arc = jarak_tempuh - (2*L + C)
        theta = math.pi/2 - (arc / R_lajur)
        return x_off + R_lajur * math.cos(theta), R_lajur * math.sin(theta)

def draw_realistic_runner(waktu, anim_speed_input, color_shirt, color_shorts):
    phase = waktu * anim_speed_input
    glScalef(0.6, 0.6, 0.6)
    color_skin = [0.9, 0.7, 0.5]
    swing_ang = math.sin(phase) * 35.0 
    leg_swing_ang = math.sin(phase) * 30.0 
    
    # --- Kepala ---
    glColor3fv(color_skin)
    glPushMatrix()
    glTranslatef(0.0, 3.1, 0.0); glScalef(0.18, 0.18, 0.18); draw_box(1.0, 1.0, 1.0); glPopMatrix()
    # --- Torso ---
    glColor3fv(color_shirt)
    glPushMatrix(); glTranslatef(0.0, 2.3, 0.0); glScalef(0.25, 0.7, 0.15); draw_box(1.0, 1.0, 1.0); glPopMatrix()
    # --- Pinggul ---
    glColor3fv(color_shorts)
    glPushMatrix(); glTranslatef(0.0, 1.5, 0.0); glScalef(0.2, 0.2, 0.15); draw_box(1.0, 1.0, 1.0); glPopMatrix()
    
    # --- Lengan & Kaki (Simpel) ---
    def draw_limb(angle, c1, c2, x_off, y_pos, is_leg):
        glPushMatrix()
        glTranslatef(x_off, y_pos, 0.0); glRotatef(angle, 1.0, 0.0, 0.0)
        glColor3fv(c1); glPushMatrix(); glScalef(0.1, 0.4, 0.1); draw_box(1.0, 1.0, 1.0); glPopMatrix()
        glTranslatef(0.0, -0.6, 0.0); glRotatef(abs(angle), 1.0 if is_leg else -1.0, 0.0, 0.0)
        glColor3fv(c2); glPushMatrix(); glScalef(0.08, 0.4, 0.08); draw_box(1.0, 1.0, 1.0); glPopMatrix()
        glPopMatrix()

    draw_limb(swing_ang, color_shirt, color_skin, -0.35, 2.9, False) # Lengan Kiri
    draw_limb(-swing_ang, color_shirt, color_skin, 0.35, 2.9, False)  # Lengan Kanan
    draw_limb(-leg_swing_ang, color_shorts, color_skin, -0.15, 1.4, True) # Kaki Kiri
    draw_limb(leg_swing_ang, color_shorts, color_skin, 0.15, 1.4, True)   # Kaki Kanan

# --- KOORDINAT LINGKUNGAN ---
tree_positions = [
    (15.0, 12.0, 2.5), (-16.0, 4.0, 2.2), (0.0, -14.0, 2.8), (-14.0, 12.0, 2.0), (10.0, 14.0, 2.6)
]
lamp_positions = [
    (10.0, 9.0, 135), (-10.0, 9.0, 45), (10.0, -9.0, 225), (-10.0, -9.0, -45)
]

def init_lighting():
    glEnable(GL_LIGHTING)      
    glEnable(GL_COLOR_MATERIAL) 
    glEnable(GL_NORMALIZE)     
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.35, 0.35, 0.4, 1.0])
    lights = [GL_LIGHT0, GL_LIGHT1, GL_LIGHT2, GL_LIGHT3]
    for l in lights:
        glEnable(l)
        glLightfv(l, GL_DIFFUSE, [0.9, 0.8, 0.5, 1.0])
        glLightf(l, GL_SPOT_CUTOFF, 40.0)      
        glLightf(l, GL_SPOT_EXPONENT, 10.0)    
        glLightf(l, GL_LINEAR_ATTENUATION, 0.01)

def main():
    if not glfw.init(): return
    window = glfw.create_window(800, 600, "Stadion UAS Grafkom - Rumput Penuh", None, None)
    if not window: glfw.terminate(); return
    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST) 
    glClearColor(0.25, 0.35, 0.5, 1.0) 
    init_lighting()
    gl_lights = [GL_LIGHT0, GL_LIGHT1, GL_LIGHT2, GL_LIGHT3]

    while not glfw.window_should_close(window):
        glfw.poll_events(); glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION); glLoadIdentity(); gluPerspective(45, 800/600, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        waktu = glfw.get_time()
        
        # Kamera Orbit
        gluLookAt(math.sin(waktu*0.4)*28.0, 14.0, math.cos(waktu*0.4)*28.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)     

        draw_stadium_ground()
        draw_fence()

        for i, pos in enumerate(lamp_positions):
            draw_lamp_post(pos[0], pos[1], pos[2])
            glLightfv(gl_lights[i], GL_POSITION, [pos[0], 6.0, pos[1], 1.0])
            glLightfv(gl_lights[i], GL_SPOT_DIRECTION, [-pos[0], -6.0, -pos[1]])

        for pos in tree_positions: draw_small_leaf_tree(pos[0], pos[1], pos[2])

        # Gambar 2 Pelari
        def run(w_in, t_put, R, c1, c2, off):
            x, z = get_runner_pos_multi(w_in + off, t_put, R)
            glPushMatrix(); glTranslatef(x, 0.0, z)
            glRotatef(math.degrees(math.atan2(get_runner_pos_multi(w_in+off+0.1, t_put, R)[0]-x, get_runner_pos_multi(w_in+off+0.1, t_put, R)[1]-z)), 0.0, 1.0, 0.0)
            draw_realistic_runner(waktu, 15.0, c1, c2); glPopMatrix()

        run(waktu, 12.0, 4.8, [0.2, 0.4, 0.8], [0.8, 0.2, 0.2], 0) # Pelari 1
        run(waktu, 14.0, 6.4, [0.9, 0.8, 0.2], [0.2, 0.3, 0.7], 6.0) # Pelari 2

        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__": main()