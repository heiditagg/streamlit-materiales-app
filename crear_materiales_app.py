import streamlit as st
import pandas as pd
from datetime import date
import io

st.set_page_config(page_title="Creación de Materiales", layout="wide")
st.title("📦 Formulario de Creación de Materiales")

# --- Campos pestaña Solicitante ---
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

# --- Campos pestaña Gestión de la Calidad ---
LINEAS = [
    "01 Pollo Beneficiado entero","02 Pollo Trozado","03 Cerdo Beneficiado entero","04 Cerdo Trozado",
    "05 Pavo","06 Preparados","07 Empanizados","08 Embutidos","09 Filete",
    "10 Trozado Marinado","11 Menudencias","12 Filete Marinado","13 Semielaborados"
]
ESTADOS = ["01 Fresco","02 Congelado","03 Por Congelar"]

QC_CAMPOS = [
    ("qc_categoria", ""),           # autocalculado: "001" si hay descripción
    ("qc_asignacion_clase", ""),    # autocalculado: "ZMM_CLASS_MAT" si categoria "001"
    ("qc_linea", ""),
    ("qc_estado", "")
]

def limpiar_campos():
    # pestaña solicitante
    for k, v in CAMPOS:
        st.session_state[k] = date.today() if k == "fecha" else v
    # pestaña calidad
    for k, v in QC_CAMPOS:
        st.session_state[k] = v

if "materiales" not in st.session_state:
    st.session_state.materiales = []

# ------------------------ UI ------------------------
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

        # ---------- Guardar / Reset ----------
        if enviado:
            # autocalcular campos de calidad antes de guardar (por si no visitaron la pestaña)
            desc = st.session_state.get("descripcion", "").strip()
            st.session_state["qc_categoria"] = "001" if desc else ""
            st.session_state["qc_asignacion_clase"] = "ZMM_CLASS_MAT" if st.session_state["qc_categoria"] == "001" else ""

            campos = {k: st.session_state[k] for k, _ in CAMPOS}
            qc_campos = {k: st.session_state.get(k, "") for k, _ in QC_CAMPOS}
            payload = {**campos, **qc_campos}

            # validación mínima: obligatorios de solicitante
            if any((v == "" or v == 0.0) for k, v in campos.items() if k != "fecha"):
                st.warning("Favor complete todos los campos de la pestaña Solicitante.")
            else:
                st.session_state.materiales.append(payload)
                st.success("Datos guardados.")
                limpiar_campos()
                st.experimental_rerun()

        if reestablecer:
            limpiar_campos()
            st.experimental_rerun()

# ---------- TAB 2: Gestión de la Calidad ----------
with tabs[1]:
    st.subheader("Gestión de la Calidad")

    # Autocálculo en tiempo real
    desc = st.session_state.get("descripcion", "").strip()
    categoria = "001" if desc else ""
    st.session_state["qc_categoria"] = categoria
    st.session_state["qc_asignacion_clase"] = "ZMM_CLASS_MAT" if categoria == "001" else ""

    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Categoría (auto)", key="qc_categoria", disabled=True)
        st.selectbox("Línea", [""] + LINEAS, key="qc_linea")
    with c2:
        st.text_input("Asignaciones: Clase (auto)", key="qc_asignacion_clase", disabled=True)
        st.selectbox("Estado", [""] + ESTADOS, key="qc_estado")

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
