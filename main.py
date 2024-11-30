import cv2
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys


pygame.init()


# project settings
screen_width = 1360
screen_height = 768
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Espada')



# Camera settings
camera_position = [0, 5, -50]  # X, Y, Z
camera_speed = 2.0  # Speed of camera movement

def inicializar_iluminacao():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [10.0, -5.0, 10.0, 0.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.5, 1.5, 1.5, 1.0])

def configurar_material():
    glMaterialfv(GL_FRONT, GL_AMBIENT, [1.5, 1.5, 1.5, 1.0])  # Reflexão ambiente
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])  # Reflexão difusa
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.2, 1.2, 1.2, 1.0])  # Reflexão especular
    glMaterialf(GL_FRONT, GL_SHININESS, 80.0)  # Brilho do material

scale_factor = 1.0

def load_texture(image_path):
    # Carrega a imagem usando OpenCV
    image = cv2.imread(image_path)
    if image is None:
        raise Exception(f"Erro ao carregar a imagem: {image_path}")
    # Converte de BGR (OpenCV) para RGB (OpenGL usa RGB)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Inverte a imagem verticalmente para coincidir com o OpenGL
    image = cv2.flip(image, 0)
    # Converte a imagem para bytes
    texture_data = image.tobytes()

    # Gera um ID de textura no OpenGL
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Define parâmetros da textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Envia os dados da textura para o OpenGL
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
            if parts[0] == 'v':  # Vértices
                vertices.append([float(v) for v in parts[1:4]])
            elif parts[0] == 'vt':  # Coordenadas UV
                uvs.append([float(v) for v in parts[1:3]])
            elif parts[0] == 'f':  # Faces
                face = []
                for vertex in parts[1:]:
                    indices = vertex.split('/')
                    v_idx = int(indices[0]) - 1  # Índice do vértice
                    vt_idx = int(indices[1]) - 1  # Índice da coordenada UV
                    face.append((v_idx, vt_idx))
                faces.append(face)

    return vertices, uvs, faces

def render_obj(texture_id1, texture_id2, texture_id3, texture_id4, texture_id5, vertices, uvs, faces):
    glEnable(GL_TEXTURE_2D)
    glActiveTexture(GL_TEXTURE0)  # Ativa a unidade de textura 0
    glBindTexture(GL_TEXTURE_2D, texture_id1)
    glActiveTexture(GL_TEXTURE4)  # Ativa a unidade de textura 0
    glBindTexture(GL_TEXTURE_2D, texture_id2)
    glActiveTexture(GL_TEXTURE2)  # Ativa a unidade de textura 0
    glBindTexture(GL_TEXTURE_2D, texture_id3)
    glActiveTexture(GL_TEXTURE3)  # Ativa a unidade de textura 0
    glBindTexture(GL_TEXTURE_2D, texture_id4)




    glBegin(GL_TRIANGLES)  # Renderizando faces triangulares
    for face in faces:
        for vertex_index, uv_index in face:
            glTexCoord2fv(uvs[uv_index])       # Aplica coordenadas UV
            glVertex3fv(vertices[vertex_index])  # Desenha vértices
    glEnd()

    glDisable(GL_TEXTURE_2D)


# Inicialização
pygame.init()
screen = pygame.display.set_mode((1360, 768), DOUBLEBUF | OPENGL)
glEnable(GL_DEPTH_TEST)

# Carregar textura e modelo
texture1 = load_texture("img/aerondlight_textura.jpg")  # Substitua pelo nome da sua textura
texture2 = load_texture("img/AOtextura.jpg")
texture3 = load_texture("img/metallictextura.jpg")
texture4 = load_texture("img/roughnesstextura.jpg")
texture5 = load_texture("img/wire_174174174_normal.png")
vertices, uvs, faces = load_obj("obj/Aerondight_tex.obj")  # Substitua pelo nome do seu .obj

# Configuração da câmera
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (screen_width / screen_height), 0.1, 1000)  # Aumenta o zFar para 1000
glMatrixMode(GL_MODELVIEW)
glTranslatef(0, 0, -200)  # Leva a câmera mais longe para compensar o novo zFar
glRotatef(90, 1, -1, 0)  # Rotaciona a câmera 90 graus ao redor do eixo X

def handle_input():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        glTranslatef(camera_speed, 0, 0)
    if keys[pygame.K_s]:
        glTranslatef(-camera_speed, 0, 0)
    if keys[pygame.K_a]:
        glTranslatef(0, -camera_speed, 0)
    if keys[pygame.K_d]:
        glTranslatef(0, camera_speed, 0)


def display():
    glRotatef(1, 0, 0, 1)


# Loop principal
running = True
glEnable(GL_DEPTH_TEST)
inicializar_iluminacao()
glScalef(scale_factor, scale_factor, scale_factor)
while running:
    for event in pygame.event.get():
        handle_input()
        if event.type == QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    render_obj(texture1, texture2, texture3, texture4, texture5, vertices, uvs, faces)
    display()
 
    pygame.display.flip()

    pygame.time.wait(10)

pygame.quit()

