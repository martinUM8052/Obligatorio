class Evaluacion:
    """Evaluación de una opción de IA para un caso de uso."""

    RECOMENDADA = "Recomendada"
    FUERA_DE_PRESUPUESTO = "Fuera de presupuesto"
    PUNTAJE_INSUFICIENTE = "Puntaje insuficiente"

    def __init__(self, codigo, opcion, caso, fecha):
        self.__codigo = codigo
        self.__opcion = opcion
        self.__caso = caso
        self.__fecha = fecha
        self.__estado = ""

    @property
    def codigo(self):
        return self.__codigo

    @property
    def opcion(self):
        return self.__opcion

    @property
    def caso(self):
        return self.__caso

    @property
    def fecha(self):
        return self.__fecha

    @property
    def estado(self):
        return self.__estado

    def puntaje_total(self, criterios):
        """Devuelve suma(puntaje × peso) / suma de pesos, sin redondear."""
        puntajes = self.__opcion.puntajes
        suma_ponderada = 0
        suma_pesos = 0
        posicion = 0
        while posicion < len(criterios):
            criterio = criterios[posicion]
            suma_ponderada += puntajes[criterio.codigo] * criterio.peso
            suma_pesos += criterio.peso
            posicion += 1
        return suma_ponderada / suma_pesos

    def costo_total(self):
        return self.__opcion.costo_estimado()

    def recalcular(self, criterios):
        """Fija el estado en el orden de la letra; la igualdad con cada límite es válida."""
        # Redondeo para que 5 × 5.99 sea igual a 29.95.
        if round(self.costo_total() - self.__caso.presupuesto, 6) > 0:
            self.__estado = Evaluacion.FUERA_DE_PRESUPUESTO
        elif self.puntaje_total(criterios) < self.__caso.puntaje_minimo:
            self.__estado = Evaluacion.PUNTAJE_INSUFICIENTE
        else:
            self.__estado = Evaluacion.RECOMENDADA
