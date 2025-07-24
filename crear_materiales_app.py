import streamlit as st
import pandas as pd
from datetime import date
import io

st.set_page_config(page_title="Creación de Materiales", layout="wide")
st.title("📦 Formulario de Creación de Materiales")

# --- Definir keys de todos los campos ---
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

def limpiar_campos():
    for k, v in CAMPOS:
        # Usar date.today() para "fecha", evitar siempre el mismo valor
        if k == "fecha":
            st.session_state[k] = date.today()
        else:
            st.session_state[k] = v

if "materiales" not in st.session_state:
    st.session_state.materiales = []

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

        col1, col2 = st.columns(2)
        with col1:
            usuario = st.text_input("Usuario Solicitante", key="usuario")
        with col2:
            um_valoracion = st.selectbox("UM_VALORACIÓN", ["", "BOL", "BOT", "CJ"], key="um_valoracion")

        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha de Solicitud", key="fecha")
        with col2:
            codigo_material = st.selectbox("Código de material", ["", "FERT", "HALB", "ZHAL"], key="codigo_material")

        col1, col2 = st.columns(2)
        with col1:
            correo = st.text_input("Correo electrónico", key="correo")
        with col2:
            tipo_material = st.selectbox("Tipo de material", ["", "PRODUCTO_TERMINADO", "PRODUCTO_SEMIELABORADO"], key="tipo_material")

        col1, col2 = st.columns(2)
        with col1:
            descripcion = st.text_input("Descripción del material", key="descripcion")
        with col2:
            um_base = st.selectbox("UM_BASE", ["", "BOL", "BOT", "CJ"], key="um_base")

        col1, col2 = st.columns(2)
        with col1:
            ramo = st.text_input("Ramo", key="ramo")
        with col2:
            sector = st.text_input("Sector", key="sector")

        col1, col2 = st.columns(2)
        with col1:
            grupo_tipo_post = st.text_input("Grupo Tipo Post Gral", key="grupo_tipo_post")
        with col2:
            jerarquia = st.text_input("Jerarquía de productos", key="jerarquia")

        col1, col2 = st.columns(2)
        with col1:
            dim_ean_bruto = st.text_input("Dimensiones EAN (peso bruto)", key="dim_ean_bruto")
        with col2:
            dim_ean_unidad = st.selectbox("Dimensiones EAN (unidad de peso)", ["", "KG", "G", "LB"], key="dim_ean_unidad")

        col1, col2 = st.columns(2)
        with col1:
            dim_ean_neto = st.text_input("Dimensiones EAN (peso neto (kg))", key="dim_ean_neto")
        with col2:
            grupo_me = st.selectbox("Grupo materiales ME", ["", "Z001-GPO. PALETS", "Z002-GPO. JABAS"], key="grupo_me")

        col1, col2 = st.columns(2)
        with col1:
            grupo_articulos = st.text_area("Grupo de artículos", key="grupo_articulos")
        with col2:
            costo_kg = st.number_input("Costo (KG)", min_value=0.0, step=0.01, key="costo_kg")

        costo_un = st.number_input("Costo (UN)", min_value=0.0, step=0.01, key="costo_un")

        col_guardar, col_reset = st.columns([1, 1])
        enviado = col_guardar.form_submit_button("Guardar solicitud")
        reestablecer = col_reset.form_submit_button("Reestablecer formulario")

        if enviado:
            campos = {k: st.session_state[k] for k, _ in CAMPOS}
            if any(v == "" or v == 0.0 for k, v in campos.items() if k not in ["fecha"]):
                st.warning("Favor complete todos los campos.")
            else:
                st.session_state.materiales.append(campos)
                st.success("Datos guardados.")
                limpiar_campos()
                st.experimental_rerun()

        if reestablecer:
            limpiar_campos()
            st.experimental_rerun()

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
