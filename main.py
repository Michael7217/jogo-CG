import glfw
import time
from grid.grid import Grade
from engine.camera import Camera
from engine.entrada import (
    retorno_teclado,
    retorno_mouse_clique,
    retorno_mouse_movimento,
    registrar_callback_clique,
    teclas_pressionadas
)
from engine.conversao_mouse import mouse_para_tile
from engine.opengl import configurar_opengl
from graficos.renderer import Renderizador3D
from game.gerenciador_jogo import GerenciadorJogo
import config.config as config
from OpenGL.GL import *


def main():
    
    if not glfw.init():
        print("[Erro] Falha ao inicializar GLFW")
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)
    glfw.window_hint(glfw.DEPTH_BITS, 24)

    janela = glfw.create_window(
        config.LARGURA_TELA,
        config.ALTURA_TELA,
        "Colapso energético",
        None,
        None
    )

    if not janela:
        print("[Erro] Falha ao criar janela")
        glfw.terminate()
        return

    glfw.make_context_current(janela)
    
    # Callbacks de entrada
    glfw.set_key_callback(janela, retorno_teclado)
    glfw.set_mouse_button_callback(janela, retorno_mouse_clique)
    glfw.set_cursor_pos_callback(janela, retorno_mouse_movimento)
    
    # Configura OpenGL
    programa_shader = configurar_opengl()
    renderizador = Renderizador3D(programa_shader)

    # Inicialização do jogo
    grade = Grade(config.GRADE_LARGURA, config.GRADE_ALTURA)
    camera = Camera()
    
    camera.x = 0.0
    camera.y = 0.0
    camera.z = 80.0
    
    # Gerenciador do jogo com modo posicionamento
    gerenciador_jogo = GerenciadorJogo(grade, unidades_por_jogador=2)
    gerenciador_jogo.setup_inicial()
    
    # Callback de clique
    def callback_clique(x, y, botao):
        tile = mouse_para_tile(
            x, y,
            config.LARGURA_TELA,
            config.ALTURA_TELA,
            camera
        )
        
        if tile:
            tile_x, tile_y = tile
            gerenciador_jogo.processar_clique_mouse(tile_x, tile_y)
    
    registrar_callback_clique(callback_clique)
    
    tempo_anterior = time.time()
    
    teclas_pressionadas_anteriormente = set()
    
    while not glfw.window_should_close(janela):
        tempo_atual = time.time()
        delta_tempo = tempo_atual - tempo_anterior
        tempo_anterior = tempo_atual
        
        glfw.poll_events()
        camera.mover()
        
        # Processa teclas (evita múltiplos triggers)
        teclas_atuais = set()
        for tecla, pressionada in teclas_pressionadas.items():
            if pressionada:
                teclas_atuais.add(tecla)
                if tecla not in teclas_pressionadas_anteriormente:
                    if tecla == glfw.KEY_SPACE:
                        gerenciador_jogo.processar_tecla(tecla)
                    elif tecla == glfw.KEY_ESCAPE:
                        gerenciador_jogo.processar_tecla(tecla)
        
        teclas_pressionadas_anteriormente = teclas_atuais
        
        gerenciador_jogo.atualizar(delta_tempo)
        
        if gerenciador_jogo.verificar_fim_jogo():
            vencedor = gerenciador_jogo.obter_vencedor()
            print(f"\n[Jogo] FIM! Vencedor: {vencedor}")
            break
        
        # Renderização
        glClearColor(0.05, 0.05, 0.08, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        renderizador.desenhar_grade(grade, camera)
        
        # Desenha tiles alcançáveis
        tiles_alcancaveis = gerenciador_jogo.obter_tiles_alcancaveis_para_renderizar()
        if tiles_alcancaveis:
            renderizador.desenhar_tiles_alcancaveis(tiles_alcancaveis, grade, camera)
        
        # Desenha unidades
        renderizador.desenhar_unidades(gerenciador_jogo.gerenciador_unidades, camera)
        
        glfw.swap_buffers(janela)
    
    print("[Jogo] Encerrando...")
    glfw.terminate()


if __name__ == "__main__":
    main()
