import streamlit as st
import pandas as pd
import datetime
import os

# Archivo CSV para guardar los pedidos
CSV_FILENAME = "pedidos.csv"

# Cargar datos existentes o crear un DataFrame vacío
if os.path.exists(CSV_FILENAME):
    pedidos = pd.read_csv(CSV_FILENAME)
else:
    pedidos = pd.DataFrame(columns=["ID", "Solicitante", "Descripción", "Estado", "Historial"])

# Función para guardar cambios
def guardar_pedidos(df):
    df.to_csv(CSV_FILENAME, index=False)

# Título principal
st.title("📦 Plataforma de Seguimiento de Pedidos - Proveeduría")

# --- Sección: Agregar nuevo pedido ---
st.header("📝 Registrar Nuevo Pedido")
with st.form("form_pedido"):
    id_pedido = st.text_input("ID del Pedido")
    solicitante = st.text_input("Nombre del solicitante")
    descripcion = st.text_area("Descripción del pedido")
    submitted = st.form_submit_button("Agregar")

    if submitted:
        if id_pedido and solicitante and descripcion:
            nuevo_pedido = {
                "ID": id_pedido,
                "Solicitante": solicitante,
                "Descripción": descripcion,
                "Estado": "Solicitado",
                "Historial": f"{datetime.date.today()} - Pedido creado por {solicitante}"
            }
            pedidos = pd.concat([pedidos, pd.DataFrame([nuevo_pedido])], ignore_index=True)
            guardar_pedidos(pedidos)
            st.success("✅ Pedido agregado exitosamente.")
        else:
            st.warning("⚠️ Por favor completa todos los campos.")

# --- Sección: Visualizar pedidos existentes ---
st.header("📋 Pedidos Existentes")
if not pedidos.empty:
    st.dataframe(pedidos[["ID", "Solicitante", "Descripción", "Estado"]], use_container_width=True)

    # --- Sección: Actualizar estado del pedido ---
    st.subheader("🔄 Actualizar Estado")
    pedido_seleccionado = st.selectbox("Seleccionar ID del pedido a actualizar", pedidos["ID"])
    nuevo_estado = st.selectbox(
        "Seleccionar nuevo estado",
        [
            "Cotización solicitada",
            "Esperando aprobación/pago",
            "En proceso de entrega",
            "Entregado",
            "Demora: proveedor / pago / gestión interna"
        ]
    )

    if st.button("Actualizar estado"):
        idx = pedidos[pedidos["ID"] == pedido_seleccionado].index[0]
        pedidos.at[idx, "Estado"] = nuevo_estado
        pedidos.at[idx, "Historial"] += f"\n{datetime.date.today()} - Estado actualizado a '{nuevo_estado}'"
        guardar_pedidos(pedidos)
        st.success("🔁 Estado actualizado correctamente.")

    # --- Sección: Ver historial ---
    st.subheader("📜 Historial del Pedido")
    historial = pedidos[pedidos["ID"] == pedido_seleccionado]["Historial"].values[0]
    st.text(historial)
else:
    st.info("ℹ️ No hay pedidos registrados aún.")
