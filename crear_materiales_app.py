import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from datetime import date
import io

# Configura la página
st.set_page_config(page_title="Creación de Materiales", layout="wide")

# ========== SECCIÓN DE AUTENTICACIÓN ==========
# Ejemplo de usuarios (puedes cambiar los datos)
names = ['Heidi Guevara', 'Juan Pérez']
usernames = ['heidi', 'juan']
passwords = ['demo123', 'demo456']  # Cambia por contraseñas más seguras

# Genera los hashes solo una vez (en la vida real, NO guardes contraseñas planas)
hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    "materiales_app", "abcdef", cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login('main')

if authentication_status is False:
    st.error("Usuario o contraseña incorrectos.")
elif authentication_status is None:
    st.warning("Por favor, ingresa tus credenciales.")
elif authentication_status:
    authenticator.logout('Cerrar sesión', 'sidebar')
    st.success(f"¡Bienvenido/a, {name}!")

    st.title("📦 Formulario de Creación de Materiales")

    # Sesión para almacenar los datos ingresados
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
            usuario = st.text_input("Usuario Solicitante", value=username)
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

    # Mostrar materiales cargados
    if st.session_state.materiales:
        st.subheader("📋 Materiales Ingresados")
        df = pd.DataFrame(st.session_state.materiales)
        st.dataframe(df, use_container_width=True)

        # Crear archivo en memoria para descargar
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

        # Botón de descarga
        st.download_button(
            label="📥 Descargar archivo Excel",
            data=output,
            file_name="material_creado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
