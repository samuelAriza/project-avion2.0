#Definicion de prioridades
#Emergencia
#Especial
#Militar
#Comercial
import json
from operator import attrgetter
filename = "data.json"
from datetime import datetime
import random

#Clase QueuePriority : Cola que organiza segun la prioridad de hora. El metodo encolar recibe un item que es un archivo de tipo .json. y las ordena segun la hora, metodo desencolar, meto __str__ para mostrar las colas, metodo get_first para retornar el primero de la lista, metodo get_size para retornar el tamano de la lista y el metodo penalization que realiza la penalizacion de los vuelos que estan Delayed de a lo sumo 10 posiciones
class QueuePriority:
    def __init__(self):
        self._list = []
        self.size = 0
    def glue(self, item):
        data_order = []
        with open(item, "r+") as file:
            data = json.load(file)

        if len(data)!= 0:
            for i in range(0, len(data)):
                data[i]["hora"] = datetime.strptime(data[i]["hora"], '%Y-%m-%d %H:%M')
        
            data_order = sorted(data, key=lambda x: x["hora"])

            for j in range(0, len(data_order)):
                data_order[j]["hora"] = data_order[j]["hora"].strftime('%Y-%m-%d %H:%M')

        #Archivo auxiliar para ver las colas
        with open("colas.json", "r+") as colas:
            cola = json.load(colas)
        cola.append(data_order)
        
        for i in range(0, len(data_order)):
            self._list.append(data_order[i])

        with open("colas.json", "w") as colas:
            json.dump(cola, colas, indent=4)

        self.size = len(data_order)
    def unglue(self):
        first = None
        if(len(self._list) > 0):
            self._list.pop(0)    
            self.size = self.size - 1   
        else: 
            raise ValueError("The queue is empty")
        return first
    def __str__(self):
        for i in range(0, len(self._list)):
             print(self._list[i])
    def get_first(self):
        if(len(self._list) > 0):
            first = self._list[0]
            return first
        else:
            return []
    def get_size(self):
        return self.size
    def penalization(self, type):
        if(type == "exit"):
            tipo = "salida"
        else:
            tipo = "entrada"
        if(len(self._list) > 0):
            print(f'| Avion {self._list[0]["numero_vuelo"]} | Hora de {tipo} : {self._list[0]["hora"]} esta retrasado.')
            self._list[0]["estado"] = "On time"
            number = random.randint(1, 10)
            self._list.insert(number, self._list[0])
            self._list.pop(0)
            
