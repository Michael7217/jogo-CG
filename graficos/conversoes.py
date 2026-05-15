from config.config import GRADE_LARGURA, GRADE_ALTURA, TAMANHO_BLOCO


def bloco_para_mundo(bloco_x, bloco_y):
    largura_mundo = GRADE_LARGURA * TAMANHO_BLOCO
    altura_mundo = GRADE_ALTURA * TAMANHO_BLOCO
    mundo_x = bloco_x * TAMANHO_BLOCO - largura_mundo * 0.5 + TAMANHO_BLOCO * 0.5
    mundo_y = bloco_y * TAMANHO_BLOCO - altura_mundo * 0.5 + TAMANHO_BLOCO * 0.5
    return mundo_x, mundo_y, 0.0


def tela_para_mundo(tela_x, tela_y, camera):
    mundo_x = tela_x + camera.x
    mundo_y = tela_y + camera.y
    return mundo_x, mundo_y


def mundo_para_bloco(mundo_x, mundo_y):
    bloco_x = int(mundo_x // TAMANHO_BLOCO)
    bloco_y = int(mundo_y // TAMANHO_BLOCO)
    return bloco_x, bloco_y