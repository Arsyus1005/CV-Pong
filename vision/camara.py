import cv2
import numpy as np
import os
import time
import threading
import pygame
from configuracion import ANCHO, ALTO, CAMARA_ANCHO, CAMARA_ALTO, CAMARA_USAR_HILO, CAMARA_ESPEJO

try:
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.vision.core import image as modulo_imagen
except Exception:
    python = None
    vision = None
    modulo_imagen = None


class GestorCamara:
    def __init__(self):
        self.cap = None
        self.detector = None
        self.listo = False
        self.cuadro = None
        self.superficie = None
        self.posiciones = []
        self.conexiones = None
        self.fps = 0.0
        self._candado = threading.Lock()
        self._hilo = None
        self._detener = threading.Event()
        try:
            self.conexiones = vision.HandLandmarksConnections.HAND_CONNECTIONS
        except Exception:
            self.conexiones = None

    def iniciar(self):
        if python is None or vision is None or modulo_imagen is None:
            self.listo = False
            return False
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.listo = False
            return False
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMARA_ANCHO)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMARA_ALTO)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        ruta_modelo = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "hand_landmarker.task")
        if not os.path.exists(ruta_modelo):
            ruta_modelo = os.path.join(os.getcwd(), "assets", "hand_landmarker.task")
        opciones_base = python.BaseOptions(model_asset_path=ruta_modelo)
        opciones = vision.HandLandmarkerOptions(
            base_options=opciones_base,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.4,
            min_tracking_confidence=0.4,
            running_mode=vision.RunningMode.VIDEO,
        )
        try:
            self.detector = vision.HandLandmarker.create_from_options(opciones)
        except Exception as e:
            print("Error al iniciar la cámara:", e)
            if self.cap:
                self.cap.release()
            self.cap = None
            self.listo = False
            return False
        self.listo = True
        if CAMARA_USAR_HILO:
            self._detener.clear()
            self._hilo = threading.Thread(target=self._bucle, daemon=True)
            self._hilo.start()
        return True

    def detener(self):
        self._detener.set()
        if self._hilo is not None:
            self._hilo.join(timeout=2.0)
            self._hilo = None
        if self.cap is not None:
            self.cap.release()
        self.cap = None
        if self.detector is not None:
            try:
                self.detector.close()
            except Exception:
                pass
        self.detector = None
        self.listo = False

    def _dibujar_mano(self, cuadro, puntos_mano, w, h):
        puntos = [(int(lm.x * w), int(lm.y * h)) for lm in puntos_mano]
        if self.conexiones:
            for conexion in self.conexiones:
                inicio = conexion.start
                fin = conexion.end
                if inicio < len(puntos) and fin < len(puntos):
                    cv2.line(cuadro, puntos[inicio], puntos[fin], (0, 180, 255), 1, cv2.LINE_AA)
        for p in puntos:
            cv2.circle(cuadro, p, 3, (0, 255, 0), -1, cv2.LINE_AA)

    def _procesar(self):
        ok, cuadro = self.cap.read()
        if not ok:
            return
        if CAMARA_ESPEJO:
            cuadro = cv2.flip(cuadro, 1)
        h, w, _ = cuadro.shape
        cuadro_rgb = cv2.cvtColor(cuadro, cv2.COLOR_BGR2RGB)
        imagen_mp = modulo_imagen.Image(image_format=modulo_imagen.ImageFormat.SRGB, data=cuadro_rgb)
        marca_tiempo_ms = int(time.time() * 1000)
        try:
            resultado = self.detector.detect_for_video(imagen_mp, marca_tiempo_ms)
        except Exception:
            try:
                resultado = self.detector.detect(imagen_mp)
            except Exception:
                return
        posiciones = []
        anotado = cuadro  # ya está en BGR
        if resultado.hand_landmarks:
            for indice, puntos_mano in enumerate(resultado.hand_landmarks):
                if puntos_mano:
                    muneca = puntos_mano[0]
                    posiciones.append({
                        "indice": indice,
                        "xn": float(muneca.x),
                        "yn": float(muneca.y),
                        "puntos": puntos_mano,
                    })
                    self._dibujar_mano(anotado, puntos_mano, w, h)
        anotado = cv2.resize(anotado, (ANCHO, ALTO), interpolation=cv2.INTER_LINEAR)
        superficie = pygame.image.frombuffer(anotado.tobytes(), anotado.shape[1::-1], "BGR").copy()
        with self._candado:
            self.superficie = superficie
            self.posiciones = posiciones

    def _bucle(self):
        while not self._detener.is_set():
            t0 = time.time()
            try:
                self._procesar()
            except Exception:
                pass
            dt = time.time() - t0
            if dt > 0:
                self.fps = 0.9 * self.fps + 0.1 * (1.0 / dt)

    def actualizar(self):
        if not self.listo:
            return None, []
        if CAMARA_USAR_HILO:
            with self._candado:
                return self.superficie, list(self.posiciones)
        self._procesar()
        with self._candado:
            return self.superficie, list(self.posiciones)
