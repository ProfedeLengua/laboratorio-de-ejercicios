import streamlit as st
import pandas as pd
import io

st.title("📓 Cuaderno del Profesor con Excel")
st.subheader("Gestión de Aula, Fábrica de Plantillas y Notas LOMLOE")
st.caption("Herramienta integrada para generar tus planillas de evaluación y procesar las medias")

CLAVE_API = st.secrets["gemini_key"]

# -------------------------------------------------------------
# 🌟 SECCIÓN NUEVA: FÁBRICA DE PLANTILLAS EXCEL OFICIALES
# -------------------------------------------------------------
st.markdown("### 🛠️ 1. Fábrica de Plantillas Oficiales de Aula")
st.write("Escribe o pega los nombres de tus alumnos para que la app fabrique tus archivos Excel personalizados:")

nombres_input = st.text_area(
    "Introduce los nombres de tus alumnos (separa cada uno con una coma):",
    value="García López, Alejandro, Martínez Soler, Elena, Sánchez Ruiz, Hugo",
    height=80
)

# Botón para activar el convertidor interno de Excel
if st.button("📦 Fabricar mis Plantillas de Excel"):
    lista_alumnos = [n.strip() for n in nombres_input.split(",") if n.strip()]
    
    if not lista_alumnos:
        st.error("Por favor, introduce al menos el nombre de un alumno.")
    else:
        st.success(f"¡Estructura diseñada con éxito para {len(lista_alumnos)} alumnos!")
        
        # 1. Creamos la estructura exacta del Excel Semanal Diario (0, 5, 10)
        datos_diario = {"Alumno/a": lista_alumnos}
        # Añadimos 6 columnas de ejemplo para que el profesor empiece a anotar días
        for i in range(1, 7):
            datos_diario[f"Clase {i}"] = [10] * len(lista_alumnos) # Rellenamos con 10 por defecto
            
        df_p_diario = pd.DataFrame(datos_diario)
        
        # 2. Creamos la estructura exacta del Excel Trimestral Cuantitativo (90%)
        datos_trimestral = {
            "Alumno/a": lista_alumnos,
            "Parcial 1": [5.0] * len(lista_alumnos),
            "Parcial 2": [5.0] * len(lista_alumnos),
            "Parcial 3": [5.0] * len(lista_alumnos),
            "Trabajo y Esfuerzo": [5.0] * len(lista_alumnos),
            "Examen Final": [5.0] * len(lista_alumnos)
        }
        df_p_trimestral = pd.DataFrame(datos_trimestral)
        
        # Guardamos los archivos en memoria binaria de Streamlit para la descarga
        buffer_diario = io.BytesIO()
        buffer_trimestral = io.BytesIO()
        
        with pd.ExcelWriter(buffer_diario, engine='openpyxl') as writer:
            df_p_diario.to_excel(writer, index=False)
            
        with pd.ExcelWriter(buffer_trimestral, engine='openpyxl') as writer:
            df_p_trimestral.to_excel(writer, index=False)
            
        # Desplegamos los dos botones nativos de descarga inmediata
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.download_button(
                label="📥 Descargar Lista A: Control Diario (.xlsx)",
                data=buffer_diario.getvalue(),
                file_name="Lista_A_Control_Diario.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with col_d2:
            st.download_button(
                label="📥 Descargar Lista B: Exámenes (.xlsx)",
                data=buffer_trimestral.getvalue(),
                file_name="Lista_B_Notas_Examenes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

st.markdown("---")

# -------------------------------------------------------------
# 📊 SECCIÓN DE CALIFICACIÓN (LO QUE YA FUNCIONABA PERFECTO)
# -------------------------------------------------------------
st.markdown("### 🧮 2. Procesador y Evaluador de Actas")
col_g1, col_g2 = st.columns(2)
with col_g1:
    curso = st.selectbox("Curso destinatario:", ["1º de ESO", "2º de ESO", "3º de ESO", "4º de ESO"])
    grupo = st.text_input("Identificador del Grupo:", placeholder="Ej: A, B, C...")
with col_g2:
    peso_parciales = st.slider("Peso total Exámenes Parciales (%):", 10, 80, 40)
    peso_final = st.slider("Peso Examen Final de Evaluación (%):", 10, 80, 50)

if (peso_parciales + peso_final) != 90:
    st.error("⚠️ La suma de parciales y examen final debe ser el 90%. El 10% es el control diario.")

archivo_diario = st.file_uploader("Subir tu Lista A rellenada (.xlsx)", type=["xlsx"])
archivo_trimestral = st.file_uploader("Subir tu Lista B rellenada (.xlsx)", type=["xlsx"])

if archivo_diario and archivo_trimestral:
    try:
        df_diario = pd.read_excel(archivo_diario)
        df_trimestral = pd.read_excel(archivo_trimestral)
        
        st.success(f"¡Planillas de {curso} Grupo {grupo} vinculadas con éxito!")
        
        if st.button("🧮 Procesar Medias Ponderadas Finales"):
            st.markdown(f"### 🏆 Acta de Evaluación Final — {curso} Grupo {grupo}")
            lineas_acta = []
            
            for index, row in df_trimestral.iterrows():
                nombre_alumno = row["Alumno/a"]
                fila_diario = df_diario[df_diario["Alumno/a"] == nombre_alumno]
                
                nota_diario_final = 0.0
                if not fila_diario.empty:
                    columnas_fechas = [col for col in df_diario.columns if col != "Alumno/a"]
                    valores_dias = fila_diario[columnas_fechas].values
                    valores_validos = [float(v) for f_v in [valores_dias] for v in f_v if pd.notna(v)]
                    
                    if valores_validos:
                        nota_diario_final = sum(valores_validos) / len(valores_validos)
                
                media_parciales = (row["Parcial 1"] + row["Parcial 2"] + row["Parcial 3"]) / 3
                nota_cuantitativa = (media_parciales * (peso_parciales / 100)) + (row["Examen Final"] * (peso_final / 100))
                
                nota_final = (nota_diario_final * 0.10) + nota_cuantitativa
                nota_redondeada = round(nota_final, 2)
                estado = "Aprobado" if nota_redondeada >= 5 else "Suspenso"
                
                st.write(f"• **{nombre_alumno}** — Diario Medio: {round(nota_diario_final,2)} | Nota Trimestre: **{nota_redondeada}** ({estado})")
                lineas_acta.append(f"{nombre_alumno};{nota_redondeada};{estado}")
                
            texto_acta = "\n".join(lineas_acta)
            st.download_button(
                label="📥 Descargar Acta de Calificaciones Oficial (.txt)",
                data=texto_acta,
                file_name=f"Acta_Notas_{curso.replace(' ', '')}_{grupo}.txt",
                mime="text/plain"
            )
    except Exception as e:
        st.error(f"Error técnico al procesar las planillas: {str(e)}")
