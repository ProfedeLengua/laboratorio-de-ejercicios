import streamlit as st

# 🌟 DIRECTOR DE ORQUESTA: Definimos las rutas reales separadas para evitar el bucle infinito
pagina_inicio = st.Page("pages/0_🏫_Inicio.py", title="Inicio", icon="🏫", default=True)
pagina_examenes = st.Page("pages/1_📝_Exámenes.py", title="Generador de Exámenes", icon="📝")

# Inicializamos el menú de navegación con la lista de herramientas
navegacion = st.navigation([pagina_inicio, pagina_examenes])

# Ejecutamos la navegación segura
navegacion.run()
go abierto | 100% Gratuita")
