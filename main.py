import app

import streamlit as st
import database as database

st.set_page_config(page_title="Mi Tienda", layout="wide")

# Menú lateral
st.sidebar.title("🏪 Sistema de Tienda")
opcion = st.sidebar.radio("Navegación:", ["📦 Inventario", "🛒 Registrar Venta", "📊 Historial"])

if opcion == "📦 Inventario":
    st.title("📦 Gestión de Inventario")
    database.inicializar_tablas()
    # Aquí va la vista de inventario
    
elif opcion == "🛒 Registrar Venta":
    st.title("🛒 Punto de Venta")
    # Aquí va la vista de cobros

elif opcion == "📊 Historial":
    st.title("📊 Historial de Transacciones")
    # Aquí van los reportes