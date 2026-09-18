import streamlit as st
import asyncio
import edge_tts
import os
import time

# Configuración de la interfaz
st.set_page_config(page_title="Asistente Visual Jarvis", page_icon="🤖", layout="centered")

VOICE = "es-MX-JorgeNeural"  # La voz masculina neuronal ideal para Jarvis
AUDIO_FILE = "jarvis_voice.mp3"

def jarvis_habla_y_escribe(texto):
    """Genera la voz natural de Jarvis y muestra el texto para los supervisores."""
    # Mostrar texto en pantalla (Filtro anti-chismosos)
    st.info(f"🤖 **Jarvis:** {texto}")
    
    # Generar audio con la voz neuronal de Microsoft
    async def generate_audio():
        communicate = edge_tts.Communicate(texto, VOICE)
        await communicate.save(AUDIO_FILE)
        
    asyncio.run(generate_audio())
    
    # Reproducir audio automáticamente en el navegador/celular
    st.audio(AUDIO_FILE, format="audio/mp3", autoplay=True)
    
    # Tiempo de espera calculado según el texto para que Jarvis termine de hablar
    time.sleep(max(2.0, len(texto) * 0.07))

st.title("🤖 Asistente Visual Jarvis")
st.subheader("Sistema Automatizado de Navegación por Voz")

# Control de fases automático
if "fase" not in st.session_state:
    st.session_state.fase = "inicio"
    st.session_state.origen = ""
    st.session_state.destino = ""

# --- PANTALLA PRINCIPAL AUTOMATIZADA ---

if st.session_state.fase == "inicio":
    jarvis_habla_y_escribe("Iniciando sistemas. Hola, soy Jarvis. Por favor, introduce en qué espacio te encuentras ahora mismo.")
    
    origen = st.text_input("Ubicación actual:", placeholder="Ej: Pasillo principal")
    if origen:
        st.session_state.origen = origen
        st.session_state.fase = "preguntar_destino"
        st.rerun()

elif st.session_state.fase == "preguntar_destino":
    jarvis_habla_y_escribe(f"Ubicación registrada. Te encuentras en {st.session_state.origen}. ¿A qué lugar deseas dirigirte?")
    
    destino = st.text_input("Destino deseado:", placeholder="Ej: Laboratorio de cómputo")
    if destino:
        st.session_state.destino = destino
        st.session_state.fase = "analizar_mapa"
        st.rerun()

elif st.session_state.fase == "analizar_mapa":
    jarvis_habla_y_escribe(f"Analizando el mapa cargado. Trazando ruta óptima desde {st.session_state.origen} hacia {st.session_state.destino}.")
    
    # Cargar mapa si existe
    if os.path.exists("mapa_escuela.jpg"):
        st.image("mapa_escuela.jpg", caption="Mapa del entorno analizado", use_container_width=True)
    
    st.success(" RUTA TRAZADA CON ÉXITO")
    jarvis_habla_y_escribe("Ruta establecida. Por favor, camina despacio para poder analizar correctamente los obstáculos del entorno. Iniciando escaneo de cámara delantera.")
    
    # Botón disparador para otorgar permisos de cámara en el celular
    if st.button("Activar Escaneo en Tiempo Real"):
        st.session_state.fase = "camara_activa"
        st.rerun()

elif st.session_state.fase == "camara_activa":
    st.write("### 🎥 Escaneo Frontal Automatizado")
    
    # En celulares, esto abrirá la cámara frontal de manera nativa
    foto_entorno = st.camera_input("Captura automática de obstáculos")
    
    if foto_entorno is not None:
        # Simula el procesamiento instantáneo
        st.warning("⚠️ Obstáculo detectado a 2 metros. Mantén el paso lento.")
        jarvis_habla_y_escribe("Alerta. Detecto actividad al frente. Recuerda mantener un paso lento y constante para evitar accidentes.")
    else:
        # Recordatorio constante automático si no hay foto en el buffer
        jarvis_habla_y_escribe("Cámara activa. Por favor, captura el frente y avanza despacio.")
        
    if st.button("Terminar navegación"):
        st.session_state.fase = "inicio"
        jarvis_habla_y_escribe("Sistemas apagados. Navegación finalizada. Jarvis fuera.")
        st.rerun()
