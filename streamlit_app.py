import streamlit as st

# Director de orquesta con iconos nativos estándar compatibles al 100%
pagina_inicio = st.Page("pages/0_Inicio.py", title="Inicio", icon=":material/school:", default=True)
pagina_examenes = st.Page("pages/1_Exámenes.py", title="Generador de Exámenes", icon=":material/edit_document:")
pagina_sda = st.Page("pages/2_SDA.py", title="Situaciones de Aprendizaje", icon=":material/explore:")
pagina_rubricas = st.Page("pages/3_Rúbricas.py", title="Rúbricas Formativas", icon=":material/assignment:")
pagina_talleres = st.Page("pages/4_Talleres.py", title="Taller de Oratoria y Comentario", icon=":material/record_voice_over:")
pagina_adaptaciones = st.Page("pages/5_Adaptaciones.py", title="Inclusión y DÚA", icon=":material/psychology:")
pagina_cuaderno = st.Page("pages/6_Cuaderno.py", title="Cuaderno del Profesor", icon=":material/menu_book:")

# Inicialización segura de la barra de navegación
navegacion = st.navigation([
    pagina_inicio, 
    pagina_examenes, 
    pagina_sda, 
    pagina_rubricas, 
    pagina_talleres,
    pagina_adaptaciones,
    pagina_cuaderno
])

st.set_page_config(page_title="Asistente de Lengua - Inicio", layout="centered")
navegacion.run()
