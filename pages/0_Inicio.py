import streamlit as st

st.title("Centro de Recursos Didácticos de Lengua")
st.subheader("Plataforma Inteligente para el Profesorado de ESO")
st.caption("Herramienta de código abierto basada en el Decreto 65/2022")
st.markdown("---")

st.write(
    "¡Sé bienvenido a nuestro Laboratorio Pedagógico! Esta aplicación multiplataforma "
    "está diseñada para automatizar, agilizar y enriquecer tu práctica "
    "docente diaria. Recuerda que es una herramienta de APOYO y nunca un sustituto. "
    "Este centro de recursos utiliza como base el Decreto 65/2022 del BOCM. "
)

st.info("👈 Utiliza el menú lateral izquierdo para navegar por las herramientas.")

st.markdown("### 🛠️ Ecosistema de Herramientas Diseñadas:")

# Distribución equilibrada en dos columnas estéticas
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Generador de Exámenes")
    st.write(
        "Crea textos inéditos y adaptados por la IA en la modalidad que elijas "
        "con actividades de comprensión, léxico, historia de la literatura "
        "y sintaxis acordes al curso. Incluye solucionario detallado."
    )
    
    st.markdown("#### Rúbricas Formativas")
    st.write(
        "Diseña descriptores y matrices de evaluación en formato tabla Markdown con los "
        "criterios oficiales de Madrid. Desglosa los indicadores en 4 niveles "
        "de logro listos para Additio o iDoceo."
    )

with col2:
    st.markdown("#### Situaciones de Aprendizaje")
    st.write(
        "Planifica unidades didácticas a partir de la combinación de "
        "contenidos y saberes básicos de los distintos bloques curriculares "
        "y adaptarlos al producto final que tú elijas."
    )
    
    st.markdown("#### Taller de Oratoria y Comentario")
    st.write(
        "Fabrica guías completas de comentario estilístico o fichas de debate "
        "formal para el aula con argumentos contrapuestos, falacias lógicas "
        "más comunes y léxico formal obligatorio."
    )

st.markdown("---")
st.markdown("#### Módulo de Adaptaciones avanzadas y DÚA")
st.write(
    "Sube cualquier archivo PDF con tus actividades o exámenes originales y "
    "selecciona una situación o diagnóstico (Dislexia, TDAH, Altas Capacidades, Español L2). "
    "La IA rediseñará el material aplicando pautas del Diseño Universal para el "
    "Aprendizaje y redactará la justificación pedagógica para tu memoria."
)

st.markdown("---")
st.caption("Plataforma Escolar de Código Abierto | 100% Gratuita para el Docente")
