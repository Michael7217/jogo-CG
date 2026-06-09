"""
Definição da classe Unidade.

Representa uma unidade no tabuleiro:
- posição (tile_x, tile_y)
- atributos (vida, movimento, equipe)
- estado (selecionado, ja_agiu)
"""

from enum import Enum, auto
from dataclasses import dataclass, field


class Equipe(Enum):
    """Enumeração das equipes no jogo."""
    JOGADOR_1 = auto()
    JOGADOR_2 = auto()


@dataclass
class Unidade:
    """
    Representa uma unidade do jogo.
    
    Atributos:
        id: identificador único da unidade
        tile_x: posição X no tabuleiro (baseado em tiles)
        tile_y: posição Y no tabuleiro (baseado em tiles)
        vida: pontos de vida atual
        vida_maxima: pontos de vida máximos
        movimento: tiles que pode mover por turno
        equipe: a qual jogador pertence (JOGADOR_1 ou JOGADOR_2)
        selecionado: se está selecionado atualmente
        ja_agiu: se já realizou ação neste turno
    """
    
    id: int
    tile_x: int
    tile_y: int
    vida: int = 30
    vida_maxima: int = 30
    movimento: int = 5
    equipe: Equipe = Equipe.JOGADOR_1
    selecionado: bool = False
    ja_agiu: bool = False
    
    # Atributos adicionais para futuras expansões
    ataque: int = 0
    defesa: int = 0
    nome: str = "Unidade"
    
    def __hash__(self):
        """Permite usar Unidade em sets e dicts."""
        return hash(self.id)
    
    def esta_viva(self) -> bool:
        """Retorna se a unidade ainda tem vida."""
        return self.vida > 0
    
    def mover_para(self, novo_x: int, novo_y: int):
        """Move a unidade para uma nova posição (sem validação)."""
        self.tile_x = novo_x
        self.tile_y = novo_y
    
    def receber_dano(self, dano: int) -> bool:
        """
        Aplica dano à unidade.
        
        Returns:
            True se a unidade morreu, False caso contrário
        """
        self.vida = max(0, self.vida - dano)
        return not self.esta_viva()
    
    def curar(self, quantidade: int):
        """Cura a unidade até o máximo de vida."""
        self.vida = min(self.vida_maxima, self.vida + quantidade)
    
    def resetar_turno(self):
        """Reseta estado da unidade para o novo turno."""
        self.ja_agiu = False
        self.selecionado = False
    
    def marcar_como_agida(self):
        """Marca a unidade como tendo agido este turno."""
        self.ja_agiu = True
    
    def selecionar(self):
        """Marca a unidade como selecionada."""
        self.selecionado = True
    
    def desselecionar(self):
        """Marca a unidade como não selecionada."""
        self.selecionado = False
    
    def obter_posicao(self) -> tuple:
        """Retorna a posição atual como tupla (x, y)."""
        return (self.tile_x, self.tile_y)
    
    def __repr__(self) -> str:
        return (
            f"Unidade(id={self.id}, nome='{self.nome}', "
            f"pos=({self.tile_x}, {self.tile_y}), "
            f"vida={self.vida}/{self.vida_maxima}, "
            f"equipe={self.equipe.name}, "
            f"agida={self.ja_agiu})"
        )
