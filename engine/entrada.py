import glfw

teclas_pressionadas = {}


def retorno_teclado(_janela, codigo_tecla, _scancode, acao, _mods):

    if acao == glfw.PRESS:
        teclas_pressionadas[codigo_tecla] = True

    elif acao == glfw.RELEASE:
        teclas_pressionadas[codigo_tecla] = False