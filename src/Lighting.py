from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import *

class Lighting:
    def __init__ (self):
        self.start_lighting()
        self.configure_material()

    def update_light_position(self):
        glPushMatrix()
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 5.0, -60.0, 1.0])
        glPopMatrix()

    def start_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    def configure_material(self):
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
        