import streamlit as st
import pandas as pd
from datetime import date
import io
import streamlit_authenticator as stauth

names = ['Heidi Guevara', 'Usuario Demo']
usernames = ['heidi', 'demo']
hashed_passwords = [
    '$2b$12$5fzpyOj0oSjs3Q1RHywOjeYzck/gQ6keP0XZxIpPa.mqFByfRxy5y',  # miclaveSegura1
    '$2b$12$ve4SxNKeP4NEZTTkQuyQruYXG5r9J8.MXHnFA.LTkPvXTSqVnmIUa'   # demopass
]

# Credenciales estructuradas para la versión moderna del paquete
credentials = {
    "usernames": {
        usernames[0]: {
            "name": names[0],
            "password": hashed_passwords[0]
        },
        usernames[1]: {
            "name": names[1],
            "password": hashed_passwords[1]
        }
    }
}

authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="materiales_app",
    key="abcdef",
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login('main')

if authentication_status == False:
    st.error("Usuario/contraseña incorrectos")
if authentication_status == None:
    st.warning("Por favor, ingresa usuario y contraseña")
if authentication_status:
    authenticator.logout("Cerrar sesión", "sidebar")
    st.sidebar.success(f"Bienvenido, {name}")

    st.set_page_config(page_title="Creación de Materiales", layout="wide")

    st.title("📦 Formulario de Creación de Materiales")

    if "materiales" not in st.session_state:
        st.session_state.materiales = []

    with st.form("formulario_materiales"):
        col1, col2 = st.columns(2)

        with col1:
            codigo = st.text_input("Código SAP")
            descripcion = st.text_input("Descripción")
            unidad = st.selectbox("Unidad de Medida", ["KG", "L", "TN", "UND"])
            grupo = st.text_input("Grupo de Artículos")
            almacen = st.text_input("Almacén")

        with col2:
            costo = st.number_input("Costo (S/)", min_value=0.0, step=0.01)
            detraccion = st.radio("¿Aplica Detracción?", ["Sí", "No"])
            usuario = st.text_input("Usuario Solicitante")
            fecha = st.date_input("Fecha de Solicitud", value=date.today())

        submitted = st.form_submit_button("➕ Agregar Material")

        if submitted:
            nuevo_material = {
                "Código SAP": codigo,
                "Descripción": descripcion,
                "Unidad de Medida": unidad,
                "Grupo de Artículos": grupo,
                "Costo": costo,
                "Aplica Detracción": detraccion,
                "Almacén": almacen,
                "Usuario Solicitante": usuario,
                "Fecha de Solicitud": fecha
            }
            st.session_state.materiales.append(nuevo_material)
            st.success("Material agregado correctamente ✅")

    if st.session_state.materiales:
        st.subheader("📋 Materiales Ingresados")
        df = pd.DataFrame(st.session_state.materiales)
        st.dataframe(df, use_container_width=True)

        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

        st.download_button(
            label="📥 Descargar archivo Excel",
            data=output,
            file_name="material_creado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
