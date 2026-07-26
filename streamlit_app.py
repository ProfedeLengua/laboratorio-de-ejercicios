import streamlit as st

# Definimos las páginas de la plataforma de forma limpia y directa, sin iconos conflictivos
pagina_inicio = st.Page("pages/0_Inicio.py", title="Inicio", default=True)
pagina_examenes = st.Page("pages/1_Exámenes.py", title="Generador de Exámenes")
pagina_sda = st.Page("pages/2_SDA.py", title="Situaciones de Aprendizaje")
pagina_rubricas = st.Page("pages/3_Rúbricas.py", title="Rúbricas Formativas")
pagina_talleres = st.Page("pages/4_Talleres.py", title="Taller de Oratoria y Comentario")
pagina_adaptaciones = st.Page("pages/5_Adaptaciones.py", title="Inclusión y DÚA")
pagina_cuaderno = st.Page("pages/6_Cuaderno.py", title="Cuaderno del Profesor")

# Inicialización segura de la barra de navegación nativa
navegacion = st.navigation([
    pagina_inicio, 
    pagina_examenes, 
    pagina_sda, 
    pagina_rubricas, 
    pagina_talleres,
    pagina_adaptaciones,
    pagina_cuaderno
])

# Configuración base de la web publicando el título
st.set_page_config(page_title="Asistente de Lengua - Inicio", layout="centered")
navegacion.run()
