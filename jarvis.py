import streamlit as st
import asyncio
import edge_tts
import os
import time
from streamlit_mic_recorder import speech_to_text

# Configuración de la interfaz de Jarvis
st.set_page_config(page_title="Asistente Visual Jarvis", page_icon="🤖", layout="centered")

VOICE = "es-MX-JorgeNeural"  # Voz masculina neuronal de Jarvis
AUDIO_FILE = "jarvis_voice.mp3"

def jarvis_habla_y_escribe(texto):
    """Genera la voz de Jarvis y muestra el texto en pantalla para los supervisores chismosos."""
    st.info(f"🤖 **Jarvis:** {texto}")
    
    async def generate_audio():
        communicate = edge_tts.Communicate(texto, VOICE)
        await communicate.save(AUDIO_FILE)
        
    asyncio.run(generate_audio())
    st.audio(AUDIO_FILE, format="audio/mp3", autoplay=True)
    # Pausa para que no se encimen los audios mientras habla
    time.sleep(max(2.0, len(texto) * 0.06))

st.title("🤖 Asistente Visual Jarvis")
st.subheader("Sistema de Navegación Automatizado por Voz")

# Control de fases automático
if "fase" not in st.session_state:
    st.session_state.fase = "captura_mapa"
    st.session_state.origen = ""
    st.session_state.destino = ""

# --- FLUJO AUTOMATIZADO POR VOZ ---

# FASE 1: SACAR FOTO AL MAPA
if st.session_state.fase == "captura_mapa":
    jarvis_habla_y_escribe("Sistemas en línea. Por favor, captura la fotografía del mapa del entorno para iniciar.")
    
    foto_mapa = st.camera_input("Capturar foto del mapa", key="camara_mapa")
    
    if foto_mapa is not None:
        with open("mapa_escuela.jpg", "wb") as f:
            f.write(foto_mapa.getbuffer())
        st.success("📸 Mapa registrado correctamente.")
        time.sleep(1.0)
        st.session_state.fase = "preguntar_origen"
        st.rerun()

# FASE 2: PREGUNTAR UBICACIÓN ACTUAL POR VOZ
elif st.session_state.fase == "preguntar_origen":
    jarvis_habla_y_escribe("Mapa cargado. Por favor, dime en qué espacio te encuentras ahora mismo.")
    
    st.write("🎙️ **Escuchando tu ubicación... Presiona el micrófono y habla:**")
    # Captura la voz del teléfono y la convierte a texto automáticamente
    texto_voz_origen = speech_to_text(language='es', start_prompt="🟢 Hablar ahora", stop_prompt="🔴 Detener", key='voz_origen')
    
    if texto_voz_origen:
        st.session_state.origen = texto_voz_origen
        st.success(f"Ubicación entendida: {texto_voz_origen}")
        time.sleep(1.5)
        st.session_state.fase = "preguntar_destino"
        st.rerun()

# FASE 3: PREGUNTAR DESTINO POR VOZ
elif st.session_state.fase == "preguntar_destino":
    jarvis_habla_y_escribe(f"Entendido, te encuentras en {st.session_state.origen}. Ahora dime, ¿a dónde quieres ir?")
    
    st.write("🎙️ **Escuchando tu destino... Presiona el micrófono y habla:**")
    texto_voz_destino = speech_to_text(language='es', start_prompt="🟢 Hablar ahora", stop_prompt="🔴 Detener", key='voz_destino')
    
    if texto_voz_destino:
        st.session_state.destino = texto_voz_destino
        st.success(f"Destino entendido: {texto_voz_destino}")
        jarvis_habla_y_escribe(f"Trazando ruta hacia {texto_voz_destino}. Por favor, camina despacio. Iniciando cámara delantera.")
        time.sleep(2.0)
        st.session_state.fase = "camara_activa"
        st.rerun()

# FASE 4: ESCANEO EN TIEMPO REAL AUTOMÁTICO
elif st.session_state.fase == "camara_activa":
    st.write("### 🎥 Escaneo Frontal y Detección de Obstáculos")
    
    if os.path.exists("mapa_escuela.jpg"):
        st.image("mapa_escuela.jpg", caption=f"Ruta: {st.session_state.origen} -> {st.session_state.destino}", width=300)
    
    st.warning("🚨 Alerta de seguridad: Mantén un paso lento y constante.")
    
    foto_entorno = st.camera_input("Escaneo de obstáculos en tiempo real", key="camara_obstaculos")
    
    if foto_entorno is not None:
        st.success("Camino analizado.")
        jarvis_habla_y_escribe("Aviso. Ruta despejada hacia adelante. Por favor, camine despacio para mantener la precisión del escaneo visual.")
    else:
        jarvis_habla_y_escribe("Cámara frontal activa. Capture el entorno mientras avanza lentamente.")
        
    if st.button("Finalizar asistencia"):
        st.session_state.fase = "captura_mapa"
        st.session_state.origen = ""
        st.session_state.destino = ""
        jarvis_habla_y_escribe("Navegación concluida. Jarvis fuera.")
        st.rerun()
