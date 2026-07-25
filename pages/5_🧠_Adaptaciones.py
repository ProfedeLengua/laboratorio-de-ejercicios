import streamlit as st
from google import genai
import os
import base64

st.title("Generador de Adaptaciones y DÚA")
st.subheader("Atención a la Diversidad e Inclusión Educativa")
st.caption("Adaptación inmediata de materiales mediante subida de archivos PDF")

# Clave de la API segura
CLAVE_API = st.secrets["gemini_key"]

# Función para transformar el PDF del Decreto de la carpeta contexto
def preparar_pdf_ley(nombre_archivo):
    ruta_completa = os.path.join("contexto", nombre_archivo)
    if os.path.exists(ruta_completa):
        with open(ruta_completa, "rb") as f:
            d = base64.b64encode(f.read()).decode("utf-8")
            return genai.types.Part.from_bytes(data=base64.b64decode(d), mime_type="application/pdf")
    return None

with st.form("formulario_inclusion_pdf"):
    st.markdown("### 🎛️ Parámetros de Inclusión")
    
    curso = st.selectbox(
        "Selecciona el Curso de ESO:",
        ["1º de ESO", "2º de ESO", "3º de ESO", "4º de ESO"]
    )
    
    necesidad = st.selectbox(
        "Selecciona la Necesidad Específica de Apoyo (NEAE):",
        [
            "Dislexia / Dificultades de comprensión lectora",
            "TDAH / Necesidad de estructuración visual y pausas",
            "Incorporación tardía / Desfase lingüístico (Español L2)",
            "Altas Capacidades / Necesidad de profundización y retos",
            "Discapacidad auditiva o visual ligera (Adecuación de formatos)"
        ]
    )
    
    # EL NUEVO BOTÓN MÁGICO: Lector de archivos PDF subidos por el profesor
    archivo_subido = st.file_uploader(
        "Sube aquí el PDF del examen, apuntes o actividades que deseas adaptar:",
        type=["pdf"]
    )
    
    st.form_submit_button(" Aplicar Adaptación Inclusiva al PDF")

if archivo_subido is not None:
    with st.spinner("Leyendo tus materiales y aplicando las pautas DÚA (esto puede tardar unos segundos)..."):
        try:
            client = genai.Client(api_key=CLAVE_API)
            
            # 1. Cargamos el PDF del decreto de Madrid que está fijo en tu GitHub
            pdf_ley = preparar_pdf_ley("decreto_madrid.pdf")
            
            # 2. Procesamos en vivo el PDF que acaba de subir el usuario en la pantalla
            datos_archivo = archivo_subido.read()
            base64_archivo = base64.b64encode(datos_archivo).decode("utf-8")
            pdf_profesor = genai.types.Part.from_bytes(
                data=base64.b64decode(base64_archivo),
                mime_type="application/pdf"
            )
            
            # Instrucciones troceadas de forma compacta para blindar la caja gris
            i1 = "Actúa como un inspector experto en Inclusión y pedagogía DÚA. "
            i2 = f"Usa el PDF decreto_madrid.pdf como marco legal para {curso}. "
            i3 = f"El alumno presenta la siguiente necesidad: '{necesidad}'. "
            i4 = "Se te proporciona un segundo PDF adjunto con el examen o las "
            i5 = "actividades originales diseñadas por el docente. "
            i6 = "INSTRUCCIÓN: Analiza el contenido del PDF del docente y rediseña "
            i7 = "todas sus preguntas para adaptarlas a la necesidad seleccionada. "
            i8 = "Aplica pautas DÚA estrictas: segmenta pasos si es TDAH, simplifica "
            i9 = "enunciados si es dislexia o eleva el reto cognitivo si son Altas "
            i10 = "Capidades. REQUISITO: Devuelve el documento con dos secciones: "
            i11 = "1. EL MATERIAL ADAPTADO final listo para imprimir y entregar, "
            i12 = "2. Una breve JUSTIFICACIÓN PEDAGÓGICA de las adaptaciones. "
            i13 = "Usa un lenguaje formal, técnico y limpio. Sin saludos iniciales."
            
            prompt_inclusion = i1+i2+i3+i4+i5+i6+i7+i8+i9+i10+i11+i12+i13
            
            # Empaquetamos los dos PDFs (el de la ley y el del profesor) y las instrucciones
            elementos_envio = []
            if pdf_ley: elementos_envio.append(pdf_ley)
            elementos_envio.append(pdf_profesor)
            elementos_envio.append(prompt_inclusion)
            
            response = client.models.generate_content(model='gemini-flash-latest', contents=elementos_envio)
            
            if response and response.text:
                st.success("¡Material adaptado con éxito bajo pautas DÚA!")
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
                st.download_button(
                    label="📥 Descargar Adaptación (.txt)",
                    data=response.text,
                    file_name=f"Adaptacion_{curso.replace(' ', '')}.txt",
                    mime="text/plain"
                )
            else:
                st.error("La IA respondió pero el material llegó vacío.")
        except Exception as e:
            st.error(f"Error al conectar con la IA de Google: {str(e)}")
else:
    if st.session_state.get('formulario_inclusion_pdf_submitted'):
        st.info("Por favor, selecciona y sube un archivo PDF para poder realizar la adaptación.")
