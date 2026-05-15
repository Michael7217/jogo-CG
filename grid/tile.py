from config.config import (
    TIPO_BLOCO_SOLO, TIPO_BLOCO_PAREDE,
    TIPO_BLOCO_AGUA, TIPO_BLOCO_BURACO
)


class Bloco:

    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.caminhavel = True
        self.destacado = False

        if tipo == TIPO_BLOCO_PAREDE:
            self.caminhavel = False
        elif tipo == TIPO_BLOCO_AGUA:
            self.caminhavel = False
        elif tipo == TIPO_BLOCO_BURACO:
            self.caminhavel = False