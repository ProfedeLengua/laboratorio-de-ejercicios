import streamlit as st
from google import genai
import os
import base64

st.title("Taller de Comentario de Texto y Oratoria")
st.subheader("Laboratorio de Expresión y Comprensión Crítica")
st.caption("Recursos didácticos para el desarrollo de la retórica y el análisis textual")

# Clave de la API segura
CLAVE_API = st.secrets["gemini_key"]

def preparar_pdf_para_ia(nombre_archivo):
    ruta_completa = os.path.join("contexto", nombre_archivo)
    if os.path.exists(ruta_completa):
        with open(ruta_completa, "rb") as f:
            d = base64.b64encode(f.read()).decode("utf-8")
            return genai.types.Part.from_bytes(data=base64.b64decode(d), mime_type="application/pdf")
    return None

with st.form("formulario_talleres"):
    st.markdown("### Parámetros del Taller")
    
    curso = st.selectbox(
        "Selecciona el Curso de ESO:",
        ["1º de ESO", "2º de ESO", "3º de ESO", "4º de ESO"]
    )
    
    tipo_taller = st.radio(
        "Selecciona la herramienta que deseas generar:",
        ["Guía de Comentario de Texto (Lectura y Crítica)", 
         "Guía de Debate Formal y Oratoria (Retórica)"]
    )
    
    foco_tematico = st.text_input(
        "Introduce el Autor, Obra o Tema motor del taller:",
        placeholder="Ej: Bécquer, El Quijote, Las redes sociales, El cambio climático..."
    )
    
    st.form_submit_button("Fabricar Material Didáctico")

if foco_tematico:
    if not foco_tematico.strip():
        st.error("Por favor, escribe un tema, autor u obra para activar el taller.")
    else:
        with st.spinner("Consultando el currículo de Madrid y redactando los materiales..."):
            try:
                client = genai.Client(api_key=CLAVE_API)
                pdf = preparar_pdf_para_ia("decreto_madrid.pdf")
                
                # Instrucciones troceadas para blindar la caja gris
                t1 = "Actúa como un catedrático experto en Filología y Retórica. "
                t2 = f"Usa el PDF decreto_madrid.pdf para adecuar el nivel a {curso}. "
                t3 = f"El profesor solicita la opción: '{tipo_taller}'. "
                t4 = f"El foco o tema motor elegido es: '{foco_tematico}'. "
                t5 = "INSTRUCCIÓN SI ES COMENTARIO DE TEXTO: Genera un fragmento "
                t6 = "representativo (o búscalo si es autor clásico) y diseña 4 "
                t7 = "preguntas guiadas divididas en: Localización, Comprensión "
                t8 = "(Tema y estructura) y Análisis Lingüístico/Estilístico acordes al curso. "
                t9 = "INSTRUCCIÓN SI ES ORATORIA/DEBATE: Diseña una ficha con: "
                t10 = "1. Introducción al dilema, 2. Tres argumentos sólidos a favor, "
                t11 = "3. Tres argumentos sólidos en contra, 4. Tres falacias lógicas "
                t12 = "habituales que el alumnado debe evitar, 5. Un banco de 6 palabras "
                t13 = "o nexos formales obligatorios para el debate. Redacta de forma "
                t14 = "técnica, limpia y formal. No incluyas comentarios iniciales."
                
                prompt_taller = t1+t2+t3+t4+t5+t6+t7+t8+t9+t10+t11+t12+t13+t14
                
                envio = [pdf, prompt_taller] if pdf else [prompt_taller]
                response = client.models.generate_content(model='gemini-flash-latest', contents=envio)
                
                if response and response.text:
                    st.success("¡Material didáctics generado con éxito!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.markdown("---")
                    st.download_button(
                        label="📥 Descargar Material (.txt)",
                        data=response.text,
                        file_name=f"Taller_{curso.replace(' ', '')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("La IA respondió pero el material llegó vacío.")
            except Exception as e:
                st.error(f"Error al conectar con la IA de Google: {str(e)}")
