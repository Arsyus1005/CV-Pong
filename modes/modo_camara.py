import pygame
from configuracion import ALTO_PALA, ALTO, ANCHO, SUAVIZADO, CAMARA_Y_MIN, CAMARA_Y_MAX


class ModoCamara:
    def __init__(self, estado, camara):
        self.estado = estado
        self.camara = camara
        self.ultimo_izq = estado.oponente.centery
        self.ultimo_der = estado.jugador.centery

    def _remapear(self, yn):
        rango = max(1e-6, CAMARA_Y_MAX - CAMARA_Y_MIN)
        t = (yn - CAMARA_Y_MIN) / rango
        t = max(0.0, min(1.0, t))
        return t * ALTO

    def _interpolar(self, a, b, t):
        return a + (b - a) * max(0.0, min(1.0, t))

    def actualizar(self, dt, posiciones=None):
        posiciones = posiciones or []
        medio = 0.5
        objetivo_izq = None
        objetivo_der = None

        if posiciones:
            ordenadas = sorted(posiciones, key=lambda p: p["xn"])
            if len(ordenadas) >= 2:
                objetivo_izq = ordenadas[0]
                objetivo_der = ordenadas[-1]
            else:
                unica = ordenadas[0]
                if unica["xn"] < medio:
                    objetivo_izq = unica
                else:
                    objetivo_der = unica

        if objetivo_izq is not None:
            y = self._remapear(objetivo_izq["yn"])
            cy_nuevo = self._interpolar(self.ultimo_izq, y, SUAVIZADO)
            cy_nuevo = max(ALTO_PALA // 2, min(ALTO - ALTO_PALA // 2, cy_nuevo))
            self.ultimo_izq = cy_nuevo
            self.estado.oponente.centery = int(cy_nuevo)
        else:
            self.ultimo_izq = self.estado.oponente.centery

        if objetivo_der is not None:
            y = self._remapear(objetivo_der["yn"])
            cy_nuevo = self._interpolar(self.ultimo_der, y, SUAVIZADO)
            cy_nuevo = max(ALTO_PALA // 2, min(ALTO - ALTO_PALA // 2, cy_nuevo))
            self.ultimo_der = cy_nuevo
            self.estado.jugador.centery = int(cy_nuevo)
        else:
            self.ultimo_der = self.estado.jugador.centery

        self.estado.oponente.top = int(self.estado.oponente.centery - ALTO_PALA // 2)
        self.estado.oponente.bottom = int(self.estado.oponente.centery + ALTO_PALA // 2)
        self.estado.jugador.top = int(self.estado.jugador.centery - ALTO_PALA // 2)
        self.estado.jugador.bottom = int(self.estado.jugador.centery + ALTO_PALA // 2)
