# core/fisica.py
import pygame
import random
from configuracion import ANCHO, ALTO, VELOCIDAD_PELOTA_X, VELOCIDAD_PELOTA_Y


def crear_pelota():
    return pygame.Rect(ANCHO / 2 - 15, ALTO / 2 - 15, 30, 30)


def centrar_pelota(pelota):
    pelota.center = (ANCHO // 2, ALTO // 2)


def lanzar_pelota(direccion):
    vel_x = VELOCIDAD_PELOTA_X * direccion
    vel_y = VELOCIDAD_PELOTA_Y * random.choice((1, -1))
    return vel_x, vel_y

# Me toco poner esta webada para que no se pegara la pelota en la raqueta xd
def _resolver_pala(pelota, pala, vel_x, vel_y):

    if not pelota.colliderect(pala):
        return vel_x, vel_y, False

    solape_izq = pelota.right - pala.left
    solape_der = pala.right - pelota.left
    solape_sup = pelota.bottom - pala.top
    solape_inf = pala.bottom - pelota.top

    menor_x = min(solape_izq, solape_der)
    menor_y = min(solape_sup, solape_inf)

    if menor_x <= menor_y:
        #rebote horizontal
        if solape_izq < solape_der:
            pelota.right = pala.left
            if vel_x > 0:
                vel_x = -vel_x
        else:
            pelota.left = pala.right
            if vel_x < 0:
                vel_x = -vel_x
    else:
        # rebote vertical
        if solape_sup < solape_inf:
            pelota.bottom = pala.top
            if vel_y > 0:
                vel_y = -vel_y
        else:
            pelota.top = pala.bottom
            if vel_y < 0:
                vel_y = -vel_y

    return vel_x, vel_y, True


def animar_pelota(pelota, jugador, oponente, vel_x, vel_y):
    pelota.x += vel_x
    pelota.y += vel_y

    # Paredes
    pared = False
    if pelota.top <= 0:
        pelota.top = 0
        vel_y = abs(vel_y)
        pared = True
    if pelota.bottom >= ALTO:
        pelota.bottom = ALTO
        vel_y = -abs(vel_y)
        pared = True


    anotado_jugador = False
    anotado_oponente = False
    if pelota.right < 0:
        anotado_jugador = True
    elif pelota.left > ANCHO:
        anotado_oponente = True

    raqueta = False
    if not anotado_jugador and not anotado_oponente:
        vel_x, vel_y, golpe_jugador = _resolver_pala(pelota, jugador, vel_x, vel_y)
        vel_x, vel_y, golpe_oponente = _resolver_pala(pelota, oponente, vel_x, vel_y)
        raqueta = golpe_jugador or golpe_oponente

    return vel_x, vel_y, anotado_jugador, anotado_oponente, pared, raqueta


def limitar_pala(pala):
    if pala.top <= 0:
        pala.top = 0
    if pala.bottom >= ALTO:
        pala.bottom = ALTO
