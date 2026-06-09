from typing import Tuple, Optional
from config.config import TAMANHO_BLOCO, GRADE_LARGURA, GRADE_ALTURA


def mouse_para_tile(
    mouse_x: int,
    mouse_y: int,
    largura_janela: int,
    altura_janela: int,
    camera
) -> Optional[Tuple[int, int]]:

    
    mouse_relativo_x = mouse_x - largura_janela * 0.5
    mouse_relativo_y = mouse_y - altura_janela * 0.5
    
    # Compensa zoom da câmera (quanto maior o Z, mais "zoom out" = maior area visível)
    escala = camera.z / 60.0  # Z=60 é o padrão
    mundo_x = mouse_relativo_x * escala + camera.x
    mundo_y = -mouse_relativo_y * escala + camera.y  # Y invertido
    
    # Converte para tile
    return mundo_para_tile(mundo_x, mundo_y)


def mundo_para_tile(mundo_x: float, mundo_y: float) -> Optional[Tuple[int, int]]:
    """
    Converte coordenadas do mundo para tile.
    
    Args:
        mundo_x: posição X no mundo
        mundo_y: posição Y no mundo
    
    Returns:
        Tupla (tile_x, tile_y) ou None se fora do grid
    """
    
    # Calcula o centro do mundo
    largura_mundo = GRADE_LARGURA * TAMANHO_BLOCO
    altura_mundo = GRADE_ALTURA * TAMANHO_BLOCO
    
    # Converte para coordenadas relativas ao centro
    x_relativo = mundo_x + (largura_mundo * 0.5)
    y_relativo = mundo_y + (altura_mundo * 0.5)
    
    # Converte para tile (com floor para garantir inteiro correto)
    tile_x = int(x_relativo / TAMANHO_BLOCO)
    tile_y = int(y_relativo / TAMANHO_BLOCO)
    
    # Valida se está dentro do grid
    if 0 <= tile_x < GRADE_LARGURA and 0 <= tile_y < GRADE_ALTURA:
        return (tile_x, tile_y)
    
    return None


def tile_para_mundo(tile_x: int, tile_y: int) -> Tuple[float, float, float]:
    """
    Converte coordenadas de tile para mundo.
    
    Retorna posição no centro do tile.
    
    Args:
        tile_x: posição X no tile
        tile_y: posição Y no tile
    
    Returns:
        Tupla (mundo_x, mundo_y, mundo_z)
    """
    
    largura_mundo = GRADE_LARGURA * TAMANHO_BLOCO
    altura_mundo = GRADE_ALTURA * TAMANHO_BLOCO
    
    mundo_x = tile_x * TAMANHO_BLOCO - largura_mundo * 0.5 + TAMANHO_BLOCO * 0.5
    mundo_y = tile_y * TAMANHO_BLOCO - altura_mundo * 0.5 + TAMANHO_BLOCO * 0.5
    
    return mundo_x, mundo_y, 0.0


def eh_tile_valido(tile_x: int, tile_y: int) -> bool:
    """Verifica se tile está dentro do grid."""
    return 0 <= tile_x < GRADE_LARGURA and 0 <= tile_y < GRADE_ALTURA

