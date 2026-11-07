class CasoUso:
    """Caso de uso con un presupuesto mensual y un puntaje mínimo."""

    def __init__(self, codigo, nombre, presupuesto, puntaje_minimo):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__presupuesto = presupuesto
        self.__puntaje_minimo = puntaje_minimo

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def presupuesto(self):
        return self.__presupuesto

    @presupuesto.setter
    def presupuesto(self, nuevo_presupuesto):
        self.__presupuesto = nuevo_presupuesto

    @property
    def puntaje_minimo(self):
        return self.__puntaje_minimo
