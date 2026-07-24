import streamlit as st
import requests
import json
import os
import base64

# Configuración visual de la pestaña
st.title("🧭 Diseñador de Situaciones de Aprendizaje")
st.subheader("Planificación de Secuencias Didácticas LOMLOE (Comunidad de Madrid)")
st.caption("Selección interactiva de saberes básicos y diseño curricular")

# Leemos la clave de forma segura desde el panel secreto de Streamlit
CLAVE_API = st.secrets["gemini_key"]

# 🌟 BANCO DE SABERES BÁSICOS DE MADRID (Simulado por bloques para agilizar la interfaz sin saturar el PDF)
SABERES_POR_CURSO = {
    "1º de ESO": [
        "Bloque 1: Biografía lectora y estrategias de elección de textos.",
        "Bloque 1: Lectura guiada de obras clásicas y populares.",
        "Bloque 2: Distinción entre sujeto y predicado en enunciados.",
        "Bloque 2: Reconocimiento de núcleos y complementos del nombre.",
        "Bloque 3: Tipologías textuales: El texto narrativo tradicional.",
        "Bloque 3: Comprensión y producción de textos líricos populares."
    ],
    "2º de ESO": [
        "Bloque 1: Expresión e identificación de géneros literarios clásicos.",
        "Bloque 1: Análisis de temas recurrentes en la literatura juvenil.",
        "Bloque 2: Estructura y análisis de la oración simple completa.",
        "Bloque 2: Complementos verbales (CD, CI, CC, Atributo, CPred).",
        "Bloque 3: Comprensión de textos descriptivos y dialogados.",
        "Bloque 3: Coherencia y cohesión en la producción de textos breves."
    ],
    "3º de ESO": [
        "Bloque 1: Historia de la literatura: Del Prerrenacimiento al Siglo de Oro.",
        "Bloque 1: Lectura y comentario de textos medievales y renacentistas.",
        "Bloque 2: Introducción a la oración compuesta (Coordinación y Yuxtaposición).",
        "Bloque 2: Análisis de los valores sintácticos y semánticos del 'se'.",
        "Bloque 3: Comprensión de textos expositivos de carácter académico.",
        "Bloque 3: El discurso argumentativo básico en medios de comunicación."
    ],
    "4º de ESO": [
        "Bloque 1: Evolución literaria: Del Siglo de las Luces al Siglo XX.",
        "Bloque 1: Análisis crítico de movimientos literarios contemporáneos.",
        "Bloque 2: Estructura de la oración compuesta compleja y subordinación.",
        "Bloque 2: Proposiciones subordinadas sustantivas, adjetivas y adverbiales.",
        "Bloque 3: Comprensión y producción de textos argumentativos complejos.",
        "Bloque 3: Técnicas avanzadas de oratoria y debate académico formal."
    ]
}

# Función para transformar el PDF de la ley en datos para Google
def preparar_pdf_para_ia(nombre_archivo):
    ruta_completa = os.path.join("contexto", nombre_archivo)
    if os.path.exists(ruta_completa):
        with open(ruta_completa, "rb") as f:
            return {"inlineData": {"mimeType": "application/pdf", "data": base64.b64encode(f.read()).decode("utf-8")}}
    return None

# Selector de curso prioritario fuera del formulario para actualizar los contenidos al vuelo
curso_seleccionado = st.selectbox(
    "1. Selecciona el Curso de ESO destinatario:",
    ["1º de ESO", "2º de ESO", "3º de ESO", "4º de ESO"]
)

st.markdown("### 🗂️ 2. Configuración de Saberes Básicos (Decreto 65/2022)")
st.caption("Selecciona los contenidos en la caja izquierda para moverlos al plan de trabajo de la derecha:")

# 🌟 INTERFAZ EN PARALELO (Doble columna para arrastrar/seleccionar contenidos)
col_disponibles, col_seleccionados = st.columns(2)

with col_disponibles:
    st.info("📋 Contenidos disponibles en el Decreto:")
    saberes_disponibles = SABERES_POR_CURSO[curso_seleccionado]
    # Sistema de selección múltiple interactiva
    saberes_elegidos = st.multiselect(
        "Haz clic para seleccionar y enviar a la derecha:",
        saberes_disponibles,
        default=[]
    )

with col_seleccionados:
    st.success("🎯 Contenidos seleccionados para la Unidad:")
    if saberes_elegidos:
        for saber in saberes_elegidos:
            st.markdown(f"**•** {saber}")
    else:
        st.warning("La caja está vacía. Selecciona elementos en la columna izquierda.")

st.markdown("---")

# Formulario para los parámetros restantes y el botón de envío
with st.form("formulario_SDA_avanzado"):
    st.markdown("### 🎛️ 3. Parámetros Finales del Proyecto")
    
    centro_interes = st.text_input(
        "Centro de Interés / Temática motora:",
        placeholder="Ej: Las 'fake news', el cambio climático, la novela de misterio..."
    )
    
    # 🌟 LISTA AMPLIADA DE PRODUCTOS FINALES PEDIDOS
    producto_final = st.selectbox(
        "Producto Final Esperado:",
        [
            "Examen tradicional impreso (Preguntas de desarrollo y tipo test)",
            "Cómic digital diseñado con la plataforma Pixton",
            "Podcast o programa de radio literario grabado en equipo",
            "Debate formal en el aula con turnos de réplica (Oratoria)",
            "Periódico digital escolar o reportaje de investigación escrito",
            "Campaña publicitaria con cartelería digital y eslóganes redes sociales",
            "Antología lírica comentada e ilustrada por los alumnos",
            "Representación teatral o lectura dramatizada en el salón de actos"
        ]
    )
    
    num_sesiones = st.slider("Número de sesiones estimadas:", min_value=3, max_value=12, value=6)
    
    st.form_submit_button("✨ Generar Situación de Aprendizaje con Saberes Seleccionados")

# Acción al enviar el formulario
if centro_interes:
    if not saberes_elegidos:
        st.error("Por favor, selecciona al menos un saber básico en las columnas de arriba antes de generar.")
    elif not centro_interes.strip():
        st.error("Por favor, introduce un centro de interés.")
    else:
        with st.spinner("Leyendo decreto_madrid.pdf y estructurando tu Situación de Aprendizaje a la carta..."):
            try:
                pdf_bocm = preparar_pdf_para_ia("decreto_madrid.pdf")
                
                # Instrucción orientada a los saberes específicos que eligió el profesor
                indicacion_texto = f"""
                Actúa como un catedrático experto en Didáctica de la Lengua Castellana y la Literatura. 
                Se te proporciona el PDF de la normativa oficial de Madrid (decreto_madrid.pdf) como marco legal supremo.
                
                EL DOCENTE HA SELECCIONADO ESTOS SABERES BÁSICOS ESPECÍFICOS PARA LA UNIDAD:
                {chr(10).join(saberes_elegidos)}
                
                DATOS COMPLEMENTARIOS:
                - CURSO: {curso_seleccionado}
                - CENTRO DE INTERÉS: {centro_interes}
                - PRODUCTO FINAL EXIGIDO: {producto_final}
                - DURACIÓN: {num_sesiones} sesiones.

                INSTRUCCIONES DE REDACCIÓN:
                Diseña una Situación de Aprendizaje LOMLOE completa. Es OBLIGATORIO que las actividades de la secuencia didáctica (Inicio, Desarrollo y Cierre) estén diseñadas específicamente para enseñar y evaluar los SABERES BÁSICOS SELECCIONADOS por el profesor y que guarden relación con el PRODUCTO FINAL elegido (por ejemplo, si es un cómic con Pixton, detalla el uso de la herramienta informática en el desarrollo; si es un examen tradicional, planifica las sesiones de repaso previas). 
                Asocia la unidad con Competencias Específicas y Criterios de Evaluación reales del PDF para el curso {curso_seleccionado}. Redacta con lenguaje técnico formal.
                """
                
                partes_contenido = []
                if pdf_bocm: partes_contenido.append(pdf_bocm)
                partes_contenido.append({"text": indicacion_texto})
                
                url_base = "https://googleapis.com"
                parametros_consulta = {"key": CLAVE_API}
                
                payload = {"contents": [{"parts": partes_contenido}]}
                headers = {"Content-Type": "application/json"}
                
                respuesta = requests.post(url_base, params=parametros_consulta, json=payload, headers=headers)
                
                if respuesta.status_code == 200:
                    datos = respuesta.json()
                    texto_sda = datos['candidates'][0]['content']['parts'][0]['text']
                    
                    st.success("¡Situación de Aprendizaje diseñada con éxito con tus saberes elegidos!")
                    st.markdown("---")
                    st.markdown(texto_sda)
                    st.markdown("---")
                    
                    st.download_button(
                        label="📥 Descargar Proyecto para tu Programación (.txt)",
                        data=texto_sda,
                        file_name=f"SDA_{curso_seleccionado.replace(' ', '')}_{producto_final[:10].replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"Error de Google al procesar la SDA. Código: {respuesta.status_code}")
                    st.text(respuesta.text)
                    
            except Exception as e:
                st.error(f"Error al procesar los archivos: {str(e)}")
