from config.config import (
    TIPO_BLOCO_SOLO, TIPO_BLOCO_PAREDE,
    TIPO_BLOCO_AGUA, TIPO_BLOCO_BURACO,
    TIPO_BLOCO_ACUDE, TIPO_BLOCO_POCO,
    TIPO_BLOCO_CACIMBA, TIPO_BLOCO_DISPUTA
)


class Bloco:

    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.caminhavel = True
        self.destacado = False

        if tipo in (
            TIPO_BLOCO_PAREDE,
            TIPO_BLOCO_AGUA,
            TIPO_BLOCO_BURACO,
            TIPO_BLOCO_ACUDE,
        ):
            self.caminhavel = False