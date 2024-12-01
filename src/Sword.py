from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import *

import cv2 # type: ignore

class Sword:
    def __init__(self):
        self.angle = 0
        self.texture_path = 'assets/textures/sword_texture.jpg'
        self.obj_path = 'assets/models/sword.obj'
    
    def render(self):
        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        glRotatef(self.angle, 1, 0, 0)

        vertices, uvs, faces = self.load_object()
        texture_id = self.load_texture()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glBegin(GL_TRIANGLES)

        for face in faces:
            for vertex_index, uv_index in face:
                glTexCoord2fv(uvs[uv_index])
                glVertex3fv(vertices[vertex_index])

        glEnd()
        
        glDisable(GL_TEXTURE_2D)
        glDeleteTextures([texture_id])

        self._increment_angle()

        glPopMatrix()

    def load_texture(self):
        image = cv2.imread(self.texture_path)

        if image is None:
            raise Exception(f"Erro ao carregar a imagem: {self.texture_path}")
        
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
    
    def load_object(self):
        vertices = []
        uvs = []
        faces = []

        with open(self.obj_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if not parts:
                    continue

                if parts[0] == 'v':
                    vertex = [float(coord) for coord in parts[1:4]]
                    vertices.append(vertex)

                elif parts[0] == 'vt':
                    uv = [float(coord) for coord in parts[1:3]]
                    uvs.append(uv)

                elif parts[0] == 'f':
                    face = self._parse_face(parts[1:])
                    faces.append(face)

        return vertices, uvs, faces
    
    def _parse_face(self, face_parts):
        face = []
        for vertex in face_parts:
            vertex_indices = vertex.split('/')
            vertex_index = int(vertex_indices[0]) - 1
            uv_index = int(vertex_indices[1]) - 1
            face.append((vertex_index, uv_index))

        return face
    
    def _increment_angle(self):
        self.angle += 1

        if self.angle >= 360:
            self.angle = 0
