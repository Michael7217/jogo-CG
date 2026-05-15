import glfw
from OpenGL.GL import glTranslatef, glRotatef
from engine.entrada import teclas_pressionadas
from config.config import VELOCIDADE_CAMERA, ZOOM_PADRAO


class Camera:

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 60.0
        self.pitch = 40.0
        self.yaw = 45.0
        self.velocidade = VELOCIDADE_CAMERA
        self.zoom = ZOOM_PADRAO

    def mover(self):
        if teclas_pressionadas.get(glfw.KEY_W):
            self.y -= self.velocidade

        if teclas_pressionadas.get(glfw.KEY_S):
            self.y += self.velocidade

        if teclas_pressionadas.get(glfw.KEY_A):
            self.x -= self.velocidade

        if teclas_pressionadas.get(glfw.KEY_D):
            self.x += self.velocidade

        if teclas_pressionadas.get(glfw.KEY_Q):
            self.z += self.velocidade * 0.5

        if teclas_pressionadas.get(glfw.KEY_E):
            self.z = max(16.0, self.z - self.velocidade * 0.5)

    def aplicar_transformacao(self):
        glTranslatef(-self.x, -self.y, -self.z)
        glRotatef(-self.pitch, 1.0, 0.0, 0.0)
        glRotatef(-self.yaw, 0.0, 0.0, 1.0)