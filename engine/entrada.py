import glfw
from typing import Callable, Optional

teclas_pressionadas = {}

# Callbacks de mouse
callback_clique_mouse: Optional[Callable[[int, int, int], None]] = None
callback_movimento_mouse: Optional[Callable[[float, float], None]] = None


def retorno_teclado(_janela, codigo_tecla, _scancode, acao, _mods):
    if acao == glfw.PRESS:
        teclas_pressionadas[codigo_tecla] = True
    elif acao == glfw.RELEASE:
        teclas_pressionadas[codigo_tecla] = False


def retorno_mouse_clique(_janela, botao, acao, _mods):
    """Callback para cliques de mouse."""
    if acao == glfw.PRESS and botao == glfw.MOUSE_BUTTON_LEFT:
        if callback_clique_mouse:
            x, y = glfw.get_cursor_pos(_janela)
            callback_clique_mouse(int(x), int(y), botao)


def retorno_mouse_movimento(_janela, x, y):
    """Callback para movimento de mouse."""
    if callback_movimento_mouse:
        callback_movimento_mouse(x, y)


def registrar_callback_clique(funcao: Callable[[int, int, int], None]):
    """Registra callback para cliques de mouse."""
    global callback_clique_mouse
    callback_clique_mouse = funcao


def registrar_callback_movimento(funcao: Callable[[float, float], None]):
    """Registra callback para movimento de mouse."""
    global callback_movimento_mouse
    callback_movimento_mouse = funcao