import streamlit as st
import requests
import json
import os
import base64

# Configuración visual interna de la pestaña
st.title("🧭 Diseñador de Situaciones de Aprendizaje")
st.subheader("Planificación de Secuencias Didácticas LOMLOE (Comunidad de Madrid)")
st.caption("Generación guiada mediante lectura de documentos PDF oficiales")

# Leemos la clave de forma segura desde el panel secreto de Streamlit
CLAVE_API = st.secrets["gemini_key"]

# 🌟 FUNCIÓN INTELIGENTE: Transforma un PDF local en datos decodificados para Google Gemini
def preparar_pdf_para_ia(nombre_archivo):
    ruta_completa = os.path.join("contexto", nombre_archivo)
    if os.path.exists(ruta_completa):
        with open(ruta_completa, "rb") as f:
            datos_binarios = f.read()
            # Convertimos el PDF en un formato de texto seguro (base64)
            datos_base64 = base64.b64encode(datos_binarios).decode("utf-8")
            return {
                "inlineData": {
                    "mimeType": "application/pdf",
                    "data": datos_base64
                }
            }
    return None

# Configuración del formulario
with st.form("formulario_sda"):
    st.markdown("### 🎛️ Parámetros de la Situación de Aprendizaje")
    
    curso = st.selectbox(
        "Curso de la ESO destinatario:",
        ["1º de ESO", "2º de ESO", "3º de ESO", "4º de ESO"]
    )
    
    centro_interes = st.text_input(
        "Centro de Interés / Temática motora:",
        placeholder="Ej: El misterio en la literatura, las 'fake news' en la prensa, ecología..."
    )
    
    producto_final = st.selectbox(
        "Producto Final Esperado:",
        [
            "Antología poética comentada",
            "Podcast o programa de radio literario",
            "Debate formal en clase (Oratoria)",
            "Periódico digital o reportaje escrito",
            "Campaña publicitaria social (Cartelería y eslóganes)",
            "Representación teatral o lectura dramatizada"
        ]
    )
    
    num_sesiones = st.slider("Número de sesiones estimadas:", min_value=3, max_value=12, value=6)
    
    st.form_submit_button("✨ Generar Situación de Aprendizaje")

# Acción al enviar el formulario
if centro_interes:
    if not centro_interes.strip():
        st.error("Por favor, introduce una temática para la secuencia didáctica.")
    else:
        with st.spinner("Analizando tus PDFs de referencia y diseñando la Situación de Aprendizaje (esto puede tardar unos segundos)..."):
            try:
                # 🌟 CARGA MULTIMEDIA: Preparamos los dos PDFs para enviárselos a Google
                pdf_bocm = preparar_pdf_para_ia("decreto_madrid.pdf")
                pdf_pautas = preparar_pdf_para_ia("pautas_sda.pdf")
                
                if not pdf_bocm or not pdf_pautas:
                    st.warning("Aviso: No se ha encontrado alguno de los archivos PDF ('decreto_madrid.pdf' o 'pautas_sda.pdf') en la carpeta 'contexto'. La IA responderá de forma genérica.")
                
                # Instrucción técnica para ligar los PDFs a la consulta
                indicacion_texto = f"""
                Actúa como un catedrático experto en Didáctica de la Lengua Castellana y la Literatura. 
                Se te proporcionan dos archivos PDF adjuntos que contienen la normativa oficial y las pautas metodológicas que debes seguir obligatoriamente.
                
                INSTRUCCIONES DE DISEÑO:
                1. Analiza el PDF del decreto de la Comunidad de Madrid (decreto_madrid.pdf) y extrae de forma literal las Competencias Específicas, Criterios de Evaluación y Saberes Básicos correspondientes estrictamente a {curso}.
                2. Analiza el PDF de las pautas del docente (pautas_sda.pdf) y aplica su estructura metodológica, principios DÚA y secuenciación para dar forma al documento.
                
                DATOS ESPECÍFICOS DE ESTA UNIDAD:
                - CURSO DESTINATARIO: {curso}
                - CENTRO DE INTERÉS PROMOTOR: {centro_interes}
                - PRODUCTO FINAL EVALUABLE: {producto_final}
                - DURACIÓN ACADÉMICA: {num_sesiones} sesiones.

                Devuelve la Situación de Aprendizaje LOMLOE perfectamente estructurada y maquetada con lenguaje formal, sin comentarios informales por tu parte.
                """
                
                # Preparamos el paquete de envío de Google integrando los archivos y el texto
                partes_contenido = []
                if pdf_bocm: partes_contenido.append(pdf_bocm)
                if pdf_pautas: partes_contenido.append(pdf_pautas)
                partes_contenido.append({"text": indicacion_texto})
                
                # Endpoint v1 oficial para subida de archivos incrustados
                url_base = "https://googleapis.com"
                parametros_consulta = {"key": CLAVE_API}
                
                payload = {
                    "contents": [{
                        "parts": partes_contenido
                    }]
                }
                
                headers = {"Content-Type": "application/json"}
                
                respuesta = requests.post(url_base, params=parametros_consulta, json=payload, headers=headers)
                
                if respuesta.status_code == 200:
                    datos = respuesta.json()
                    texto_sda = datos['candidates'][0]['content']['parts'][0]['text']
                    
                    st.success("¡Situación de Aprendizaje diseñada con éxito leyendo tus directrices PDF!")
                    st.markdown("---")
                    st.markdown(texto_sda)
                    st.markdown("---")
                    
                    st.download_button(
                        label="📥 Descargar Unidad para tu Programación (.txt)",
                        data=texto_sda,
                        file_name=f"SDA_{curso.replace(' ', '')}_{producto_final.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"El servidor de Google rechazó la petición. Código: {respuesta.status_code}")
                    st.text(respuesta.text)
                    
            except Exception as e:
                st.error(f"Error interno al procesar los archivos de la SDA: {str(e)}")
