import streamlit as st
import pandas as pd

st.title("📓 Cuaderno del Profesor con Excel")
st.subheader("Importación Dinámica y Calificación Automatizada LOMLOE")
st.caption("Cálculo ponderado basado en tu escala diaria: 0 (nada), 5 (regular) y 10 (perfecto)")

CLAVE_API = st.secrets["gemini_key"]

# 1. Configuración de parámetros de grupo y evaluación
st.markdown("### 🎛️ 1. Configuración del Grupo y Criterios")
col_g1, col_g2 = st.columns(2)
with col_g1:
    curso = st.selectbox("Curso destinatario:", ["1º de ESO", "2º de ESO", "3º de ESO", "4º de ESO"])
    grupo = st.text_input("Identificador del Grupo:", placeholder="Ej: A, B, C, Diver...")
with col_g2:
    peso_parciales = st.slider("Peso total Exámenes Parciales (%):", 10, 80, 40)
    peso_final = st.slider("Peso Examen Final de Evaluación (%):", 10, 80, 50)

if (peso_parciales + peso_final) != 90:
    st.error("⚠️ La suma de parciales y examen final debe ser exactamente el 90%. El 10% restante es el control diario.")

st.markdown("---")

# 2. Entrada de archivos Excel vivos del profesor
st.markdown("### 📊 2. Carga de Planillas de Evaluación")
st.caption("Arrastra los dos archivos Excel independientes desde tu ordenador:")

archivo_diario = st.file_uploader("Subir Lista A: Seguimiento Diario Semanal (.xlsx)", type=["xlsx"])
archivo_trimestral = st.file_uploader("Subir Lista B: Notas de Exámenes (.xlsx)", type=["xlsx"])

# 3. Procesamiento matemático de las listas en paralelo
if archivo_diario and archivo_trimestral:
    try:
        # Leemos los Excels usando la librería pandas
        df_diario = pd.read_excel(archivo_diario)
        df_trimestral = pd.read_excel(archivo_trimestral)
        
        st.success(f"¡Archivos de {curso} {grupo} cargados y vinculados correctamente!")
        
        # Mostramos las dos pestañas para que el profesor verifique los datos subidos
        tab_v1, tab_v2 = st.tabs(["📋 Vista Control Diario (0-5-10)", "🏆 Vista Calificaciones"])
        
        with tab_v1:
            st.dataframe(df_diario, use_container_width=True)
        with tab_v2:
            st.dataframe(df_trimestral, use_container_width=True)
            
        st.markdown("---")
        
        # 🧮 BOTÓN DE PROCESAMIENTO MATEMÁTICO AVANZADO
        if st.button("🧮 Procesar Medias Ponderadas Finales"):
            st.markdown(f"### 🏆 Acta de Evaluación Final — {curso} Grupo {grupo}")
            lineas_acta = []
            
            # Recorremos la lista de alumnos basándonos en la planilla trimestral
            for index, row in df_trimestral.iterrows():
                nombre_alumno = row["Alumno/a"]
                
                # 🌟 TRATAMIENTO L LISTA A (DIARIO): Buscamos al alumno en el Excel semanal
                fila_diario = df_diario[df_diario["Alumno/a"] == nombre_alumno]
                
                nota_diario_final = 0.0
                if not fila_diario.empty:
                    # Extraemos todas las columnas que no sean el nombre del alumno (es decir, los días de clase)
                    columnas_fechas = [col for col in df_diario.columns if col != "Alumno/a"]
                    valores_dias = fila_diario[columnas_fechas].values[0]
                    
                    # Convertimos los datos a números y filtramos celdas vacías
                    valores_validos = [float(v) for f_v in [valores_dias] for v in f_v if pd.notna(v)]
                    
                    if valores_validos:
                        # Calculamos la media de todos los 0, 5 y 10 anotados en el trimestre
                        nota_diario_final = sum(valores_validos) / len(valores_validos)
                
                # 🌟 TRATAMIENTO DE LISTA B (EXÁMENES -> 90%)
                media_parciales = (row["Parcial 1"] + row["Parcial 2"] + row["Parcial 3"]) / 3
                nota_cuantitativa = (media_parciales * (peso_parciales / 100)) + (row["Examen Final"] * (peso_final / 100))
                
                # 🌟 FUSIÓN MATEMÁTICA DEFINITIVA (10% Diario + 90% Exámenes)
                nota_final = (nota_diario_final * 0.10) + nota_cuantitativa
                nota_redondeada = round(nota_final, 2)
                estado = "Aprobado" if nota_redondeada >= 5 else "Suspenso"
                
                st.write(f"• **{nombre_alumno}** — Control Diario Medio: {round(nota_diario_final,2)} | Nota Final Trimestre: **{nota_redondeada}** ({estado})")
                lineas_acta.append(f"{nombre_alumno};{nota_redondeada};{estado}")
                
            texto_acta = "\n".join(lineas_acta)
            st.download_button(
                label="📥 Descargar Acta de Calificaciones Oficial (.txt)",
                data=texto_acta,
                file_name=f"Acta_Notas_{curso.replace(' ', '')}_{grupo}.txt",
                mime="text/plain"
            )
            
    except Exception as e:
        st.error(f"Error técnico al leer las columnas de los Excels: {str(e)}")
        st.info("Asegúrate de que ambos Excels tengan una columna llamada exactamente 'Alumno/a' en la primera celda.")
else:
    st.info("Por favor, sube los dos archivos Excel de tu grupo para desbloquear el procesador de actas.")
