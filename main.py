import database as database
import streamlit as st
from models.producto import Producto

st.title("📦 Control de Inventario")

# 1. Crear las tablas SQLite
database.inicializar_tablas()

# 2. Botón para cargar productos de prueba
if st.button("Cargar productos de prueba"):
    p1 = Producto(0, "Inca Kola 500ml", precio_compra=2.50, precio_venta=3.50, stock=50, es_favorito=True)
    p2 = Producto(0, "Papa Rellena", precio_compra=2.00, precio_venta=3.50, stock=20, es_favorito=True)

    database.guardar_producto(p1)
    database.guardar_producto(p2)
    st.success("¡Productos guardados correctamente!")

# 3. Leer y mostrar los productos en pantalla
st.subheader("Productos en Base de Datos")
lista_productos = database.obtener_productos()

if lista_productos:
    for prod in lista_productos:
        st.write(prod)
else:
    st.info("No hay productos registrados en la base de datos.")