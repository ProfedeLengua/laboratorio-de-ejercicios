import streamlit as st

# 🌟 NUEVA DIRECTRIZ EXPLICITA DE NAVEGACIÓN (Evita el bloqueo del menú lateral)
# Definimos los archivos reales que componen nuestra plataforma escolar
pagina_inicio = st.Page("streamlit_app.py", title="Inicio", icon="🏫", default=True)
pagina_examenes = st.Page("pages/1_📝_Exámenes.py", title="Generador de Exámenes", icon="📝")

# Inicializamos el menú de navegación nativo de Streamlit
navegacion = st.navigation([pagina_inicio, pagina_examenes])

# Configuración de la pantalla de bienvenida
st.set_page_config(page_title="Asistente de Lengua - Inicio", page_icon="🏫", layout="centered")

# Ejecutamos la navegación para que pinte la página correspondiente
navegacion.run()

# 🎨 TODO EL DISEÑO DE TU PORTADA VISUAL DE BIENVENIDA:
st.title("🏫 Centro de Recursos Didácticos de Lengua")
st.subheader("Plataforma Inteligente para el Profesorado de ESO (Comunidad de Madrid)")
st.markdown("---")

st.write(
    "¡Bienvenido/a al Laboratorio Pedagógico! Esta aplicación multiplataforma está diseñada "
    "para ayudar al profesorado de Secundaria a automatizar y enriquecer su práctica docente "
    "under las directrices oficiales del **Decreto 65/2022 de la Comunidad de Madrid**."
)

st.info("👈 Utiliza el menú lateral izquierdo para navegar por las distintas herramientas de la aplicación.")

st.markdown("### 🛠️ Herramientas Disponibles:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📝 Generador de Exámenes")
    st.write(
        "Crea textos inéditos adaptados por la IA en la modalidad que elijas "
        "con actividades de comprensión, léxico, historia de la literatura y sintaxis "
        "acordes al curso (1º-4º ESO). Incluye solucionario para el docente."
    )
    
    st.markdown("#### 📊 Rúbricas Formativas")
    st.write(
        "Diseña matrices de evaluación en formato tabla ponderadas con los criterios "
        "oficiales de Madrid. Niveles de logro totalmente editables y listos para usar."
    )

with col2:
    st.markdown("#### 🧭 Situaciones de Aprendizaje")
    st.write(
        "Planifica secuencias didácticas completas por proyectos (LOMLOE). "
        "Estructuradas en sesiones, con justificación, principios DÚA y asignación "
        "de Competencias Específicas."
    )
    
    st.markdown("#### 📚 Saberes Básicos Madrid")
    st.write(
        "Consulta rápida de los bloques de contenido normativos para agilizar "
        "la redacción de tus memorias de departamento."
    )

st.markdown("---")
st.caption("Herramienta pedagógica de código abierto | 100% Gratuita")
