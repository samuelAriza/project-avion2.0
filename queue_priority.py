#Definicion de prioridades
#Emergencia
#Especial
#Militar
#Comercial
import json
from operator import attrgetter
filename = "data.json"
from datetime import datetime

class QueuePriority:
    def __init__(self):
        self._list = []
        self.size = 0
    def glue(self, item):
        with open(item, "r+") as file:
            data = json.load(file)
        print(type(data[0]["hora"]))

        for i in range(0, len(data)):
             data[i]["hora"] = datetime.strptime(data[i]["hora"], '%Y-%m-%d %H:%M:%S')
        
        data_order = sorted(data, key=lambda x: x["hora"])

        for j in range(0, len(data_order)):
            data_order[j]["hora"] = data_order[j]["hora"].strftime('%Y-%m-%d %H:%M:%S')


        with open(filename, "w") as file_order:
            json.dump(data_order, file_order, indent=4)
        
        self._list.append(data_order)
        self.size = self.size + 1
    def unglue(self):
        first = None
        if(len(self._list) > 0):
             first = self._list[0]
             self._list = self._list[1:]
             self.size = self.size - 1       
        else: 
            raise ValueError("The queue is empty")
        return first
    def __str__(self):
        for i in range(0, len(self._list)):
             print(self._list[i])
    def get_first(self):
         first = self._list[0]