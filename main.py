def menu_principal():
    opcion = 0

    while opcion != 5:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registrar")
        print("2. Comparar opciones para un caso")
        print("3. Actualizar")
        print("4. Listar")
        print("5. Salir del sistema")

        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            menu_registrar()
        elif opcion == 2:
            print("Comparar opciones para un caso")
        elif opcion == 3:
            menu_actualizar()
        elif opcion == 4:
            menu_listar()
        elif opcion == 5:
            print("Saliendo del sistema...")
        else:
            print("Opción incorrecta. Intente nuevamente.")


def menu_registrar():
    opcion = 0

    while opcion != 5:
        print("\n--- REGISTRAR ---")
        print("1. Criterio")
        print("2. Opción de IA")
        print("3. Caso de uso")
        print("4. Evaluación individual")
        print("5. Salir")

        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            print("Registrar criterio")
        elif opcion == 2:
            print("Registrar opción de IA")
        elif opcion == 3:
            print("Registrar caso de uso")
        elif opcion == 4:
            print("Registrar evaluación individual")
        elif opcion == 5:
            print("Volviendo al menú principal...")
        else:
            print("Opción incorrecta. Intente nuevamente.")


def menu_actualizar():
    opcion = 0

    while opcion != 3:
        print("\n--- ACTUALIZAR ---")
        print("1. Presupuesto de un caso")
        print("2. Precio o consumo de una opción")
        print("3. Salir")

        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            print("Actualizar presupuesto de un caso")
        elif opcion == 2:
            print("Actualizar precio o consumo de una opción")
        elif opcion == 3:
            print("Volviendo al menú principal...")
        else:
            print("Opción incorrecta. Intente nuevamente.")


def menu_listar():
    opcion = 0

    while opcion != 6:
        print("\n--- LISTAR ---")
        print("1. Criterios")
        print("2. Opciones")
        print("3. Casos de uso")
        print("4. Evaluaciones de un caso")
        print("5. Ranking de un caso")
        print("6. Salir")

        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            print("Listar criterios")
        elif opcion == 2:
            print("Listar opciones")
        elif opcion == 3:
            print("Listar casos de uso")
        elif opcion == 4:
            print("Listar evaluaciones de un caso")
        elif opcion == 5:
            print("Mostrar ranking de un caso")
        elif opcion == 6:
            print("Volviendo al menú principal...")
        else:
            print("Opción incorrecta. Intente nuevamente.")

menu_principal()

