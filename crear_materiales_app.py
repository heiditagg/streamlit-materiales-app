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

        # Defaults según descripción
        descripcion = ""
        ramo_default = ""
        sector_default = ""
        grupo_tipo_post_default = ""

        # PRIMERA FILA (Usuario, UM_VALORACIÓN)
        col1, col2 = st.columns(2)
        usuario = col1.text_input("Usuario Solicitante")
        um_valoracion = col2.selectbox(
            "UM_VALORACIÓN",
            ["BOL", "BOT", "CJ", "CIE", "CIL", "DOC", "GLN", "G", "KG", "LB", "L", "M", "M2", "M3", "MIL", "PAR", "T", "UN"]
        )

        # SEGUNDA FILA (Fecha, Código material)
        col1, col2 = st.columns(2)
        fecha = col1.date_input("Fecha de Solicitud", value=date.today())
        codigo_material = col2.selectbox(
            "Código de material",
            ["FERT", "HALB", "ZHAL"]
        )

        # TERCERA FILA (Correo, Tipo material)
        col1, col2 = st.columns(2)
        correo = col1.text_input("Correo electrónico")
        tipo_material = col2.selectbox(
            "Tipo de material",
            ["PRODUCTO_TERMINADO", "PRODUCTO_SEMIELABORADO", "SUB_PRODUCTOS_DESECHOS_Y_DESPERDICIOS"]
        )

        # CUARTA FILA (Descripción, UM_BASE)
        col1, col2 = st.columns(2)
        descripcion = col1.text_input("Descripción del material")
        um_base = col2.selectbox(
            "UM_BASE",
            ["BOL", "BOT", "CJ", "CIE", "CIL", "DOC", "GLN", "G", "KG", "LB", "L", "M", "M2", "M3", "MIL", "PAR", "T", "UN"]
        )

        # Lógica de defaults, recalculada si hay descripción
        if descripcion:
            ramo_default = "R"
            sector_default = "10"
            grupo_tipo_post_default = "NORM"
        else:
            ramo_default = ""
            sector_default = ""
            grupo_tipo_post_default = ""

        # QUINTA FILA (Ramo, Sector)
        col1, col2 = st.columns(2)
        ramo = col1.text_input("Ramo (por default 'R' si 'Descripción del material' tiene valor)", value=ramo_default)
        sector = col2.text_input("Sector (por default '10' si 'Descripción del material' tiene valores)", value=sector_default)

        # SEXTA FILA (Grupo Tipo Post, Jerarquía)
        col1, col2 = st.columns(2)
        grupo_tipo_post = col1.text_input("Grupo Tipo Post Gral (por default 'NORM' si 'Descripción del material' tiene valor)", value=grupo_tipo_post_default)
        jerarquia = col2.text_input("Jerarquía de productos")

        # SÉPTIMA FILA (Dimensiones EAN bruto, Dimensiones EAN unidad)
        col1, col2 = st.columns(2)
        dim_ean_bruto = col1.text_input("Dimensiones EAN (peso bruto)")
        dim_ean_unidad = col2.selectbox(
            "Dimensiones EAN (unidad de peso)",
            ["BOL", "BOT", "CJ", "CIE", "CIL", "DOC", "GLN", "G", "KG", "LB", "L", "M", "M2", "M3", "MIL", "PAR", "T", "UN"]
        )

        # OCTAVA FILA (Dimensiones EAN neto, Grupo materiales ME)
        col1, col2 = st.columns(2)
        dim_ean_neto = col1.text_input("Dimensiones EAN (peso neto (kg))")
        grupo_me = col2.selectbox(
            "Grupo materiales ME",
            ["Z001-GPO. PALETS", "Z002-GPO. JABAS", "Z003-GPO. BANDEJAS", "Z004-GPO. CAJAS", "Z005-GPO. SACOS", "Z006-GPO. FULL CONTAINER LOAD (FCL)", "Z007-GPO. CARGA SUELTA", "Z008-GPO. LESS THAN CONTAINER LOAD (LCL)"]
        )

        # NOVENA FILA (Grupo artículos, Costo (KG))
        col1, col2 = st.columns(2)
        grupo_articulos = col1.text_area("Grupo de artículos")
        costo_kg = col2.number_input("Costo (KG)", min_value=0.0, step=0.01)

        # DÉCIMA FILA (Costo (UN), vacío)
        col1, col2 = st.columns(2)
        costo_un = col1.number_input("Costo (UN)", min_value=0.0, step=0.01)
        # col2 vacío para mantener estructura

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
