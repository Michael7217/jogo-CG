import glfw

teclas_pressionadas = {}


def retorno_teclado(codigo_tecla, acao):

    if acao == glfw.PRESS:
        teclas_pressionadas[codigo_tecla] = True

    elif acao == glfw.RELEASE:
        teclas_pressionadas[codigo_tecla] = False