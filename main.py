import math
import pygame
import sys
from configuracion import (
    ANCHO, ALTO, FPS, FUENTE_REGULAR, TAMANO_FUENTE, COLOR_FONDO, HUD_DEPURACION, PUNTOS_VICTORIA,
    MOSTRAR_FPS, MOSTRAR_MANOS, MOSTRAR_AYUDA_ESC,
)
from core.estado import EstadoJuego
from core.fisica import animar_pelota, lanzar_pelota
from core.audio import GestorAudio
from modes.teclado import ModoTeclado
from modes.modo_camara import ModoCamara
from vision.camara import GestorCamara
from ui.renderizador import Renderizador

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("CamPONG o PONGCam?")
reloj = pygame.time.Clock()
try:
    fuente = pygame.font.Font(FUENTE_REGULAR, TAMANO_FUENTE)
except Exception:
    fuente = pygame.font.Font(None, TAMANO_FUENTE)

estado = EstadoJuego()
renderizador = Renderizador(pantalla, fuente)


def actualizar_juego(dt, usar_camara, modo_camara, teclado, posiciones, audio=None):
    if usar_camara:
        modo_camara.actualizar(dt, posiciones)
    else:
        teclado.actualizar(dt)

    if estado.juego_terminado:
        return

    if estado.esperando_saque:
        estado.temporizador_saque -= dt
        if estado.temporizador_saque <= 0:
            estado.temporizador_saque = 0
            estado.esperando_saque = False
            estado.vel_x, estado.vel_y = lanzar_pelota(estado.direccion_saque)
    else:
        vel_x, vel_y, anotado_j, anotado_o, pared, raqueta = animar_pelota(
            estado.pelota, estado.jugador, estado.oponente, estado.vel_x, estado.vel_y
        )
        estado.vel_x, estado.vel_y = vel_x, vel_y
        if audio is not None:
            if pared:
                audio.sonar_pared()
            if raqueta:
                audio.sonar_raqueta()
        if anotado_j or anotado_o:
            if anotado_j:
                estado.puntaje_j += 1
            if anotado_o:
                estado.puntaje_o += 1
            if PUNTOS_VICTORIA and (estado.puntaje_j >= PUNTOS_VICTORIA or estado.puntaje_o >= PUNTOS_VICTORIA):
                estado.juego_terminado = True
                estado.ganador = estado.determinar_ganador()
            else:
                direccion = -1 if anotado_j else 1
                estado.iniciar_saque(direccion)

    if not estado.juego_terminado:
        estado.temporizador_partida -= dt
        if estado.temporizador_partida <= 0:
            estado.temporizador_partida = 0
            estado.juego_terminado = True
            estado.ganador = estado.determinar_ganador()


def main():
    seleccionado = 0
    opciones = ["Modo Teclado", "Modo Camara", "Salir"]
    audio = GestorAudio()
    camara = GestorCamara()
    teclado = ModoTeclado(estado)
    modo_camara = ModoCamara(estado, camara)

    ejecutando = True
    en_menu = True
    usar_camara = False
    fps_juego = 0.0
    while ejecutando:
        dt = reloj.tick(FPS) / 1000
        inst = 1.0 / dt if dt > 0 else 0.0
        fps_juego = 0.9 * fps_juego + 0.1 * inst

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if en_menu and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    seleccionado = (seleccionado + 1) % len(opciones)
                if evento.key == pygame.K_UP:
                    seleccionado = (seleccionado - 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    if seleccionado == 0:
                        en_menu = False
                        usar_camara = False
                        estado.reiniciar()
                    elif seleccionado == 1:
                        en_menu = False
                        usar_camara = True
                        estado.reiniciar()
                        camara.iniciar()
                    elif seleccionado == 2:
                        ejecutando = False
            if not en_menu and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    try:
                        camara.detener()
                    except Exception:
                        pass
                    en_menu = True
                    estado.reiniciar()
                elif estado.juego_terminado and evento.key == pygame.K_RETURN:
                    estado.reiniciar()

        if en_menu:
            pantalla.fill(COLOR_FONDO)
            titulo = renderizador.fuente_grande.render("Pong Trucho", True, (255, 255, 255))
            pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 80))
            for i, opcion in enumerate(opciones):
                color = (255, 255, 255) if i == seleccionado else (150, 150, 150)
                txt = fuente.render(opcion, False, color)
                pantalla.blit(txt, (ANCHO // 2 - txt.get_width() // 2, 240 + i * 60))
            pygame.display.update()
            continue

        if usar_camara and camara.listo:
            superficie_camara, posiciones = camara.actualizar()
        else:
            superficie_camara, posiciones = None, []

        actualizar_juego(dt, usar_camara, modo_camara, teclado, posiciones, audio)

        renderizador.dibujar_fondo(superficie_camara if usar_camara else None)
        renderizador.dibujar_juego(estado)
        renderizador.dibujar_puntajes(estado)
        renderizador.dibujar_temporizador(estado.temporizador_partida)

        if estado.juego_terminado:
            nombre = {"jugador": "JUGADOR 2 Gana", "oponente": "JUGADOR 1 Gana",
                    "empate": "EMPATE"}.get(estado.ganador, "")
            renderizador.dibujar_ganador(f"{nombre}  {estado.puntaje_j} - {estado.puntaje_o}")
        elif estado.esperando_saque:
            renderizador.dibujar_mensaje_centro(str(max(1, math.ceil(estado.temporizador_saque))))

        if HUD_DEPURACION and usar_camara:
            y = 10
            if MOSTRAR_FPS:
                y = renderizador.dibujar_hud([
                    f"FPS juego: {fps_juego:4.1f}",
                    f"FPS camara: {camara.fps:4.1f}",
                ], y=y)
            if MOSTRAR_MANOS:
                y = renderizador.dibujar_manos(len(posiciones), y=y)
            if MOSTRAR_AYUDA_ESC:
                renderizador.dibujar_hud(["ESC: menu"], y=y)
        pygame.display.update()

    try:
        camara.detener()
    except Exception:
        pass
    try:
        audio.detener()
    except Exception:
        pass
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
