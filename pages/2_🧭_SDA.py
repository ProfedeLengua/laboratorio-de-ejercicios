import streamlit as st
from google import genai
import os
import base64
import requests

# Configuración visual de la pestaña
st.title("🧭 Diseñador de Situaciones de Aprendizaje")
st.subheader("Planificación de Secuencias Didácticas LOMLOE (Comunidad de Madrid)")
st.caption("Selección interactiva de saberes básicos y diseño curricular")

# Leemos la clave de forma segura desde el panel secreto de Streamlit
CLAVE_API = st.secrets["gemini_key"]

# 🌟 BANCO DE SABERES OFICIALES DE MADRID SUBDIVIDIDO POR BLOQUES Y CURSOS
SABERES_DETALLADOS = {
    "1º de ESO": {
        "Bloque 1: Comunicación oral y escrita": [
            "Léxico formal e informal en textos narrativos.",
            "Comprensión de textos narrativos tradicionales (mitos, leyendas).",
            "Estructura del texto expositivo académico de nivel básico.",
            "Estrategias de lectura guiada y fomento de la biografía lectora."
        ],
        "Bloque 2: Conocimiento de la lengua": [
            "Diferenciación entre enunciado, frase y oración.",
            "Estructura del sujeto sintáctico y el predicado verbal.",
            "Reconocimiento de sustantivos, adjetivos y determinantes.",
            "Reglas generales de acentuación y ortografía."
        ],
        "Bloque 3: Educación literaria": [
            "Características básicas de la narrativa tradicional.",
            "La lírica popular y tradicional (romances, canciones).",
            "Lectura comentada de relatos breves adaptados."
        ]
    },
    "2º de ESO": {
        "Bloque 1: Comunicación oral y escrita": [
            "Comprensión y análisis de textos descriptivos técnicos y literarios.",
            "Estructura y convenciones del diálogo en textos teatrales y narrativos.",
            "Mecanismos básicos de coherencia y cohesión en la escritura.",
            "Técnicas de exposición oral y uso de soportes visuales básicos."
        ],
        "Bloque 2: Conocimiento de la lengua": [
            "El núcleo verbal y la estructura de la oración simple.",
            "Análisis del Atributo y el Complemento Predicativo.",
            "Identificación del Complemento Directo (CD) e Indirecto (CI).",
            "Uso de los diversos Complementos Circunstanciales (CC)."
        ],
        "Bloque 3: Educación literaria": [
            "Diferenciación de los grandes géneros literarios clásicos.",
            "Tópicos y temas recurrentes en la literatura juvenil.",
            "Lectura guiada de clásicos adaptados a la secundaria."
        ]
    },
    "3º de ESO": {
        "Bloque 1: Comunicación oral y escrita": [
            "Comprensión avanzada de textos expositivos y divulgativos.",
            "El discurso argumentativo en los editoriales y columnas de prensa.",
            "Planificación y redacción de textos argumentativos estructurados.",
            "Estrategias de debate grupal y escucha activa en el aula."
        ],
        "Bloque 2: Conocimiento de la lengua": [
            "Introducción a la oración compuesta: La Coordinación.",
            "Reconocimiento de oraciones yuxtapuestas y sus conectores.",
            "Valores sintácticos del pronombre 'se' (reflexivo, recíproco, pasiva).",
            "Procedimientos de formación de palabras (prefijos y sufijos)."
        ],
        "Bloque 3: Educación literaria": [
            "Contextualización literaria: De la Edad Media al Prerrenacimiento.",
            "El esplendor del Siglo de Oro (Poesía, Prosa y Teatro nacional).",
            "Lectura y comentario crítico de obras del Renacimiento y Barroco."
        ]
    },
    "4º de ESO": {
        "Bloque 1: Comunicación oral y escrita": [
            "Análisis crítico del discurso en textos periodísticos complejos.",
            "Redacción de ensayos y artículos de opinión formalizados.",
            "Estructura formal del debate académico y técnicas de oratoria.",
            "Estrategias de síntesis: Resúmenes y mapas conceptuales complejos."
        ],
        "Bloque 2: Conocimiento de la lengua": [
            "La oración compuesta compleja: La subordinación.",
            "Análisis de proposiciones subordinadas sustantivas.",
            "Análisis de proposiciones subordinadas adjetivas (relativas).",
            "Estructura de las subordinadas adverbiales (causales, finales, etc.)."
        ],
        "Bloque 3: Educación literaria": [
            "El Siglo de las Luces y la literatura de la Ilustración (S. XVIII).",
            "El Romanticismo y el Realismo en el Siglo XIX.",
            "Las vanguardias y los movimientos literarios clave del Siglo XX."
        ]
    }
}

# Función para transformar el PDF en un bloque multimedia compatible con google-genai
def preparar_pdf_para_ia(nombre_archivo):
    ruta_completa = os.path.join("contexto", nombre_archivo)
    if os.path.exists(ruta_completa):
        with open(ruta_completa, "rb") as f:
            datos_base64 = base64.b64encode(f.read()).decode("utf-8")
            return genai.types.Part.from_bytes(
                data=base64.b64decode(datos_base64),
                mime_type="application/pdf"
            )
    return None

# 1. Selector de curso principal
st.markdown("### 🎛️ 1. Nivel Académico")
curso_seleccionado = st.selectbox(
    "Selecciona el Curso de ESO destinatario:",
    ["1º de ESO", "2º de ESO", "3º de ESO", "4º de ESO"]
)

# 🌟 2. SUBMENÚ MÁGICO: El profesor elige qué bloque de contenidos quiere trabajar hoy
st.markdown("### 📚 2. Bloque Curricular (Decreto 65/2022)")
bloques_disponibles = list(SABERES_DETALLADOS[curso_seleccionado].keys())
bloque_elegido = st.selectbox("Elige el bloque específico para desglosar sus contenidos:", bloques_disponibles)

st.markdown("### 🗂️ 3. Configuración de Saberes Básicos")
st.caption("Selecciona los contenidos en la caja izquierda para moverlos al plan de trabajo de la derecha:")

# Interfaz en paralelo (Doble columna interactiva)
col_disponibles, col_seleccionados = st.columns(2)

with col_disponibles:
    st.info("📋 Contenidos desglosados en el bloque:")
    # Mostramos únicamente los saberes correspondientes al bloque que ha seleccionado arriba
    saberes_disponibles = SABERES_DETALLADOS[curso_seleccionado][bloque_elegido]
    saberes_elegidos = st.multiselect(
        "Haz clic para seleccionar y enviar a la derecha:",
        saberes_disponibles,
        default=[]
    )

with col_seleccionados:
    st.success("🎯 Contenidos seleccionados para la Unidad:")
    if saberes_elegidos:
        # Añadimos el nombre del bloque para que la IA sepa de dónde viene
        st.markdown(f"**Eje de trabajo:** {bloque_elegido}")
        for saber in saberes_elegidos:
            st.markdown(f"**•** {saber}")
    else:
        st.warning("La caja está vacía. Selecciona elementos en la columna izquierda.")

st.markdown("---")

# Formulario para los parámetros restantes
with st.form("formulario_SDA_avanzado"):
    st.markdown("### 🎛️ 4. Parámetros Finales del Proyecto")
    
    centro_interes = st.text_input(
        "Centro de Interés / Temática motora:",
        placeholder="Ej: Las 'fake news', el cambio climático, la novela de misterio..."
    )
    
    producto_final = st.selectbox(
        "Producto Final Esperado:",
        [
            "Examen tradicional impreso (Preguntas de desarrollo y tipo test)",
            "Cómic digital diseñado con la plataforma Pixton",
            "Podcast o programa de radio literario grabado en equipo",
            "Debate formal en el aula con turnos de réplica (Oratoria)",
            "Periódico digital escolar o reportaje de investigación escrito",
            "Campaña publicitaria con cartelería digital y eslóganes para redes sociales",
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
        with st.spinner("Leyendo tu decreto_madrid.pdf y estructurando la Situación de Aprendizaje a la carta..."):
            try:
                client = genai.Client(api_key=CLAVE_API)
                parte_pdf_bocm = preparar_pdf_para_ia("decreto_madrid.pdf")
                
                indicacion_texto = f"""
                Actúa como un catedrático experto en Didáctica de la Lengua Castellana y la Literatura. 
                Se te proporciona adjunto el PDF de la normativa oficial de Madrid (decreto_madrid.pdf) como marco legal.
                
                EL DOCENTE HA SELECCIONADO ESTE EJE Y SABERES BÁSICOS ESPECÍFICOS:
                Eje curricular: {bloque_elegido}
                Contenidos específicos:
                {chr(10).join(saberes_elegidos)}
                
                DATOS COMPLEMENTARIOS DEL PROYECTO:
                - CURSO: {curso_seleccionado}
                - CENTRO DE INTERÉS: {centro_interes}
                - PRODUCTO FINAL EXIGIDO: {producto_final}
                - DURACIÓN ACADÉMICA: {num_sesiones} sesiones.

                INSTRUCCIONES DE REDACCIÓN:
                Diseña una Situación de Aprendizaje LOMLOE completa. Es obligatorio que las actividades de la secuencia didáctica (Inicio, Desarrollo y Cierre) estén diseñadas específicamente para enseñar y evaluar los SABERES BÁSICOS SELECCIONADOS por el profesor y que guarden estrecha relación con el PRODUCTO FINAL elegido (por ejemplo, si es un cómic con Pixton, detalla el uso y evaluación de la herramienta de diseño de cómics; si es un examen tradicional, planifica las sesiones de repaso previas).
                Asocia la unidad con Competencias Específicas y Criterios de Evaluación reales extraídos del PDF para el curso {curso_seleccionado}. Redacta con lenguaje técnico formal escolar, sin comentarios informales."""elementos_envio = []if parte_pdf_bocm:elementos_envio.append(parte_pdf_bocm)elementos_envio.append(indicacion_texto)response = client.models.generate_content(model='gemini-flash-latest',contents=elementos_envio,)if response and response.text:st.success("¡Situación de Aprendizaje diseñada con éxito con tus saberes elegidos!")st.markdown("---")st.markdown(response.text)st.markdown("---")st.download_button(label="📥 Descargar Proyecto para tu Programación (.txt)",data=response.text,file_name=f"SDA_{curso_seleccionado.replace(' ', '')}{producto_final[:10].replace(' ', '')}.txt",mime="text/plain")else:st.error("La IA de Google respondió pero el texto de la unidad didáctica llegó vacío.")except Exception as e:st.error(f"Error al conectar o procesar con la IA de Google: {str(e)}")
