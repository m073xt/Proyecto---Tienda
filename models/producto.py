class Producto:

    def __init__(self, id_: int, nombre: str, precio_compra: float,
                precio_venta: float, stock: int, es_favorito: bool = False):
        self.__id = id_
        self.__nombre = nombre
        self.__precio_compra = precio_compra
        self.__precio_venta = precio_venta
        self.__stock = stock
        self.__es_favorito = es_favorito

    #---------- Atributos ----------
    @property
    def id(self) -> int:
        return self.__id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, val: str) -> None:
        if not val.strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        self.__nombre = val

    @property
    def precio_compra(self) -> float:
        return self.__precio_compra

    @property
    def precio_venta(self) -> float:
        return self.__precio_venta

    @precio_venta.setter
    def precio_venta(self, val: float) -> None:
        if val < 0:
            raise ValueError("El precio de venta no puede ser negativo")
        self.__precio_venta = val

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, val: int) -> None:
        if val < 0:
            raise ValueError("El stock no puede ser negativo")
        self.__stock = val

    @property
    def es_favorito(self) -> bool:
        return self.__es_favorito

    @es_favorito.setter
    def es_favorito(self, val: bool) -> None:
        self.__es_favorito = val

    #---------- Metodos ----------
    def tiene_stock(self, cantidad: int) -> bool:
        """Indica si hay suficiente stock para vender "cantidad" unidades."""
        return self.__stock >= cantidad

    def descontar_stock(self, cantidad: int) -> None:
        """Descuenta stock al vender. Lanza error si no alcanza."""
        if not self.tiene_stock(cantidad):
            raise ValueError(
                f"Stock insuficiente de '{self.__nombre}': "
                f"disponible {self.__stock}, solicitado {cantidad}"
            )
        self.__stock -= cantidad

    def reponer_stock(self, cantidad: int) -> None:
        """Aumenta el stock cuando llega un pedido del preventista."""
        if cantidad <= 0:
            raise ValueError("La cantidad a reponer debe ser positiva")
        self.__stock += cantidad

    def __str__(self) -> str:
        fav = "✩" if self.__es_favorito else ""
        return f"[{self.__id}] {self.__nombre} - S/ {self.__precio_venta:.2f} (stock: {self.__stock}){fav}"