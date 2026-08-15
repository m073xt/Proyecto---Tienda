"""
Módulo database.py
------------------
Manejo de la base de datos SQLite y consultas de reportes.
"""

import sqlite3
from datetime import datetime

from models.producto import Producto
from models.usuario import Usuario
from models.cliente import Cliente
from models.venta import Venta
from models.detalle_venta import DetalleVenta

DB_NAME = "tienda.db"

def obtener_conexion():
    """Devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def inicializar_tablas():
    """Crea las tablas necesarias en la base de datos si aún no existen."""
    with obtener_conexion() as conn:
        cursor = conn.cursor()

        # 1. Tabla Productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio_compra REAL NOT NULL,
                precio_venta REAL NOT NULL,
                stock INTEGER NOT NULL,
                es_favorito BOOLEAN NOT NULL DEFAULT 0
            )
        """)

        # 2. Tabla Usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                rol TEXT NOT NULL
            )
        """)

        # 3. Tabla Clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
        """)

        # 4. Tabla Ventas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_hora TEXT NOT NULL,
                vendedor_id INTEGER NOT NULL,
                es_fiado BOOLEAN NOT NULL,
                cliente_id INTEGER,
                total REAL NOT NULL,
                FOREIGN KEY (vendedor_id) REFERENCES usuarios (id),
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        """)

        # 5. Tabla Detalle_Ventas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalles_venta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES ventas (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        """)

        # 6. Tabla Pagos_Deuda
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pagos_deuda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                monto REAL NOT NULL,
                fecha TEXT NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        """)
        conn.commit()


# ==========================================
# FUNCIONES PARA PRODUCTOS
# ==========================================

def guardar_producto(p: Producto) -> int:
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, precio_compra, precio_venta, stock, es_favorito)
            VALUES (?, ?, ?, ?, ?)
        """, (p.nombre, p.precio_compra, p.precio_venta, p.stock, p.es_favorito))
        conn.commit()
        return cursor.lastrowid

def obtener_productos() -> list[Producto]:
    productos = []
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()
        for f in filas:
            prod = Producto(
                id_=f["id"],
                nombre=f["nombre"],
                precio_compra=f["precio_compra"],
                precio_venta=f["precio_venta"],
                stock=f["stock"],
                es_favorito=bool(f["es_favorito"])
            )
            productos.append(prod)
    return productos


# ==========================================
# FUNCIONES PARA USUARIOS Y CLIENTES
# ==========================================

def guardar_usuario(u: Usuario) -> int:
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, rol) VALUES (?, ?)", (u.nombre, u.rol))
        conn.commit()
        return cursor.lastrowid

def guardar_cliente(c: Cliente) -> int:
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nombre) VALUES (?)", (c.nombre,))
        conn.commit()
        return cursor.lastrowid


# ==========================================
# FUNCIONES PARA VENTAS Y ABONOS
# ==========================================

def guardar_venta(v: Venta) -> int:
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        
        cliente_id = v.cliente.id if v.cliente else None
        fecha_str = v.fecha_hora.strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO ventas (fecha_hora, vendedor_id, es_fiado, cliente_id, total)
            VALUES (?, ?, ?, ?, ?)
        """, (fecha_str, v.vendedor.id, v.es_fiado, cliente_id, v.total))
        
        venta_id = cursor.lastrowid

        for d in v.detalles:
            cursor.execute("""
                INSERT INTO detalles_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (venta_id, d.producto.id, d.cantidad, d.producto.precio_venta, d.subtotal))

            cursor.execute("""
                UPDATE productos SET stock = stock - ? WHERE id = ?
            """, (d.cantidad, d.producto.id))

        conn.commit()
        return venta_id

def guardar_pago_deuda(cliente_id: int, monto: float):
    fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pagos_deuda (cliente_id, monto, fecha)
            VALUES (?, ?, ?)
        """, (cliente_id, monto, fecha_str))
        conn.commit()


# ==========================================
# CONSULTAS DE REPORTES (FIADOS Y CAJA)
# ==========================================

def obtener_clientes_con_deuda() -> list[dict]:
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        filas = cursor.fetchall()
        
        lista_clientes = []
        for f in filas:
            c_id = f["id"]
            cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas WHERE cliente_id = ? AND es_fiado = 1", (c_id,))
            total_fiado = cursor.fetchone()[0]
            
            cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM pagos_deuda WHERE cliente_id = ?", (c_id,))
            total_pagado = cursor.fetchone()[0]
            
            saldo_pendiente = total_fiado - total_pagado
            lista_clientes.append({
                "id": c_id,
                "nombre": f["nombre"],
                "deuda": saldo_pendiente
            })
        return lista_clientes

def obtener_resumen_caja_hoy() -> dict:
    hoy = datetime.now().strftime("%Y-%m-%d")
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas WHERE fecha_hora LIKE ? AND es_fiado = 0", (f"{hoy}%",))
        contado = cursor.fetchone()[0]
        
        cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas WHERE fecha_hora LIKE ? AND es_fiado = 1", (f"{hoy}%",))
        fiado = cursor.fetchone()[0]
        
        cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM pagos_deuda WHERE fecha LIKE ?", (f"{hoy}%",))
        abonos = cursor.fetchone()[0]
        
        return {
            "efectivo_ventas": contado,
            "efectivo_abonos": abonos,
            "total_efectivo_caja": contado + abonos,
            "total_fiado_hoy": fiado
        }