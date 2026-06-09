"""
Sistema de turnos baseado em rodadas.

Gerencia:
- qual jogador tem a vez
- número da rodada
- transição entre turnos
"""

from enum import Enum, auto
from .unidade import Equipe
from .gerenciador_unidades import GerenciadorUnidades


class Jogador(Enum):
    """Identificação dos jogadores."""
    JOGADOR_1 = Equipe.JOGADOR_1
    JOGADOR_2 = Equipe.JOGADOR_2


class SistemaTurno:
    """
    Gerencia o sistema de turnos do jogo.
    
    Funciona com alternância entre dois jogadores:
    - JOGADOR_1 (humano)
    - JOGADOR_2 (humano)
    
    Uma rodada completa = turno JOGADOR_1 + turno JOGADOR_2
    """
    
    def __init__(self, gerenciador_unidades: GerenciadorUnidades):
        self.gerenciador_unidades = gerenciador_unidades
        
        # Estado do turno
        self.jogador_atual = Jogador.JOGADOR_1
        self.rodada_numero = 1
        self.turno_numero = 1
        
        # Histórico para debug
        self._historico_turnos = []
    
    def obter_jogador_atual(self) -> Jogador:
        """Retorna o jogador que tem a vez."""
        return self.jogador_atual
    
    def obter_equipe_atual(self) -> Equipe:
        """Retorna a equipe do jogador que tem a vez."""
        return self.jogador_atual.value
    
    def obter_rodada(self) -> int:
        """Retorna o número da rodada."""
        return self.rodada_numero
    
    def obter_turno(self) -> int:
        """Retorna o número total de turnos jogados."""
        return self.turno_numero
    
    def eh_turno_jogador(self, equipe: Equipe) -> bool:
        """Verifica se é o turno de uma equipe específica."""
        return self.obter_equipe_atual() == equipe
    
    def finalizar_turno(self):
        """
        Finaliza o turno atual e passa para o próximo jogador.
        
        Lógica:
        - reseta ações das unidades do jogador atual
        - muda para o próximo jogador
        - incrementa número de rodadas se ambos tiverem terminado
        """
        # Reseta ações das unidades do jogador que terminou
        unidades_jogador = self.gerenciador_unidades.obter_unidades_equipe(
            self.obter_equipe_atual()
        )
        
        for unidade in unidades_jogador:
            unidade.resetar_turno()
        
        # Registra este turno no histórico
        self._historico_turnos.append({
            'turno': self.turno_numero,
            'rodada': self.rodada_numero,
            'jogador': self.jogador_atual
        })
        
        # Muda para próximo jogador
        self._trocar_jogador()
        
        # Se voltou para JOGADOR_1, incrementa rodada
        if self.jogador_atual == Jogador.JOGADOR_1:
            self.rodada_numero += 1
        
        self.turno_numero += 1
        
        print(f"[Turno] Rodada {self.rodada_numero}, Turno {self.turno_numero}")
        print(f"[Turno] Vez de {self.jogador_atual.name}")
    
    def resetar_jogo(self):
        """Reseta o sistema de turnos para começar um novo jogo."""
        self.jogador_atual = Jogador.JOGADOR_1
        self.rodada_numero = 1
        self.turno_numero = 1
        self._historico_turnos.clear()
        print("[Turno] Jogo resetado")
    
    def _trocar_jogador(self):
        """Muda para o outro jogador."""
        if self.jogador_atual == Jogador.JOGADOR_1:
            self.jogador_atual = Jogador.JOGADOR_2
        else:
            self.jogador_atual = Jogador.JOGADOR_1
    
    def obter_historico(self) -> list:
        """Retorna histórico de turnos jogados."""
        return self._historico_turnos.copy()
    
    def obter_informacao_turno(self) -> str:
        """Retorna string formatada com informações do turno atual."""
        return (
            f"Rodada {self.rodada_numero} | "
            f"Turno {self.turno_numero} | "
            f"Jogador: {self.jogador_atual.name}"
        )
    
    def __repr__(self) -> str:
        return (
            f"SistemaTurno(rodada={self.rodada_numero}, "
            f"turno={self.turno_numero}, "
            f"jogador={self.jogador_atual.name})"
        )
