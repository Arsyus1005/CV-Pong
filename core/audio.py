import os
import pygame
from configuracion import (
    SONIDO_PARED, SONIDO_RAQUETA, MUSICA_FONDO,
    VOLUMEN_PARED, VOLUMEN_RAQUETA, VOLUMEN_MUSICA,
    MUSICA_ACTIVA, SONIDOS_ACTIVOS,
)


class GestorAudio:
    def __init__(self):
        self.disponible = False
        self.sonido_pared = None
        self.sonido_raqueta = None
        self.volumen_musica = VOLUMEN_MUSICA
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
            self.sonido_pared = self._cargar(SONIDO_PARED, VOLUMEN_PARED)
            self.sonido_raqueta = self._cargar(SONIDO_RAQUETA, VOLUMEN_RAQUETA)
            self.disponible = True
            if MUSICA_ACTIVA:
                self._iniciar_musica()
        except Exception as e:
            print("Audio no disponible:", e)
            self.disponible = False

    def _cargar(self, ruta, volumen):
        if not os.path.exists(ruta):
            return None
        snd = pygame.mixer.Sound(ruta)
        snd.set_volume(volumen)
        return snd

    def _iniciar_musica(self):
        if not os.path.exists(MUSICA_FONDO):
            return
        try:
            pygame.mixer.music.load(MUSICA_FONDO)
            pygame.mixer.music.set_volume(self.volumen_musica)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("No se pudo reproducir la musica we", e)

    def sonar_pared(self):
        if SONIDOS_ACTIVOS and self.sonido_pared is not None:
            self.sonido_pared.play()

    def sonar_raqueta(self):
        if SONIDOS_ACTIVOS and self.sonido_raqueta is not None:
            self.sonido_raqueta.play()

    def detener(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
