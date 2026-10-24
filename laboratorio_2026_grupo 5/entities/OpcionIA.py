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

class Plan_Mensual:
    def __init__(usuarios:int, costo_por_usuario:float):
     self.__costo_por_mil = costo_por_mil
     self.__consultas_estimadas = consultas_estimadas
    
    def costo_estimado(self) -> float:

class Evaluacion:
    def __init__(self,codigo:int,opcion:OpcionIA, caso:casoUso , fecha:datetime, estado:str):
    self.__codigo = codigo
    self.__opcion = opcion
    self.__caso = caso
    self.__fecha = datetime.now()

    def Puntaje_total() -> float:

    def costo_total() -> float:
    
     