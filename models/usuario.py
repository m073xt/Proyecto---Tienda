class Usuario:
    """Representa a una persona que puede registrar ventas en el sistema."""

    roles_validos = ("admin", "vendedor")

    def __init__(self, id_: int, nombre: str, rol: str = "vendedor"):
        if rol not in self.roles_validos:
            raise ValueError(f"Rol inválido: {rol}. Use uno de {self.roles_validos}")
        self.__id = id_
        self.__nombre = nombre
        self.__rol = rol

    # ---------- Propiedades ----------
    @property
    def id(self) -> int:
        return self.__id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def rol(self) -> str:
        return self.__rol

    # ---------- Métodos ----------
    def es_admin(self) -> bool:
        return self.__rol == "admin"

    def __str__(self) -> str:
        return f"{self.__nombre} ({self.__rol})"