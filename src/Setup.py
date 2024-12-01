import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import *

from src.Camera import Camera
from src.Sword import Sword
from src.Lighting import Lighting

class Setup:
    def __init__(self):
        pygame.init()

        self.screen_width = 1360
        self.screen_height = 768
        
        self.initialize_screen()
        self.initialize_openGL()

        self.camera = Camera()
        self.camera.initialize_camera(self.screen_width, self.screen_height)

        self.lighting = Lighting()

        self.sword = Sword()

    def initialize_screen(self):
        self.SCREEN = pygame.display.set_mode((self.screen_width, self.screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption('Espada Aerondight - The Witcher 3')

    def initialize_openGL(self):
        glEnable(GL_DEPTH_TEST)

    def start(self):
        is_running = True
        while is_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    is_running = False
                
                if event.type == KEYDOWN:
                    self.camera.move_camera(pygame.key.get_pressed())
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.lighting.update_light_position()

            self.sword.render()

            pygame.display.flip()
            pygame.time.wait(10)

        pygame.quit()
    
