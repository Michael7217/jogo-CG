"""
Módulo de lógica do jogo (GAME LOGIC).

Este pacote contém toda a lógica de gameplay, completamente separada da renderização.
Oferece classes para gerenciar turnos, unidades, seleção e movimento.
"""

from .estados_jogo import EstadoJogo, TransicaoEstado
from .unidade import Unidade, Equipe
from .gerenciador_unidades import GerenciadorUnidades
from .sistema_turno import SistemaTurno, Jogador
from .sistema_selecao import SistemaSelecao
from .calculos_movimento import calcular_tiles_alcancaveis
from .gerenciador_jogo import GerenciadorJogo

__all__ = [
    'EstadoJogo',
    'TransicaoEstado',
    'Unidade',
    'Equipe',
    'GerenciadorUnidades',
    'SistemaTurno',
    'Jogador',
    'SistemaSelecao',
    'calcular_tiles_alcancaveis',
    'GerenciadorJogo',
]

