import database as database
from models.producto import Producto

def main():
    # 1. Crear las tablas SQLite
    database.inicializar_tablas()

    # 2. Guardar un par de productos de prueba
    p1 = Producto(0, "Inca Kola 500ml", precio_compra=2.50, precio_venta=3.50, stock=50, es_favorito=True)
    p2 = Producto(0, "Papa Rellena", precio_compra=2.00, precio_venta=3.50, stock=20, es_favorito=True)

    database.guardar_producto(p1)
    database.guardar_producto(p2)

    # 3. Leer los productos guardados en la BD real
    print("\n📦 PRODUCTOS RECUPERADOS DESDE LA BASE DE DATOS:")
    lista_productos = database.obtener_productos()
    for prod in lista_productos:
        print(prod)

if __name__ == "__main__":
    main()