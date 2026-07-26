import streamlit as st

# Director de orquesta con iconos de un solo carácter Unicode minimalista (Sin color)
pagina_inicio = st.Page("pages/0_Inicio.py", title="Inicio", icon="☖", default=True)
pagina_examenes = st.Page("pages/1_Exámenes.py", title="Generador de Exámenes", icon="✍")
pagina_sda = st.Page("pages/2_SDA.py", title="Situaciones de Aprendizaje", icon="☩")
pagina_rubricas = st.Page("pages/3_Rúbricas.py", title="Rúbricas Formativas", icon="⌗")
pagina_talleres = st.Page("pages/4_Talleres.py", title="Taller de Oratoria y Comentario", icon="☡")
pagina_adaptaciones = st.Page("pages/5_Adaptaciones.py", title="Inclusión y DÚA", icon="⚛")
pagina_cuaderno = st.Page("pages/6_Cuaderno.py", title="Cuaderno del Profesor", icon="⚙")

# Inicialización de la barra de navegación segura
navegacion = st.navigation([
    pagina_inicio, 
    pagina_examenes, 
    pagina_sda, 
    pagina_rubricas, 
    pagina_talleres,
    pagina_adaptaciones,
    pagina_cuaderno
])

st.set_page_config(page_title="Asistente de Lengua - Inicio", page_icon="🏫", layout="centered")
navegacion.run()
