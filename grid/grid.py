from grid.tile import Bloco
from config.config import (
    TIPO_BLOCO_SOLO, TIPO_BLOCO_PAREDE,
    TIPO_BLOCO_AGUA, TIPO_BLOCO_BURACO
)


class Grade:

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.blocos = []

        for y in range(altura):
            linha = []
            for x in range(largura):
                tipo = TIPO_BLOCO_SOLO

                if x == 5 and y < 8:
                    tipo = TIPO_BLOCO_PAREDE
                if x == 10 and y > 8:
                    tipo = TIPO_BLOCO_AGUA
                if x == 3 and y == 12:
                    tipo = TIPO_BLOCO_BURACO

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