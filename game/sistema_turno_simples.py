"""
Sistema de turnos simples.

Alterna entre JOGADOR_1 e JOGADOR_2 (ambos humanos).
Cada jogador tem sua vez de jogar por turno completo.
"""

from enum import Enum
from .unidade import Equipe


class JogadorAtual(Enum):
    """Jogador que tem a vez de jogar."""
    JOGADOR_1 = 1
    JOGADOR_2 = 2


class SistemaTurnoSimples:
    """
    Sistema de turnos simples para 2 jogadores humanos.
    
    Funcionalidade:
    - Alterna entre JOGADOR_1 e JOGADOR_2
    - Cada jogador joga até pressionar SPACE
    - Sem limite de ações por turno (pode mover todas as unidades)
    """
    
    def __init__(self):
        self.jogador_atual = JogadorAtual.JOGADOR_1
        self.numero_turno = 1
        self.numero_rodada = 1
        
    def finalizar_turno(self):
        """
        Finaliza o turno do jogador atual e passa para o próximo.
        """
        print(f"\n[Turno] Jogador {self.jogador_atual.value} finalizou seu turno")
        
        # Alterna jogador
        if self.jogador_atual == JogadorAtual.JOGADOR_1:
            self.jogador_atual = JogadorAtual.JOGADOR_2
        else:
            self.jogador_atual = JogadorAtual.JOGADOR_1
            self.numero_rodada += 1  # Nova rodada quando volta para J1
        
        self.numero_turno += 1
        
        print(f"[Turno] Agora é a vez do Jogador {self.jogador_atual.value}")
        print(f"[Turno] Rodada {self.numero_rodada} | Turno {self.numero_turno}\n")
    
    def obter_jogador_atual(self) -> JogadorAtual:
        """Retorna o jogador que tem a vez."""
        return self.jogador_atual
    
    def obter_equipe_atual(self) -> Equipe:
        """Retorna a equipe do jogador atual."""
        if self.jogador_atual == JogadorAtual.JOGADOR_1:
            return Equipe.JOGADOR_1
        else:
            return Equipe.JOGADOR_2
    
    def obter_numero_jogador(self) -> int:
        """Retorna o número do jogador (1 ou 2)."""
        return self.jogador_atual.value
    
    def obter_info(self) -> str:
        """Retorna informação formatada do turno."""
        return (
            f"Rodada {self.numero_rodada} | "
            f"Turno {self.numero_turno} | "
            f"Jogador {self.jogador_atual.value}"
        )
    
    def eh_vez_de(self, equipe: Equipe) -> bool:
        """Verifica se é a vez de uma equipe específica."""
        return self.obter_equipe_atual() == equipe
