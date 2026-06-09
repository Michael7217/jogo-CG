"""
Sistema de preview de movimento estilo Into the Breach.

Mostra visualmente:
- Caminho que a unidade vai percorrer
- Posição final com preview da unidade
- Linha conectando posição atual e destino
"""

from typing import List, Tuple, Optional
from game.unidade import Unidade


class PreviewMovimento:
    """
    Gerencia preview visual de movimento antes de confirmar.
    
    Estilo Into the Breach:
    - Mostra caminho com linha
    - Preview da unidade no destino
    - Confirma com clique ou cancela com ESC
    """
    
    def __init__(self):
        self.ativo = False
        self.unidade_preview: Optional[Unidade] = None
        self.posicao_origem: Optional[Tuple[int, int]] = None
        self.posicao_destino: Optional[Tuple[int, int]] = None
        self.caminho: List[Tuple[int, int]] = []
    
    def ativar(
        self,
        unidade: Unidade,
        origem: Tuple[int, int],
        destino: Tuple[int, int]
    ):
        """
        Ativa preview de movimento.
        
        Args:
            unidade: unidade que vai mover
            origem: posição atual (tile_x, tile_y)
            destino: posição de destino (tile_x, tile_y)
        """
        self.ativo = True
        self.unidade_preview = unidade
        self.posicao_origem = origem
        self.posicao_destino = destino
        self.caminho = self._calcular_caminho_simples(origem, destino)
    
    def desativar(self):
        """Desativa o preview."""
        self.ativo = False
        self.unidade_preview = None
        self.posicao_origem = None
        self.posicao_destino = None
        self.caminho.clear()
    
    def obter_posicao_destino(self) -> Optional[Tuple[int, int]]:
        """Retorna posição de destino do preview."""
        return self.posicao_destino if self.ativo else None
    
    def obter_caminho(self) -> List[Tuple[int, int]]:
        """Retorna caminho do preview."""
        return self.caminho if self.ativo else []
    
    def _calcular_caminho_simples(
        self,
        origem: Tuple[int, int],
        destino: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """
        Calcula caminho simples (linha reta em grid).
        
        Move primeiro no eixo X, depois no eixo Y.
        """
        caminho = []
        x_atual, y_atual = origem
        x_dest, y_dest = destino
        
        # Move no eixo X
        while x_atual != x_dest:
            if x_atual < x_dest:
                x_atual += 1
            else:
                x_atual -= 1
            caminho.append((x_atual, y_atual))
        
        # Move no eixo Y
        while y_atual != y_dest:
            if y_atual < y_dest:
                y_atual += 1
            else:
                y_atual -= 1
            caminho.append((x_atual, y_atual))
        
        return caminho
