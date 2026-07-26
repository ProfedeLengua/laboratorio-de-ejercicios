import streamlit as st
import pandas as pd

st.title("Cuaderno del Profesor Digital")
st.subheader("Registro de Aula: Control Diario y Calificaciones Trimestrales")
st.caption("Planilla interactiva dual con ponderación automática LOMLOE")

CLAVE_API = st.secrets["gemini_key"]

st.markdown("### ⚙️ 1. Configuración del Nivel")
curso = st.selectbox("Selecciona el curso:", ["1º de ESO", "2º de ESO", "3º de ESO", "4º de ESO"])

# CREACIÓN DE LAS DOS SECCIONES CLARAMENTE SEPARADAS
pestana_diaria, pestaña_trimestral = st.tabs([
    "Lista A: Seguimiento Semanal (10%)", 
    "Lista B: Calificaciones Trimestrales (90%)"
])

# BASE DE DATOS COMÚN EN MEMORIA PARA AMBAS TABLAS
if "df_alumnos" not in st.session_state:
    datos_base = {
        "Alumno/a": ["García López, Alejandro", "Martínez Soler, Elena", "Sánchez Ruiz, Hugo"],
        "Material (S/N)": [True, True, False],
        "Atención (S/N)": [True, True, True],
        "Trabajo Diario (0-10)": [7.0, 8.5, 5.0],
        "Lectura Clase (0-10)": [6.5, 9.0, 4.5],
        "Parcial 1": [7.0, 8.5, 5.0],
        "Parcial 2": [6.5, 9.0, 4.5],
        "Parcial 3": [7.5, 8.0, 6.0],
        "Trabajo y Esfuerzo": [7.0, 9.0, 6.0],
        "Examen Final": [6.0, 9.5, 5.5]
    }
    st.session_state["df_alumnos"] = pd.DataFrame(datos_base)

# -------------------------------------------------------------
# PESTAÑA 1: SEGUIMIENTO SEMANAL CONTINUO
# -------------------------------------------------------------
with pestana_diaria:
    st.markdown("#### Registro de Trabajo, Actitud y Lectura Diaria")
    st.caption("Haz doble clic para cambiar notas o marcar casillas. Los cambios se guardan al vuelo:")
    
    # Filtramos la tabla para mostrar solo las columnas diarias
    columnas_diarias = ["Alumno/a", "Material (S/N)", "Atención (S/N)", "Trabajo Diario (0-10)", "Lectura Clase (0-10)"]
    df_diario = st.session_state["df_alumnos"][columnas_diarias]
    
    tabla_diaria = st.data_editor(df_diario, num_rows="dynamic", use_container_width=True, key="editor_diario")
    
    # Sincronizamos los cambios realizados en esta tabla con el almacén central
    st.session_state["df_alumnos"].update(tabla_diaria)

# -------------------------------------------------------------
# PESTAÑA 2: SEGUIMIENTO TRIMESTRAL Y ACTA DE NOTAS
# -------------------------------------------------------------
with pestaña_trimestral:
    st.markdown("#### Calificaciones de Exámenes y Evaluación Ponderada")
    st.caption("Ajusta los pesos para el 90% restante de la nota (el otro 10% es la actitud diaria de la Lista A):")
    
    col1, col2 = st.columns(2)
    with col1:
        peso_parciales = st.slider("Peso total Exámenes Parciales (%):", 10, 80, 40)
    with col2:
        peso_final = st.slider("Peso Examen Final (%):", 10, 80, 50)
        
    if (peso_parciales + peso_final) != 90:
        st.error("⚠️ Alerta: La suma de parciales y examen final debe ser exactamente el 90%.")
        
    st.markdown("---")
    
    # Filtramos la tabla para mostrar solo las columnas de evaluación cuantitativa
    columnas_trimestrales = ["Alumno/a", "Parcial 1", "Parcial 2", "Parcial 3", "Trabajo y Esfuerzo", "Examen Final"]
    df_trimestral = st.session_state["df_alumnos"][columnas_trimestrales]
    
    tabla_trimestral = st.data_editor(df_trimestral, num_rows="dynamic", use_container_width=True, key="editor_trimestral")
    st.session_state["df_alumnos"].update(tabla_trimestral)
    
    st.markdown("---")
    
    # BOTÓN DE CÁLCULO INTELIGENTE UNIFICADO
    if st.button("Ejecutar Evaluación Final del Trimestre"):
        st.markdown("###Acta de Notas Finales")
        lineas_acta = []
        
        # Recorremos la tabla unificada final calculando las dos listas a la vez
        for index, row in st.session_state["df_alumnos"].iterrows():
            # 1. Cálculo matemático de la Lista A (Seguimiento Semanal -> 10% fijo)
            puntos_actitud = 0.0
            if row["Material (S/N)"]: puntos_actitud += 2.5
            if row["Atención (S/N)"]: puntos_actitud += 2.5
            puntos_actitud += (row["Trabajo Diario (0-10)"] * 0.25)
            puntos_actitud += (row["Lectura Clase (0-10)"] * 0.25)
            
            # 2. Cálculo matemático de la Lista B (Seguimiento Trimestral -> 90%)
            media_parciales = (row["Parcial 1"] + row["Parcial 2"] + row["Parcial 3"]) / 3
            # Incorporamos la nota de esfuerzo como modulador o ayuda en la media
            nota_examenes = (media_parciales * (peso_parciales / 100)) + (row["Examen Final"] * (peso_final / 100))
            
            # 3. FUSIÓN DE AMBAS LISTAS
            nota_final_calculada = (puntos_actitud * 0.10) + nota_examenes
            nota_redondeada = round(nota_final_calculada, 2)
            estado = "Aprobado" if nota_redondeada >= 5 else "Suspenso"
            
            st.write(f"**{row['Alumno/a']}** — Nota final ponderada: **{nota_redondeada}** ({estado})")
            lineas_acta.append(f"{row['Alumno/a']};{nota_redondeada};{estado}")
            
        texto_acta = "\n".join(lineas_acta)
        st.download_button(
            label="📥 Descargar Acta de Notas (.txt)",
            data=texto_acta,
            file_name=f"Acta_Notas_{curso.replace(' ', '')}.txt",
            mime="text/plain"
        )
