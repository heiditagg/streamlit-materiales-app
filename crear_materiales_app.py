import streamlit as st
import pandas as pd
from datetime import date
import io

st.set_page_config(page_title="Creación de Materiales", layout="wide")
st.title("GD-F003 Creación de Materiales _ Producto Terminado, Semielaborado y Sub-Productos ")

# -------------------- Flags / Estado --------------------
if "_pending_reset" not in st.session_state:
    st.session_state._pending_reset = False
if "_flash" not in st.session_state:
    st.session_state._flash = None
if "materiales" not in st.session_state:
    st.session_state.materiales = []
if "_row_counter" not in st.session_state:
    st.session_state._row_counter = 0
# Confirmador de borrado
if "_show_confirm_delete" not in st.session_state:
    st.session_state._show_confirm_delete = False
if "_confirm_delete_ids" not in st.session_state:
    st.session_state._confirm_delete_ids = []

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

# -------------------- Campos Gestión de la Calidad (manuales) ------------
QC_CAMPOS = [
    ("qc_linea", ""),
    ("qc_estado", "")
]

FIELD_GROUPS = [CAMPOS, QC_CAMPOS]

# -------------------- Utilidades --------------------
def limpiar_campos():
    for group in FIELD_GROUPS:
        for k, v in group:
            if k == "fecha":
                st.session_state[k] = date.today()
            elif isinstance(v, list):
                st.session_state[k] = list(v)
            else:
                st.session_state[k] = v

def recolectar_payload():
    payload = {}
    for group in FIELD_GROUPS:
        for k, _ in group:
            payload[k] = st.session_state.get(k, "")
    return payload

def calcular_qc():
    desc = st.session_state.get("descripcion", "").strip()
    categoria = "001" if desc else ""
    asignacion = "ZMM_CLASS_MAT" if categoria == "001" else ""
    return categoria, asignacion

def validar_solicitante():
    campos_solicitante = {k: st.session_state.get(k, "") for k, _ in CAMPOS}
    return not any((v == "" or v == 0.0) for k, v in campos_solicitante.items() if k != "fecha")

def guardar_solicitud():
    if not validar_solicitante():
        st.warning("Favor complete todos los campos de la pestaña Solicitante.")
        return

    payload = recolectar_payload()
    cat, asig = calcular_qc()
    payload["qc_categoria"] = cat
    payload["qc_asignacion_clase"] = asig

    st.session_state._row_counter += 1
    payload["_id"] = f"R{st.session_state._row_counter:05d}"

    st.session_state.materiales.append(payload)

    st.session_state._flash = "Datos guardados."
    st.session_state._pending_reset = True
    st.rerun()

def eliminar_por_ids(ids):
    if not ids:
        return
    st.session_state.materiales = [r for r in st.session_state.materiales if r.get("_id") not in ids]
    st.session_state._flash = f"Se eliminaron {len(ids)} registro(s)."
    st.session_state._show_confirm_delete = False
    st.session_state._confirm_delete_ids = []
    st.rerun()

# --------- Reset pendiente tras un submit previo ----------
if st.session_state._pending_reset:
    limpiar_campos()
    st.session_state._pending_reset = False

# --------- Mensaje 'flash' si existe ----------
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

# ---------- Tabla + Borrado (con confirmación) y descarga ----------
if st.session_state.materiales:
    st.subheader("📋 Solicitudes Registradas")

    df = pd.DataFrame(st.session_state.materiales)
    view_df = df.copy()
    view_df.insert(0, "🗑️", False)

    edited_df = st.data_editor(
        view_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "🗑️": st.column_config.CheckboxColumn("🗑️", help="Selecciona para eliminar")
        },
        key="editor_solicitudes",
    )

    seleccionados = edited_df.loc[edited_df["🗑️"] == True]

    cols = st.columns([1, 3])
    with cols[0]:
        clicked_del = st.button("Eliminar seleccionados", disabled=seleccionados.empty)

    if clicked_del:
        ids_a_borrar = df.loc[seleccionados.index, "_id"].tolist()
        st.session_state._confirm_delete_ids = ids_a_borrar
        st.session_state._show_confirm_delete = True
        st.rerun()

    # --- Modal/confirmación simple ---
    if st.session_state._show_confirm_delete:
        ids = st.session_state._confirm_delete_ids
        st.warning(
            f"¿Seguro que deseas eliminar {len(ids)} registro(s)? "
            f"IDs: {', '.join(ids)}"
        )
        c_ok, c_cancel = st.columns(2)
        with c_ok:
            if st.button("✅ Confirmar eliminación"):
                eliminar_por_ids(ids)
        with c_cancel:
            if st.button("❌ Cancelar"):
                st.session_state._show_confirm_delete = False
                st.session_state._confirm_delete_ids = []
                st.rerun()

    # Exportar sin columnas internas
    export_df = df.drop(columns=[c for c in df.columns if c.startswith("_")], errors="ignore")
    output = io.BytesIO()
    export_df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    st.download_button(
        label="📥 Descargar archivo Excel",
        data=output,
        file_name="solicitudes_materiales.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
