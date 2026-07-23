import streamlit as st
import google.generativeai as genai
import json

# Configuración visual de la página web (Estilo académico)
st.set_page_config(page_title="Laboratorio de Lengua y Literatura", page_icon="📝", layout="centered")

st.title("📝 Laboratorio de Lengua y Literatura")
st.subheader("Generador inteligente de exámenes de ESO (Comunidad de Madrid)")
st.caption("Herramienta 100% gratuita y de código abierto basada en el Decreto 65/2022")

# 🛑 PON TU CLAVE DE GOOGLE AI STUDIO AQUÍ ADENTRO MANTENIENDO LAS COMILLAS:
CLAVE_API = st.secrets["gemini_key"]

# Configuración del formulario con los menús desplegables de la ESO
with st.form("formulario_examen"):
    curso = st.selectbox(
        "Selecciona el Curso de ESO:",
        [
            "1º de ESO (Sujeto/Predicado, Narrativa/Lírica tradicional)",
            "2º de ESO (Oración simple completa, Géneros literarios)",
            "3º de ESO (Valores de 'se', Coordinadas, Edad Media al S. Oro)",
            "4º de ESO (Subordinación compleja, Siglo XVIII al XX)"
        ]
    )
    
    modalidad = st.selectbox(
        "Modalidad Textual del Fragmento:",
        ["Narrativo", "Descriptivo", "Expositivo", "Argumentativo", "Dialogado"]
    )
    
    tematica = st.text_input("Temática del Texto:", placeholder="Ej: Las redes sociales, la naturaleza...")
    
    st.write("Contenidos obligatorios en las preguntas:")
    col1, col2 = st.columns(2)
    with col1:
        p1 = st.checkbox("Comprensión Lectora", value=True)
        p2 = st.checkbox("Morfología y Léxico", value=True)
    with col2:
        p3 = st.checkbox("Análisis Sintáctico", value=True)
        p4 = st.checkbox("Educación Literaria", value=False)
        
    boton_generar = st.form_submit_button("✨ Generar Examen Gratis")

# Acción al pulsar el botón
if boton_generar:
    if not tematica.strip():
        st.error("Por favor, introduce una temática para el texto.")
    else:
        bloques = []
        if p1: bloques.append("Comprensión Lectora")
        if p2: bloques.append("Morfología y Léxico")
        if p3: bloques.append("Análisis Sintáctico")
        if p4: bloques.append("Educación Literaria")
        
        with st.spinner("Fabricando el examen según el currículo de Madrid... Por favor, espera unos 15 segundos."):
            try:
                # 🌟 CORRECCIÓN CRÍTICA PARA EL NUEVO FORMATO DE CLAVES "AQ."
                # Inicializamos el cliente forzando la clave de forma explícita en la configuración
                genai.configure(api_key=CLAVE_API, client_options={"api_key": CLAVE_API})
                
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt_maestro = f"""
                Genera un examen oficial de Lengua Castellana y Literatura para la Comunidad de Madrid basándote estrictamente en el Decreto 65/2022. 
                PARÁMETROS:
                - CURSO: {curso}
                - MODALIDAD TEXTUAL: {modalidad}
                - TEMÁTICA CENTRAL: {tematica}
                - BLOQUES REQUERIDOS: {', '.join(bloques)}

                ESTRUCTURA REQUERIDA:
                1. Un texto original e inédito redactado por ti adaptado a la temática, modalidad y nivel sintáctico del curso (entre 150 y 300 palabras).
                2. Preguntas asociadas a los bloques requeridos utilizando frases literales del texto. Si se pide Sintaxis, usa enunciados del nivel exacto del curso.
                3. Sección 'SOLUCIONARIO Y CLAVE DE CORRECCIÓN' al final.
                
                Devuelve directamente el examen sin saludos ni comentarios preliminares.
                """
                
                respuesta = model.generate_content(prompt_maestro)
                
                # Mostrar el resultado maquetado en pantalla
                st.success("¡Examen generado con éxito!")
                st.markdown("---")
                st.markdown(respuesta.text)
                st.markdown("---")
                
                # Botón nativo para descargar el examen como archivo de texto listo para Word
                st.download_button(
                    label="📥 Descargar examen para Word (.txt)",
                    data=respuesta.text,
                    file_name=f"Examen_{modalidad}_{tematica.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Error al conectar con la IA: {str(e)}")

                
            except Exception as e:
                st.error(f"Error al conectar con la IA: {str(e)}")
