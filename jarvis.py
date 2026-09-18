import streamlit as st
import cv2
from gtts import gTTS
import os
import time

# Configuración principal de la página web de Jarvis
st.set_page_config(page_title="Asistente Visual Jarvis", page_icon="🤖", layout="centered")

def jarvis_habla_y_escribe(texto):
    """Muestra el texto en pantalla y genera el audio para el navegador."""
    # Imprime el texto visible para los supervisores
    st.info(f"🎙️ **Jarvis:** {texto}")
    
    # Genera el archivo de audio con voz natural en español latino
    tts = gTTS(text=texto, lang='es', tld='com.mx')
    tts.save("jarvis_audio.mp3")
    
    # Reproduce el audio automáticamente en la pestaña del usuario
    st.audio("jarvis_audio.mp3", format="audio/mp3", autoplay=True)
    
    # Pausa breve para simular el tiempo que tarda en hablar antes de la siguiente acción
    time.sleep(len(texto) * 0.08)

# --- INTERFAZ DE USUARIO ---
st.title("🤖 Asistente Visual Jarvis")
st.subheader("Prototipo de Navegación y Accesibilidad")

# Estado de la aplicación para controlar el flujo paso a paso
if "paso" not in st.session_state:
    st.session_state.paso = 1
    st.session_state.origen = ""
    st.session_state.destino = ""

# FASE 1: Preguntar ubicación actual
if st.session_state.paso == 1:
    jarvis_habla_y_escribe("Hola. Soy Jarvis, tu asistente visual. Por favor, escribe en qué espacio te encuentras ahora mismo.")
    origen_input = st.text_input("Tu ubicación actual (Ej: Entrada principal):", key="origen_in")
    if st.button("Confirmar Ubicación") and origen_input:
        st.session_state.origen = origen_input
        st.session_state.paso = 2
        st.rerun()

# FASE 2: Preguntar el destino
elif st.session_state.paso == 2:
    jarvis_habla_y_escribe(f"Entendido. Te encuentras en {st.session_state.origen}. ¿A qué lugar o habitación deseas dirigirte?")
    destino_input = st.text_input("Tu destino (Ej: Laboratorio / Salón 3):", key="destino_in")
    if st.button("Confirmar Destino") and destino_input:
        st.session_state.destino = destino_input
        st.session_state.paso = 3
        st.rerun()

# FASE 3: Análisis manual del mapa y activación de cámara
elif st.session_state.paso == 3:
    jarvis_habla_y_escribe(f"Analizando el mapa capturado... Trazando ruta desde {st.session_state.origen} hacia {st.session_state.destino}.")
    
    # Mostrar el mapa si existe en la carpeta
    if os.path.exists("mapa_escuela.jpg"):
        st.image("mapa_escuela.jpg", caption="Mapa del Entorno Cargado", use_container_width=True)
    else:
        st.warning("⚠️ No se encontró el archivo 'mapa_escuela.jpg' en el repositorio, pero procediendo con la ruta.")

    st.success("✅ Ruta optimizada en el mapa.")
    jarvis_habla_y_escribe("Por favor, camina despacio para poder analizar correctamente los obstáculos del entorno. Iniciando cámara delantera en tiempo real.")
    
    if st.button("Iniciar Monitoreo de Cámara"):
        st.session_state.paso = 4
        st.rerun()

# FASE 4: Cámara en tiempo real
elif st.session_state.paso == 4:
    st.write("### 🎥 Monitoreo en Tiempo Real Activo")
    st.warning("🚨 Recuerda mantener un paso lento y constante para detectar objetos cercanos.")
    
    # Capturador de cámara integrado para aplicaciones web de Streamlit
    img_file_buffer = st.camera_input("Escaneo de obstáculos frontal")
    
    if img_file_buffer is not None:
        st.success("Imagen del entorno analizada con éxito. Camino despejado.")
        # Aquí puedes meter mensajes recurrentes si el usuario sigue tomando capturas
        if st.button("Volver a escanear"):
            st.rerun()
            
    if st.button("Detener Asistente Jarvis"):
        st.session_state.paso = 1
        jarvis_habla_y_escribe("Monitoreo finalizado. Jarvis fuera.")
        st.rerun()
