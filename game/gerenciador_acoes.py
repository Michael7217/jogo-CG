"""
Sistema de ações estilo Into the Breach.

Características:
- Cada unidade pode agir apenas 1 vez por turno
- Ações: Mover OU Atacar (futuro)
- Turno termina quando todas unidades agirem ou jogador finalizar
"""

from typing import Set
from .unidade import Unidade, Equipe


class GerenciadorAcoes:
    """
    Gerencia ações de unidades no turno atual.
    
    Into the Breach:
    - 1 ação por unidade por turno
    - Ação = mover OU atacar
    - Unidades que agiram ficam "cinzas"
    """
    
    def __init__(self):
        # IDs de unidades que já agiram neste turno
        self._unidades_que_agiram: Set[int] = set()
    
    def marcar_como_agida(self, unidade: Unidade):
        """
        Marca unidade como tendo agido este turno.
        
        Args:
            unidade: a unidade que agiu
        """
        self._unidades_que_agiram.add(unidade.id)
        unidade.ja_agiu = True
        print(f"[Ações] {unidade.nome} agiu (ID: {unidade.id})")
    
    def pode_agir(self, unidade: Unidade) -> bool:
        """
        Verifica se unidade pode agir este turno.
        
        Args:
            unidade: unidade a verificar
            
        Returns:
            True se pode agir, False caso contrário
        """
        return unidade.id not in self._unidades_que_agiram
    
    def resetar_turno(self, equipe: Equipe = None):
        """
        Reseta ações para novo turno.
        
        Args:
            equipe: se especificado, reseta apenas unidades dessa equipe
        """
        if equipe is None:
            # Reseta tudo
            self._unidades_que_agiram.clear()
            print("[Ações] Todas ações resetadas")
        else:
            # Futuro: resetar apenas unidades de uma equipe
            print(f"[Ações] Ações de {equipe.name} resetadas")
    
    def todas_agiram(self, unidades_equipe: list) -> bool:
        """
        Verifica se todas unidades de uma equipe já agiram.
        
        Args:
            unidades_equipe: lista de unidades da equipe
            
        Returns:
            True se todas agiram
        """
        if not unidades_equipe:
            return True
        
        for unidade in unidades_equipe:
            if unidade.id not in self._unidades_que_agiram:
                return False
        
        return True
    
    def contar_acoes_restantes(self, unidades_equipe: list) -> int:
        """
        Conta quantas unidades ainda podem agir.
        
        Args:
            unidades_equipe: lista de unidades
            
        Returns:
            número de unidades que ainda podem agir
        """
        count = 0
        for unidade in unidades_equipe:
            if unidade.id not in self._unidades_que_agiram:
                count += 1
        return count
