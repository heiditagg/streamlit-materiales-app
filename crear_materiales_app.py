import streamlit as st
import pandas as pd
from datetime import date
import io

st.set_page_config(page_title="Creación de Materiales", layout="wide")
st.title("📦 Formulario de Creación de Materiales")

# -------------------- Flags de control --------------------
if "_pending_reset" not in st.session_state:
    st.session_state._pending_reset = False
if "_flash" not in st.session_state:
    st.session_state._flash = None
if "materiales" not in st.session_state:
    st.session_state.materiales = []

# -------------------- Constantes de Calidad --------------------
LINEAS = [
    "01 Pollo Beneficiado entero","02 Pollo Trozado","03 Cerdo Beneficiado entero","04 Cerdo Trozado",
    "05 Pavo","06 Preparados","07 Empanizados","08 Embutidos","09 Filete",
    "10 Trozado Marinado","11 Menudencias","12 Filete Marinado","13 Semielaborados"
]
ESTADOS = ["01 Fresco","02 Congelado","03 Por Congelar"]

# -------------------- Campos Solicitante -----------------------
CAMPOS = [
    ("usuario", ""),
    ("um_valoracion", ""),
    ("fecha", date.today()),
    ("codigo_material", ""),
    ("correo", ""),
    ("tipo_material", ""),
    ("descripcion", ""),
    ("um_base", ""),
    ("ramo", ""),
    ("sector", ""),
    ("grupo_tipo_post", ""),
    ("jerarquia", ""),
    ("dim_ean_bruto", ""),
    ("dim_ean_unidad", ""),
    ("dim_ean_neto", ""),
    ("grupo_me", ""),
    ("grupo_articulos", ""),
    ("costo_kg", 0.0),
    ("costo_un", 0.0),
]

# -------------------- Campos Gestión de la Calidad ------------
# OJO: qc_categoria y qc_asignacion_clase SE CALCULAN, no se guardan en session_state
QC_CAMPOS = [
    ("qc_linea", ""),
    ("qc_estado", "")
]

FIELD_GROUPS = [CAMPOS, QC_CAMPOS]

def limpiar_campos():
    """Resetea todos los campos de todas las pestañas."""
    for group in FIELD_GROUPS:
        for k, v in group:
            if k == "fecha":
                st.session_state[k] = date.today()
            elif isinstance(v, list):
                st.session_state[k] = list(v)
            else:
                st.session_state[k] = v

def recolectar_payload():
    """Recolecta todos los campos definidos en FIELD_GROUPS."""
    payload = {}
    for group in FIELD_GROUPS:
        for k, _ in group:
            payload[k] = st.session_state.get(k, "")
    return payload

def calcular_qc():
    """Devuelve (categoria, asignacion_clase) sin escribir en session_state."""
    desc = st.session_state.get("descripcion", "").strip()
    categoria = "001" if desc else ""
    asignacion = "ZMM_CLASS_MAT" if categoria == "001" else ""
    return categoria, asignacion

def validar_solicitante():
    """Valida mínimos de la pestaña Solicitante."""
    campos_solicitante = {k: st.session_state.get(k, "") for k, _ in CAMPOS}
    return not any((v == "" or v == 0.0) for k, v in campos_solicitante.items() if k != "fecha")

def guardar_solicitud():
    """Guarda la solicitud consolidando todas las pestañas."""
    if not validar_solicitante():
        st.warning("Favor complete todos los campos de la pestaña Solicitante.")
        return

    payload = recolectar_payload()

    # Inyectar cálculo de Calidad al payload (sin tocar session_state)
    cat, asig = calcular_qc()
    payload["qc_categoria"] = cat
    payload["qc_asignacion_clase"] = asig

    st.session_state.materiales.append(payload)

    # Programar limpieza y mostrar mensaje en el próximo run
    st.session_state._flash = "Datos guardados."
    st.session_state._pending_reset = True
    st.rerun()

# --------- Ejecutar limpieza si quedó pendiente de un submit previo ----------
if st.session_state._pending_reset:
    limpiar_campos()
    st.session_state._pending_reset = False

# --------- Mostrar mensaje 'flash' si existe ----------
if st.session_state._flash:
    st.success(st.session_state._flash)
    st.session_state._flash = None

# ----------------------------- UI ------------------------------
tabs = st.tabs([
    "Solicitante",
    "Gestión de la Calidad",
    "Comercial",
    "Planificación",
    "Producción",
    "Contabilidad"
])

# ---------- TAB 1: Solicitante ----------
with tabs[0]:
    st.subheader("Datos del solicitante y del material")
    with st.form("form_solicitante", clear_on_submit=False):

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Usuario Solicitante", key="usuario")
        with col2:
            st.selectbox("UM_VALORACIÓN", ["", "BOL", "BOT", "CJ"], key="um_valoracion")

        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Fecha de Solicitud", key="fecha")
        with col2:
            st.selectbox("Código de material", ["", "FERT", "HALB", "ZHAL"], key="codigo_material")

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Correo electrónico", key="correo")
        with col2:
            st.selectbox("Tipo de material", ["", "PRODUCTO_TERMINADO", "PRODUCTO_SEMIELABORADO"], key="tipo_material")

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Descripción del material", key="descripcion")
        with col2:
            st.selectbox("UM_BASE", ["", "BOL", "BOT", "CJ"], key="um_base")

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Ramo", key="ramo")
        with col2:
            st.text_input("Sector", key="sector")

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Grupo Tipo Post Gral", key="grupo_tipo_post")
        with col2:
            st.text_input("Jerarquía de productos", key="jerarquia")

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Dimensiones EAN (peso bruto)", key="dim_ean_bruto")
        with col2:
            st.selectbox("Dimensiones EAN (unidad de peso)", ["", "KG", "G", "LB"], key="dim_ean_unidad")

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Dimensiones EAN (peso neto (kg))", key="dim_ean_neto")
        with col2:
            st.selectbox("Grupo materiales ME", ["", "Z001-GPO. PALETS", "Z002-GPO. JABAS"], key="grupo_me")

        col1, col2 = st.columns(2)
        with col1:
            st.text_area("Grupo de artículos", key="grupo_articulos")
        with col2:
            st.number_input("Costo (KG)", min_value=0.0, step=0.01, key="costo_kg")

        st.number_input("Costo (UN)", min_value=0.0, step=0.01, key="costo_un")

        col_guardar, col_reset = st.columns([1, 1])
        enviado = col_guardar.form_submit_button("Guardar solicitud")
        reestablecer = col_reset.form_submit_button("Reestablecer formulario")

        if enviado:
            guardar_solicitud()
        if reestablecer:
            st.session_state._pending_reset = True
            st.rerun()

# ---------- TAB 2: Gestión de la Calidad ----------
with tabs[1]:
    st.subheader("Gestión de la Calidad")

    # Mostrar los campos calculados SOLO como visualización (no guardan estado)
    cat_view, asig_view = calcular_qc()

    with st.form("form_calidad", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Categoría (auto)", value=cat_view, key="qc_categoria_view", disabled=True)
            st.selectbox("Línea", [""] + LINEAS, key="qc_linea")
        with c2:
            st.text_input("Asignaciones: Clase (auto)", value=asig_view, key="qc_asignacion_clase_view", disabled=True)
            st.selectbox("Estado", [""] + ESTADOS, key="qc_estado")

        col_guardar_qc, col_reset_qc = st.columns([1, 1])
        enviado_qc = col_guardar_qc.form_submit_button("Guardar solicitud")
        reestablecer_qc = col_reset_qc.form_submit_button("Reestablecer formulario")

        if enviado_qc:
            guardar_solicitud()
        if reestablecer_qc:
            st.session_state._pending_reset = True
            st.rerun()

# ---------- Tabla y descarga ----------
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



