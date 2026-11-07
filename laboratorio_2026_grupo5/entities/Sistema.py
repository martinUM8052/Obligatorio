from datetime import datetime

from entities.CasoUso import CasoUso
from entities.Criterio import Criterio
from entities.Evaluacion import Evaluacion
from entities.OpcionIA import PlanMensual, ServicioAPI
from exceptions.ErrorLaboratorio import ErrorLaboratorio


class Sistema:
    """Guarda las cuatro listas del programa y un contador de códigos por entidad."""

    def __init__(self):
        self.__criterios = []
        self.__opciones = []
        self.__casos = []
        self.__evaluaciones = []
        self.__proximo_codigo_criterio = 1
        self.__proximo_codigo_opcion = 1
        self.__proximo_codigo_caso = 1
        self.__proximo_codigo_evaluacion = 1

    @property
    def criterios(self):
        return self.__criterios

    @property
    def opciones(self):
        return self.__opciones

    @property
    def casos(self):
        return self.__casos

    def validar_nombre(self, registros, nombre):
        """Lanza ErrorLaboratorio si ya hay un registro con ese nombre, sin distinguir mayúsculas."""
        for registro in registros:
            if registro.nombre.lower() == nombre.lower():
                raise ErrorLaboratorio(f"Ya existe un registro llamado {nombre}.")

    def buscar(self, registros, codigo):
        """Devuelve el registro con ese código o lanza ErrorLaboratorio si no existe."""
        for registro in registros:
            if registro.codigo == codigo:
                return registro
        raise ErrorLaboratorio(f"No existe un registro con código {codigo}.")

    def registrar_criterio(self, nombre, peso):
        """Crea un criterio con el próximo código, lo guarda y lo devuelve."""
        criterio = Criterio(self.__proximo_codigo_criterio, nombre, peso)
        self.__criterios.append(criterio)
        self.__proximo_codigo_criterio += 1
        return criterio

    def registrar_servicio_api(self, nombre, puntajes, costo_por_1000, consultas):
        """Crea una opción que se paga por consultas, la guarda y la devuelve."""
        opcion = ServicioAPI(self.__proximo_codigo_opcion, nombre, puntajes,
                             costo_por_1000, consultas)
        self.__opciones.append(opcion)
        self.__proximo_codigo_opcion += 1
        return opcion

    def registrar_plan_mensual(self, nombre, puntajes, usuarios, costo_por_usuario):
        """Crea una opción que se paga por usuario, la guarda y la devuelve."""
        opcion = PlanMensual(self.__proximo_codigo_opcion, nombre, puntajes,
                             usuarios, costo_por_usuario)
        self.__opciones.append(opcion)
        self.__proximo_codigo_opcion += 1
        return opcion

    def registrar_caso(self, nombre, presupuesto, puntaje_minimo):
        """Crea un caso de uso sin evaluaciones, lo guarda y lo devuelve."""
        caso = CasoUso(self.__proximo_codigo_caso, nombre, presupuesto, puntaje_minimo)
        self.__casos.append(caso)
        self.__proximo_codigo_caso += 1
        return caso

    def __crear_evaluacion(self, opcion, caso):
        """Crea la evaluación con el próximo código y la fecha actual, la calcula y la guarda."""
        evaluacion = Evaluacion(self.__proximo_codigo_evaluacion, opcion, caso, datetime.now())
        evaluacion.recalcular(self.__criterios)
        self.__evaluaciones.append(evaluacion)
        self.__proximo_codigo_evaluacion += 1
        return evaluacion

    def evaluar(self, opcion, caso):
        """Crea la evaluación de una opción para un caso; lanza ErrorLaboratorio si ya existe."""
        for evaluacion in self.evaluaciones_de_caso(caso):
            if evaluacion.opcion.codigo == opcion.codigo:
                raise ErrorLaboratorio(
                    f"Ya existe una evaluación de {opcion.nombre} para {caso.nombre}.")
        return self.__crear_evaluacion(opcion, caso)

    def comparar_caso(self, caso):
        """Reemplaza todas las evaluaciones del caso por una por cada opción registrada.

        Conserva las evaluaciones de los otros casos; el contador de códigos no se reinicia.
        """
        conservadas = []
        for evaluacion in self.__evaluaciones:
            if evaluacion.caso.codigo != caso.codigo:
                conservadas.append(evaluacion)
        self.__evaluaciones = conservadas
        for opcion in self.__opciones:
            self.__crear_evaluacion(opcion, caso)

    def recalcular(self, evaluaciones):
        """Recalcula el estado de las evaluaciones indicadas; no cambia códigos, fechas ni puntajes."""
        for evaluacion in evaluaciones:
            evaluacion.recalcular(self.__criterios)

    def actualizar_presupuesto(self, caso, nuevo):
        """Cambia el presupuesto del caso y recalcula solo las evaluaciones de ese caso."""
        caso.presupuesto = nuevo
        self.recalcular(self.evaluaciones_de_caso(caso))

    def actualizar_costos_opcion(self, opcion, primer_valor, segundo_valor):
        """Cambia los costos de la opción y recalcula sus evaluaciones en todos los casos."""
        opcion.actualizar_costos(primer_valor, segundo_valor)
        afectadas = []
        for evaluacion in self.__evaluaciones:
            if evaluacion.opcion.codigo == opcion.codigo:
                afectadas.append(evaluacion)
        self.recalcular(afectadas)

    def evaluaciones_de_caso(self, caso):
        """Devuelve una lista nueva con las evaluaciones del caso indicado."""
        resultado = []
        for evaluacion in self.__evaluaciones:
            if evaluacion.caso.codigo == caso.codigo:
                resultado.append(evaluacion)
        return resultado

    def ranking_caso(self, caso):
        """Devuelve las evaluaciones recomendadas del caso, de mejor a peor.

        Orden: mayor puntaje sin redondear, menor costo (redondeado a 6 decimales
        para ignorar el ruido de los decimales) y menor código de opción.
        """
        recomendadas = []
        for evaluacion in self.evaluaciones_de_caso(caso):
            if evaluacion.estado == Evaluacion.RECOMENDADA:
                recomendadas.append(evaluacion)
        return sorted(recomendadas, key=lambda evaluacion: (
            -evaluacion.puntaje_total(self.__criterios),
            round(evaluacion.costo_total(), 6),
            evaluacion.opcion.codigo))
