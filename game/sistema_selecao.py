"""
Sistema de seleção baseado em mouse.

Gerencia:
- detecção de cliques do mouse
- seleção de unidades
- movimento de unidades
- validação de ações

Fluxo:
1. Clique em unidade do jogador atual → seleciona
2. Destaca tiles alcançáveis
3. Clique em tile válido → move unidade
4. Unidade recebe ja_agiu = True
"""

from typing import Optional, Tuple, Set
from .unidade import Unidade, Equipe
from .gerenciador_unidades import GerenciadorUnidades
from .calculos_movimento import (
    calcular_tiles_alcancaveis_com_obstaculos,
    calcular_distancia_manhattan
)
from .preview_movimento import PreviewMovimento


class SistemaSelecao:
    """
    Gerencia seleção e movimento de unidades via mouse.
    
    Estados de seleção:
    - nenhuma unidade selecionada
    - unidade selecionada (mostrando tiles alcançáveis)
    - unidade sendo movida
    """
    
    def __init__(
        self,
        gerenciador_unidades: GerenciadorUnidades,
        sistema_turno,  # Aceita qualquer tipo de sistema de turno
        grade: 'Grade'
    ):
        self.gerenciador = gerenciador_unidades
        self.sistema_turno = sistema_turno
        self.grade = grade
        
        # Estado de seleção
        self.unidade_selecionada: Optional[Unidade] = None
        self.tiles_alcancaveis: Set[Tuple[int, int]] = set()
        
        # Preview de movimento (estilo Into the Breach)
        self.preview = PreviewMovimento()
        
        # Debug
        self._ultimo_clique_pos = None
    
    def processar_clique(self, tile_x: int, tile_y: int) -> bool:
        """
        Processa clique do mouse em um tile.
        
        Lógica:
        1. Se nenhuma unidade selecionada:
           - verifica se tem unidade no tile
           - se é do jogador atual, seleciona
        2. Se unidade selecionada:
           - se clique em unidade selecionada, deseleciona
           - se clique em outro tile alcançável, move
           - se clique em unidade amiga, seleciona outra
           - se clique fora de range, deseleciona
        
        Args:
            tile_x: posição X do clique
            tile_y: posição Y do clique
        
        Returns:
            True se houve ação, False caso contrário
        """
        
        self._ultimo_clique_pos = (tile_x, tile_y)
        
        # Nenhuma unidade selecionada
        if not self.unidade_selecionada:
            return self._processar_clique_sem_selecao(tile_x, tile_y)
        
        # Unidade já selecionada
        return self._processar_clique_com_selecao(tile_x, tile_y)
    
    def _processar_clique_sem_selecao(self, tile_x: int, tile_y: int) -> bool:
        """Processa clique quando nenhuma unidade está selecionada."""
        
        # Verifica se há unidade no tile
        unidade = self.gerenciador.obter_unidade_posicao(tile_x, tile_y)
        
        if not unidade:
            return False
        
        # Verifica se é do jogador atual
        if unidade.equipe != self.sistema_turno.obter_equipe_atual():
            print(f"[Seleção] Unidade inimiga! Selecione uma unidade sua.")
            return False
        
        # Verifica se já agiu (apenas se o sistema de turno tiver controle de ações)
        if hasattr(unidade, 'ja_agiu') and unidade.ja_agiu:
            print(f"[Seleção] Unidade já agiu neste turno!")
            return False
        
        # Seleciona unidade
        self.selecionar_unidade(unidade)
        return True
    
    def _processar_clique_com_selecao(self, tile_x: int, tile_y: int) -> bool:
        """Processa clique quando já existe unidade selecionada."""
        
        # Clique na mesma unidade = deseleciona
        if (self.unidade_selecionada.tile_x == tile_x and
            self.unidade_selecionada.tile_y == tile_y):
            self.desselecionar_unidade()
            return True
        
        # Clique em unidade amiga = seleciona outra
        unidade = self.gerenciador.obter_unidade_posicao(tile_x, tile_y)
        if unidade:
            if unidade.equipe == self.sistema_turno.obter_equipe_atual():
                if not unidade.ja_agiu:
                    self.selecionar_unidade(unidade)
                    return True
            return False
        
        # Clique em tile alcançável = move
        if (tile_x, tile_y) in self.tiles_alcancaveis:
            self.mover_unidade(tile_x, tile_y)
            return True
        
        # Clique fora de range = deseleciona
        self.desselecionar_unidade()
        return False
    
    def selecionar_unidade(self, unidade: Unidade):
        """
        Seleciona uma unidade e calcula seus tiles alcançáveis.
        
        Args:
            unidade: unidade a selecionar
        """
        # Deseleciona anterior se existir
        if self.unidade_selecionada:
            self.unidade_selecionada.desselecionar()
        
        # Seleciona nova
        self.unidade_selecionada = unidade
        unidade.selecionar()
        
        # Calcula tiles alcançáveis
        self._recalcular_tiles_alcancaveis()
        
        print(f"[Seleção] Unidade selecionada: {unidade.nome} (id={unidade.id})")
        print(f"[Seleção] Tiles alcançáveis: {len(self.tiles_alcancaveis)}")
    
    def desselecionar_unidade(self):
        """Deseleciona a unidade atual."""
        if self.unidade_selecionada:
            self.unidade_selecionada.desselecionar()
            self.unidade_selecionada = None
            self.tiles_alcancaveis.clear()
            self.grade.limpar_destaques()
            print("[Seleção] Unidade deseleccionada")
    
    def mover_unidade(self, tile_x_destino: int, tile_y_destino: int) -> bool:
        """
        Move a unidade selecionada para um novo tile.
        
        Validações:
        - tile deve estar em tiles_alcancaveis
        - tile deve estar vazio
        - calcula custo de movimento
        
        Args:
            tile_x_destino: nova posição X
            tile_y_destino: nova posição Y
        
        Returns:
            True se moveu com sucesso, False caso contrário
        """
        
        if not self.unidade_selecionada:
            return False
        
        # Valida se tile é alcançável
        if (tile_x_destino, tile_y_destino) not in self.tiles_alcancaveis:
            return False
        
        # Calcula distância (custo de movimento)
        distancia = calcular_distancia_manhattan(
            self.unidade_selecionada.tile_x,
            self.unidade_selecionada.tile_y,
            tile_x_destino,
            tile_y_destino
        )
        
        # Verifica se há espaço
        if self.gerenciador.obter_unidade_posicao(tile_x_destino, tile_y_destino):
            return False
        
        # Move unidade
        sucesso = self.gerenciador.mover_unidade(
            self.unidade_selecionada,
            tile_x_destino,
            tile_y_destino
        )
        
        if sucesso:
            # Marca como tendo agido (apenas se suportado)
            if hasattr(self.unidade_selecionada, 'marcar_como_agida'):
                self.unidade_selecionada.marcar_como_agida()
            
            print(
                f"[Seleção] {self.unidade_selecionada.nome} moveu de "
                f"({self.unidade_selecionada.tile_x}, "
                f"{self.unidade_selecionada.tile_y}) "
                f"para ({tile_x_destino}, {tile_y_destino}) "
                f"(distância: {distancia})"
            )
            
            # Deseleciona após movimento
            self.desselecionar_unidade()
        
        return sucesso
    
    def _recalcular_tiles_alcancaveis(self):
        """Recalcula tiles alcançáveis para unidade selecionada."""
        
        if not self.unidade_selecionada:
            self.tiles_alcancaveis.clear()
            return
        
        unidade = self.unidade_selecionada
        
        # Calcula usando BFS
        self.tiles_alcancaveis = calcular_tiles_alcancaveis_com_obstaculos(
            self.grade,
            unidade.tile_x,
            unidade.tile_y,
            unidade.movimento,
            self.gerenciador
        )
        
        # Destaca tiles na grade
        self.grade.limpar_destaques()
        for tile_x, tile_y in self.tiles_alcancaveis:
            bloco = self.grade.obter_bloco(tile_x, tile_y)
            if bloco:
                bloco.destacado = True
    
    def obter_unidade_selecionada(self) -> Optional[Unidade]:
        """Retorna unidade selecionada ou None."""
        return self.unidade_selecionada
    
    def obter_tiles_alcancaveis(self) -> Set[Tuple[int, int]]:
        """Retorna set de tiles alcançáveis."""
        return self.tiles_alcancaveis.copy()
    
    def desselecionar_todas(self):
        """Deseleciona tudo (útil para transição de turno)."""
        self.desselecionar_unidade()
        self.preview.desativar()
    
    def processar_hover_mouse(self, tile_x: int, tile_y: int):
        """
        Processa hover do mouse sobre tile (preview de movimento).
        
        Estilo Into the Breach: mostra preview antes de confirmar.
        """
        if not self.unidade_selecionada:
            self.preview.desativar()
            return
        
        if (tile_x, tile_y) in self.tiles_alcancaveis:
            origem = (self.unidade_selecionada.tile_x, self.unidade_selecionada.tile_y)
            self.preview.ativar(self.unidade_selecionada, origem, (tile_x, tile_y))
        else:
            self.preview.desativar()
    
    def obter_preview_movimento(self) -> PreviewMovimento:
        """Retorna o preview de movimento atual."""
        return self.preview
    
    def __repr__(self) -> str:
        selecionada = self.unidade_selecionada.nome if self.unidade_selecionada else "None"
        return (
            f"SistemaSelecao(selecionada={selecionada}, "
            f"alcancaveis={len(self.tiles_alcancaveis)})"
        )
