import streamlit as st
from google import genai
import os
import base64

st.title("Diseñador de Rúbricas Formativas")
st.subheader("Matrices de Evaluación según la LOMLOE")
st.caption("Generación automatizada de tablas de evaluación basadas en el Decreto 65/2022 del BOCM")

# Clave de la API segura
CLAVE_API = st.secrets["gemini_key"]

def preparar_pdf_para_ia(nombre_archivo):
    ruta_completa = os.path.join("contexto", nombre_archivo)
    if os.path.exists(ruta_completa):
        with open(ruta_completa, "rb") as f:
            d = base64.b64encode(f.read()).decode("utf-8")
            return genai.types.Part.from_bytes(data=base64.b64decode(d), mime_type="application/pdf")
    return None

with st.form("formulario_rubricas"):
    st.markdown("### Parámetros de la Rúbrica")
    
    curso = st.selectbox(
        "Selecciona el Curso de ESO:",
        ["1º de ESO", "2º de ESO", "3º de ESO", "4º de ESO"]
    )
    
    producto_evaluar = st.selectbox(
        "Producto Final o Tarea a evaluar:",
        [
            "Cómic digital diseñado con la plataforma Pixton",
            "Examen tradicional impreso (Desarrollo y test)",
            "Exposición oral para la clase",
            "Podcast o programa de radio literario en equipo",
            "Debate formal en el aula con turnos (Oratoria)",
            "Periódico digital escolar o reportaje escrito",
            "Campaña publicitaria con cartelería digital",
            "Antología lírica comentada e ilustrada",
            "Representación teatral o lectura dramatizada"
        ]
    )
    
    aspecto_clave = st.text_input(
        "Enfoque o contenido prioritario (Opcional):",
        placeholder="Ej: Coherencia textual, uso de nexos, ortografía, creatividad..."
    )
    
    st.form_submit_button(" Diseñar Rúbrica en Tabla")

if producto_evaluar:
    with st.spinner("Leyendo decreto_madrid.pdf y redactando la matriz de evaluación..."):
        try:
            client = genai.Client(api_key=CLAVE_API)
            pdf = preparar_pdf_para_ia("decreto_madrid.pdf")
            
            # Textos troceados en líneas cortas para evitar roturas de formato
            r1 = "Actúa como un catedrático experto en evaluación formativa. "
            r2 = f"Usa el PDF decreto_madrid.pdf para extraer los criterios de {curso}. "
            r3 = f"Diseña una rúbrica formal para evaluar: '{producto_evaluar}'. "
            r4 = f"Enfoque especial del profesor: '{aspecto_clave}'. "
            r5 = "REQUISITO OBLIGATORIO: Devuelve el resultado ESTRICTAMENTE en "
            r6 = "formato de TABLA MARKDOWN con las siguientes columnas: "
            r7 = "1. Aspecto/Criterio Evaluado (vinculado a la ley), "
            r8 = "2. Insuficiente (1-4), 3. Suficiente (5), "
            r9 = "4. Notable (6-8), 5. Sobresaliente (9-10). "
            r10 = "Redacta los indicadores de logro de forma técnica, clara y adaptada "
            r11 = "al producto (ej. si es Pixton, evalúa el uso de viñetas y diálogos). "
            r12 = "Entrega directamente la tabla sin comentarios informales preliminares."
            
            prompt_rubrica = r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9 + r10 + r11 + r12
            
            envio = [pdf, prompt_rubrica] if pdf else [prompt_rubrica]
            response = client.models.generate_content(model='gemini-flash-latest', contents=envio)
            
            if response and response.text:
                st.success("¡Rúbrica diseñada con éxito!")
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
                st.download_button(
                    label="📥 Descargar Rúbrica (.txt)",
                    data=response.text,
                    file_name=f"Rubrica_{curso.replace(' ', '')}.txt",
                    mime="text/plain"
                )
            else:
                st.error("La IA respondió pero la rúbrica llegó vacía.")
        except Exception as e:
            st.error(f"Error al conectar con la IA de Google: {str(e)}")
