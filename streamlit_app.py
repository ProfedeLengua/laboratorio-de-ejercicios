import streamlit as st

# Configuración de la página de bienvenida
st.set_page_config(page_title="Asistente de Lengua - Inicio", page_icon="🏫", layout="centered")

# Estética y presentación de la Portada
st.title("🏫 Centro de Recursos Didácticos de Lengua")
st.subheader("Plataforma Inteligente para el Profesorado de ESO (Comunidad de Madrid)")
st.markdown("---")

st.write(
    "¡Bienvenido/a al Laboratorio Pedagógico! Esta aplicación multiplataforma está diseñada "
    "para ayudar al profesorado de Secundaria a automatizar y enriquecer su práctica docente "
    "bajo las directrices oficiales del **Decreto 65/2022 de la Comunidad de Madrid**."
)

st.info("👈 Utiliza el menú lateral izquierdo para navegar por las distintas herramientas de la aplicación.")

# Bloques informativos visuales para el profesor
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
