import streamlit as st
import pandas as pd
from datetime import date
import io

st.set_page_config(page_title="Creación de Materiales", layout="wide")
st.title("📦 Formulario de Creación de Materiales")

if "materiales" not in st.session_state:
    st.session_state.materiales = []

# --------- CSS PARA MARCAR CAMPOS EN ROJO ---------
st.markdown("""
    <style>
    .field-required label {
        color: red !important;
    }
    .field-required input, .field-required textarea, .field-required select {
        border: 2px solid red !important;
        background: #fff0f0 !important;
    }
    </style>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "Solicitante",
    "Gestión de la Calidad",
    "Comercial",
    "Planificación",
    "Producción",
    "Contabilidad"
])

with tabs[0]:
    st.subheader("Datos del solicitante y del material")
    with st.form("form_solicitante"):
        # Variables y recolección de inputs (guardamos refs para CSS)
        fields = {}

        # 1
        col1, col2 = st.columns(2)
        with col1:
            fields['Usuario Solicitante'] = st.text_input("Usuario Solicitante", key="usuario")
        with col2:
            fields['UM_VALORACIÓN'] = st.selectbox(
                "UM_VALORACIÓN",
                ["", "BOL", "BOT", "CJ", "CIE", "CIL", "DOC", "GLN", "G", "KG", "LB", "L", "M", "M2", "M3", "MIL", "PAR", "T", "UN"],
                key="um_valoracion"
            )
        # 2
        col1, col2 = st.columns(2)
        with col1:
            fields['Fecha de Solicitud'] = st.date_input("Fecha de Solicitud", value=date.today(), key="fecha")
        with col2:
            fields['Código de material'] = st.selectbox(
                "Código de material",
                ["", "FERT", "HALB", "ZHAL"], key="codigo_material"
            )
        # 3
        col1, col2 = st.columns(2)
        with col1:
            fields['Correo electrónico'] = st.text_input("Correo electrónico", key="correo")
        with col2:
            fields['Tipo de material'] = st.selectbox(
                "Tipo de material",
                ["", "PRODUCTO_TERMINADO", "PRODUCTO_SEMIELABORADO", "SUB_PRODUCTOS_DESECHOS_Y_DESPERDICIOS"], key="tipo_material"
            )
        # 4
        col1, col2 = st.columns(2)
        with col1:
            fields['Descripción del material'] = st.text_input("Descripción del material", key="descripcion")
        with col2:
            fields['UM_BASE'] = st.selectbox(
                "UM_BASE",
                ["", "BOL", "BOT", "CJ", "CIE", "CIL", "DOC", "GLN", "G", "KG", "LB", "L", "M", "M2", "M3", "MIL", "PAR", "T", "UN"], key="um_base"
            )
        # Defaults por descripción
        descripcion_val = fields['Descripción del material']
        if descripcion_val:
            ramo_default = "R"
            sector_default = "10"
            grupo_tipo_post_default = "NORM"
        else:
            ramo_default = ""
            sector_default = ""
            grupo_tipo_post_default = ""
        # 5
        col1, col2 = st.columns(2)
        with col1:
            fields['Ramo'] = st.text_input(
                "Ramo (por default 'R' si 'Descripción del material' tiene valor)",
                value=ramo_default, key="ramo"
            )
        with col2:
            fields['Sector'] = st.text_input(
                "Sector (por default '10' si 'Descripción del material' tiene valores)",
                value=sector_default, key="sector"
            )
        # 6
        col1, col2 = st.columns(2)
        with col1:
            fields['Grupo Tipo Post Gral'] = st.text_input(
                "Grupo Tipo Post Gral (por default 'NORM' si 'Descripción del material' tiene valor)",
                value=grupo_tipo_post_default, key="grupo_tipo_post"
            )
        with col2:
            fields['Jerarquía de productos'] = st.text_input("Jerarquía de productos", key="jerarquia")
        # 7
        col1, col2 = st.columns(2)
        with col1:
            fields['Dimensiones EAN (peso bruto)'] = st.text_input("Dimensiones EAN (peso bruto)", key="dim_ean_bruto")
        with col2:
            fields['Dimensiones EAN (unidad de peso)'] = st.selectbox(
                "Dimensiones EAN (unidad de peso)",
                ["", "BOL", "BOT", "CJ", "CIE", "CIL", "DOC", "GLN", "G", "KG", "LB", "L", "M", "M2", "M3", "MIL", "PAR", "T", "UN"],
                key="dim_ean_unidad"
            )
        # 8
        col1, col2 = st.columns(2)
        with col1:
            fields['Dimensiones EAN (peso neto (kg))'] = st.text_input("Dimensiones EAN (peso neto (kg))", key="dim_ean_neto")
        with col2:
            fields['Grupo materiales ME'] = st.selectbox(
                "Grupo materiales ME",
                ["", "Z001-GPO. PALETS", "Z002-GPO. JABAS", "Z003-GPO. BANDEJAS", "Z004-GPO. CAJAS", "Z005-GPO. SACOS", "Z006-GPO. FULL CONTAINER LOAD (FCL)", "Z007-GPO. CARGA SUELTA", "Z008-GPO. LESS THAN CONTAINER LOAD (LCL)"],
                key="grupo_me"
            )
        # 9
        col1, col2 = st.columns(2)
        with col1:
            fields['Grupo de artículos'] = st.text_area("Grupo de artículos", key="grupo_articulos")
        with col2:
            fields['Costo (KG)'] = st.number_input("Costo (KG)", min_value=0.0, step=0.01, key="costo_kg")
        # 10
        col1, col2 = st.columns(2)
        with col1:
            fields['Costo (UN)'] = st.number_input("Costo (UN)", min_value=0.0, step=0.01, key="costo_un")

        enviado = st.form_submit_button("Guardar solicitud")

        # Validación de campos
        faltantes = [k for k, v in fields.items() if (not v or (isinstance(v, str) and v.strip() == ""))]
        # Costo KG y UN deben ser > 0
        if fields["Costo (KG)"] == 0:
            faltantes.append("Costo (KG)")
        if fields["Costo (UN)"] == 0:
            faltantes.append("Costo (UN)")

        # Aplica CSS a los inputs que faltan
        if enviado and faltantes:
            st.warning("Favor complete todos los campos.")
            # JavaScript/CSS hack para marcar los campos
            st.markdown(
                f"""
                <script>
                const fields = {faltantes};
                fields.forEach(function(label) {{
                    let els = Array.from(document.querySelectorAll('label')).filter(el => el.innerText.includes(label));
                    els.forEach(el => el.parentElement.classList.add('field-required'));
                }});
                </script>
                """,
                unsafe_allow_html=True
            )
        elif enviado:
            st.session_state.materiales.append({
                k: v for k, v in fields.items()
            })
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
