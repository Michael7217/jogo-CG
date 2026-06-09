"""
Gerenciador centralizado de unidades.

Responsável por:
- criar e remover unidades
- consultar unidades por posição ou equipe
- manter lista global de unidades
"""

from typing import List, Optional, Dict, Tuple
from .unidade import Unidade, Equipe


class GerenciadorUnidades:
    """
    Gerencia todas as unidades do jogo.
    
    Mantém registro centralizado de unidades e fornece métodos
    para criação, remoção e consulta.
    """
    
    def __init__(self):
        self.unidades: List[Unidade] = []
        self.proximo_id = 1
        
        # Índice para acesso rápido por posição (tile_x, tile_y) -> Unidade
        self._indice_posicao: Dict[Tuple[int, int], Unidade] = {}
    
    def criar_unidade(
        self,
        tile_x: int,
        tile_y: int,
        equipe: Equipe,
        nome: str = "Unidade",
        vida: int = 30,
        movimento: int = 5
    ) -> Unidade:
        """
        Cria uma nova unidade.
        
        Args:
            tile_x: posição X inicial
            tile_y: posição Y inicial
            equipe: JOGADOR_1 ou JOGADOR_2
            nome: nome descritivo da unidade
            vida: pontos de vida
            movimento: tiles de movimento por turno
        
        Returns:
            A unidade criada
        """
        unidade = Unidade(
            id=self.proximo_id,
            tile_x=tile_x,
            tile_y=tile_y,
            vida=vida,
            vida_maxima=vida,
            movimento=movimento,
            equipe=equipe,
            nome=nome
        )
        
        self.proximo_id += 1
        self.unidades.append(unidade)
        self._indice_posicao[(tile_x, tile_y)] = unidade
        
        print(f"[Gerenciador] Unidade criada: {unidade}")
        return unidade
    
    def remover_unidade(self, unidade: Unidade) -> bool:
        """
        Remove uma unidade do jogo.
        
        Args:
            unidade: a unidade a remover
        
        Returns:
            True se removida, False se não encontrada
        """
        if unidade in self.unidades:
            self.unidades.remove(unidade)
            self._limpar_indice_unidade(unidade)
            print(f"[Gerenciador] Unidade removida: id={unidade.id}")
            return True
        return False
    
    def mover_unidade(self, unidade: Unidade, novo_x: int, novo_y: int) -> bool:
        """
        Move uma unidade para uma nova posição.
        
        Args:
            unidade: a unidade a mover
            novo_x: nova posição X
            novo_y: nova posição Y
        
        Returns:
            True se movida com sucesso, False se nova posição ocupada
        """
        # Verifica se nova posição está ocupada
        if (novo_x, novo_y) in self._indice_posicao:
            if self._indice_posicao[(novo_x, novo_y)] != unidade:
                return False
        
        # Remove da posição antiga
        self._limpar_indice_unidade(unidade)
        
        # Atualiza posição
        unidade.mover_para(novo_x, novo_y)
        
        # Atualiza índice
        self._indice_posicao[(novo_x, novo_y)] = unidade
        
        return True
    
    def obter_unidade_posicao(self, tile_x: int, tile_y: int) -> Optional[Unidade]:
        """
        Obtém a unidade em uma posição específica.
        
        Args:
            tile_x: posição X
            tile_y: posição Y
        
        Returns:
            A unidade na posição, ou None se vazia
        """
        return self._indice_posicao.get((tile_x, tile_y))
    
    def obter_unidades_equipe(self, equipe: Equipe) -> List[Unidade]:
        """
        Obtém todas as unidades de uma equipe.
        
        Args:
            equipe: JOGADOR_1 ou JOGADOR_2
        
        Returns:
            Lista de unidades da equipe
        """
        return [u for u in self.unidades if u.equipe == equipe]
    
    def obter_todas_unidades(self) -> List[Unidade]:
        """Retorna lista de todas as unidades."""
        return self.unidades.copy()
    
    def obter_unidade_id(self, unidade_id: int) -> Optional[Unidade]:
        """
        Obtém uma unidade pelo ID.
        
        Args:
            unidade_id: ID da unidade
        
        Returns:
            A unidade ou None se não encontrada
        """
        for u in self.unidades:
            if u.id == unidade_id:
                return u
        return None
    
    def limpar(self):
        """Remove todas as unidades."""
        self.unidades.clear()
        self._indice_posicao.clear()
        self.proximo_id = 1
    
    def resetar_turno(self):
        """Reseta estado de todas as unidades para novo turno."""
        for unidade in self.unidades:
            unidade.resetar_turno()
    
    def _limpar_indice_unidade(self, unidade: Unidade):
        """Remove unidade do índice de posição."""
        posicao = (unidade.tile_x, unidade.tile_y)
        if posicao in self._indice_posicao:
            if self._indice_posicao[posicao] == unidade:
                del self._indice_posicao[posicao]
    
    def __repr__(self) -> str:
        return (
            f"GerenciadorUnidades(total={len(self.unidades)}, "
            f"j1={len(self.obter_unidades_equipe(Equipe.JOGADOR_1))}, "
            f"j2={len(self.obter_unidades_equipe(Equipe.JOGADOR_2))})"
        )
