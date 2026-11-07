from entities.OpcionIA import ServicioAPI
from entities.Sistema import Sistema
from exceptions.ErrorLaboratorio import ErrorLaboratorio


FORMATO_FECHA = "%d/%m/%Y %H:%M:%S"


def leer_entero(mensaje, minimo=None, maximo=None):
    """Pide un entero hasta que sea válido y esté dentro del rango indicado."""
    while True:
        try:
            valor = int(input(mensaje))
        except ValueError:
            print("Ingrese un número entero.")
            continue
        if minimo is not None and valor < minimo:
            print(f"Ingrese un número mayor o igual que {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"Ingrese un número menor o igual que {maximo}.")
        else:
            return valor


def leer_flotante(mensaje, minimo=None, maximo=None):
    """Pide un número decimal hasta que sea válido y esté dentro del rango indicado."""
    while True:
        try:
            valor = float(input(mensaje))
        except ValueError:
            print("Ingrese un número.")
            continue
        if minimo is not None and valor < minimo:
            print(f"Ingrese un número mayor o igual que {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"Ingrese un número menor o igual que {maximo}.")
        else:
            return valor


def leer_texto(mensaje):
    """Pide un texto hasta que no esté vacío después de quitar los espacios."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El texto no puede estar vacío.")


def leer_nombre_nuevo(sistema, mensaje, registros):
    """Pide un nombre y lo repite mientras ya exista en los registros."""
    while True:
        nombre = leer_texto(mensaje)
        try:
            sistema.validar_nombre(registros, nombre)
            return nombre
        except ErrorLaboratorio as error:
            print(f"Error: {error}")


def pedir_puntajes(criterios):
    """Pide un puntaje entero de 0 a 10 por cada criterio y devuelve {codigo: puntaje}."""
    puntajes = {}
    for criterio in criterios:
        puntajes[criterio.codigo] = leer_entero(
            f"Puntaje para {criterio.nombre} (0 a 10): ", 0, 10)
    return puntajes


def seleccionar_opcion(sistema):
    """Lista las opciones y pide un código; devuelve la opción o None si no hay opciones."""
    if not sistema.opciones:
        print("No hay opciones registradas para seleccionar.")
        return None
    listar_opciones(sistema)
    while True:
        codigo = leer_entero("Código de la opción: ")
        try:
            return sistema.buscar(sistema.opciones, codigo)
        except ErrorLaboratorio as error:
            print(f"Error: {error}")


def seleccionar_caso(sistema):
    """Lista los casos y pide un código; devuelve el caso o None si no hay casos."""
    if not sistema.casos:
        print("No hay casos de uso registrados para seleccionar.")
        return None
    listar_casos(sistema)
    while True:
        codigo = leer_entero("Código del caso de uso: ")
        try:
            return sistema.buscar(sistema.casos, codigo)
        except ErrorLaboratorio as error:
            print(f"Error: {error}")


def mostrar_evaluacion(sistema, evaluacion):
    """Muestra una evaluación: código, fecha, opción, caso, puntaje, costo y estado."""
    puntaje = evaluacion.puntaje_total(sistema.criterios)
    print(f"Código: {evaluacion.codigo} | "
          f"Fecha: {evaluacion.fecha.strftime(FORMATO_FECHA)} | "
          f"Opción: {evaluacion.opcion.nombre} | Caso: {evaluacion.caso.nombre} | "
          f"Puntaje: {puntaje:.2f} | Costo: USD {evaluacion.costo_total():.2f} | "
          f"Estado: {evaluacion.estado}")


def mostrar_evaluaciones(sistema, evaluaciones):
    """Muestra una línea por evaluación, con el presupuesto actual de su caso."""
    for evaluacion in evaluaciones:
        puntaje = evaluacion.puntaje_total(sistema.criterios)
        print(f"Código: {evaluacion.codigo} | "
              f"Fecha: {evaluacion.fecha.strftime(FORMATO_FECHA)} | "
              f"Opción: {evaluacion.opcion.nombre} | "
              f"Presupuesto: USD {evaluacion.caso.presupuesto:.2f} | "
              f"Costo: USD {evaluacion.costo_total():.2f} | "
              f"Puntaje: {puntaje:.2f} | Estado: {evaluacion.estado}")


def registrar_criterio(sistema):
    """Registra un criterio; no se admiten criterios nuevos si ya hay opciones."""
    if sistema.opciones:
        print("Ya hay opciones registradas: no se admiten nuevos criterios.")
        return
    nombre = leer_nombre_nuevo(sistema, "Nombre del criterio: ", sistema.criterios)
    peso = leer_entero("Peso del criterio (entero mayor o igual que 1): ", 1)
    criterio = sistema.registrar_criterio(nombre, peso)
    print(f"Criterio registrado con código {criterio.codigo}.")


def registrar_opcion(sistema):
    """Registra una opción de IA: nombre, tipo, datos de costo y puntajes."""
    if not sistema.criterios:
        print("Debe existir al menos un criterio para registrar opciones.")
        return
    nombre = leer_nombre_nuevo(sistema, "Nombre de la opción: ", sistema.opciones)
    print("1. Servicio API")
    print("2. Plan mensual")
    tipo = leer_entero("Tipo de opción: ", 1, 2)
    if tipo == 1:
        costo_por_1000 = leer_flotante("Precio en USD por cada 1000 consultas: ", 0)
        consultas = leer_entero("Consultas mensuales estimadas: ", 1)
        puntajes = pedir_puntajes(sistema.criterios)
        opcion = sistema.registrar_servicio_api(nombre, puntajes, costo_por_1000, consultas)
    else:
        usuarios = leer_entero("Cantidad de usuarios: ", 1)
        costo_por_usuario = leer_flotante("Costo mensual en USD por usuario: ", 0)
        puntajes = pedir_puntajes(sistema.criterios)
        opcion = sistema.registrar_plan_mensual(nombre, puntajes, usuarios, costo_por_usuario)
    print(f"Opción registrada con código {opcion.codigo}.")


def registrar_caso(sistema):
    """Registra un caso de uso con presupuesto y puntaje mínimo."""
    nombre = leer_nombre_nuevo(sistema, "Nombre del caso de uso: ", sistema.casos)
    presupuesto = leer_flotante("Presupuesto mensual en USD: ", 0)
    puntaje_minimo = leer_flotante("Puntaje mínimo aceptable (0 a 10): ", 0, 10)
    caso = sistema.registrar_caso(nombre, presupuesto, puntaje_minimo)
    print(f"Caso registrado con código {caso.codigo}.")


def registrar_evaluacion(sistema):
    """Evalúa una opción para un caso y muestra el resultado."""
    if not sistema.casos:
        print("No hay casos de uso registrados para seleccionar.")
        return
    opcion = seleccionar_opcion(sistema)
    if opcion is None:
        return
    caso = seleccionar_caso(sistema)
    if caso is None:
        return
    try:
        evaluacion = sistema.evaluar(opcion, caso)
    except ErrorLaboratorio as error:
        print(f"Error: {error}")
        return
    mostrar_evaluacion(sistema, evaluacion)


def listar_criterios(sistema):
    """Muestra una línea por criterio: código, nombre y peso."""
    if not sistema.criterios:
        print("No hay criterios registrados.")
        return
    for criterio in sistema.criterios:
        print(f"Código: {criterio.codigo} | Nombre: {criterio.nombre} | Peso: {criterio.peso}")


def texto_puntajes(criterios, opcion):
    """Devuelve el texto de los puntajes de una opción, uno por criterio."""
    partes = []
    for criterio in criterios:
        partes.append(f"{criterio.nombre} {opcion.puntajes[criterio.codigo]}")
    return ", ".join(partes)


def listar_opciones(sistema):
    """Muestra una línea por opción con su tipo, datos de costo, costo mensual y puntajes."""
    if not sistema.opciones:
        print("No hay opciones registradas.")
        return
    for opcion in sistema.opciones:
        print(f"Código: {opcion.codigo} | Nombre: {opcion.nombre} | Tipo: {opcion.tipo} | "
              f"Datos: {opcion.descripcion_costos()} | "
              f"Costo mensual: USD {opcion.costo_estimado():.2f} | "
              f"Puntajes: {texto_puntajes(sistema.criterios, opcion)}")


def listar_casos(sistema):
    """Muestra una línea por caso con la cantidad de evaluaciones recomendadas."""
    if not sistema.casos:
        print("No hay casos de uso registrados.")
        return
    for caso in sistema.casos:
        recomendadas = len(sistema.ranking_caso(caso))
        print(f"Código: {caso.codigo} | Nombre: {caso.nombre} | "
              f"Presupuesto: USD {caso.presupuesto:.2f} | "
              f"Puntaje mínimo: {caso.puntaje_minimo:.2f} | Recomendadas: {recomendadas}")


def listar_evaluaciones(sistema):
    """Muestra las evaluaciones del caso elegido."""
    caso = seleccionar_caso(sistema)
    if caso is None:
        return
    evaluaciones = sistema.evaluaciones_de_caso(caso)
    if not evaluaciones:
        print(f"No hay evaluaciones para {caso.nombre}.")
        return
    mostrar_evaluaciones(sistema, evaluaciones)


def listar_ranking(sistema):
    """Muestra el ranking de las evaluaciones recomendadas del caso elegido."""
    caso = seleccionar_caso(sistema)
    if caso is None:
        return
    ranking = sistema.ranking_caso(caso)
    if not ranking:
        print(f"No hay evaluaciones recomendadas para {caso.nombre}.")
        return
    posicion = 1
    for evaluacion in ranking:
        puntaje = evaluacion.puntaje_total(sistema.criterios)
        print(f"{posicion}. {evaluacion.opcion.nombre} | Puntaje: {puntaje:.2f} | "
              f"Costo: USD {evaluacion.costo_total():.2f}")
        posicion += 1


def comparar(sistema):
    """Compara todas las opciones para un caso y muestra las evaluaciones creadas."""
    if not sistema.opciones:
        print("No hay opciones registradas para comparar.")
        return
    caso = seleccionar_caso(sistema)
    if caso is None:
        return
    sistema.comparar_caso(caso)
    mostrar_evaluaciones(sistema, sistema.evaluaciones_de_caso(caso))


def actualizar_presupuesto(sistema):
    """Cambia el presupuesto de un caso; sus evaluaciones se recalculan."""
    caso = seleccionar_caso(sistema)
    if caso is None:
        return
    nuevo = leer_flotante("Nuevo presupuesto mensual en USD: ", 0)
    sistema.actualizar_presupuesto(caso, nuevo)
    print(f"Presupuesto de {caso.nombre} actualizado a USD {caso.presupuesto:.2f}.")


def actualizar_precio(sistema):
    """Cambia el precio o consumo de una opción; sus evaluaciones se recalculan."""
    opcion = seleccionar_opcion(sistema)
    if opcion is None:
        return
    if isinstance(opcion, ServicioAPI):
        primer_valor = leer_flotante("Nuevo precio en USD por cada 1000 consultas: ", 0)
        segundo_valor = leer_entero("Nuevas consultas mensuales estimadas: ", 1)
    else:
        primer_valor = leer_entero("Nueva cantidad de usuarios: ", 1)
        segundo_valor = leer_flotante("Nuevo costo mensual en USD por usuario: ", 0)
    sistema.actualizar_costos_opcion(opcion, primer_valor, segundo_valor)
    print(f"Opción {opcion.nombre} actualizada: costo mensual USD {opcion.costo_estimado():.2f}.")


def main():
    """Crea el sistema y muestra el menú principal hasta que se elija salir."""
    sistema = Sistema()
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registrar")
        print("2. Comparar opciones para un caso")
        print("3. Actualizar")
        print("4. Listar")
        print("5. Salir del sistema")

        match leer_entero("Seleccione una opción: ", 1, 5):
            case 1:
                menu_registrar(sistema)
            case 2:
                comparar(sistema)
            case 3:
                menu_actualizar(sistema)
            case 4:
                menu_listar(sistema)
            case 5:
                print("Programa finalizado.")
                break


def menu_registrar(sistema):
    """Submenú Registrar: se repite hasta elegir Salir."""
    while True:
        print("\n--- REGISTRAR ---")
        print("1. Criterio")
        print("2. Opción de IA")
        print("3. Caso de uso")
        print("4. Evaluación individual")
        print("5. Salir")

        match leer_entero("Seleccione una opción: ", 1, 5):
            case 1:
                registrar_criterio(sistema)
            case 2:
                registrar_opcion(sistema)
            case 3:
                registrar_caso(sistema)
            case 4:
                registrar_evaluacion(sistema)
            case 5:
                break


def menu_actualizar(sistema):
    """Submenú Actualizar: se repite hasta elegir Salir."""
    while True:
        print("\n--- ACTUALIZAR ---")
        print("1. Presupuesto de un caso")
        print("2. Precio o consumo de una opción")
        print("3. Salir")

        match leer_entero("Seleccione una opción: ", 1, 3):
            case 1:
                actualizar_presupuesto(sistema)
            case 2:
                actualizar_precio(sistema)
            case 3:
                break


def menu_listar(sistema):
    """Submenú Listar: se repite hasta elegir Salir."""
    while True:
        print("\n--- LISTAR ---")
        print("1. Criterios")
        print("2. Opciones")
        print("3. Casos de uso")
        print("4. Evaluaciones de un caso")
        print("5. Ranking de un caso")
        print("6. Salir")

        match leer_entero("Seleccione una opción: ", 1, 6):
            case 1:
                listar_criterios(sistema)
            case 2:
                listar_opciones(sistema)
            case 3:
                listar_casos(sistema)
            case 4:
                listar_evaluaciones(sistema)
            case 5:
                listar_ranking(sistema)
            case 6:
                break


if __name__ == "__main__":
    main()
