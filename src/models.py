import numpy as np
from OpenGL.GL import *
import ctypes

def create_cube():
    vertices = [
        # Back face
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0, 
         0.5, -0.5, -0.5,  0.0,  0.0, -1.0, 
         0.5,  0.5, -0.5,  0.0,  0.0, -1.0, 
         0.5,  0.5, -0.5,  0.0,  0.0, -1.0, 
        -0.5,  0.5, -0.5,  0.0,  0.0, -1.0, 
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0, 

        # Front face
        -0.5, -0.5,  0.5,  0.0,  0.0,  1.0, 
         0.5, -0.5,  0.5,  0.0,  0.0,  1.0, 
         0.5,  0.5,  0.5,  0.0,  0.0,  1.0, 
         0.5,  0.5,  0.5,  0.0,  0.0,  1.0, 
        -0.5,  0.5,  0.5,  0.0,  0.0,  1.0, 
        -0.5, -0.5,  0.5,  0.0,  0.0,  1.0, 

        # Left face
        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0, 
        -0.5,  0.5, -0.5, -1.0,  0.0,  0.0, 
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0, 
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0, 
        -0.5, -0.5,  0.5, -1.0,  0.0,  0.0, 
        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0, 

        # Right face
         0.5,  0.5,  0.5,  1.0,  0.0,  0.0, 
         0.5, -0.5,  0.5,  1.0,  0.0,  0.0, 
         0.5, -0.5, -0.5,  1.0,  0.0,  0.0, 
         0.5, -0.5, -0.5,  1.0,  0.0,  0.0, 
         0.5,  0.5, -0.5,  1.0,  0.0,  0.0, 
         0.5,  0.5,  0.5,  1.0,  0.0,  0.0, 

        # Bottom face
        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0, 
         0.5, -0.5, -0.5,  0.0, -1.0,  0.0, 
         0.5, -0.5,  0.5,  0.0, -1.0,  0.0, 
         0.5, -0.5,  0.5,  0.0, -1.0,  0.0, 
        -0.5, -0.5,  0.5,  0.0, -1.0,  0.0, 
        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0, 

        # Top face
        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0, 
        -0.5,  0.5,  0.5,  0.0,  1.0,  0.0, 
         0.5,  0.5,  0.5,  0.0,  1.0,  0.0, 
         0.5,  0.5,  0.5,  0.0,  1.0,  0.0, 
         0.5,  0.5, -0.5,  0.0,  1.0,  0.0, 
        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0
    ]
    vertices = np.array(vertices, dtype=np.float32)
    
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    # Position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # Normal
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    
    glBindVertexArray(0)
    return vao

def create_plane():
    vertices = [
        # positions           # normals
         60.0, 0.0,  60.0,   0.0, 1.0, 0.0,
        -60.0, 0.0,  60.0,   0.0, 1.0, 0.0,
        -60.0, 0.0, -60.0,   0.0, 1.0, 0.0,

         60.0, 0.0,  60.0,   0.0, 1.0, 0.0,
        -60.0, 0.0, -60.0,   0.0, 1.0, 0.0,
         60.0, 0.0, -60.0,   0.0, 1.0, 0.0
    ]
    vertices = np.array(vertices, dtype=np.float32)
    
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    
    glBindVertexArray(0)
    return vao

