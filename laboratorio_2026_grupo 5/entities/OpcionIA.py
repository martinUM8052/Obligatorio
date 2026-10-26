from abc import ABC, abstractmethod
from datetime import datetime

class OpcionIA:
     def __init__(self, codigo: int, nombre: str, puntajes: dict):
        self.__codigo = codigo
        self.__nombre = nombre
        self.puntajes = []

class ServicioAPI:
    def __init__(self,costo_por_mil:float, consultas_estimadas:int):
        self.__costo_por_mil = costo_por_mil
        self.__consultas_estimadas = consultas_estimadas

    def costo_estimado(self) -> float:
        return
class Plan_Mensual:
    def __init__(usuarios:int, costo_por_usuario:float):
        self.__costo_por_mil = costo_por_mil
        self.__consultas_estimadas = consultas_estimadas
    
    def costo_estimado(self) -> float:
        return