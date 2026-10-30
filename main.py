import casoUso from casoUso
import Criterio from Criterio
import Evaluacion from Evaluacion
import OpcionIA from OpcionIA
import Sistema from Sistema

def leer_opcion():
    return input("Seleccione una opción: ").strip()


def menu_principal():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registrar")
        print("2. Comparar opciones para un caso")
        print("3. Actualizar")
        print("4. Listar")
        print("5. Salir del sistema")

        match leer_opcion():
            case "1":
                menu_registrar()
            case "2":
                print("Comparar opciones para un caso")
            case "3":
                menu_actualizar()
            case "4":
                menu_listar()
            case "5":
                print("Saliendo del sistema...")
                break
            case _:
                print("Opción incorrecta. Intente nuevamente.")


def menu_registrar():
    while True:
        print("\n--- REGISTRAR ---")
        print("1. Criterio")
        print("2. Opción de IA")
        print("3. Caso de uso")
        print("4. Evaluación individual")
        print("5. Salir")

        match leer_opcion():
            case "1":
                print("Registrar criterio")

            case "2":
                print("Registrar opción de IA")
            case "3":
                print("Registrar caso de uso")
            case "4":
                print("Registrar evaluación individual")
            case "5":
                print("Volviendo al menú principal...")
                break
            case _:
                print("Opción incorrecta. Intente nuevamente.")


def menu_actualizar():
    while True:
        print("\n--- ACTUALIZAR ---")
        print("1. Presupuesto de un caso")
        print("2. Precio o consumo de una opción")
        print("3. Salir")

        match leer_opcion():
            case "1":
                print("Actualizar presupuesto de un caso")
            case "2":
                print("Actualizar precio o consumo de una opción")
            case "3":
                print("Volviendo al menú principal...")
                break
            case _:
                print("Opción incorrecta. Intente nuevamente.")


def menu_listar():
    while True:
        print("\n--- LISTAR ---")
        print("1. Criterios")
        print("2. Opciones")
        print("3. Casos de uso")
        print("4. Evaluaciones de un caso")
        print("5. Ranking de un caso")
        print("6. Salir")

        match leer_opcion():
            case "1":
                print("Listar criterios")
            
            case "2":
                print("Listar opciones")

            case "3":
                print("Listar casos de uso")
            case "4":
                print("Listar evaluaciones de un caso")
            case "5":
                print("Mostrar ranking de un caso")
            case "6":
                print("Volviendo al menú principal...")
                break
            case _:
                print("Opción incorrecta. Intente nuevamente.")


if __name__ == "__main__":
    menu_principal()
