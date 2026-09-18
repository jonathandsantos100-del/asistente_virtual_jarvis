import cv2
import pyttsx3
from google import genai
from google.genai import types
import os
import time

# 1. Configurar el cliente de Gemini
client = genai.Client(api_key="AQ.Ab8RN6LZjLBrfyRT_0hBUjAmjQUJ4q9vTzRSxI89MeNu0ufB7g")

# 2. Configurar la voz de Jarvis en español
engine = pyttsx3.init()
engine.setProperty('rate', 170) # Velocidad elegante, estilo Jarvis
voces = engine.getProperty('voices')
for voz in voces:
    if "spanish" in voz.name.lower() or "sabina" in voz.name.lower() or "helena" in voz.name.lower():
        engine.setProperty('voice', voz.id)
        break

def jarvis_hablar(texto):
    """Hace que Jarvis muestre el texto en pantalla y lo hable con voz elegante"""
    print(f"\n🤖 JARVIS: {texto}")
    texto_limpio = texto.replace("*", "")
    engine.say(texto_limpio)
    engine.runAndWait()

# ==========================================
# FASE 1: CAPTURA O REGISTRO DEL MAPA
# ==========================================
ruta_mapa = "mapa_escuela.jpg"

if not os.path.exists(ruta_mapa):
    jarvis_hablar("Señor, no detecto un mapa del lugar en el sistema. Iniciando cámara. Por favor, coloque el mapa frente al lente.")
    camara = cv2.VideoCapture(0)
    time.sleep(2) # Dar tiempo a que la cámara calibre la luz
    exito, fotograma_mapa = camara.read()
    camara.release()
    
    if exito:
        cv2.imwrite(ruta_mapa, fotograma_mapa)
        jarvis_hablar("Fotografía del mapa registrada con éxito en la base de datos.")
    else:
        jarvis_hablar("Error crítico: No se pudo acceder a la cámara para registrar el mapa.")
        exit()
else:
    jarvis_hablar("Mapa del establecimiento localizado en el almacenamiento local.")

# ==========================================
# FASE 2: INTERROGATORIO SEGURO POR TECLADO
# ==========================================
jarvis_hablar("Por favor, digite en el teclado su ubicación actual y presione Enter.")
ubicacion_actual = input("📍 Escribe dónde estás ahora (Ej: Entrada, Salon 1): ")

jarvis_hablar(f"Entendido, procesando {ubicacion_actual}. Ahora indique su destino final, señor.")
destino_final = input("🏁 Escribe a dónde quieres ir (Ej: Direccion, Baños): ")

jarvis_hablar(f"Coordenadas fijadas. Trazando ruta desde {ubicacion_actual} hasta {destino_final}. Iniciando asistencia visual continua.")

# Leer los bytes del mapa que guardamos
with open(ruta_mapa, "rb") as archivo_mapa:
    bytes_mapa = archivo_mapa.read()

# ==========================================
# FASE 3 Y 4: GUÍA Y ANÁLISIS EN TIEMPO REAL
# ==========================================
ruta_entorno = "foto_entorno.jpg"
jarvis_hablar("Sistema de reconocimiento de entorno en línea. Por favor, avance a paso lento para permitirme procesar los obstáculos.")

try:
    while True:
        print("\n📸 Tomando captura del frente...")
        camara = cv2.VideoCapture(0)
        exito, fotograma_entorno = camara.read()
        camara.release()
        
        if not exito:
            print("❌ Error temporal al leer la cámara del entorno.")
            time.sleep(3)
            continue
            
        cv2.imwrite(ruta_entorno, fotograma_entorno)
        
        with open(ruta_entorno, "rb") as archivo_entorno:
            bytes_entorno = archivo_entorno.read()
            
        # Jarvis analiza simultáneamente el mapa base y la foto del pasillo actual
        respuesta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=bytes_mapa, mime_type="image/jpeg"),
                types.Part.from_bytes(data=bytes_entorno, mime_type="image/jpeg"),
                f"Actúa como Jarvis, el asistente inteligente, analítico, formal y sofisticado de Tony Stark en Iron Man. "
                f"El usuario es ciego, se encuentra actualmente en '{ubicacion_actual}' y su meta es llegar a '{destino_final}'. "
                f"Imagen 1 es el mapa de la escuela. Imagen 2 es lo que su cámara ve al frente justo ahora en el pasillo. "
                f"Responde obligatoriamente en español. Recuérdale calmadamente que camine despacio si es necesario. "
                f"Dile puntualmente qué obstáculo tiene enfrente si es que hay alguno, y qué giro o paso dar según el plano de la escuela para no perderse. "
                f"Sé muy directo, elegante y no uses más de dos oraciones."
            ]
        )
        
        instruccion_jarvis = respuesta.text
        jarvis_hablar(instruccion_jarvis)
        
        # Espera 6 segundos para que el usuario camine un poco antes de analizar la siguiente foto
        print("⏳ Esperando actualización de posición...")
        time.sleep(6)

except KeyboardInterrupt:
    jarvis_hablar("Asistencia finalizada. Que tenga un excelente día, señor.")
