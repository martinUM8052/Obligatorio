Laboratorio de Programación 1 (2026) - Comparador de opciones de IA

Nro de equipo: 5

Requisitos
- Python 3.10 o superior.
- No usa librerías externas (solo abc y datetime de la biblioteca estándar).

Cómo ejecutar
Desde esta carpeta:
    python main.py
Si python no está disponible o apunta a otra versión, usar:
    python3 main.py

Estructura
- main.py: menús y entrada por consola.
- entities/: Sistema, OpcionIA (con ServicioAPI y PlanMensual), Criterio, CasoUso, Evaluacion.
- exceptions/: ErrorLaboratorio.

Nota sobre los puntajes
El puntaje total se muestra con dos decimales, pero el estado se decide con el valor sin redondear.
Por eso una evaluación que se muestra como 7.00 (por ejemplo 6.996) puede quedar "Puntaje insuficiente"
frente a un mínimo de 7.
