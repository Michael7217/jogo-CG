from grid.tile import Bloco
from config.config import (
    TIPO_BLOCO_SOLO,
    TIPO_BLOCO_ACUDE,
    TIPO_BLOCO_POCO,
    TIPO_BLOCO_CACIMBA,
    TIPO_BLOCO_DISPUTA,
)


class Grade:

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.blocos = []

        layout = [
            [TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_DISPUTA, TIPO_BLOCO_DISPUTA, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO],
            [TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_DISPUTA, TIPO_BLOCO_DISPUTA, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO],
            [TIPO_BLOCO_SOLO, TIPO_BLOCO_POCO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_CACIMBA, TIPO_BLOCO_SOLO],
            [TIPO_BLOCO_SOLO, TIPO_BLOCO_POCO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_CACIMBA, TIPO_BLOCO_SOLO],
            [TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_ACUDE, TIPO_BLOCO_ACUDE, TIPO_BLOCO_ACUDE, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO],
            [TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_ACUDE, TIPO_BLOCO_ACUDE, TIPO_BLOCO_ACUDE, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO],
            [TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO],
            [TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO, TIPO_BLOCO_SOLO],
        ]

        for y in range(altura):
            linha = []
            for x in range(largura):
                tipo = TIPO_BLOCO_SOLO
                if y < len(layout) and x < len(layout[y]):
                    tipo = layout[y][x]
                linha.append(Bloco(x, y, tipo))

            self.blocos.append(linha)

    def obter_bloco(self, x, y):
        if 0 <= x < self.largura and 0 <= y < self.altura:
            return self.blocos[y][x]
        return None

    def limpar_destaques(self):
        for linha in self.blocos:
            for bloco in linha:
                bloco.destacado = False