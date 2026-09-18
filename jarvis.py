import streamlit as st
import asyncio
import edge_tts
import os
import time
from streamlit_mic_recorder import speech_to_text
from google import genai
from PIL import Image

# Configuración de la interfaz de Jarvis
st.set_page_config(page_title="Asistente Visual Jarvis", page_icon="🤖", layout="centered")

VOICE = "es-MX-JorgeNeural"  # Voz neuronal masculina de Jarvis
AUDIO_FILE = "jarvis_voice.mp3"

# Inicializar tu clave de Gemini de forma segura
if "GEMINI_API_KEY" not in st.session_state:
    st.session_state.GEMINI_API_KEY = "AQ" # Vinculado automáticamente con tu clave

def jarvis_habla_y_escribe(texto):
    """Genera la voz de Jarvis y muestra el texto en pantalla."""
    st.info(f"🤖 **Jarvis:** {texto}")
    
    async def generate_audio():
        communicate = edge_tts.Communicate(texto, VOICE)
        await communicate.save(AUDIO_FILE)
        
    asyncio.run(generate_audio())
    st.audio(AUDIO_FILE, format="audio/mp3", autoplay=True)
    time.sleep(max(2.0, len(texto) * 0.06))

st.title("🤖 Asistente Visual Jarvis")
st.subheader("Sistema Inteligente de Navegación por Voz e IA")

# Control de fases y memoria de ruta
if "fase" not in st.session_state:
    st.session_state.fase = "bienvenida"
    st.session_state.origen = ""
    st.session_state.destino = ""
    st.session_state.intentos_camara = 0  # Historial de pasos

# --- FLUJO 100% INTEGRADO Y AUTOMATIZADO ---

# FASE 0: ADVERTENCIA DE AUDÍFONOS
if st.session_state.fase == "bienvenida":
    jarvis_habla_y_escribe("Sistemas iniciando. Se recomienda utilizar audífonos para una mejor experiencia y escuchar las alertas con claridad ante el ruido del entorno.")
    
    if st.button("Iniciar Asistente Jarvis"):
        st.session_state.fase = "captura_mapa"
        st.rerun()

# FASE 1: SACAR FOTO AL MAPA
elif st.session_state.fase == "captura_mapa":
    jarvis_habla_y_escribe("Por favor, captura la fotografía del mapa del entorno para iniciar la navegación guiada.")
    
    foto_mapa = st.camera_input("Capturar foto del mapa", key="camara_mapa")
    
    if foto_mapa is not None:
        with open("mapa_escuela.jpg", "wb") as f:
            f.write(foto_mapa.getbuffer())
        st.success("📸 Mapa guardado con éxito en memoria.")
        time.sleep(1.0)
        st.session_state.fase = "preguntar_origen"
        st.rerun()

# FASE 2: PREGUNTAR UBICACIÓN ACTUAL POR VOZ (Micrófono Automático)
elif st.session_state.fase == "preguntar_origen":
    jarvis_habla_y_escribe("Mapa cargado. Por favor, dime en qué espacio te encuentras ahora mismo.")
    
    st.write("🎙️ **Jarvis te está escuchando... Habla ahora:**")
    texto_voz_origen = speech_to_text(language='es', start_prompt="🟢 Escuchando ubicación...", stop_prompt="🔴 Procesando", just_once=False, key='voz_origen')
    
    if texto_voz_origen:
        st.session_state.origen = texto_voz_origen
        st.success(f"Ubicación entendida: {texto_voz_origen}")
        time.sleep(1.0)
        st.session_state.fase = "preguntar_destino"
        st.rerun()

# FASE 3: PREGUNTAR DESTINO POR VOZ (Micrófono Automático)
elif st.session_state.fase == "preguntar_destino":
    jarvis_habla_y_escribe(f"Entendido. Ahora dime, ¿a dónde quieres ir?")
    
    st.write("🎙️ **Jarvis te está escuchando... Habla ahora:**")
    texto_voz_destino = speech_to_text(language='es', start_prompt="🟢 Escuchando destino...", stop_prompt="🔴 Procesando", just_once=False, key='voz_destino')
    
    if texto_voz_destino:
        st.session_state.destino = texto_voz_destino
        st.success(f"Destino entendido: {texto_voz_destino}")
        jarvis_habla_y_escribe(f"Trazando ruta de {st.session_state.origen} hacia {texto_voz_destino}. Activando escaneo ocular doble: guía GPS y alerta de obstáculos.")
        time.sleep(1.5)
        st.session_state.fase = "camara_activa"
        st.rerun()

# FASE 4: CÁMARA CON DOBLE FUNCIÓN (GPS + OBSTÁCULOS) Y MODO HUMORÍSTICO
elif st.session_state.fase == "camara_activa":
    st.write("### 🎥 Escaneo Inteligente Activo")
    st.warning("🚨 Camine despacio. Analizando ruta y terreno en tiempo real.")
    
    mapa_existe = os.path.exists("mapa_escuela.jpg")
    if mapa_existe:
        st.image("mapa_escuela.jpg", caption=f"Mapa: {st.session_state.origen} -> {st.session_state.destino}", width=200)
    
    # Captura la imagen del entorno real del teléfono
    foto_entorno = st.camera_input("Enfoque frontal del camino", key="camara_obstaculos")
    
    if foto_entorno is not None:
        imagen_camara = Image.open(foto_entorno)
        st.info("🧠 Jarvis procesando datos de navegación...")
        st.session_state.intentos_camara += 1  # Contador de pasos para el desvío
        
        try:
            client = genai.Client(api_key=st.session_state.GEMINI_API_KEY)
            lista_archivos = [imagen_camara]
            
            # Simulamos si el usuario ya tomó muchas fotos seguidas (se desvió o se pasó)
            se_paso_de_ruta = st.session_state.intentos_camara >= 4
            
            instrucciones_ia = (
                f"Actúa como el asistente visual Jarvis. El usuario va desde '{st.session_state.origen}' hacia '{st.session_state.destino}'. "
                f"Mira la foto actual del suelo. Debes responder en una sola frase corta de menos de 15 palabras.\n"
            )
            
            if se_paso_de_ruta:
                # Regaño humorístico mexicano
                instrucciones_ia += (
                    "¡ATENCIÓN! El usuario se ha desviado por completo de la ruta. "
                    "Empieza tu respuesta diciendo obligatoriamente con tono divertido y mexicano: 'No seas wey, regrésate, te pasaste de la ruta.' "
                    "E indica brevemente que vas a recalcular el camino."
                )
            else:
                # La Doble Función solicitada
                instrucciones_ia += (
                    "Debes hacer una doble función combinada:\n"
                    "1. FUNCIÓN GPS: Indica cuántos pasos dar y hacia dónde girar basándote en la ruta (Ej: 'Avanza 4 pasos y gira a la derecha').\n"
                    "2. FUNCIÓN OBSTÁCULOS: Si en la foto del suelo ves algún peligro (como una escoba, mochila, silla, cable o persona) "
                    "añade una orden física inmediata al final (Ej: '¡Cuidado, escoba en el suelo, da un paso a la izquierda!' o '¡Agáchate, objeto alto!').\n"
                    "Si el camino está limpio, solo da la instrucción del GPS."
                )
            
            if mapa_existe:
                imagen_mapa = Image.open("mapa_escuela.jpg")
                lista_archivos.append(imagen_mapa)
                instrucciones_ia += " Utiliza la imagen del mapa escolar adjunto para guiar con lógica el camino del GPS."

            respuesta_ia = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=lista_archivos + [instrucciones_ia]
            )
            
            # Jarvis habla con la respuesta combinada de la IA
            jarvis_habla_y_escribe(respuesta_ia.text)
            
            # Limpiar el contador si ya se le avisó que se pasó
            if se_paso_de_ruta:
                st.session_state.intentos_camara = 0
            
        except Exception as e:
            st.error("Error en el módulo analítico de Jarvis.")
            jarvis_habla_y_escribe("Aviso. Dificultad para conectar con el satélite de análisis. Mantenga la precaución.")
            
        if st.button("Siguiente paso / Volver a escanear"):
            st.rerun()
            
    if st.button("Finalizar asistencia"):
        st.session_state.fase = "bienvenida"
        st.session_state.origen = ""
        st.session_state.destino = ""
        st.session_state.intentos_camara = 0
        jarvis_habla_y_escribe("Sistemas en modo de espera. Navegación concluida. Jarvis fuera.")
        st.rerun()
