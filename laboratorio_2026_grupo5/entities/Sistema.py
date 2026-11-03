# =====================================================================
# Sistema.py  (carpeta entities/)
#
# La clase Sistema es el "cerebro" del programa. Guarda las cuatro listas
# (criterios, opciones, casos y evaluaciones), reparte los códigos
# consecutivos y contiene las operaciones: registrar, evaluar, comparar,
# actualizar...
#
# REGLA DE ORO: aquí dentro NO hay input() ni print(). Eso va en main.py.
# El Sistema solo recibe datos ya leídos, los valida y, si algo está mal,
# lanza una excepción (ErrorLaboratorio). main.py la captura, muestra el
# mensaje y vuelve a pedir el dato, así el programa no se cae.
# =====================================================================

# datetime nos da la fecha y hora actuales para cada evaluación
from datetime import datetime

# Importamos las demás clases del proyecto. La ruta sigue la estructura
# de carpetas que pide la pauta: entities/ y exceptions/
from entities.Criterio import Criterio
from entities.OpcionIA import OpcionIA, ServicioAPI, PlanMensual
from entities.CasoUso import CasoUso
from entities.Evaluacion import Evaluacion
from exceptions.ErrorLaboratorio import ErrorLaboratorio


class Sistema:
    def __init__(self):
        # __init__ se ejecuta una sola vez, al hacer Sistema() en main.py.
        # Aquí dejamos el sistema "vacío" y listo para usar.

        # Las cuatro listas del diagrama de clases.
        # El doble guion bajo (__) las hace privadas: desde fuera de la clase
        # no se puede hacer sistema.__criterios. Esto protege los datos
        # (encapsulamiento): solo el Sistema decide cómo se modifican.
        # Los ": list[Criterio]" son solo pistas de tipo para el lector
        # (y el editor); no cambian cómo funciona el código.
        self.__criterios: list[Criterio] = []
        self.__opciones: list[OpcionIA] = []
        self.__casos: list[CasoUso] = []
        self.__evaluaciones: list[Evaluacion] = []

        # Un contador por cada tipo de objeto. Siempre guardan "el código
        # que le toca al próximo". Empiezan en 1 y solo suben.
        # Por qué contadores y no len(lista) + 1: la comparación BORRA
        # evaluaciones viejas, y la pauta dice que los códigos no se
        # reutilizan. Con len() un código podría repetirse; con un contador
        # que solo sube, nunca.
        self.__proximo_codigo_criterio = 1
        self.__proximo_codigo_opcion = 1
        self.__proximo_codigo_caso = 1
        self.__proximo_codigo_evaluacion = 1

    # ------------------------------------------------------------------
    # PROPIEDADES
    # ------------------------------------------------------------------
    # Como las listas son privadas, main.py no puede leerlas directamente.
    # @property crea un "atributo de solo lectura": desde fuera se escribe
    # sistema.criterios (sin paréntesis) y Python ejecuta este método y
    # devuelve la lista. Se usa, por ejemplo, para listar o para recorrer
    # los criterios al pedir los puntajes.
    # Ojo: devuelve la lista real, no una copia. Es lo que hace el profesor,
    # pero desde main.py conviene solo LEERLA, no modificarla.
    @property
    def criterios(self) -> list[Criterio]:
        return self.__criterios

    @property
    def opciones(self) -> list[OpcionIA]:
        return self.__opciones

    @property
    def casos(self) -> list[CasoUso]:
        return self.__casos

    @property
    def evaluaciones(self) -> list[Evaluacion]:
        return self.__evaluaciones

    # ------------------------------------------------------------------
    # BÚSQUEDAS Y AUXILIARES
    # ------------------------------------------------------------------
    def buscar_opcion(self, codigo: int) -> OpcionIA:
        # Recorre las opciones hasta encontrar la que tiene ese código.
        for opcion in self.__opciones:
            if opcion.codigo == codigo:
                return opcion  # encontrada: salimos de la función
        # Si el for termina sin hacer return, no existía.
        # "raise" lanza la excepción: corta la función y avisa del problema.
        raise ErrorLaboratorio("No existe una opción con ese código.")

    def buscar_caso(self, codigo: int) -> CasoUso:
        # Igual que buscar_opcion, pero con los casos de uso.
        for caso in self.__casos:
            if caso.codigo == codigo:
                return caso
        raise ErrorLaboratorio("No existe un caso con ese código.")

    def evaluaciones_del_caso(self, codigo_caso: int) -> list[Evaluacion]:
        # Devuelve una lista NUEVA solo con las evaluaciones de un caso.
        # Sirve para listar, para el ranking y para recalcular.
        resultado = []
        for evaluacion in self.__evaluaciones:
            # evaluacion.caso es una referencia al objeto CasoUso, por eso
            # podemos preguntarle su código con .codigo
            if evaluacion.caso.codigo == codigo_caso:
                resultado.append(evaluacion)
        return resultado

    def evaluaciones_de_la_opcion(self, codigo_opcion: int) -> list[Evaluacion]:
        # Lo mismo, pero filtrando por opción. Lo necesita "actualizar el
        # precio o consumo de una opción", que afecta a TODOS los casos.
        resultado = []
        for evaluacion in self.__evaluaciones:
            if evaluacion.opcion.codigo == codigo_opcion:
                resultado.append(evaluacion)
        return resultado

    def cantidad_recomendadas(self, codigo_caso: int) -> int:
        # Cuenta cuántas evaluaciones de un caso están "Recomendada".
        # Se muestra en el listado de casos. Si el caso no tiene
        # evaluaciones, el for no entra y devuelve 0, como pide la pauta.
        cantidad = 0
        for evaluacion in self.evaluaciones_del_caso(codigo_caso):
            if evaluacion.estado == Evaluacion.RECOMENDADA:
                cantidad += 1
        return cantidad

    @staticmethod
    def __nombre_repetido(elementos: list, nombre: str) -> bool:
        # @staticmethod: este método no usa "self" porque no necesita datos
        # del Sistema; solo recibe una lista y un nombre.
        # Sirve para criterios, opciones y casos (todos tienen .nombre).
        # Se compara en minúsculas porque la pauta dice que los nombres son
        # únicos "sin distinguir mayúsculas": "Claude" y "claude" son iguales.
        for elemento in elementos:
            if elemento.nombre.lower() == nombre.lower():
                return True
        return False

    # ------------------------------------------------------------------
    # REGISTRAR
    # Cada método valida los datos y, si todo está bien, crea el objeto
    # con el código que toca, lo guarda en su lista y sube el contador.
    # ------------------------------------------------------------------
    def registrar_criterio(self, nombre: str, peso: int) -> Criterio:
        # Validaciones: cada "if" que se cumple corta con una excepción.
        if nombre == "":
            raise ErrorLaboratorio("El nombre no puede estar vacío.")
        if peso <= 0:
            raise ErrorLaboratorio("El peso debe ser un entero positivo.")
        # Regla de la pauta: los criterios se registran ANTES de la primera
        # opción. Si ya hay opciones, ya no se pueden agregar criterios
        # (si no, esas opciones no tendrían puntaje para el criterio nuevo).
        if len(self.__opciones) > 0:
            raise ErrorLaboratorio("Ya hay opciones registradas: no se pueden agregar más criterios.")
        if self.__nombre_repetido(self.__criterios, nombre):
            raise ErrorLaboratorio("Ya existe un criterio con ese nombre.")

        # Si llegamos aquí, los datos son válidos: creamos el criterio con
        # el código actual, lo guardamos y avanzamos el contador.
        criterio = Criterio(self.__proximo_codigo_criterio, nombre, peso)
        self.__criterios.append(criterio)
        self.__proximo_codigo_criterio += 1
        return criterio  # devolvemos el objeto para que main.py muestre su código

    def __validar_nueva_opcion(self, nombre: str, puntajes: dict) -> None:
        # Validaciones comunes a los dos tipos de opción, para no repetir
        # código. Empieza por __ porque solo se usa dentro de esta clase.
        if len(self.__criterios) == 0:
            raise ErrorLaboratorio("Debe existir al menos un criterio para registrar opciones.")
        if nombre == "":
            raise ErrorLaboratorio("El nombre no puede estar vacío.")
        if self.__nombre_repetido(self.__opciones, nombre):
            raise ErrorLaboratorio("Ya existe una opción con ese nombre.")
        # TODO: comprobar que "puntajes" (un diccionario {codigo_criterio: puntaje})
        #       tiene exactamente un valor entre 0 y 10 por cada criterio, sin
        #       omisiones ni duplicados. Pista: recorre self.__criterios y mira
        #       si el código de cada uno está en puntajes (con "in").

    def registrar_servicio_api(self, nombre, puntajes, costo_por_1000, consultas_estimadas) -> ServicioAPI:
        # Opción de tipo "Servicio API": se paga por consultas realizadas.
        self.__validar_nueva_opcion(nombre, puntajes)
        # TODO: validar costo_por_1000 >= 0 y consultas_estimadas entero positivo.
        opcion = ServicioAPI(self.__proximo_codigo_opcion, nombre, puntajes,
                             costo_por_1000, consultas_estimadas)
        self.__opciones.append(opcion)
        self.__proximo_codigo_opcion += 1
        return opcion

    def registrar_plan_mensual(self, nombre, puntajes, usuarios, costo_por_usuario) -> PlanMensual:
        # Opción de tipo "Plan mensual": se paga por usuario.
        # Fíjate que ServicioAPI y PlanMensual se guardan en LA MISMA lista
        # (self.__opciones), porque las dos "son" una OpcionIA (herencia).
        self.__validar_nueva_opcion(nombre, puntajes)
        # TODO: validar usuarios entero positivo y costo_por_usuario >= 0.
        opcion = PlanMensual(self.__proximo_codigo_opcion, nombre, puntajes,
                             usuarios, costo_por_usuario)
        self.__opciones.append(opcion)
        self.__proximo_codigo_opcion += 1
        return opcion

    def registrar_caso(self, nombre: str, presupuesto: float, puntaje_minimo: float) -> CasoUso:
        if nombre == "":
            raise ErrorLaboratorio("El nombre no puede estar vacío.")
        if self.__nombre_repetido(self.__casos, nombre):
            raise ErrorLaboratorio("Ya existe un caso con ese nombre.")
        if presupuesto < 0:  # la pauta permite 0, así que solo falla si es negativo
            raise ErrorLaboratorio("El presupuesto no puede ser negativo.")
        if puntaje_minimo < 0 or puntaje_minimo > 10:
            raise ErrorLaboratorio("El puntaje mínimo debe estar entre 0 y 10.")

        caso = CasoUso(self.__proximo_codigo_caso, nombre, presupuesto, puntaje_minimo)
        self.__casos.append(caso)
        self.__proximo_codigo_caso += 1
        # Registrar un caso NO crea evaluaciones automáticamente (pauta).
        return caso

    # ------------------------------------------------------------------
    # CÁLCULO DE UNA EVALUACIÓN
    # Estas reglas viven en UN solo sitio y las usan la evaluación
    # individual, la comparación y el recálculo. La pauta pide que todas
    # usen "las mismas reglas": así, si cambian, se cambian una sola vez.
    # ------------------------------------------------------------------
    def __calcular_puntaje(self, opcion: OpcionIA) -> float:
        # Media ponderada: suma(puntaje × peso) / suma de pesos.
        # Ejemplo: criterio A (peso 3) con 8 y criterio B (peso 1) con 4
        #   → (8*3 + 4*1) / (3+1) = 28 / 4 = 7.0
        suma_ponderada = 0
        suma_pesos = 0
        for criterio in self.__criterios:
            # opcion.puntajes es un diccionario {codigo_criterio: puntaje};
            # lo consultamos con el código de cada criterio.
            suma_ponderada += opcion.puntajes[criterio.codigo] * criterio.peso
            suma_pesos += criterio.peso
        # No dividimos entre 0: registrar_criterio exige pesos positivos y
        # registrar una opción exige al menos un criterio.
        return suma_ponderada / suma_pesos

      # ---- STATICMETHOD Nº 1: __nombre_repetido ----
    # @staticmethod significa: "este método NO recibe self". No sabe nada del
    # objeto Sistema ni toca sus listas (self.__criterios, etc.). Todo lo que
    # necesita se lo pasan por parámetro: la lista donde buscar y el nombre.
    #
    # Por qué lo hice estático:
    #  - Solo hace una cosa: "¿hay en ESTA lista un elemento con ESTE nombre?"
    #  - Como la lista llega por parámetro, el mismo método sirve para
    #    criterios, opciones y casos (los tres tienen el atributo .nombre).
    #    Así no escribo tres veces el mismo bucle.
    #  - Al no llevar self, el lector ve de un vistazo que no modifica nada
    #    del sistema: solo consulta y devuelve True o False.
    #
    # Cómo se llama (ver registrar_criterio, __validar_nueva_opcion y
    # registrar_caso): self.__nombre_repetido(la_lista, nombre)
    # Aunque se llame con "self." delante, Python NO pasa self como argumento
    # a un método estático; por eso aquí solo recibe los dos parámetros
    
    @staticmethod
    def __calcular_estado(costo: float, puntaje: float, caso: CasoUso) -> str:
        # El ORDEN de los if es parte de la regla: primero se mira el
        # presupuesto y solo después el puntaje.
        # Se usan > y < (no >= ni <=) porque la igualdad con cada límite se
        # considera válida: costo == presupuesto NO es "fuera de presupuesto".
        if costo > caso.presupuesto:
            return Evaluacion.FUERA_PRESUPUESTO
        if puntaje < caso.puntaje_minimo:
            return Evaluacion.PUNTAJE_INSUFICIENTE
        return Evaluacion.RECOMENDADA
        # Ojo: aquí se compara el puntaje SIN redondear. Los 2 decimales
        # son solo para mostrarlo (:.2f al imprimir).

    def __crear_evaluacion(self, opcion: OpcionIA, caso: CasoUso) -> Evaluacion:
        # Junta todo: calcula, crea el objeto Evaluacion y lo guarda.
        puntaje = self.__calcular_puntaje(opcion)
        # costo_estimado() es POLIMORFISMO: cada tipo de opción lo calcula
        # a su manera (ServicioAPI por consultas, PlanMensual por usuarios)
        # y aquí no nos importa cuál es. Solo lo llamamos.
        costo = opcion.costo_estimado()
        estado = self.__calcular_estado(costo, puntaje, caso)

        # datetime.now() guarda la fecha y hora de este momento.
        # La evaluación guarda referencias a la opción y al caso (los
        # objetos, no sus códigos), como indica el diagrama de clases.
        evaluacion = Evaluacion(self.__proximo_codigo_evaluacion, datetime.now(),
                                opcion, caso, puntaje, costo, estado)
        self.__evaluaciones.append(evaluacion)
        self.__proximo_codigo_evaluacion += 1
        return evaluacion

    # ------------------------------------------------------------------
    # EVALUACIÓN INDIVIDUAL
    # ------------------------------------------------------------------
    def evaluar_individual(self, codigo_opcion: int, codigo_caso: int) -> Evaluacion:
        # Si la opción o el caso no existen, buscar_* ya lanza el error.
        opcion = self.buscar_opcion(codigo_opcion)
        caso = self.buscar_caso(codigo_caso)

        # Comprobamos que no exista ya una evaluación de ESA combinación
        # opción + caso. Si existe, informamos del duplicado y no creamos otra.
        for evaluacion in self.__evaluaciones:
            if evaluacion.opcion.codigo == codigo_opcion and evaluacion.caso.codigo == codigo_caso:
                raise ErrorLaboratorio("Ya existe una evaluación para esa opción y ese caso.")

        return self.__crear_evaluacion(opcion, caso)

    # ------------------------------------------------------------------
    # COMPARAR (diagrama: comparar_caso)
    # ------------------------------------------------------------------
    def comparar_caso(self, codigo_caso: int) -> list[Evaluacion]:
        # TODO (pasos):
        #  1. Buscar el caso con self.buscar_caso (lanza error si no existe).
        #  2. Si no hay opciones registradas: avisar y no hacer nada más.
        #  3. Quitar de self.__evaluaciones TODAS las del caso (incluidas las
        #     individuales) y NO tocar las de otros casos. Pista: construye
        #     una lista nueva con las evaluaciones cuyo caso NO sea este y
        #     asígnala a self.__evaluaciones.
        #  4. Por cada opción, llamar a self.__crear_evaluacion(opcion, caso).
        #     El contador de códigos sigue subiendo, no se reinicia.
        #  5. Devolver la lista de evaluaciones nuevas.
        raise NotImplementedError

    # ------------------------------------------------------------------
    # ACTUALIZAR Y RECALCULAR
    # ------------------------------------------------------------------
    def recalcular(self, evaluaciones: list[Evaluacion]) -> None:
        # Recibe una lista de evaluaciones y refresca costo y estado.
        # NO cambia código, fecha, opción, caso ni puntaje (la pauta pide
        # conservarlos; el puntaje solo depende de los puntajes por
        # criterio, que no cambian al actualizar precios o presupuestos).
        for evaluacion in evaluaciones:
            costo = evaluacion.opcion.costo_estimado()  # costo con los valores actuales
            estado = self.__calcular_estado(costo, evaluacion.puntaje_total, evaluacion.caso)
            # Necesitas añadir a la clase Evaluacion un método
            # actualizar(self, costo, estado) que cambie esos dos atributos.
            evaluacion.actualizar(costo, estado)

    def actualizar_presupuesto(self, codigo_caso: int, nuevo_presupuesto: float) -> None:
        caso = self.buscar_caso(codigo_caso)
        if nuevo_presupuesto < 0:
            raise ErrorLaboratorio("El presupuesto no puede ser negativo.")
        # Cambiamos el presupuesto del caso (CasoUso necesita un setter,
        # p. ej. con @presupuesto.setter)...
        caso.presupuesto = nuevo_presupuesto
        # ...y recalculamos solo las evaluaciones de ESE caso. Como están
        # enlazadas al objeto caso, ya "ven" el presupuesto nuevo. Si el caso
        # no tiene evaluaciones, la lista está vacía y el recálculo no hace
        # nada: solo cambia el presupuesto, como pide la pauta.
        self.recalcular(self.evaluaciones_del_caso(codigo_caso))

    def actualizar_opcion(self, codigo_opcion: int, valor_1, valor_2) -> None:
        # TODO (pasos):
        #  1. Buscar la opción con self.buscar_opcion.
        #  2. Según su tipo, validar y cambiar sus dos valores propios:
        #       ServicioAPI -> costo por 1000 consultas (>= 0) y consultas
        #                      estimadas (entero positivo)
        #       PlanMensual -> usuarios (entero positivo) y costo por usuario (>= 0)
        #     Para saber el tipo puedes usar isinstance(opcion, ServicioAPI).
        #     Necesitas setters en esas clases.
        #  3. Recalcular las evaluaciones de la opción en TODOS los casos:
        #     self.recalcular(self.evaluaciones_de_la_opcion(codigo_opcion))
        raise NotImplementedError
