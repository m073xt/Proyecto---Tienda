class Cliente:
    """Representa a un cliente con cuenta fiada en la tienda."""

    def __init__(self, id_: int, nombre: str):
        self.__id = id_
        self.__nombre = nombre
        self.__compras_mes = []  #lista de ventas fiadas (Venta) del mes
        self.__pagos_mes = 0.0
    # ---------- Propiedades ----------
    @property
    def id(self) -> int:
        return self.__id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def compras_mes(self) -> list:
        return list(self.__compras_mes)  # copia, para no exponer la lista real

    @property
    def deuda_total(self) -> float:
        # La deuda es lo que compró MENOS lo que ya pagó
        comprado = sum(venta.total for venta in self.__compras_mes)
        return max(0.0, comprado - self.__pagos_mes)

    # ---------- Métodos ----------
    def agregar_venta_fiada(self, venta) -> None:
        """Registra una venta fiada en la cuenta del cliente."""
        if not venta.es_fiado:
            raise ValueError("Solo se pueden agregar ventas marcadas como fiadas")
        self.__compras_mes.append(venta)

    def liquidar_cuenta_mes(self) -> float:
        """Cierra el mes: devuelve el saldo pendiente y reinicia la cuenta."""
        saldo_pendiente = self.deuda_total
        self.__compras_mes = []
        self.__pagos_mes = 0.0
        return saldo_pendiente

    def registrar_abono(self, monto: float) -> None:
        """Suma un abono a la cuenta del cliente."""
        if monto <= 0:
            raise ValueError("El monto del abono debe ser mayor a 0")
        self.__pagos_mes += monto

    def __str__(self) -> str:
        return f"{self.__nombre} - deuda actual: S/ {self.deuda_total}"