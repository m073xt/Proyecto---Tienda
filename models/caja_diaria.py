"""
Módulo caja_diaria
--------------------
Define la clase CajaDiaria: reemplaza al cuaderno diario, registrando
todas las ventas del día y los pagos de deuda que se van cobrando.
"""

from datetime import date

from models.venta import Venta
from models.cliente import Cliente


class CajaDiaria:
    """Registra las ventas y los pagos de deuda de un día específico."""

    def __init__(self, fecha: date = None):
        self.__fecha = fecha or date.today()
        self.__ventas_dia: list[Venta] = []
        self.__pagos_deuda: list[tuple] = []  # (Cliente, monto)

    # ---------- Propiedades ----------
    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def ventas_dia(self) -> list:
        return list(self.__ventas_dia)

    @property
    def pagos_deuda(self) -> list:
        return list(self.__pagos_deuda)

    # ---------- Métodos ----------
    def registrar_venta(self, venta: Venta) -> None:
        """Agrega una venta (contado o fiada) al registro del día."""
        self.__ventas_dia.append(venta)
        if venta.es_fiado and venta.cliente is not None:
            venta.cliente.agregar_venta_fiada(venta)

    def registrar_pago(self, cliente: Cliente, monto: float) -> None:
        """Registra que un cliente abonó `monto` a su deuda."""
        if monto <= 0:
            raise ValueError("El monto pagado debe ser mayor a 0")
        self.__pagos_deuda.append((cliente, monto))
        cliente.registrar_abono(monto)      # Notificamos al cliente para que descuente su deuda

    def total_ventas_dia(self) -> float:
        return sum(venta.total for venta in self.__ventas_dia)

    def total_efectivo_dia(self) -> float:
        return sum(venta.total for venta in self.__ventas_dia if not venta.es_fiado)

    def total_fiado_dia(self) -> float:
        return sum(venta.total for venta in self.__ventas_dia if venta.es_fiado)

    def __str__(self) -> str:
        return (f"Caja del {self.__fecha.strftime('%d/%m/%Y')}: "
                f"{len(self.__ventas_dia)} ventas - "
                f"Efectivo: S/ {self.total_efectivo_dia()} - "
                f"Fiado: S/ {self.total_fiado_dia()}")