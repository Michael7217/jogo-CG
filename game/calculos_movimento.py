"""
Cálculo de movimento usando BFS (Breadth-First Search).

Implementa busca por amplitude para encontrar todos os tiles
alcançáveis a partir de uma posição com limite de movimento.
"""

from collections import deque
from typing import Set, Tuple, Optional
from grid.grid import Grade


def calcular_tiles_alcancaveis(
    grade: Grade,
    tile_x_inicial: int,
    tile_y_inicial: int,
    distancia_maxima: int,
    eh_valido_callback=None
) -> Set[Tuple[int, int]]:
    """
    Calcula todos os tiles alcançáveis usando BFS.
    
    Implementação de algoritmo Breadth-First Search para encontrar
    todos os tiles que uma unidade pode alcançar com o movimento disponível.
    
    Algoritmo BFS:
    1. Coloca posição inicial na fila
    2. Para cada posição da fila:
       - se ainda tem movimento, explora vizinhos
       - marca vizinho como visitado
       - adiciona vizinho à fila
    3. Repete até fila vazia
    
    Complexidade:
    - Tempo: O(N) onde N = total de tiles no mapa
    - Espaço: O(movimento_maxima²) para tiles alcançáveis
    
    Args:
        grade: a Grade (grid do jogo)
        tile_x_inicial: posição X inicial
        tile_y_inicial: posição Y inicial
        distancia_maxima: número máximo de tiles que pode mover
        eh_valido_callback: função(x, y) -> bool para validar tiles
                          se None, usa validação padrão
    
    Returns:
        Set de tuplas (x, y) representando tiles alcançáveis
    """
    
    if distancia_maxima <= 0:
        return set()
    
    # Set de tiles visitados
    visitados = set()
    
    # Fila com (x, y, distancia_restante)
    fila = deque([(tile_x_inicial, tile_y_inicial, 0)])
    visitados.add((tile_x_inicial, tile_y_inicial))
    
    # 4 direções: cima, baixo, esquerda, direita
    direcoes = [
        (0, -1),   # cima
        (0, 1),    # baixo
        (-1, 0),   # esquerda
        (1, 0),    # direita
    ]
    
    # Set de tiles alcançáveis (não incluindo inicial)
    alcancaveis = set()
    
    while fila:
        x, y, dist = fila.popleft()
        
        # Explora vizinhos
        for dx, dy in direcoes:
            novo_x = x + dx
            novo_y = y + dy
            
            # Pula se já visitado
            if (novo_x, novo_y) in visitados:
                continue
            
            # Valida tile
            if not _eh_tile_valido(grade, novo_x, novo_y, eh_valido_callback):
                continue
            
            # Se temos movimento restante, adiciona à fila
            if dist + 1 <= distancia_maxima:
                visitados.add((novo_x, novo_y))
                fila.append((novo_x, novo_y, dist + 1))
                alcancaveis.add((novo_x, novo_y))
    
    return alcancaveis


def calcular_tiles_alcancaveis_com_obstaculos(
    grade: Grade,
    tile_x_inicial: int,
    tile_y_inicial: int,
    distancia_maxima: int,
    gerenciador_unidades=None
) -> Set[Tuple[int, int]]:
    """
    Calcula tiles alcançáveis considerando obstáculos (outras unidades).
    
    Args:
        grade: a Grade
        tile_x_inicial: posição X inicial
        tile_y_inicial: posição Y inicial
        distancia_maxima: movimento disponível
        gerenciador_unidades: GerenciadorUnidades para checar ocupação
    
    Returns:
        Set de tiles alcançáveis
    """
    
    def eh_valido_com_obstaculos(x, y):
        # Verifica se está dentro do grid
        if x < 0 or x >= grade.largura or y < 0 or y >= grade.altura:
            return False
        
        # Verifica se o tile é caminhável
        bloco = grade.obter_bloco(x, y)
        if not bloco or not bloco.caminhavel:
            return False
        
        # Verifica se está ocupado por outra unidade
        if gerenciador_unidades:
            unidade = gerenciador_unidades.obter_unidade_posicao(x, y)
            if unidade:
                return False
        
        return True
    
    return calcular_tiles_alcancaveis(
        grade,
        tile_x_inicial,
        tile_y_inicial,
        distancia_maxima,
        eh_valido_com_obstaculos
    )


def _eh_tile_valido(
    grade: Grade,
    tile_x: int,
    tile_y: int,
    callback_customizado=None
) -> bool:
    """
    Valida se um tile é válido para movimento.
    
    Checagens:
    1. Dentro dos limites do grid
    2. Tile é caminhável (não é água, parede, etc)
    3. Callback customizado (se fornecido)
    
    Args:
        grade: a Grade
        tile_x: posição X
        tile_y: posição Y
        callback_customizado: função(x, y) -> bool adicional
    
    Returns:
        True se tile é válido, False caso contrário
    """
    
    # Checa limites
    if tile_x < 0 or tile_x >= grade.largura or tile_y < 0 or tile_y >= grade.altura:
        return False
    
    # Checa se é caminhável
    bloco = grade.obter_bloco(tile_x, tile_y)
    if not bloco or not bloco.caminhavel:
        return False
    
    # Checa callback customizado
    if callback_customizado and not callback_customizado(tile_x, tile_y):
        return False
    
    return True


def calcular_distancia_manhattan(
    x1: int,
    y1: int,
    x2: int,
    y2: int
) -> int:
    """
    Calcula distância Manhattan entre dois tiles.
    
    Usada para heurísticas e cálculos simples.
    Distância = |x1 - x2| + |y1 - y2|
    """
    return abs(x1 - x2) + abs(y1 - y2)


def calcular_distancia_euclidiana(
    x1: int,
    y1: int,
    x2: int,
    y2: int
) -> float:
    """
    Calcula distância Euclidiana entre dois tiles.
    
    Usada para cálculos mais precisos de distância.
    Distância = √((x1-x2)² + (y1-y2)²)
    """
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
