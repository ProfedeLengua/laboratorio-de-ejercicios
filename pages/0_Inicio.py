import streamlit as st

# Cargamos la imagen de Wikimedia sin parámetros de ancho complejos para evitar bloqueos del servidor
st.image("https://wikimedia.org")

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

st.markdown("### Ecosistema de Herramientas Diseñadas:")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Generador de Exámenes")
    st.write(
        "Crea textos con IA en la modalidad que elijas, para el curso que quieras, "
        "con actividades de comprensión, léxico, historia de la literatura, "
        "morfología y sintaxis. Incluye solucionario detallado."
    )
    
    st.markdown("#### Rúbricas y Descriptores")
    st.write(
        "Diseña descriptores y rúbricas de evaluación con los "
        "criterios oficiales de Madrid. Desglosa los indicadores en 4 niveles "
        "de logro listos para Additio o iDoceo."
    )
    
    st.markdown("#### Módulo de Adaptación y DÚA")
    st.write(
        "Sube cualquier archivo PDF con tus actividades o exámenes originales. "
        "La IA rediseñará el material aplicando pautas DÚA según el diagnóstico "
        "elegido y redactará la justificación pedagógica."
    )

with col2:
    st.markdown("#### Situaciones de Aprendizaje")
    st.write(
        "Planifica unidades didácticas a partir de la combinación de contenidos "
        "y saberes básicos de los distintos bloques curriculares "
        "y adaptarlos al producto final que tú elijas."
    )
    
    st.markdown("#### Taller de Oratoria y Comentario de texto")
    st.write(
        "Fabrica guías completas de comentario estilístico o fichas de debate "
        "formal para el aula con argumentos contrapuestos, falacias lógicas "
        "más comunes y léxico formal obligatorio."
    )
    
    # EL NUEVO APARTADO EN LA PORTADA
    st.markdown("#### Cuaderno digital del Profesor")
    st.write(
        "Diseña tus listas y planillas de registro de aula dividida en control diario "
        "continuo (actitud, material, lectura) y calificaciones trimestrales "
        "de exámenes, con cálculo automatizado de medias ponderadas LOMLOE."
    )

st.markdown("---")
st.caption("Plataforma Escolar de Código Abierto | 100% Gratuita para el Docente")
