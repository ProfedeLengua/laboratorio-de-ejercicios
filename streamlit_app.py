import streamlit as st

# Director de orquesta: define los archivos de origen de la plataforma con iconos limpios
pagina_inicio = st.Page("pages/0_🏫_Inicio.py", title="Inicio", icon="school", default=True)
pagina_examenes = st.Page("pages/1_📝_Exámenes.py", title="Generador de Exámenes", icon="edit_document")
pagina_sda = st.Page("pages/2_🧭_SDA.py", title="Situaciones de Aprendizaje", icon="explore")
pagina_rubricas = st.Page("pages/3_📊_Rúbricas.py", title="Rúbricas Formativas", icon="assignment")
pagina_talleres = st.Page("pages/4_🗣️_Talleres.py", title="Taller de Oratoria y Comentario", icon="record_voice_over")
pagina_adaptaciones = st.Page("pages/5_🧠_Adaptaciones.py", title="Inclusión y DÚA", icon="psychology")

# Inicialización segura de la barra de navegación incluyendo todos los módulos
navegacion = st.navigation([
    pagina_inicio, 
    pagina_examenes, 
    pagina_sda, 
    pagina_rubricas, 
    pagina_talleres,
    pagina_adaptaciones
])

# Configuración base de la web
st.set_page_config(page_title="Asistente de Lengua - Inicio", page_icon="🏫", layout="centered")

# Ejecución de la ruta elegida por el profesor en el menú
navegacion.run()
