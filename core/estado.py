import random
import pygame
from configuracion import (
    ANCHO, ALTO, ANCHO_PALA, ALTO_PALA,
    VELOCIDAD_PELOTA_X, VELOCIDAD_PELOTA_Y, RETARDO_SAQUE, TIEMPO_PARTIDA, PUNTOS_VICTORIA,
)
from core.fisica import centrar_pelota


class EstadoJuego:
    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self.pelota = pygame.Rect(ANCHO / 2 - 15, ALTO / 2 - 15, 30, 30)
        self.jugador = pygame.Rect(ANCHO - 20, ALTO / 2 - 70, 10, 140)
        self.oponente = pygame.Rect(10, ALTO / 2 - 70, 10, 140)
        self.vel_x = 0
        self.vel_y = 0
        self.puntaje_j = 0
        self.puntaje_o = 0
        self.temporizador_saque = RETARDO_SAQUE
        self.esperando_saque = True
        self.direccion_saque = random.choice((1, -1))

        self.temporizador_partida = TIEMPO_PARTIDA
        self.juego_terminado = False
        self.ganador = None

    def iniciar_saque(self, direccion, retardo=RETARDO_SAQUE):
        centrar_pelota(self.pelota)
        self.vel_x = 0
        self.vel_y = 0
        self.direccion_saque = direccion
        self.temporizador_saque = retardo
        self.esperando_saque = True

    def determinar_ganador(self):
        if self.puntaje_j > self.puntaje_o:
            return "jugador"
        if self.puntaje_o > self.puntaje_j:
            return "oponente"
        return "empate"
