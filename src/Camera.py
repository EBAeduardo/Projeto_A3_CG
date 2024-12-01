import pygame

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import *

class Camera:
    def __init__(self):
        self.camera_x = 0
        self.camera_z = -200
        self.camera_speed = 2.0

    def initialize_camera(self, screen_width, screen_height):
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (screen_width / screen_height), 0.1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0, -10, -200)

    def move_camera(self, keys):
        if keys[pygame.K_w]:
            self.camera_z += self.camera_speed
        if keys[pygame.K_s]:
            self.camera_z -= self.camera_speed
        if keys[pygame.K_d]:
            self.camera_x -= self.camera_speed
        if keys[pygame.K_a]:
            self.camera_x += self.camera_speed
    
        self._refresh_camera_position()
    
    def _refresh_camera_position(self):
        glLoadIdentity()
        glTranslatef(self.camera_x, -10, self.camera_z)