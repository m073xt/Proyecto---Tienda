from models.producto import Producto


class DetalleVenta:
    """Representa una línea dentro de una venta (un producto vendido)."""

    def __init__(self, producto: Producto, cantidad: int):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if not producto.tiene_stock(cantidad):
            raise ValueError(f"No hay stock suficiente de '{producto.nombre}'")

        self.__producto = producto
        self.__cantidad = cantidad
        #se congela el precio de venta actual, por si luego cambia
        self.__precio_unitario = producto.precio_venta

    # ---------- Propiedades ----------
    @property
    def producto(self) -> Producto:
        return self.__producto

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @property
    def subtotal(self) -> float:
        return self.calcular_subtotal()

    # ---------- Métodos ----------
    def calcular_subtotal(self) -> float:
        return self.__precio_unitario * self.__cantidad

    def __str__(self) -> str:
        return (f"{self.__producto.nombre} x{self.__cantidad} "
                f"= S/ {self.calcular_subtotal()}")