class Criterio:
    """Criterio de evaluación con un peso entero."""

    def __init__(self, codigo, nombre, peso):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__peso = peso

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def peso(self):
        return self.__peso
