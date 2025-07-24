import streamlit as st
import pandas as pd
from datetime import date
import io

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
        col1, col2 = st.columns(2)
        
        with col1:
            usuario = st.text_input("Usuario Solicitante")
            fecha = st.date_input("Fecha de Solicitud", value=date.today())
            correo = st.text_input("Correo electrónico")
            descripcion = st.text_input("Descripción del material")
        with col2:
            um_valoracion = st.selectbox(
                "UM_VALORACIÓN",
                ["BOL", "BOT", "CJ", "CIE", "CIL", "DOC", "GLN", "G", "KG", "LB", "L", "M", "M2", "M3", "MIL", "PAR", "T", "UN"]
            )

        # Lógica para valores por default según "descripcion"
        if descripcion:
            ramo_default = "R"
            sector_default = "10"
            grupo_tipo_post_default = "NORM"
        else:
            ramo_default = ""
            sector_default = ""
            grupo_tipo_post_default = ""

        col1, col2 = st.columns(2)
        with col1:
            ramo = st.text_input("Ramo (por default 'R' si 'Descripción del material' tiene valor)", value=ramo_default)
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
            grupo_articulos = st.text_area("Grupo de artículos")
            costo_kg = st.number_input("Costo (KG)", min_value=0.0, step=0.01)
            costo_un = st.number_input("Costo (UN)", min_value=0.0, step=0.01)
        with col2:
            sector = st.text_input("Sector (por default '10' si 'Descripción del material' tiene valores)", value=sector_default)
            jerarquia = st.text_input("Jerarquía de productos")
            grupo_tipo_post = st.text_input("Grupo Tipo Post Gral (por default 'NORM' si 'Descripción del material' tiene valor)", value=grupo_tipo_post_default)
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
            nuevo_material = {
                "Usuario": usuario,
                "Fecha": fecha,
                "Correo": correo,
                "Descripción": descripcion,
                "Ramo": ramo,
                "Tipo material": tipo_material,
                "Código material": codigo_material,
                "UM Base": um_base,
                "UM Valoración": um_valoracion,
                "Grupo Artículos": grupo_articulos,
                "Costo (KG)": costo_kg,
                "Costo (UN)": costo_un,
                "Sector": sector,
                "Jerarquía": jerarquia,
                "Grupo tipo post": grupo_tipo_post,
                "Dim EAN bruto": dim_ean_bruto,
                "Dim EAN unidad": dim_ean_unidad,
                "Dim EAN neto": dim_ean_neto,
                "Grupo ME": grupo_me,
            }
            st.session_state.materiales.append(nuevo_material)
            st.success("Datos guardados.")

# ----------- RESTO DE PESTAÑAS (Áreas por completar) -----------
for i, label in enumerate([
    "Gestión de la Calidad",
    "Comercial",
    "Planificación",
    "Producción",
    "Contabilidad"
], start=1):
    with tabs[i]:
        st.subheader(label)
        st.info(f"Aquí irán los campos del área {label} (pendientes de definir).")

# ----------- MOSTRAR Y DESCARGAR TABLA -----------
if st.session_state.materiales:
    st.subheader("📋 Solicitudes Registradas")
    df = pd.DataFrame(st.session_state.materiales)
    st.dataframe(df, use_container_width=True)
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    st.download_button(
        label="📥 Descargar archivo Excel",
        data=output,
        file_name="solicitudes_materiales.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
