"""
Modo de posicionamento de personagens.

Permite que jogadores posicionem suas unidades no início do jogo.
"""

from typing import Optional, Set, Tuple
from .unidade import Unidade, Equipe
from .gerenciador_unidades import GerenciadorUnidades
from grid.grid import Grade


class ModoPosicionamento:
    """
    Gerencia o posicionamento inicial de unidades.
    
    Fluxo:
    1. JOGADOR_1 posiciona suas unidades clicando nos tiles
    2. JOGADOR_2 posiciona suas unidades clicando nos tiles
    3. Quando ambos terminarem, inicia o jogo
    """
    
    def __init__(
        self,
        gerenciador_unidades: GerenciadorUnidades,
        grade: Grade,
        unidades_por_jogador: int = 2
    ):
        self.gerenciador = gerenciador_unidades
        self.grade = grade
        self.unidades_por_jogador = unidades_por_jogador
        
        # Estado do posicionamento
        self.jogador_posicionando = Equipe.JOGADOR_1
        self.unidades_posicionadas_j1 = 0
        self.unidades_posicionadas_j2 = 0
        self.posicionamento_completo = False
        
    def processar_clique(self, tile_x: int, tile_y: int) -> bool:
        """
        Processa clique para posicionar unidade.
        
        Args:
            tile_x: posição X do tile
            tile_y: posição Y do tile
            
        Returns:
            True se posicionou unidade, False caso contrário
        """
        # Verifica se tile é válido
        if not self._tile_valido(tile_x, tile_y):
            print(f"[Posicionamento] Tile ({tile_x}, {tile_y}) inválido!")
            return False
        
        # Verifica se tile está vazio
        if self.gerenciador.obter_unidade_posicao(tile_x, tile_y):
            print(f"[Posicionamento] Tile ({tile_x}, {tile_y}) já ocupado!")
            return False
        
        # Posiciona unidade
        self._posicionar_unidade(tile_x, tile_y)
        return True
    
    def _posicionar_unidade(self, tile_x: int, tile_y: int):
        """Posiciona uma unidade no tile."""
        if self.jogador_posicionando == Equipe.JOGADOR_1:
            self.unidades_posicionadas_j1 += 1
            nome = f"Unidade J1-{self.unidades_posicionadas_j1}"
            equipe = Equipe.JOGADOR_1
        else:
            self.unidades_posicionadas_j2 += 1
            nome = f"Unidade J2-{self.unidades_posicionadas_j2}"
            equipe = Equipe.JOGADOR_2
        
        # Cria unidade
        unidade = self.gerenciador.criar_unidade(
            tile_x=tile_x,
            tile_y=tile_y,
            equipe=equipe,
            nome=nome,
            vida=30,
            movimento=5
        )
        
        print(f"[Posicionamento] {nome} posicionada em ({tile_x}, {tile_y})")
        
        # Verifica se jogador terminou
        if self._jogador_terminou():
            self._trocar_jogador()
    
    def _jogador_terminou(self) -> bool:
        """Verifica se o jogador atual terminou de posicionar."""
        if self.jogador_posicionando == Equipe.JOGADOR_1:
            return self.unidades_posicionadas_j1 >= self.unidades_por_jogador
        else:
            return self.unidades_posicionadas_j2 >= self.unidades_por_jogador
    
    def _trocar_jogador(self):
        """Troca para o próximo jogador."""
        if self.jogador_posicionando == Equipe.JOGADOR_1:
            # Se JOGADOR_2 já terminou, posicionamento completo
            if self.unidades_posicionadas_j2 >= self.unidades_por_jogador:
                self.posicionamento_completo = True
                print("\n[Posicionamento] ✓ POSICIONAMENTO COMPLETO! Iniciando jogo...\n")
            else:
                self.jogador_posicionando = Equipe.JOGADOR_2
                print(f"\n[Posicionamento] Vez de JOGADOR_2 posicionar! ({self.unidades_por_jogador} unidades)\n")
        else:
            # Se JOGADOR_1 já terminou, posicionamento completo
            if self.unidades_posicionadas_j1 >= self.unidades_por_jogador:
                self.posicionamento_completo = True
                print("\n[Posicionamento] ✓ POSICIONAMENTO COMPLETO! Iniciando jogo...\n")
            else:
                self.jogador_posicionando = Equipe.JOGADOR_1
                print(f"\n[Posicionamento] Vez de JOGADOR_1 posicionar! ({self.unidades_por_jogador} unidades)\n")
    
    def _tile_valido(self, tile_x: int, tile_y: int) -> bool:
        """Verifica se tile é válido para posicionamento."""
        # Dentro do grid
        if tile_x < 0 or tile_x >= self.grade.largura:
            return False
        if tile_y < 0 or tile_y >= self.grade.altura:
            return False
        
        # Tile é caminhável
        bloco = self.grade.obter_bloco(tile_x, tile_y)
        if not bloco or not bloco.caminhavel:
            return False
        
        return True
    
    def esta_completo(self) -> bool:
        """Retorna True se posicionamento está completo."""
        return self.posicionamento_completo
    
    def obter_jogador_posicionando(self) -> Equipe:
        """Retorna qual jogador está posicionando."""
        return self.jogador_posicionando
    
    def obter_info(self) -> str:
        """Retorna informações do posicionamento."""
        if self.jogador_posicionando == Equipe.JOGADOR_1:
            return f"JOGADOR_1 posicionando: {self.unidades_posicionadas_j1}/{self.unidades_por_jogador}"
        else:
            return f"JOGADOR_2 posicionando: {self.unidades_posicionadas_j2}/{self.unidades_por_jogador}"
