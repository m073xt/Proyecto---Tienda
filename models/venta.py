from datetime import datetime

from models.usuario import Usuario
from models.detalle_venta import DetalleVenta
from models.cliente import Cliente


class Venta:
    """Representa una venta completa, con uno o varios productos."""

    def __init__(self, id_: int, vendedor: Usuario, es_fiado: bool = False,
                cliente: Cliente = None):
        if es_fiado and cliente is None:
            raise ValueError("Una venta fiada necesita un cliente asociado")

        self.__id = id_
        self.__fecha_hora = datetime.now()
        self.__vendedor = vendedor
        self.__detalles: list[DetalleVenta] = []
        self.__es_fiado = es_fiado
        self.__cliente = cliente

    # ---------- Propiedades ----------
    @property
    def id(self) -> int:
        return self.__id

    @property
    def fecha_hora(self) -> datetime:
        return self.__fecha_hora

    @property
    def vendedor(self) -> Usuario:
        return self.__vendedor

    @property
    def es_fiado(self) -> bool:
        return self.__es_fiado

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def detalles(self) -> list:
        return list(self.__detalles)

    @property
    def total(self) -> float:
        return sum(detalle.subtotal for detalle in self.__detalles)

    # ---------- Métodos ----------
    def agregar_detalle(self, detalle: DetalleVenta) -> None:
        """Añade un producto (con su cantidad) a la venta y descuenta stock."""
        detalle.producto.descontar_stock(detalle.cantidad)
        self.__detalles.append(detalle)

    def __str__(self) -> str:
        tipo = "FIADO" if self.__es_fiado else "CONTADO"
        cliente_str = f" - Cliente: {self.__cliente.nombre}" if self.__cliente else ""
        cabecera = (f"Venta #{self.__id} [{tipo}] "
                    f"{self.__fecha_hora.strftime('%d/%m/%Y %H:%M')} "
                    f"- Vendedor: {self.__vendedor.nombre}{cliente_str}")
        lineas = "\n".join(f"  - {d}" for d in self.__detalles)
        return f"{cabecera}\n{lineas}\n  TOTAL: S/ {self.total}"