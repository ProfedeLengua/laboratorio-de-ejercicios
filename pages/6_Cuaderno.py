import streamlit as st
import pandas as pd

st.title("Cuaderno del Profesor Digital")
st.subheader("Registro de Calificaciones y Seguimiento Diario LOMLOE")
st.caption("Planilla interactiva de aula con cálculo automatizado de medias")

# 1. Configuración de los pesos de evaluación según el curso
st.markdown("### ⚙️ 1. Configuración de Ponderaciones")
curso = st.selectbox("Selecciona el curso a gestionar:", ["1º de ESO", "2º de ESO", "3º de ESO", "4º de ESO"])

col1, col2 = st.columns(2)
with col1:
    peso_parciales = st.slider("Peso total Exámenes Parciales (%):", 10, 80, 40)
    peso_final = st.slider("Peso Examen Final de Evaluación (%):", 10, 80, 40)
with col2:
    peso_diario = st.slider("Peso Seguimiento y Trabajo Diario (%):", 0, 50, 20)

if (peso_parciales + peso_final + peso_diario) != 100:
    st.warning("⚠️ Alerta: La suma de los porcentajes debe ser exactamente 100%.")

# 2. Creación de la base de datos interactiva en memoria de la web
st.markdown("### 📊 2. Planilla de Calificaciones y Actitud")
st.caption("Haz doble clic en cualquier celda para rellenar datos o marcar casillas de seguimiento:")

# Estructura base de la tabla con alumnos de ejemplo
datos_iniciales = {
    "Alumno/a": ["García López, Alejandro", "Martínez Soler, Elena", "Sánchez Ruiz, Hugo"],
    "Parcial 1": [7.0, 8.5, 5.0],
    "Parcial 2": [6.5, 9.0, 4.5],
    "Parcial 3": [7.5, 8.0, 6.0],
    "Examen Final": [6.0, 9.5, 5.5],
    "Trae Material": [True, True, False],
    "Atención Clase": [True, True, True],
    "Trabajo Diario": [True, True, False]
}

df = pd.DataFrame(datos_iniciales)

# 🌟 LA MAGIA DE STREAMLIT: Convierte el mapa en un Excel editable en vivo
tabla_editable = st.data_editor(
    df,
    num_rows="dynamic", # Permite al profesor añadir o borrar filas de alumnos con un botón
    use_container_width=True
)

# 3. Cálculo matemático automatizado de las notas finales al vuelo
if st.button("🧮 Calcular Notas Finales de la Evaluación"):
    st.markdown("### 🏆 Acta de Calificaciones Finales")
    
    lineas_acta = []
    for index, row in tabla_editable.iterrows():
        # Media de los tres parciales
        media_parciales = (row["Parcial 1"] + row["Parcial 2"] + row["Parcial 3"]) / 3
        
        # Nota del trabajo diario basada en las casillas marcadas
        puntos_actitud = 0
        if row["Trae Material"]: puntos_actitud += 3.3
        if row["Atención Clase"]: puntos_actitud += 3.3
        if row["Trabajo Diario"]: puntos_actitud += 3.4
        
        # Fórmula matemática ponderada
        nota_final_calculada = (
            (media_parciales * (peso_parciales / 100)) +
            (row["Examen Final"] * (peso_final / 100)) +
            (puntos_actitud * (peso_diario / 100))
        )
        
        nota_redondeada = round(nota_final_calculada, 2)
        estado = "Aprobado" if nota_redondeada >= 5 else "Suspenso"
        
        st.write(f"**{row['Alumno/a']}** — Nota Final: **{nota_redondeada}** ({estado})")
        lineas_acta.append(f"{row['Alumno/a']};{nota_redondeada};{estado}")
    
    # Botón para exportar los datos limpios a un archivo de texto o Excel
    texto_acta = "\n".join(lineas_acta)
    st.download_button(
        label="📥 Descargar Acta de Notas (.txt)",
        data=texto_acta,
        file_name=f"Notas_Finales_{curso.replace(' ', '')}.txt",
        mime="text/plain"
    )
