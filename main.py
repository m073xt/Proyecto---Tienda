import streamlit as st
import database
from models.producto import Producto
from models.usuario import Usuario
from models.cliente import Cliente
from models.venta import Venta
from models.detalle_venta import DetalleVenta

st.set_page_config(page_title="Tiendita de Mamá", page_icon="🏪", layout="centered")

database.inicializar_tablas()
vendedor_actual = Usuario(id_=1, nombre="Mamá", rol="vendedor")

st.title("🏪 Tiendita de Mamá")

tab_venta, tab_fiados, tab_caja, tab_inventario = st.tabs([
    "⚡ Venta Rápida", 
    "📖 Fiados", 
    "💵 Caja del Día", 
    "📦 Inventario"
])

# ==========================================
# 1. VENTA RÁPIDA (AL CONTADO)
# ==========================================
with tab_venta:
    st.header("⚡ Registrar Venta en Efectivo")
    productos = database.obtener_productos()
    
    if not productos:
        st.info("Agrega productos en la pestaña 'Inventario' para comenzar.")
    else:
        cols = st.columns(2)
        for idx, prod in enumerate(productos):
            col = cols[idx % 2]
            with col:
                label_boton = f"{prod.nombre}\nS/ {prod.precio_venta:.2f} (Stock: {prod.stock})"
                if st.button(label_boton, key=f"btn_vta_{prod.id}", use_container_width=True):
                    try:
                        nueva_venta = Venta(id_=0, vendedor=vendedor_actual, es_fiado=False)
                        nueva_venta.agregar_detalle(DetalleVenta(prod, cantidad=1))
                        database.guardar_venta(nueva_venta)
                        st.success(f"✅ Venta registrada: 1x {prod.nombre}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ {e}")

# ==========================================
# 2. CUADERNO DE FIADOS
# ==========================================
with tab_fiados:
    st.header("📖 Cuaderno de Fiados")
    
    # Subsección A: Registrar nuevo cliente
    with st.expander("➕ Agregar nuevo cliente"):
        nombre_cliente = st.text_input("Nombre del vecino / cliente")
        if st.button("Guardar Cliente"):
            if nombre_cliente.strip():
                database.guardar_cliente(Cliente(0, nombre_cliente.strip()))
                st.success(f"Cliente '{nombre_cliente}' registrado.")
                st.rerun()

    clientes = database.obtener_clientes_con_deuda()
    
    if not clientes:
        st.info("No hay clientes registrados aún.")
    else:
        # Subsección B: Anotar Fiado a un cliente existente
        st.subheader("🛒 Anotar Producto a Cuenta Fiada")
        cliente_sel = st.selectbox(
            "Selecciona al Cliente:", 
            options=clientes, 
            format_func=lambda c: f"{c['nombre']} (Deuda actual: S/ {c['deuda']:.2f})"
        )
        
        productos = database.obtener_productos()
        if productos:
            prod_fiado = st.selectbox("Producto a fiar:", options=productos, format_func=lambda p: f"{p.nombre} - S/ {p.precio_venta:.2f}")
            if st.button("📌 Registrar Venta Fiada", use_container_width=True):
                try:
                    obj_cliente = Cliente(cliente_sel["id"], cliente_sel["nombre"])
                    venta_f = Venta(id_=0, vendedor=vendedor_actual, es_fiado=True, cliente=obj_cliente)
                    venta_f.agregar_detalle(DetalleVenta(prod_fiado, cantidad=1))
                    database.guardar_venta(venta_f)
                    st.success(f"📌 Fiado anotado a {cliente_sel['nombre']}: {prod_fiado.nombre}")
                    st.rerun()
                except Exception as e:
                    st.error(f"⚠️ {e}")

        st.divider()

        # Subsección C: Registrar Cobro / Abono
        st.subheader("💵 Cobrar / Registrar Abono de Deuda")
        monto_abono = st.number_input("Monto en Soles (S/)", min_value=0.5, step=1.0)
        if st.button("✅ Registrar Pago de Deuda"):
            database.guardar_pago_deuda(cliente_sel["id"], monto_abono)
            st.success(f"Abono de S/ {monto_abono:.2f} registrado para {cliente_sel['nombre']}")
            st.rerun()

# ==========================================
# 3. CAJA DEL DÍA
# ==========================================
with tab_caja:
    st.header("💵 Resumen de Caja Chica")
    resumen = database.obtener_resumen_caja_hoy()
    
    col1, col2 = st.columns(2)
    col1.metric("Efectivo en Caja (Ventas)", f"S/ {resumen['efectivo_ventas']:.2f}")
    col2.metric("Abonos Cobrados Hoy", f"S/ {resumen['efectivo_abonos']:.2f}")
    
    st.divider()
    st.metric("💰 TOTAL EFECTIVO FÍSICO", f"S/ {resumen['total_efectivo_caja']:.2f}")
    st.caption(f"📌 Nota: Además, hoy se fió un total de S/ {resumen['total_fiado_hoy']:.2f}")

# ==========================================
# 4. INVENTARIO
# ==========================================
with tab_inventario:
    st.header("📦 Gestión de Inventario")
    with st.form("form_prod"):
        st.subheader("Agregar Nuevo Producto")
        nom = st.text_input("Nombre (ej. Pan con Pollo)")
        pc = st.number_input("Precio Compra", min_value=0.0, step=0.5)
        pv = st.number_input("Precio Venta", min_value=0.0, step=0.5)
        stk = st.number_input("Stock Inicial", min_value=1, value=20)
        if st.form_submit_button("💾 Guardar"):
            if nom.strip():
                database.guardar_producto(Producto(0, nom, pc, pv, stk, True))
                st.success(f"Producto '{nom}' guardado.")
                st.rerun()