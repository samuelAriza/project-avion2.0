import queue_priority
import json
import generator
from datetime import datetime
import time
from tqdm import tqdm

#Emergencia
#Especial
#Militar 
#Comercial
def initialize():
    with open("colas.json", "w") as file_colas:
        json.dump([], file_colas, indent=4)

    with open("data_entry.json", "w") as data_entry:
        json.dump([], data_entry, indent=4)

    #with open("data_exit.json", "w") as data_exit:
        #json.dump([], data_exit, indent=4)

    with open("entry_commercial.json", "w") as entry_commercial:
        json.dump([], entry_commercial, indent=4)

    with open("entry_emergency.json", "w") as entry_emergency:
        json.dump([], entry_emergency, indent=4)

    with open("entry_military.json", "w") as entry_military:
        json.dump([], entry_military, indent=4)

    with open("entry_special.json", "w") as file:
        json.dump([], file, indent=4)

    with open("exit_commercial.json", "w") as exit_commercial:
        json.dump([], exit_commercial, indent=4)

    with open("exit_emergency.json", "w") as exit_emergency:
        json.dump([], exit_emergency, indent=4)

    with open("exit_military.json", "w") as exit_military:
        json.dump([], exit_military, indent=4)

    with open("exit_special.json", "w") as exit_special:
        json.dump([], exit_special, indent=4)
initialize()

#Pistas iniclamente todas libres
exit_track = [True, True, True, True]
entry_track = [True, True, True, True]


#Creacion de colas de salida
exit_emergency = queue_priority.QueuePriority()
exit_special = queue_priority.QueuePriority()
exit_military = queue_priority.QueuePriority()
exit_commercial = queue_priority.QueuePriority()

#Creacion de colas de llegada
entry_emergency = queue_priority.QueuePriority()
entry_special = queue_priority.QueuePriority()
entry_military = queue_priority.QueuePriority()
entry_commercial = queue_priority.QueuePriority()

#Encolar exit

#Funcion que ordena por prioridad, segun el type: exit o entry
def order(filename, type):
    emergency = []
    special = []
    military = []
    commercial = []
    cancelled = []

    with open(filename, "r+") as file:
        data = json.load(file)

    for i in range(0, len(data)):
        if (data[i]["estado"] != "Cancelled"):
            if(data[i]["prioridad"] == "Emergencia"):
                emergency.append(data[i])
            elif (data[i]["prioridad"] == "Especial"):
                special.append(data[i])
            elif (data[i]["prioridad"] == "Militar"):
                military.append(data[i])
            else:
                commercial.append(data[i])
        else:
            cancelled.append(data[i])
            
    with open(f'{type}_emergency.json', "w") as data_emergency:
        json.dump(emergency, data_emergency, indent=4)

    with open(f'{type}_special.json', "w") as data_special:
        json.dump(special, data_special, indent=4)

    with open(f'{type}_military.json', "w") as data_military:
        json.dump(military, data_military, indent=4)

    with open(f'{type}_commercial.json', "w") as data_commercial:
        json.dump(commercial, data_commercial, indent=4)

print("Iniciar simulacion\n")
#generator.save_as_json("data_exit.json", 5, "Salida")
generator.save_as_json("data_entry.json", 5, "Llegada")


#Ordenar los aviones de salida y enviarlos al archivo correspondiente
order("data_exit.json", "exit")

#Encolar los aviones de salida segun la hora
exit_emergency.glue("exit_emergency.json")
exit_special.glue("exit_special.json")
exit_military.glue("exit_military.json")
exit_commercial.glue("exit_commercial.json")

#Ordenar los aviones de llegada y enviarlos a los archivos correspondientes
order("data_entry.json", "entry")

#Encolar los aviones de llegada segun la hora
entry_emergency.glue("entry_emergency.json")
entry_special.glue("entry_special.json")
entry_military.glue("entry_military.json")
entry_commercial.glue("entry_commercial.json")

def firsts():
    array = []
    assign_track = []
    #[[], {}, [], []]
    array.append(exit_emergency.get_first())
    array.append(exit_special.get_first())
    array.append(exit_military.get_first())
    array.append(exit_commercial.get_first())

    for i in range(0, len(array)):
        if(len(array[i]) != 0):
            assign_track.append(array[i])

    assign_track = sorted(assign_track, key=lambda x: x["hora"])

    #Mirar si hay empate de hora
    if(len(assign_track) > 1):
        data_priority = {"Emergencia":0, "Especial": 1, "Militar": 2, "Comercial":3}
        priority = []
        priority.append(assign_track[0])
        priority.append(assign_track[1])

        if(priority[0]["hora"] == priority[1]["hora"]):
            priority[0]["prioridad"] = data_priority[priority[0]["prioridad"]]
            priority[1]["prioridad"] = data_priority[priority[1]["prioridad"]]

            priority = sorted(priority, key=lambda x: x["prioridad"])

            organize = list(data_priority.keys())

            priority[0]["prioridad"] = organize[priority[0]["prioridad"]]
            priority[1]["prioridad"] = organize[priority[1]["prioridad"]]

    with open("prueba.json", "w") as prueba:
        json.dump(assign_track, prueba, indent=4)

    for i in range(0, len(assign_track)):
        print(f'| Avion {assign_track[i]["numero_vuelo"]} | Hora de salida : {assign_track[i]["hora"]}')
    print("\n")
    print("Proximo avion de salida")
    print(f'| Avion {assign_track[0]["numero_vuelo"]} | Hora de salida : {assign_track[0]["hora"]}')
    print("\n")
    return assign_track

#Asignar pistas para aviones de salida
def assign_track():

    queue_is_empty = False
    flag = True
    while(flag == True):

        assign_track = firsts()
        if(exit_track[0] == True):
            exit_track[0] == False
            print(f'Pista : {0} Asignada a avion con numero de vuelo :  {assign_track[0]["numero_vuelo"]}')
            for i in tqdm(range(0, 100), total=100, desc="Despegando ..."):
                time.sleep(0.05)
            print("\n")
            print(f'Avion con numero de vuelo {assign_track[0]["numero_vuelo"]} | Despegue completado')
            print("\n")
            priority = assign_track[0]["prioridad"]
            if(priority == "Emergencia"):
                exit_emergency.unglue()
            elif (priority == "Especial"):
                exit_special.unglue()
            elif(priority == "Militar"):
                exit_military.unglue()
            else:
                exit_commercial.unglue()
            exit_track[0] == True
        if(len(assign_track) == 1):
            break
        
assign_track()