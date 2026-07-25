import streamlit as st
from google import genai
import os
import base64

st.title("🧠 Generador de Adaptaciones y DÚA")
st.subheader("Atención a la Diversidad e Inclusión Educativa (Madrid)")
st.caption("Adaptación inmediata de materiales y actividades según el Decreto 65/2022")

# Clave de la API segura
CLAVE_API = st.secrets["gemini_key"]

def preparar_pdf_para_ia(nombre_archivo):
    ruta_completa = os.path.join("contexto", nombre_archivo)
    if os.path.exists(ruta_completa):
        with open(ruta_completa, "rb") as f:
            d = base64.b64encode(f.read()).decode("utf-8")
            return genai.types.Part.from_bytes(data=base64.b64decode(d), mime_type="application/pdf")
    return None

with st.form("formulario_inclusion"):
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
    
    texto_original = st.text_area(
        "Pega aquí las preguntas del examen o las actividades de la unidad a adaptar:",
        placeholder="Ej: 1. Analiza sintácticamente... 2. Redacta un texto de 200 palabras sobre...",
        height=150
    )
    
    st.form_submit_button("✨ Aplicar Adaptación Inclusiva")

if texto_original:
    if not texto_original.strip():
        st.error("Por favor, pega algún texto o actividad original para poder adaptarlo.")
    else:
        with st.spinner("Procesando pautas de inclusión y rediseñando el material..."):
            try:
                client = genai.Client(api_key=CLAVE_API)
                pdf = preparar_pdf_para_ia("decreto_madrid.pdf")
                
                # Instrucciones troceadas para blindar la caja gris contra roturas
                i1 = "Actúa como un inspector experto en Inclusión y pedagogía DÚA. "
                i2 = f"Usa el PDF decreto_madrid.pdf como marco para {curso}. "
                i3 = f"El alumno presenta la siguiente necesidad: '{necesidad}'. "
                i4 = f"El material original que el profesor aporta es: '{texto_original}'. "
                i5 = "INSTRUCCIÓN DE TRABAJO: Rediseña el material original para "
                i6 = "adaptarlo de forma personalizada a esa necesidad. "
                i7 = "Aplica pautas DÚA claras: si es dislexia, simplifica enunciados; "
                i8 = "si es TDAH, segmenta pasos; si es español L2, añade apoyos; "
                i9 = "si son Altas Capacidades, eleva la complejidad intelectual "
                i10 = "sin añadir más carga de trabajo. REQUISITO: Devuelve: "
                i11 = "1. El MATERIAL ADAPTADO listo para entregar al alumno, "
                i12 = "2. Una breve JUSTIFICACIÓN PEDAGÓGICA de las medidas "
                i13 = "adoptadas para la memoria del profesor. Redacta de forma "
                i14 = "técnica, formal y limpia sin comentarios preliminares."
                
                prompt_inclusion = i1+i2+i3+i4+i5+i6+i7+i8+i9+i10+i11+i12+i13+i14
                
                envio = [pdf, prompt_inclusion] if pdf else [prompt_inclusion]
                response = client.models.generate_content(model='gemini-flash-latest', contents=envio)
                
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
