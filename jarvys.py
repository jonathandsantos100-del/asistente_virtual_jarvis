import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS
import io
import time

# Configuración del panel visual de Jarvis
st.set_page_config(page_title="Asistente Visual Jarvis", page_icon="🤖", layout="centered")

st.title("🤖 Asistente Visual Jarvis (Versión Web)")
st.write("Panel de control para supervisores del proyecto. El usuario ciego escuchará el audio automáticamente.")

# 1. Configurar cliente de Gemini
API_KEY = "AQ.Ab8RN6LZjLBrfyRT_0hBUjAmjQUJ4q9vTzRSxI89MeNu0ufB7g"
client = genai.Client(api_key=API_KEY)

# 2. Guardar el mapa en la memoria de la página
if 'mapa_bytes' not in st.session_state:
    st.session_state.mapa_bytes = None

def hablar_jarvis(texto):
    """Muestra el texto en pantalla y lo reproduce con voz elegante en el altavoz del celular"""
    st.info(f"🗣️ **Jarvis:** {texto}")
    texto_limpio = texto.replace("*", "")
    tts = gTTS(text=texto_limpio, lang='es', tld='com') # TLD .com le da un tono formal tipo Jarvis
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp, format="audio/mp3", autoplay=True)

# FASE 1: REGISTRO DEL MAPA
st.subheader("📁 Fase 1: Calibración del Plano")
archivo_mapa = st.file_uploader("Capture o suba una foto del mapa del lugar:", type=["jpg", "jpeg", "png"])

if archivo_mapa is not None:
    st.session_state.mapa_bytes = archivo_mapa.getvalue()
    st.success("✅ Plano escolar integrado con éxito en la memoria del asistente.")

# FASE 2, 3 Y 4: COORDENADAS Y CÁMARA
if st.session_state.mapa_bytes is not None:
    st.write("---")
    st.subheader("🗺️ Fase 2: Coordenadas de Ruta")
    
    # En el celular, el usuario puede presionar el ícono de micrófono de su teclado para dictar en estas casillas
    ubicacion_actual = st.text_input("¿En qué espacio te encuentras ahora? (Ej: Entrada, Canchas):", placeholder="Dicte o escriba aquí...")
    destino_final = st.text_input("¿A dónde quieres que te lleve? (Ej: Dirección, Baños):", placeholder="Dicte o escriba aquí...")
    
    if ubicacion_actual and destino_final:
        st.write("---")
        st.subheader("📸 Fase 3 y 4: Copiloto de Entorno en Tiempo Real")
        
        # Abre automáticamente la cámara frontal/trasera del celular o laptop
        foto_entorno = st.camera_input("Enfoque hacia el frente y avance a paso lento")
        
        if foto_entorno is not None:
            bytes_entorno = foto_entorno.getvalue()
            
            with st.spinner("🧠 Jarvis calculando ruta y analizando obstáculos en el mapa..."):
                try:
                    respuesta = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            types.Part.from_bytes(data=st.session_state.mapa_bytes, mime_type="image/jpeg"),
                            types.Part.from_bytes(data=bytes_entorno, mime_type="image/jpeg"),
                            f"Actúa como Jarvis, el asistente inteligente, analítico, formal y sofisticado de Tony Stark en Iron Man. "
                            f"El usuario es ciego, se encuentra en '{ubicacion_actual}' y su meta es ir a '{destino_final}'. "
                            f"La Imagen 1 es el mapa del lugar. La Imagen 2 es lo que ve su cámara enfrente. "
                            f"Responde en español. Recuérdale calmadamente que camine despacio. "
                            f"Dile puntualmente qué obstáculo tiene enfrente si ve alguno (botes de basura, personas, mochilas) y qué giro o paso dar según el plano. "
                            f"Sé muy directo, elegante y no uses más de dos oraciones."
                        ]
                    )
                    
                    instruccion = respuesta.text
                    hablar_jarvis(instruccion)
                    
                    # Espera 7 segundos para que el usuario avance y actualiza la cámara sola
                    time.sleep(7)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Fallo en los servidores de la IA: {e}")
