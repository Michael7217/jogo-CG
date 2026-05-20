import glfw
from grid.grid import Grade
from engine.camera import Camera
from engine.entrada import retorno_teclado
from engine.opengl import configurar_opengl
from graficos.renderer import Renderizador3D
import config.config as config
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, glClear, glClearColor
from graficos.conversoes import bloco_para_mundo


def principal():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)
    glfw.window_hint(glfw.DEPTH_BITS, 24)

    janela = glfw.create_window(
        config.LARGURA_TELA,
        config.ALTURA_TELA,
        "Sertão Tático",
        None,
        None
    )

    if not janela:
        glfw.terminate()
        return

    glfw.make_context_current(janela)
    glfw.set_key_callback(janela, retorno_teclado)
    programa_shader = configurar_opengl()
    renderer = Renderizador3D(programa_shader)

    grade = Grade(config.GRADE_LARGURA, config.GRADE_ALTURA)
    camera = Camera()

    camera.x = 0.0
    camera.y = 0.0
    camera.z = 80.0

    while not glfw.window_should_close(janela):
        glfw.poll_events()
        camera.mover()

        glClearColor(0.05, 0.05, 0.08, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        renderer.desenhar_grade(grade, camera)
        mx, my, mz = bloco_para_mundo(1, 2)
        renderer.desenhar_modelo('aldeao', camera, mx, my, mz + 0.0, escala=1.0)
        glfw.swap_buffers(janela)

    glfw.terminate()


if __name__ == "__main__":
    principal()
