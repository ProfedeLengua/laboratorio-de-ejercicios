import streamlit as st

# Director de orquesta: define los archivos de origen de la plataforma
pagina_inicio = st.Page("pages/0_🏫_Inicio.py", title="Inicio", icon="🏫", default=True)
pagina_examenes = st.Page("pages/1_📝_Exámenes.py", title="Generador de Exámenes", icon="📝")
pagina_sda = st.Page("pages/2_🧭_SDA.py", title="Situaciones de Aprendizaje", icon="🧭")

# Inicialización segura de la barra de navegación incluyendo el nuevo módulo
navegacion = st.navigation([pagina_inicio, pagina_examenes, pagina_sda])

# Configuración base de la web
st.set_page_config(page_title="Asistente de Lengua - Inicio", page_icon="🏫", layout="centered")

# Ejecución de la ruta elegida por el profesor en el menú
navegacion.run()
