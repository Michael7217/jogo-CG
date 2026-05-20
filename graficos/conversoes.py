from config.config import GRADE_LARGURA, GRADE_ALTURA, TAMANHO_BLOCO


def bloco_para_mundo(bloco_x, bloco_y):
    largura_mundo = GRADE_LARGURA * TAMANHO_BLOCO
    altura_mundo = GRADE_ALTURA * TAMANHO_BLOCO
    mundo_x = bloco_x * TAMANHO_BLOCO - largura_mundo * 0.5 + TAMANHO_BLOCO * 0.5
    mundo_y = bloco_y * TAMANHO_BLOCO - altura_mundo * 0.5 + TAMANHO_BLOCO * 0.5
    return mundo_x, mundo_y, 0.0