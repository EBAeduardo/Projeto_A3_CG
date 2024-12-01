import cv2
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math


pygame.init()

screen_width = 1360
screen_height = 768

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Espada com Reflexo Dinâmico e Movimentação')

def inicializar_iluminacao():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])  
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])  
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  

def configurar_material():
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])  
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])  
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)  

def load_texture(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise Exception(f"Erro ao carregar a imagem: {image_path}")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 0)
    texture_data = image.tobytes()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.shape[1], image.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

    return texture_id

def load_obj(file_path):
    vertices = []
    uvs = []
    faces = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == 'v': 
                vertices.append([float(v) for v in parts[1:4]])
            elif parts[0] == 'vt':
                uvs.append([float(v) for v in parts[1:3]])
            elif parts[0] == 'f':  
                face = []
                for vertex in parts[1:]:
                    indices = vertex.split('/')
                    v_idx = int(indices[0]) - 1 
                    vt_idx = int(indices[1]) - 1
                    face.append((v_idx, vt_idx))
                faces.append(face)

    return vertices, uvs, faces

def render_obj(texture_id, vertices, uvs, faces):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex_index, uv_index in face:
            glTexCoord2fv(uvs[uv_index])
            glVertex3fv(vertices[vertex_index])
    glEnd()

    glDisable(GL_TEXTURE_2D)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (screen_width / screen_height), 0.1, 1000)
glMatrixMode(GL_MODELVIEW)
glTranslatef(0, -10, -150)

inicializar_iluminacao()
configurar_material()

texture = load_texture("assets/textures/sword_texture.jpg") 
vertices, uvs, faces = load_obj("assets/models/sword.obj")

sword_angle = 0.0
camera_x, camera_z = 0.0, -100.0  
camera_speed = 2.0

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_z += camera_speed
    if keys[pygame.K_s]:
        camera_z -= camera_speed
    if keys[pygame.K_a]:
        camera_x -= camera_speed
    if keys[pygame.K_d]:
        camera_x += camera_speed

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 5.0, -60.0, 1.0])
    glPopMatrix()

    glLoadIdentity()
    glTranslatef(camera_x, -10, camera_z)

    glPushMatrix()
    glRotatef(90, 1, 0, 0) 
    glRotatef(sword_angle, 1, 0, 0) 
    render_obj(texture, vertices, uvs, faces)
    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)
    sword_angle += 1.0 

pygame.quit()