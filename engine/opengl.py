import ctypes
from pathlib import Path
from OpenGL.GL import *
from config.config import LARGURA_TELA, ALTURA_TELA


def carregar_shader(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def compilar_shader(fonte, tipo):
    shader = glCreateShader(tipo)
    glShaderSource(shader, fonte)
    glCompileShader(shader)

    sucesso = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not sucesso:
        info = glGetShaderInfoLog(shader).decode(errors="ignore")
        glDeleteShader(shader)
        raise RuntimeError(f"Falha ao compilar shader: {info}")

    return shader


def criar_programa_shader():
    shaders_dir = Path(__file__).resolve().parent.parent / "shaders"
    vert_path = shaders_dir / "quad.vert.glsl"
    frag_path = shaders_dir / "quad.frag.glsl"

    vert_shader = compilar_shader(carregar_shader(vert_path), GL_VERTEX_SHADER)
    frag_shader = compilar_shader(carregar_shader(frag_path), GL_FRAGMENT_SHADER)

    programa = glCreateProgram()
    glAttachShader(programa, vert_shader)
    glAttachShader(programa, frag_shader)
    glBindAttribLocation(programa, 0, b"a_position")
    glBindAttribLocation(programa, 1, b"a_color")
    glLinkProgram(programa)

    sucesso = glGetProgramiv(programa, GL_LINK_STATUS)
    if not sucesso:
        info = glGetProgramInfoLog(programa).decode(errors="ignore")
        glDeleteProgram(programa)
        raise RuntimeError(f"Falha ao linkar programa de shader: {info}")

    glDeleteShader(vert_shader)
    glDeleteShader(frag_shader)
    return programa


def configurar_opengl():
    glViewport(0, 0, LARGURA_TELA, ALTURA_TELA)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(
        -LARGURA_TELA * 0.5,
        LARGURA_TELA * 0.5,
        -ALTURA_TELA * 0.5,
        ALTURA_TELA * 0.5,
        -1000,
        1000
    )
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearDepth(1.0)

    return criar_programa_shader()
