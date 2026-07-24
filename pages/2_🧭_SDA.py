import streamlit as st
from google import genai
import os
import base64

st.title("🧭 Diseñador de Situaciones de Aprendizaje")
st.subheader("Planificación de Secuencias LOMLOE (Madrid)")
st.caption("Selección interactiva y acumulativa de saberes básicos")

CLAVE_API = st.secrets["gemini_key"]

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
            "Mecanismos de cohesencia en la escritura.",
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
            d = base64.b64encode(f.read()).decode("utf-8")
            return genai.types.Part.from_bytes(data=base64.b64decode(d), mime_type="application/pdf")
    return None

if "saberes_cesta" not in st.session_state:
    st.session_state["saberes_cesta"] = []

st.markdown("### 🎛️ 1. Nivel Académico")
curso_seleccionado = st.selectbox("Selecciona el Curso de ESO:", ["1º de ESO", "2º de ESO", "3º de ESO", "4º de ESO"])

if "curso_previo" not in st.session_state:
    st.session_state["curso_previo"] = curso_seleccionado
elif st.session_state["curso_previo"] != curso_seleccionado:
    st.session_state["saberes_cesta"] = []
    st.session_state["curso_previo"] = curso_seleccionado

st.markdown("### 📚 2. Bloque Curricular (Decreto 65/2022)")
bloques_disponibles = list(SABERES_DETALLADOS[curso_seleccionado].keys())
bloque_elegido = st.selectbox("Elige el bloque específico:", bloques_disponibles)

st.markdown("### 🗂️ 3. Configuración de Saberes Básicos")
col_disp, col_sel = st.columns(2)

with col_disp:
    st.info("📋 Contenidos desglosados:")
    saberes_bloque = SABERES_DETALLADOS[curso_seleccionado][bloque_elegido]
    seleccion_actual = st.multiselect("Selecciona elementos:", saberes_bloque, default=[])
    if st.button("➕ Añadir al plan"):
        for elem in seleccion_actual:
            txt = f"[{bloque_elegido}] {elem}"
            if txt not in st.session_state["saberes_cesta"]:
                st.session_state["saberes_cesta"].append(txt)
        st.success("¡Guardados!")

with col_sel:
    st.success("🎯 Cesta de contenidos acumulados:")
    if st.session_state["saberes_cesta"]:
        for saber in st.session_state["saberes_cesta"]:
            st.markdown(f"**•** {saber}")
        if st.button("🗑️ Vaciar cesta"):
            st.session_state["saberes_cesta"] = []
            st.rerun()
    else:
        st.warning("La cesta está vacía.")

st.markdown("---")

with st.form("formulario_SDA_avanzado"):
    st.markdown("### 🎛️ 4. Parámetros Finales")
    centro_interes = st.text_input("Centro de Interés / Temática motora:", placeholder="Ej: Las 'fake news'...")
    producto_final = st.selectbox("Producto Final:", [
        "Examen tradicional impreso (Desarrollo y test)",
        "Cómic digital diseñado con la plataforma Pixton",
        "Podcast o programa de radio literario en equipo",
        "Debate formal en el aula con turnos (Oratoria)",
        "Periódico digital escolar o reportaje escrito",
        "Campaña publicitaria con cartelería digital",
        "Antología lírica comentada e ilustrada",
        "Representación teatral o lectura dramatizada"
    ])
    num_sesiones = st.slider("Sesiones:", min_value=3, max_value=12, value=6)
    st.form_submit_button("✨ Generar Situación de Aprendizaje")

if centro_interes:
    if not st.session_state["saberes_cesta"]:
        st.error("Por favor, añade al menos un saber básico a tu cesta.")
    elif not centro_interes.strip():
        st.error("Por favor, introduce un centro de interés.")
    else:
        with st.spinner("Diseñando la Unidad con el PDF..."):
            try:
                client = genai.Client(api_key=CLAVE_API)
                pdf = preparar_pdf_para_ia("decreto_madrid.pdf")
                prompt = f"Actúa como catedrático experto. Usa el PDF decreto_madrid.pdf. Genera una Situación de Aprendizaje LOMLOE para {curso_seleccionado}. Saberes acumulados elegidos: {', '.join(st.session_state['saberes_cesta'])}. Centro de interés: {centro_interes}. Producto esperado: {producto_final}. Duración: {num_sesiones} sesiones. Estructura el documento con justificación, desglose por sesiones (inicio, desarrollo, cierre) adaptado al producto (ej. Pasos para usar Pixton o repaso para examen), criterios reales del PDF y medidas DÚA. Redacta de forma técnica, formal y limpia sin comentarios informales."
                
                envio = [pdf, prompt] if pdf else [prompt]
                response = client.models.generate_content(model='gemini-flash-latest', contents=envio)
                
                if response and response.text:
                    st.success("¡Unidad diseñada con éxito!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.markdown("---")
                    st.download_button(label="📥 Descargar Proyecto (.txt)", data=response.text, file_name="SDA_Planificada.txt", mime="text/plain")
                else:
                    st.error("La IA respondió pero el texto llegó vacío.")
            except Exception as e:
                st.error(f"Error al conectar con la IA de Google: {str(e)}")
