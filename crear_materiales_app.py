import streamlit as st
import pandas as pd
import yaml
import streamlit_authenticator as stauth
from datetime import date
import io

# ----------- CARGA CONFIGURACIÓN DESDE YAML ------------
with open('config.yaml') as file:
    config = yaml.safe_load(file)

# ----------- AUTENTICACIÓN -----------
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('main')

if authentication_status is False:
    st.error('Usuario o contraseña incorrectos.')
elif authentication_status is None:
    st.warning('Por favor, ingrese usuario y contraseña.')
elif authentication_status:
    st.set_page_config(page_title="Creación de Materiales", layout="wide")
    st.title("📦 Formulario de Creación de Materiales")

    if "materiales" not in st.session_state:
        st.session_state.materiales = []

    # ----------- PESTAÑAS GLOBALES -----------
    tabs = st.tabs([
        "Solicitante",
        "Gestión de la Calidad",
        "Comercial",
        "Planificación",
        "Producción",
        "Contabilidad"
    ])

    # ----------- PESTAÑA 1: SOLICITANTE -----------
    with tabs[0]:
        st.subheader("Datos del solicitante y del material")
        with st.form("form_solicitante"):
            usuario = st.text_input("Usuario Solicitante", value=name)
            fecha = st.date_input("Fecha de Solicitud", value=date.today())
            correo = st.text_input("Correo electrónico")
            telefono = st.text_input("Teléfono de contacto")

            descripcion = st.text_input("Descripción del material")
            ramo = st.text_input("Ramo (si existe valor en D5, por default 'R')")
            tipo_material = st.selectbox(
                "Tipo de material",
                ["PRODUCTO_TERMINADO", "PRODUCTO_SEMIELABORADO", "SUB_PRODUCTOS_DESECHOS_Y_DESPERDICIOS"]
            )
            codigo_material = st.selectbox(
                "Código de material",
                ["FERT", "HALB", "ZHAL"]
            )
            um_base = st.selectbox(
                "UM_BASE",
                ["BOL", "BOT", "CJ", "CIE", "CIL", "DOC", "GLN", "G", "KG", "LB", "L", "M", "M2", "M3", "MIL", "PAR", "T", "UN"]
            )
            um_valoracion = st.selectbox(
                "UM_VALORACIÓN",
                ["BOL", "BOT", "CJ", "CIE", "CIL", "DOC", "GLN", "G", "KG", "LB", "L", "M", "M2", "M3", "MIL", "PAR", "T", "UN"]
            )
            grupo_articulos = st.text_area("Grupo de artículos")
            costo_kg = st.number_input("Costo (KG)", min_value=0.0, step=0.01)
            costo_un = st.number_input("Costo (UN)", min_value=0.0, step=0.01)
            sector = st.text_input("Sector (por default '10' si D5 tiene valor)")
            jerarquia = st.text_input("Jerarquía de productos")
            grupo_tipo_post = st.text_input("Grupo Tipo Post Gral (por default 'NORM' si D5 tiene valor)")
            dim_ean_bruto = st.text_input("Dimensiones EAN (peso bruto)")
            dim_ean_unidad = st.selectbox(
                "Dimensiones EAN (unidad de peso)",
                ["BOL", "BOT", "CJ", "CIE", "CIL", "DOC", "GLN", "G", "KG", "LB", "L", "M", "M2", "M3", "MIL", "PAR", "T", "UN"]
            )
            dim_ean_neto = st.text_input("Dimensiones EAN (peso neto (kg))")
            grupo_me = st.selectbox(
                "Grupo materiales ME",
                ["Z001-GPO. PALETS", "Z002-GPO. JABAS", "Z003-GPO. BANDEJAS", "Z004-GPO. CAJAS", "Z005-GPO. SACOS", "Z006-GPO. FULL CONTAINER LOAD (FCL)", "Z007-GPO. CARGA SUELTA", "Z008-GPO. LESS THAN CONTAINER LOAD (LCL)"]
            )
            enviado = st.form_submit_button("Guardar solicitud")
            if enviado:
                st.success("Datos guardados.")

    # ----------- RESTO DE PESTAÑAS (Áreas por completar) -----------
    with tabs[1]:
        st.subheader("Gestión de la Calidad")
        st.info("Aquí irán los campos de Gestión de la Calidad (pendientes de definir).")
    with tabs[2]:
        st.subheader("Comercial")
        st.info("Aquí irán los campos del área Comercial (pendientes de definir).")
    with tabs[3]:
        st.subheader("Planificación")
        st.info("Aquí irán los campos del área Planificación (pendientes de definir).")
    with tabs[4]:
        st.subheader("Producción")
        st.info("Aquí irán los campos del área Producción (pendientes de definir).")
    with tabs[5]:
        st.subheader("Contabilidad")
        st.info("Aquí irán los campos del área Contabilidad (pendientes de definir).")

    authenticator.logout("Salir", "sidebar")
