import ctypes
from OpenGL.GL import *
from config.config import (
    LARGURA_TELA, ALTURA_TELA,
    TAMANHO_BLOCO, TIPO_BLOCO_SOLO, TIPO_BLOCO_PAREDE,
    TIPO_BLOCO_AGUA, TIPO_BLOCO_BURACO
)
from graficos.conversoes import bloco_para_mundo


class Renderizador3D:
    def __init__(self, programa_shader):
        self.programa = programa_shader
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, 0, None, GL_DYNAMIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(
            0,
            3,
            GL_FLOAT,
            GL_FALSE,
            7 * ctypes.sizeof(ctypes.c_float),
            ctypes.c_void_p(0)
        )

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(
            1,
            4,
            GL_FLOAT,
            GL_FALSE,
            7 * ctypes.sizeof(ctypes.c_float),
            ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float))
        )

        glBindVertexArray(0)

        self._loc_projection = glGetUniformLocation(self.programa, b"u_projection")
        self._loc_view = glGetUniformLocation(self.programa, b"u_view")

        glUseProgram(self.programa)
        if self._loc_projection != -1:
            proj = glGetFloatv(GL_PROJECTION_MATRIX)
            glUniformMatrix4fv(self._loc_projection, 1, GL_FALSE, proj)
        glUseProgram(0)

    def _atualizar_matrizes(self, camera):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        camera.aplicar_transformacao()

        if self._loc_view != -1:
            view = glGetFloatv(GL_MODELVIEW_MATRIX)
            glUseProgram(self.programa)
            glUniformMatrix4fv(self._loc_view, 1, GL_FALSE, view)
            glUseProgram(0)

    def _enviar_vertices(self, vertices, modo):
        if not vertices:
            return

        buffer = (ctypes.c_float * len(vertices))(*vertices)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(buffer), buffer, GL_DYNAMIC_DRAW)
        glUseProgram(self.programa)
        glDrawArrays(modo, 0, len(vertices) // 7)
        glUseProgram(0)
        glBindVertexArray(0)

    def desenhar_grade(self, grade, camera):
        self._atualizar_matrizes(camera)

        triangulos = []
        linhas = []

        for linha in grade.blocos:
            for bloco in linha:
                mundo_x, mundo_y, mundo_z = bloco_para_mundo(bloco.x, bloco.y)

                if bloco.tipo == TIPO_BLOCO_SOLO:
                    cor = (0.2, 0.2, 0.2, 1.0)
                elif bloco.tipo == TIPO_BLOCO_PAREDE:
                    cor = (0.5, 0.5, 0.5, 1.0)
                elif bloco.tipo == TIPO_BLOCO_AGUA:
                    cor = (0.1, 0.3, 0.8, 1.0)
                elif bloco.tipo == TIPO_BLOCO_BURACO:
                    cor = (0.0, 0.0, 0.0, 1.0)
                else:
                    cor = (0.2, 0.2, 0.2, 1.0)

                triangulos.extend(self._quads_para_triangulos(mundo_x, mundo_y, mundo_z, TAMANHO_BLOCO, cor))

                if bloco.destacado:
                    destaque = (0.0, 1.0, 1.0, 0.5)
                    triangulos.extend(self._quads_para_triangulos(mundo_x, mundo_y, mundo_z, TAMANHO_BLOCO, destaque))

                linhas.extend(self._quads_para_linhas(mundo_x, mundo_y, mundo_z, TAMANHO_BLOCO, (0.1, 0.1, 0.1, 1.0)))

        self._enviar_vertices(triangulos, GL_TRIANGLES)
        self._enviar_vertices(linhas, GL_LINES)

    @staticmethod
    def _quads_para_triangulos(x, y, z, tamanho, cor):
        r, g, b, a = cor
        return [
            x - tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a,
            x + tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a,
            x + tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a,
            x - tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a,
            x + tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a,
            x - tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a,
        ]

    @staticmethod
    def _quads_para_linhas(x, y, z, tamanho, cor):
        r, g, b, a = cor
        return [
            x - tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a,
            x + tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a,
            x + tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a,
            x + tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a,
            x + tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a,
            x - tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a,
            x - tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a,
            x - tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a,
        ]

