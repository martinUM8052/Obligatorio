from abc import ABC, abstractmethod


class OpcionIA(ABC):
    """Opción de IA abstracta. Los puntajes son un diccionario {codigo_criterio: puntaje}."""

    def __init__(self, codigo, nombre, puntajes):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__puntajes = puntajes

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def puntajes(self):
        return self.__puntajes

    @abstractmethod
    def costo_estimado(self):
        """Devuelve el costo mensual estimado; cada clase derivada escribe el suyo."""
        pass


class ServicioAPI(OpcionIA):
    """Opción que se paga por consultas a una API."""

    def __init__(self, codigo, nombre, puntajes, costo_por_1000, consultas_estimadas):
        super().__init__(codigo, nombre, puntajes)
        self.__costo_por_1000 = costo_por_1000
        self.__consultas_estimadas = consultas_estimadas

    @property
    def costo_por_1000(self):
        return self.__costo_por_1000

    @property
    def consultas_estimadas(self):
        return self.__consultas_estimadas

    @property
    def tipo(self):
        return "Servicio API"

    def costo_estimado(self):
        """Costo mensual = (consultas mensuales / 1000) × precio por cada 1000."""
        return self.__consultas_estimadas / 1000 * self.__costo_por_1000

    def descripcion_costos(self):
        return (f"USD {self.__costo_por_1000:.2f} por cada 1000 consultas, "
                f"{self.__consultas_estimadas} consultas estimadas")

    def actualizar_costos(self, costo_por_1000, consultas_estimadas):
        self.__costo_por_1000 = costo_por_1000
        self.__consultas_estimadas = consultas_estimadas


class PlanMensual(OpcionIA):
    """Opción que se paga por usuario y por mes."""

    def __init__(self, codigo, nombre, puntajes, usuarios, costo_por_usuario):
        super().__init__(codigo, nombre, puntajes)
        self.__usuarios = usuarios
        self.__costo_por_usuario = costo_por_usuario

    @property
    def usuarios(self):
        return self.__usuarios

    @property
    def costo_por_usuario(self):
        return self.__costo_por_usuario

    @property
    def tipo(self):
        return "Plan mensual"

    def costo_estimado(self):
        """Costo mensual = usuarios × costo por usuario."""
        return self.__usuarios * self.__costo_por_usuario

    def descripcion_costos(self):
        return (f"{self.__usuarios} usuarios, "
                f"USD {self.__costo_por_usuario:.2f} por usuario")

    def actualizar_costos(self, usuarios, costo_por_usuario):
        self.__usuarios = usuarios
        self.__costo_por_usuario = costo_por_usuario
