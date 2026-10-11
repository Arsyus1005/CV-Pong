import pygame
from configuracion import VELOCIDAD_PALA, ALTO
from core.fisica import limitar_pala


class ModoTeclado:
    def __init__(self, estado):
        self.estado = estado

    def actualizar(self, dt):
        teclas = pygame.key.get_pressed()
        vel_jugador = 0
        if teclas[pygame.K_UP]:
            vel_jugador = -VELOCIDAD_PALA
        if teclas[pygame.K_DOWN]:
            vel_jugador = VELOCIDAD_PALA
        self.estado.jugador.y += int(vel_jugador * dt * 60)
        limitar_pala(self.estado.jugador)

        vel_oponente = 0
        if teclas[pygame.K_w]:
            vel_oponente = -VELOCIDAD_PALA
        if teclas[pygame.K_s]:
            vel_oponente = VELOCIDAD_PALA
        self.estado.oponente.y += int(vel_oponente * dt * 60)
        limitar_pala(self.estado.oponente)
