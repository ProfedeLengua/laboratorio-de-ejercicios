import streamlit as st
from google import genai
import os
import base64

# Configuración visual de la pestaña
st.title("🧭 Diseñador de Situaciones de Aprendizaje")
st.subheader("Planificación de Secuencias LOMLOE (Madrid)")
st.caption("Selección interactiva de saberes básicos")

# Clave de la API
CLAVE_API = st.secrets["gemini_key"]

# BANCO DE SABERES (Líneas cortadas para evitar errores de formato)
SABERES_DETALLADOS = {
    "1º de ESO": {
        "Bloque 1: Comunicación": [
            "Léxico formal e informal en textos narrativos.",
            "Comprensión de mitos y leyendas tradicionales.",
            "Estructura del texto expositivo académico básico.",
            "Estrategias de fomento de la biografía lectora."
        ],
        "Bloque 2: Lengua": [
            "Diferenciación entre enunciado, frase y oración.",
            "Estructura del sujeto y el predicado verbal.",
            "Reconocimiento de sustantivos y adjetivos.",
            "Reglas generales de acentuación y ortografía."
        ],
        "Bloque 3: Literatura": [
            "Características de la narrativa tradicional.",
            "La lírica popular (romances y canciones).",
            "Lectura comentada de relatos breves adaptados."
        ]
    },
    "2º de ESO": {
        "Bloque 1: Comunicación": [
            "Análisis de textos descriptivos literarios.",
            "Convenciones del diálogo en textos teatrales.",
            "Mecanismos de coherencia en la escritura.",
            "Técnicas de exposición oral y soportes visuales."
        ],
        "Bloque 2: Lengua": [
            "El núcleo verbal y la oración simple.",
            "Análisis del Atributo y el Predicativo.",
            "Identificación del CD y el CI verbal.",
            "Uso de los Complementos Circunstanciales (CC)."
        ],
        "Bloque 3: Literatura": [
            "Diferenciación de grandes géneros clásicos.",
            "Tópicos y temas en la literatura juvenil.",
            "Lectura guiada de clásicos adaptados."
        ]
    },
    "3º de ESO": {
        "Bloque 1: Comunicación": [
            "Comprensión de textos expositivos y divulgativos.",
            "El discurso argumentativo en editoriales y prensa.",
            "Planificación y redacción de textos argumentativos.",
            "Estrategias de debate grupal y escucha activa."
        ],
        "Bloque 2: Lengua": [
            "Introducción a la oración compuesta: Coordinación.",
            "Reconocimiento de oraciones yuxtapuestas.",
            "Valores sintácticos del pronombre 'se' completo.",
            "Procedimientos de formación: prefijos y sufijos."
        ],
        "Bloque 3: Literatura": [
            "Contexto: De la Edad Media al Prerrenacimiento.",
            "El esplendor del Siglo de Oro (Poesía y Teatro).",
            "Lectura y comentario crítico de obras del Barroco."
        ]
    },
    "4º de ESO": {
        "Bloque 1: Comunicación": [
            "Análisis del discurso en prensa compleja.",
            "Redacción de ensayos y artículos de opinión.",
            "Estructura del debate académico y oratoria.",
            "Estrategias de síntesis: Resúmenes y mapas."
        ],
        "Bloque 2: Lengua": [
            "La oración compuesta compleja: Subordinación.",
            "Análisis de proposiciones subordinadas sustantivas.",
            "Análisis de subordinadas adjetivas de relativo.",
            "Estructura de las subordinadas adverbiales."
        ],
        "Bloque 3: Literatura": [
            "El Siglo de las Luces e Ilustración (S. XVIII).",
            "El Romanticismo y el Realismo en el Siglo XIX.",
            "Las vanguardias y movimientos del Siglo XX."
        ]
    }
}

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

# 2. Selector de bloque curricular
st.markdown("### 📚 2. Bloque Curricular (Decreto 65/2022)")
bloques_disponibles = list(SABERES_DETALLADOS[curso_seleccionado].keys())
bloque_elegido = st.selectbox("Elige el bloque específico:", bloques_disponibles)

st.markdown("### 🗂️ 3. Configuración de Saberes Básicos")
st.caption("Selecciona los contenidos en la caja izquierda:")

# Interfaz en paralelo
col_disponibles, col_seleccionados = st.columns(2)

with col_disponibles:
    st.info("📋 Contenidos desglosados:")
    saberes_disponibles = SABERES_DETALLADOS[curso_seleccionado][bloque_elegido]
    saberes_elegidos = st.multiselect(
        "Haz clic para seleccionar:",
        saberes_disponibles,
        default=[]
    )

with col_seleccionados:
    st.success("🎯 Contenidos seleccionados:")
    if saberes_elegidos:
        st.markdown(f"**Eje:** {bloque_elegido}")
        for saber in saberes_elegidos:
            st.markdown(f"**•** {saber}")
    else:
        st.warning("La caja está vacía.")

st.markdown("---")

# Formulario final
with st.form("formulario_SDA_avanzado"):
    st.markdown("### 🎛️ 4. Parámetros Finales del Proyecto")
    
    centro_interes = st.text_input(
        "Centro de Interés / Temática motora:",
        placeholder="Ej: Las 'fake news', el cambio climático..."
    )
    
    producto_final = st.selectbox(
        "Producto Final Esperado:",
        [
            "Examen tradicional impreso (Desarrollo y test)",
            "Cómic digital diseñado con la plataforma Pixton",
            "Podcast o programa de radio literario en equipo",
            "Debate formal en el aula con turnos (Oratoria)",
            "Periódico digital escolar o reportaje escrito",
            "Campaña publicitaria con cartelería digital",
            "Antología lírica comentada e ilustrada",
            "Representación teatral o lectura dramatizada"
        ]
    )
    
    num_sesiones = st.slider("Sesiones:", min_value=3, max_value=12, value=6)
    st.form_submit_button("✨ Generar Situación de Aprendizaje")

# Acción al enviar el formulario
if centro_interes:
    if not saberes_elegidos:
        st.error("Por favor, selecciona al menos un saber básico.")
    elif not centro_interes.strip():
        st.error("Por favor, introduce un centro de interés.")
    else:
        with st.spinner("Leyendo pdf y diseñando la Unidad..."):
            try:
                client = genai.Client(api_key=CLAVE_API)
                parte_pdf_bocm = preparar_pdf_para_ia("decreto_madrid.pdf")
                
                # Texto de instrucciones cortado para evitar roturas de caja
                t1 = "Actúa como un catedrático experto en Didáctica. "
                t2 = f"Usa el PDF decreto_madrid.pdf. CURSO: {curso_seleccionado}. "
                t3 = f"EJE: {bloque_elegido}. SABERES: {', '.join(saberes_elegidos)}. "
                t4 = f"TEMA: {centro_interes}. PRODUCTO: {producto_final}. "
                t5 = f"DURACIÓN: {num_sesiones} sesiones. Redacta una SDA LOMLOE "
                t6 = "completa con inicio, desarrollo, cierre, criterios y DÚA. "
                t7 = "Usa lenguaje técnico formal escolar y entrega el texto limpio."
                
                indicacion_texto = t1 + t2 + t3 + t4 + t5 + t6 + t7
                
                elementos_envio = []
                if parte_pdf_bocm:
                    elementos_envio.append(parte_pdf_bocm)
                elementos_envio.append(indicacion_texto)
                
                response = client.models.generate_content(
                    model='gemini-flash-latest',
                    contents=elementos_envio,
                )
                
                if response and response.text:
                    st.success("¡Unidad diseñada con éxito!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.markdown("---")
                    
                    st.download_button(
                        label="📥 Descargar Proyecto (.txt)",
                        data=response.text,
                        file_name="SDA_Planificada.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("La IA respondió pero el texto llegó vacío.")
                    
            except Exception as e:
                st.error(f"Error al conectar con la IA de Google: {str(e)}")
