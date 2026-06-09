"""
Gerenciador geral do estado do jogo.

Integra todos os sistemas:
- turnos
- unidades
- seleção
- estados

Coordena a lógica do jogo mantendo separação entre gameplay e renderização.
"""

from typing import Optional
from game.estados_jogo import EstadoJogo, TransicaoEstado
from game.gerenciador_unidades import GerenciadorUnidades
from game.sistema_turno_simples import SistemaTurnoSimples
from game.sistema_selecao import SistemaSelecao
from game.modo_posicionamento import ModoPosicionamento
from game.gerenciador_acoes import GerenciadorAcoes
from game.unidade import Equipe
from grid.grid import Grade


class GerenciadorJogo:
    """
    Gerenciador central do jogo.
    
    Mantém referência a todos os sistemas e coordena o fluxo do jogo.
    Responsável por:
    - inicializar sistemas
    - processar entrada
    - atualizar lógica
    - consultar estado para renderização
    """
    
    def __init__(self, grade: Grade, unidades_por_jogador: int = 2):
        """
        Inicializa o gerenciador do jogo.
        
        Args:
            grade: a Grade (tabuleiro do jogo)
            unidades_por_jogador: quantas unidades cada jogador pode posicionar
        """
        self.grade = grade
        self.unidades_por_jogador = unidades_por_jogador
        
        # Inicializa sistemas
        self.gerenciador_unidades = GerenciadorUnidades()
        self.sistema_turno = SistemaTurnoSimples()
        self.gerenciador_acoes = GerenciadorAcoes()
        self.modo_posicionamento = ModoPosicionamento(
            self.gerenciador_unidades,
            self.grade,
            unidades_por_jogador
        )
        self.sistema_selecao = SistemaSelecao(
            self.gerenciador_unidades,
            self.sistema_turno,
            self.grade
        )
        self.transicao_estado = TransicaoEstado()
        
        # Estado do jogo
        self.jogo_ativo = True
        self.tempo_total = 0.0
        self.em_posicionamento = True  # Começa em modo posicionamento
    
    # ===================================================================
    # INICIALIZAÇÃO
    # ===================================================================
    
    def setup_inicial(self):
        """Configura o estado inicial do jogo."""
        print("\n" + "="*60)
        print("MODO POSICIONAMENTO")
        print("="*60)
        print(f"Cada jogador deve posicionar {self.unidades_por_jogador} unidades")
        print("Clique em um tile vazio para posicionar sua unidade")
        print("="*60)
        print(f"\n{self.modo_posicionamento.obter_info()}\n")
    
    # ===================================================================
    # INPUT
    # ===================================================================
    
    def processar_clique_mouse(self, tile_x: int, tile_y: int):
        """
        Processa clique do mouse no tabuleiro.
        
        Args:
            tile_x: posição X do tile clicado
            tile_y: posição Y do tile clicado
        """
        
        # Se em modo posicionamento
        if self.em_posicionamento:
            sucesso = self.modo_posicionamento.processar_clique(tile_x, tile_y)
            
            # Verifica se posicionamento terminou
            if self.modo_posicionamento.esta_completo():
                self.em_posicionamento = False
                print(f"\n[Jogo] Iniciando partida!")
                print(f"[Jogo] {self.sistema_turno.obter_info()}\n")
            return
        
        # Modo de jogo normal - só processa se no modo de seleção
        if self.transicao_estado.estado_atual != EstadoJogo.MODO_SELECAO:
            return
        
        # Processa clique através do sistema de seleção
        houve_acao = self.sistema_selecao.processar_clique(tile_x, tile_y)
        
        # Verifica se deve mudar para modo movimento
        if self.sistema_selecao.unidade_selecionada:
            self.transicao_estado.mudar_estado(EstadoJogo.MODO_MOVIMENTO)
        else:
            self.transicao_estado.mudar_estado(EstadoJogo.MODO_SELECAO)
    
    def processar_tecla(self, codigo_tecla: int):
        """
        Processa pressionamento de tecla.
        
        Args:
            codigo_tecla: código GLFW da tecla
        """
        import glfw
        
        # Ignora teclas durante posicionamento
        if self.em_posicionamento:
            return
        
        if codigo_tecla == glfw.KEY_SPACE:
            # Space para finalizar turno
            self.finalizar_turno_atual()
        
        elif codigo_tecla == glfw.KEY_ESCAPE:
            # Escape para deselecionar
            self.sistema_selecao.desselecionar_todas()
            self.transicao_estado.mudar_estado(EstadoJogo.MODO_SELECAO)
    
    # ===================================================================
    # LÓGICA DO JOGO
    # ===================================================================
    
    def atualizar(self, delta_tempo: float):
        """
        Atualiza lógica do jogo.
        
        Args:
            delta_tempo: tempo decorrido desde último frame (segundos)
        """
        self.tempo_total += delta_tempo
        
        # Atualiza transição de estado
        self.transicao_estado.atualizar(delta_tempo)
        
        # Lógica específica de cada estado
        if self.transicao_estado.estado_atual == EstadoJogo.MODO_ANIMACAO:
            self._atualizar_animacoes(delta_tempo)
        
        elif self.transicao_estado.estado_atual == EstadoJogo.MODO_TRANSICAO_TURNO:
            self._atualizar_transicao_turno(delta_tempo)
    
    def _atualizar_animacoes(self, delta_tempo: float):
        """Atualiza animações em progresso."""
        # Placeholder para animações futuras
        # Quando transição completa, volta para modo seleção
        if self.transicao_estado.transicao_completa():
            self.transicao_estado.mudar_estado(EstadoJogo.MODO_SELECAO)
    
    def _atualizar_transicao_turno(self, delta_tempo: float):
        """Atualiza transição de turno."""
        # Quando transição completa, volta para seleção
        if self.transicao_estado.transicao_completa():
            self.transicao_estado.mudar_estado(EstadoJogo.MODO_SELECAO)
    
    def finalizar_turno_atual(self):
        """Finaliza o turno do jogador atual."""
        # Reseta ações
        self.gerenciador_acoes.resetar_turno()
        
        # Reseta unidades (ja_agiu = False)
        for unidade in self.gerenciador_unidades.obter_todas_unidades():
            unidade.resetar_turno()
        
        # Transição de turno
        self.sistema_turno.finalizar_turno()
        self.sistema_selecao.desselecionar_todas()
        
        # Muda estado
        self.transicao_estado.mudar_estado(EstadoJogo.MODO_TRANSICAO_TURNO)
    
    # ===================================================================
    # CONSULTAS PARA RENDERIZAÇÃO
    # ===================================================================
    
    def obter_unidades_para_renderizar(self):
        """Retorna lista de unidades para renderizar."""
        return self.gerenciador_unidades.obter_todas_unidades()
    
    def obter_tiles_alcancaveis_para_renderizar(self):
        """Retorna tiles alcançáveis para desenhar destaque."""
        return self.sistema_selecao.obter_tiles_alcancaveis()
    
    def obter_unidade_selecionada(self):
        """Retorna unidade selecionada ou None."""
        return self.sistema_selecao.obter_unidade_selecionada()
    
    def obter_estado_turno(self) -> str:
        """Retorna string com informações do turno."""
        if self.em_posicionamento:
            return self.modo_posicionamento.obter_info()
        return self.sistema_turno.obter_info()
    
    def obter_estado_jogo_atual(self) -> EstadoJogo:
        """Retorna estado atual do jogo."""
        return self.transicao_estado.estado_atual
    
    # ===================================================================
    # CONSULTAS GERAIS
    # ===================================================================
    
    def verificar_fim_jogo(self) -> bool:
        """Verifica se jogo terminou (uma equipe sem unidades)."""
        if self.em_posicionamento:
            return False

        unidades_totais = self.gerenciador_unidades.obter_todas_unidades()
        if not unidades_totais:
            return False

        j1 = self.gerenciador_unidades.obter_unidades_equipe(Equipe.JOGADOR_1)
        j2 = self.gerenciador_unidades.obter_unidades_equipe(Equipe.JOGADOR_2)
        
        return len(j1) == 0 or len(j2) == 0
    
    def obter_vencedor(self) -> Optional[str]:
        """Retorna o vencedor ou None se jogo não terminou."""
        if self.em_posicionamento or not self.verificar_fim_jogo():
            return None
        
        j1 = self.gerenciador_unidades.obter_unidades_equipe(Equipe.JOGADOR_1)
        j2 = self.gerenciador_unidades.obter_unidades_equipe(Equipe.JOGADOR_2)
        
        if len(j1) > 0:
            return "JOGADOR_1"
        elif len(j2) > 0:
            return "JOGADOR_2"
        
        return None
    
    # ===================================================================
    # DEBUG
    # ===================================================================
    
    def debug_info(self) -> str:
        """Retorna informações debug do jogo."""
        return (
            f"Estado: {self.transicao_estado.estado_atual.name} | "
            f"{self.sistema_turno.obter_informacao_turno()} | "
            f"Unidades: {len(self.gerenciador_unidades.obter_todas_unidades())}"
        )
    
    def __repr__(self) -> str:
        return (
            f"GerenciadorJogo("
            f"estado={self.transicao_estado.estado_atual.name}, "
            f"{self.sistema_turno}, "
            f"{self.gerenciador_unidades})"
        )
