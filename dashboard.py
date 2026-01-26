import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(page_title="Karma Admin", layout="wide")

# CSS personalizado para mejorar la apariencia
st.markdown("""
    <style>
    .stApp { max-width: 1200px; margin: 0 auto; }
    .stHeading { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("Gestión de Usuarios - Karma")

# Conexión a Google Sheets
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
    gc = gspread.authorize(creds)
    sheet = gc.open(os.getenv("NOMBRE_EXCEL")).sheet1

    # 1. Obtener datos actuales
    data = sheet.get_all_records()
    if data:
        df = pd.DataFrame(data)
        
        st.markdown("### Editor de Registros")
        st.info("Haz doble clic en una celda para editar. Al terminar, pulsa el botón 'Guardar Cambios'.")

        edited_df = st.data_editor(
            df, 
            width="stretch", 
            hide_index=True, 
            num_rows="dynamic" # Permite añadir o borrar filas desde la web
        )
        
        # 3. Botón para sincronizar con Google Sheets
        if st.button('Guardar Cambios en la Nube', use_container_width=True):
            try:
                # 1. Limpiamos la hoja completamente
                sheet.clear()
                
                # 2. Preparamos los datos: Cabeceras + Filas
                cabeceras = edited_df.columns.tolist()
                filas = edited_df.values.tolist()
                
                # Combinamos todo en una sola lista de listas
                cuerpo_completo = [cabeceras] + filas
                
                # 3. Actualizamos la hoja empezando desde la celda A1
                sheet.update('A1', cuerpo_completo)
                
                st.success("¡Base de datos actualizada con éxito!")
                st.balloons() # Un pequeño efecto visual de éxito para tu presentación
                
            except Exception as error_guardado:
                st.error(f"Error al guardar: {error_guardado}")

    else:
        st.info("No hay registros en la base de datos.")

except Exception as e:
    st.error(f"Error de conexión o permisos: {e}")