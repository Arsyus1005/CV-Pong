import os
import pygame

ANCHO, ALTO = 1280, 720
FPS = 60
ANCHO_PALA = 10
ALTO_PALA = 140
TAMANO_PELOTA = 30
VELOCIDAD_PALA = 7
VELOCIDAD_PELOTA_X = 7
VELOCIDAD_PELOTA_Y = 7
OPACIDAD_CAMARA = 55
COLOR_LINEA_MEDIA = (200, 200, 200)
COLOR_RELLENO = (255, 255, 255)
COLOR_FONDO = pygame.Color("grey12")
DIR_FUENTES = os.path.join(os.path.dirname(__file__), "ui", "font")
FUENTE_REGULAR = os.path.join(DIR_FUENTES, "Rajdhani-Medium.ttf")
FUENTE_NEGRITA = os.path.join(DIR_FUENTES, "Rajdhani-SemiBold.ttf")
TAMANO_FUENTE = 34
TAMANO_FUENTE_GRANDE = 72
SUAVIZADO = 0.35

# Rango vertical camara
CAMARA_Y_MIN = 0.15
CAMARA_Y_MAX = 0.85

# Rendimiento de cámara
CAMARA_ANCHO = 640       # resolución de captura
CAMARA_ALTO = 480
CAMARA_USAR_HILO = True  # captura+inferencia en hilo aparte
CAMARA_ESPEJO = True

HUD_DEPURACION = True    
MOSTRAR_FPS = False     
MOSTRAR_MANOS = True     
MOSTRAR_AYUDA_ESC = False  
TAMANO_FUENTE_MANOS = 20  
ALFA_MANOS = 120   

# Reglas de partida
RETARDO_SAQUE = 3.0      
TIEMPO_PARTIDA = 60.0
# puntos para ganar, con 0 se desactiva y queda solo con el tiempo
PUNTOS_VICTORIA = 5 

# Audio
DIR_AUDIO = os.path.join(os.path.dirname(__file__), "assets", "audio")
SONIDO_PARED = os.path.join(DIR_AUDIO, "Ping.wav")   # rebote en paredes
SONIDO_RAQUETA = os.path.join(DIR_AUDIO, "Pong.wav")  # rebote en raqueta
MUSICA_FONDO = os.path.join(DIR_AUDIO, "BG_song.wav")  # musica de fondo
VOLUMEN_MUSICA = 0.12    
VOLUMEN_PARED = 0.45
VOLUMEN_RAQUETA = 0.55
MUSICA_ACTIVA = True
SONIDOS_ACTIVOS = True
