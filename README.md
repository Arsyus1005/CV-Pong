
# CV-PONG (CamPONG)

Copia del videojuego Pong hecho con Pygame, con dos modos de control: teclado o "cámara con seguimiento de manos" usando OpenCV y MediaPipe. En el modo cámara, cada jugador mueve su pala moviendo la mano frente a la webcam.

## Descripción

CamPong es una reinterpretación del clásico Pong. La pantalla se divide en dos mitades: la pala derecha pertenece al **jugador (O Jugador 2)** y la izquierda al **oponente (O Jugador 1)**. Además del control clásico por teclado, el juego puede usar la cámara para detectar manos y mapear su posición vertical a la posición de cada pala, de forma que cada jugador mueve su raqueta con la mano en el aire.

La captura y la inferencia de MediaPipe pueden ejecutarse en un hilo aparte para que el bucle de render no se bloquee.

## Requisitos

- Python 3.12 (probado en 3.12.6 y 3.14.5)
- Dependencias:
  - `pygame-ce`
  - `opencv-python`
  - `mediapipe`
  - `numpy`
- Cámara o webcam (solo para el modo cámara)

## Instalación

1. Clona el repositorio o descarga el código.
2. Crea y activa un entorno virtual (recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instala las dependencias:

```powershell
pip install pygame-ce opencv-python mediapipe numpy
```

4. Verifica que el modelo `assets/hand_landmarker.task` esté presente. Es necesario para el modo cámara.

## Cómo ejecutar

Desde la raíz del proyecto:

```powershell
python main.py
```

Al iniciar aparece un menú con tres opciones:

- **Modo Teclado**
- **Modo Cámara**
- **Salir**

Usa las flechas `Arriba` / `Abajo` para moverte por el menú y `Enter` para elegir.

## Controles

### Modo teclado

| Acción | Tecla |
| --- | --- |
| Raqueta del jugador (derecha) arriba | `Flecha arriba` |
| Raqueta del jugador (derecha) abajo | `Flecha abajo` |
| Raqueta del oponente (izquierda) arriba | `W` |
| Raqueta del oponente (izquierda) abajo | `S` |
| Volver al menú | `Esc` |
| Reiniciar al terminar la partida | `Enter` |

### Modo cámara

| Acción | Gesto |
| --- | --- |
| Raqueta del jugador (derecha) | Mano derecha |
| Raqueta del oponente (izquierda) | Mano izquierda |
| Volver al menú | `Esc` |
| Reiniciar al terminar la partida | `Enter` |

El movimiento vertical de la muñeca se mapea al alto de la pantalla. El rango útil de la cámara se ajusta con `CAMARA_Y_MIN` y `CAMARA_Y_MAX`.

## Reglas de la partida

- La pelota se sirve automáticamente tras un breve retardo (`RETARDO_SAQUE`, por defecto 3 s).
- Se anota cuando la pelota sale por completo de la pantalla por un lateral.
- La partida dura `TIEMPO_PARTIDA` segundos (por defecto 60). Al agotarse, gana quien tenga más puntos; si hay igualdad, es empate.
- La victoria anticipada por puntaje está activada (`PUNTOS_VICTORIA = 5`). Al alcanzar 5 puntos, la partida termina de inmediato.

## Estructura del proyecto

```
Pong_Pygame/
├── main.py                  # Punto de entrada, bucle principal y menú
├── configuracion.py         # Constantes y ajustes globales
├── core/
│   ├── audio.py             # Gestión de música y efectos de sonido
│   ├── estado.py            # Estado de la partida (puntajes, tiempos, raquetas)
│   └── fisica.py            # Movimiento de la pelota, rebotes y colisiones
├── modes/
│   ├── teclado.py           # Control mediante teclado
│   └── modo_camara.py       # Control mediante manos detectadas por la cámara
├── vision/
│   └── camara.py            # Captura de cámara y seguimiento de manos (MediaPipe)
├── ui/
│   ├── renderizador.py      # Dibujo de la escena, marcadores, HUD y mensajes
│   └── font/                # Tipografías (Rajdhani)
└── assets/
    ├── audio/               # Efectos y música (Ping, Pong, BG_song)
    └── hand_landmarker.task # Modelo de MediaPipe para las manos
```

## Configuración

Casi todos los ajustes están en `configuracion.py`:

- Tamaño de pantalla y FPS: `ANCHO`, `ALTO`, `FPS`.
- Dimensiones y velocidades: `ANCHO_PALA`, `ALTO_PALA`, `TAMANO_PELOTA`, `VELOCIDAD_PALA`, `VELOCIDAD_PELOTA_X`, `VELOCIDAD_PELOTA_Y`.
- Cámara: `CAMARA_ANCHO`, `CAMARA_ALTO`, `CAMARA_USAR_HILO`, `CAMARA_ESPEJO`, `CAMARA_Y_MIN`, `CAMARA_Y_MAX`.
- HUD: `HUD_DEPURACION`, `MOSTRAR_FPS`, `MOSTRAR_MANOS`, `MOSTRAR_AYUDA_ESC`.
- Reglas: `RETARDO_SAQUE`, `TIEMPO_PARTIDA`, `PUNTOS_VICTORIA`.
- Audio: rutas, volúmenes y conmutadores `MUSICA_ACTIVA` y `SONIDOS_ACTIVOS`.

## Tecnologías utilizadas

- Python 3.12
- Pygame (pygame-ce)
- OpenCV
- MediaPipe (Hand Landmarker)
- NumPy


## Créditos y atribuciones

### Música

- **"It's Watering Time"** por **Ategon**
  - Fuente: https://opengameart.org/content/its-watering-time
  - Licencia: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
  - Sin modificaciones.

### Efectos de sonido

- **Ping.wav** y **Pong.wav**
  - Fuente: freesound.org
  - Licencia: Creative Commons 0 (CC0) — dominio público.
  - Sin modificaciones.

### Fuente tipográfica

- **Rajdhani** (Medium y SemiBold)
  - Licencia: SIL Open Font License 1.1 (OFL-1.1)
  - https://scripts.sil.org/OFL

### Modelo de detección de manos

- **hand_landmarker.task**
  - Parte de MediaPipe (Google)
  - Licencia: Apache License 2.0
  - https://github.com/google-ai-edge/mediapipe

### Bibliotecas de terceros

- **Pygame-ce** — LGPL 2.1
- **OpenCV** — Apache 2.0
- **MediaPipe** — Apache 2.0
- **NumPy** — BSD 3-Clause


---

© 2026 Arsyus1005
