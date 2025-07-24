import streamlit as st
import pandas as pd
from datetime import date
import io

st.set_page_config(page_title="Creación de Materiales", layout="wide")
st.title("📦 Formulario de Creación de Materiales")

if "materiales" not in st.session_state:
    st.session_state.materiales = []

# CSS para visualización de campos
st.markdown("""
    <style>
    .field-filled input, .field-filled textarea, .field-filled select {
        background-color: #e8f1fc !important;
        border: 1.5px solid #e8f1fc !important;
    }
    .field-empty input, .field-empty textarea, .field-empty select {
        background-color: #f5f6fa !important;
        border: 1.5px solid #f5f6fa !important;
    }
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
    with st.form("form_solicitante", clear_on_submit=False):

        # Inicializar fecha sólo si no está ya en session_state
        if "fecha" not in st.session_state:
            st.session_state["fecha"] = date.today()

        # Defaults automáticos según descripción
        if st.session_state.get("descripcion"):
            if not st.session_state.get("ramo"): st.session_state["ramo"] = "R"
            if not st.session_state.get("sector"): st.session_state["sector"] = "10"
            if not st.session_state.get("grupo_tipo_post"): st.session_state["grupo_tipo_post"] = "NORM"

        fields = {}
        # ---- Fila 1
        col1, col2 = st.columns(2)
        with col1:
            fields['Usuario Solicitante'] = st.text_input("Usuario Solicitante", key="usuario")
        with col2:
            fields['UM_VALORACIÓN'] = st.selectbox(
                "UM_VALORACIÓN",
                ["", "BOL", "BOT", "CJ", "CIE", "CIL", "DOC", "GLN", "G", "KG", "LB", "L", "M", "M2", "M3", "MIL", "PAR", "T", "UN"],
                key="um_valoracion"
            )
        # ---- Fila 2
        col1, col2 = st.columns(2)
        with col1:
            fields['Fecha de Solicitud'] = st.date_input("Fecha de Solicitud", key="fecha")
        with col2:
            fields['Código de material'] = st.selectbox(
                "Código de material",
                ["", "FERT", "HALB", "ZHAL"], key="codigo_material"
            )
        # ---- Fila 3
        col1, col2 = st.columns(2)
        with col1:
            fields['Correo electrónico'] = st.text_input("Correo electrónico", key="correo")
        with col2:
            fields['Tipo de material'] = st.selectbox(
                "Tipo de material",
                ["", "PRODUCTO_TERMINADO", "PRODUCTO_SEMIELABORADO", "SUB_PRODUCTOS_DESECHOS_Y_DESPERDICIOS"], key="tipo_material"
            )
        # ---- Fila 4
        col1, col2 = st.columns(2)
        with col1:
            fields['Descripción del material'] = st.text_input("Descripción del material", key="descripcion")
        with col2:
            fields['UM_BASE'] = st.selectbox(
                "UM_BASE",
                ["", "BOL", "BOT", "CJ", "CIE", "CIL", "DOC", "GLN", "G", "KG", "LB", "L", "M", "M2", "M3", "MIL", "PAR", "T", "UN"], key="um_base"
            )
        # ---- Fila 5
        col1, col2 = st.columns(2)
        with col1:
            fields['Ramo'] = st.text_input(
                "Ramo (por default 'R' si 'Descripción del material' tiene valor)",
                key="ramo"
            )
        with col2:
            fields['Sector'] = st.text_input(
                "Sector (por default '10' si 'Descripción del material' tiene valores)",
                key="sector"
            )
        # ---- Fila 6
        col1, col2 = st.columns(2)
        with col1:
            fields['Grupo Tipo Post Gral'] = st.text_input(
                "Grupo Tipo Post Gral (por default 'NORM' si 'Descripción del material' tiene valor)",
                key="grupo_tipo_post"
            )
        with col2:
            fields['Jerarquía de productos'] = st.text_input("Jerarquía de productos", key="jerarquia")
        # ---- Fila 7
        col1, col2 = st.columns(2)
        with col1:
            fields['Dimensiones EAN (peso bruto)'] = st.text_input("Dimensiones EAN (peso bruto)", key="dim_ean_bruto")
        with col2:
            fields['Dimensiones EAN (unidad de peso)'] = st.selectbox(
                "Dimensiones EAN (unidad de peso)",
                ["", "BOL", "BOT", "CJ", "CIE", "CIL", "DOC", "GLN", "G", "KG", "LB", "L", "M", "M2", "M3", "MIL", "PAR", "T", "UN"],
                key="dim_ean_unidad"
            )
        # ---- Fila 8
        col1, col2 = st.columns(2)
        with col1:
            fields['Dimensiones EAN (peso neto (kg))'] = st.text_input("Dimensiones EAN (peso neto (kg))", key="dim_ean_neto")
        with col2:
            fields['Grupo materiales ME'] = st.selectbox(
                "Grupo materiales ME",
                ["", "Z001-GPO. PALETS", "Z002-GPO. JABAS", "Z003-GPO. BANDEJAS", "Z004-GPO. CAJAS", "Z005-GPO. SACOS", "Z006-GPO. FULL CONTAINER LOAD (FCL)", "Z007-GPO. CARGA SUELTA", "Z008-GPO. LESS THAN CONTAINER LOAD (LCL)"],
                key="grupo_me"
            )
        # ---- Fila 9
        col1, col2 = st.columns(2)
        with col1:
            fields['Grupo de artículos'] = st.text_area("Grupo de artículos", key="grupo_articulos")
        with col2:
            fields['Costo (KG)'] = st.number_input("Costo (KG)", min_value=0.0, step=0.01, key="costo_kg")
        # ---- Fila 10
        col1, col2 = st.columns(2)
        with col1:
            fields['Costo (UN)'] = st.number_input("Costo (UN)", min_value=0.0, step=0.01, key="costo_un")

        # ----------- Botones en la misma fila, dentro del form -----------
        col_guardar, col_reset = st.columns([1, 1])
        enviado = col_guardar.form_submit_button("Guardar solicitud")
        reestablecer = col_reset.form_submit_button("Reestablecer formulario")

        # ----------- Validación de campos -----------
        faltantes = [k for k, v in fields.items() if (not v or (isinstance(v, str) and v.strip() == ""))]
        if fields["Costo (KG)"] == 0:
            faltantes.append("Costo (KG)")
        if fields["Costo (UN)"] == 0:
            faltantes.append("Costo (UN)")

        st.markdown(
            f"""
            <script>
            const fieldNames = {list(fields.keys())};
            fieldNames.forEach(function(label) {{
                let inputs = Array.from(document.querySelectorAll('label')).filter(el => el.innerText.includes(label));
                inputs.forEach(function(labelEl) {{
                    let formField = labelEl.parentElement;
                    let input = formField.querySelector('input,textarea,select');
                    if (input) {{
                        if (input.value && input.value !== "0" && input.value !== "") {{
                            formField.classList.remove('field-empty');
                            formField.classList.add('field-filled');
                        }} else {{
                            formField.classList.remove('field-filled');
                            formField.classList.add('field-empty');
                        }}
                    }}
                }});
            }});
            </script>
            """, unsafe_allow_html=True
        )

        # Marcar en rojo si falta al guardar
        if enviado and faltantes:
            st.warning("Favor complete todos los campos.")
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
            st.session_state.materiales.append({k: v for k, v in fields.items()})
            st.success("Datos guardados.")

        # ----------- Reset: Limpia todos los campos, menos 'materiales' ----------
        if reestablecer:
            materiales = st.session_state.get("materiales", [])
            st.session_state.clear()
            st.session_state.materiales = materiales
            st.rerun()  # Ahora sí funciona y los campos quedan vacíos

# ----------- RESTO DE PESTAÑAS -----------
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
if "materiales" in st.session_state and st.session_state.materiales:
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
