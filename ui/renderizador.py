import pygame
from configuracion import (
    COLOR_FONDO, COLOR_RELLENO, COLOR_LINEA_MEDIA, OPACIDAD_CAMARA, ANCHO, ALTO,
    FUENTE_NEGRITA, FUENTE_REGULAR, TAMANO_FUENTE_GRANDE, TAMANO_FUENTE_MANOS, ALFA_MANOS,
)


class Renderizador:
    def __init__(self, pantalla, fuente):
        self.pantalla = pantalla
        self.fuente = fuente
        self.fuente_grande = pygame.font.Font(FUENTE_NEGRITA, TAMANO_FUENTE_GRANDE)
        self.fuente_manos = pygame.font.Font(FUENTE_REGULAR, TAMANO_FUENTE_MANOS)
        self.atenuador = pygame.Surface((ANCHO, ALTO))
        self.atenuador.set_alpha(120)
        self.atenuador.fill((0, 0, 0))

    def dibujar_fondo(self, superficie_camara=None):
        self.pantalla.fill(COLOR_FONDO)
        if superficie_camara is not None:
            superficie_camara.set_alpha(OPACIDAD_CAMARA)
            self.pantalla.blit(superficie_camara, (0, 0))
            self.pantalla.blit(self.atenuador, (0, 0))

    def dibujar_juego(self, estado):
        pygame.draw.rect(self.pantalla, COLOR_RELLENO, estado.jugador)
        pygame.draw.rect(self.pantalla, COLOR_RELLENO, estado.oponente)
        pygame.draw.ellipse(self.pantalla, COLOR_RELLENO, estado.pelota)
        pygame.draw.aaline(self.pantalla, COLOR_LINEA_MEDIA, (ANCHO // 2, 0), (ANCHO // 2, ALTO))

    def dibujar_puntajes(self, estado):
        t_j = self.fuente.render(f"{estado.puntaje_j}", False, COLOR_RELLENO)
        t_o = self.fuente.render(f"{estado.puntaje_o}", False, COLOR_RELLENO)
        self.pantalla.blit(t_j, (ANCHO // 2 + 20, 10))
        self.pantalla.blit(t_o, (ANCHO // 2 - 50, 10))

    def dibujar_temporizador(self, segundos):
        mins = int(segundos) // 60
        segs = int(segundos) % 60
        txt = self.fuente.render(f"{mins:02d}:{segs:02d}", True, (255, 220, 120))
        rect = txt.get_rect(center=(ANCHO // 2, ALTO - 40))
        self.pantalla.blit(txt, rect)

    def dibujar_mensaje_centro(self, texto, color=COLOR_RELLENO, fuente=None):
        f = fuente or self.fuente_grande
        txt = f.render(texto, True, color)
        rect = txt.get_rect(center=(ANCHO // 2, ALTO // 2 - 60))
        self.pantalla.blit(txt, rect)

    def dibujar_ganador(self, texto):
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(170)
        overlay.fill((0, 0, 0))
        self.pantalla.blit(overlay, (0, 0))
        txt = self.fuente_grande.render(texto, True, (255, 255, 255))
        rect = txt.get_rect(center=(ANCHO // 2, ALTO // 2 - 40))
        self.pantalla.blit(txt, rect)
        sub = self.fuente.render("ENTER: reiniciar   |   ESC: menu", True, (200, 200, 200))
        self.pantalla.blit(sub, (ANCHO // 2 - sub.get_width() // 2, ALTO // 2 + 50))

    def dibujar_hud(self, filas, fuente=None, color=(0, 255, 0), alfa=255, y=10):
        f = fuente or self.fuente
        for fila in filas:
            txt = f.render(fila, True, color)
            if alfa < 255:
                txt.set_alpha(alfa)
            self.pantalla.blit(txt, (10, y))
            y += f.get_height() + 2
        return y

    def dibujar_manos(self, cantidad, y=10):
        txt = self.fuente_manos.render(f"Manos: {cantidad}", True, (0, 255, 0))
        txt.set_alpha(ALFA_MANOS)
        self.pantalla.blit(txt, (10, y))
        return y + self.fuente_manos.get_height() + 2
