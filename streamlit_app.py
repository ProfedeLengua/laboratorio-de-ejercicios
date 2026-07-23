import streamlit as st
import requests
import json

# Configuración visual de la página web (Estilo académico)
st.set_page_config(page_title="Laboratorio de Lengua y Literatura", page_icon="📝", layout="centered")

st.title("📝 Laboratorio de Lengua y Literatura")
st.subheader("Generador inteligente de exámenes de ESO (Comunidad de Madrid)")
st.caption("Herramienta 100% gratuita y de código abierto basada en el Decreto 65/2022")

# Leemos la clave de forma segura desde el panel secreto de Streamlit
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
                # Instrucción curricular para la IA
                prompt_maestro = f"""
                Genera un examen oficial de Lengua Castellana y Literatura para la Comunidad de Madrid basándote estrictamente en el Decreto 65/2022. 
                PARÁMETROS:
                - CURSO: {curso}
                - MODALIDAD TEXTUAL: {modalidad}
                - TEMÁTICA CENTRAL: {tematica}
                - BLOQUES REQUERIDOS: {', '.join(bloques)}

                ESTRUCTURA REQUERIDA:
                1. Un texto original e inédito redactado por ti adaptado a la temática, modalidad y nivel sintáctico del curso (entre 150 y 300 palabras).
                2. Preguntas asociadas a los bloques requeridos utilizando frases literales del texto. Si se pide Sintaxis, usa enunciados del nivel exacto del curso (oración simple para 1º/2º ESO, subordinación para 4º ESO, etc.).
                3. Sección 'SOLUCIONARIO Y CLAVE DE CORRECCIÓN' al final.
                
                Devuelve directamente el examen sin saludos ni comentarios preliminares.
                """
                
                # 🌟 LA DIRECCIÓN WEB OFICIAL CORREGIDA MANUALMENTE:
                # Se utiliza la ruta con la etiqueta "-latest" que exige Google para responder por HTTP externo
                direccion_servidor = "https://googleapis.com"
                
                parametros_consulta = {"key": CLAVE_API}
                
                payload = {
                    "contents": [{
                        "parts": [{"text": prompt_maestro}]
                    }]
                }
                
                headers = {"Content-Type": "application/json"}
                
                # Ejecutamos la petición enviando los datos de forma segura
                respuesta = requests.post(direccion_servidor, params=parametros_consulta, json=payload, headers=headers)
                datos = respuesta.json()
                
                # Extracción manual de los datos del examen
                if respuesta.status_code == 200:
                    texto_examen = datos['candidates'][0]['content']['parts'][0]['text']
                    
                    st.success("¡Examen generado con éxito!")
                    st.markdown("---")
                    st.markdown(texto_examen)
                    st.markdown("---")
                    
                    # Botón nativo para descargar el examen listo para Word
                    st.download_button(
                        label="📥 Descargar examen para Word (.txt)",
                        data=texto_examen,
                        file_name=f"Examen_{modalidad}_{tematica.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"El servidor de Google rechazó la petición. Código de respuesta: {respuesta.status_code}")
                    st.text(respuesta.text)
                
            except Exception as e:
                st.error(f"Error interno al procesar los datos: {str(e)}")
