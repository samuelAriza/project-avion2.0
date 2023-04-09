import queue_priority
import json
import generator

#Emergencia
#Especial
#Militar 
#Comercial
def initialize():
    with open("colas.json", "w") as file_colas:
        json.dump([], file_colas, indent=4)

    with open("data_entry.json", "w") as data_entry:
        json.dump([], data_entry, indent=4)

    with open("data_exit.json", "w") as data_exit:
        json.dump([], data_exit, indent=4)

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
exit_track = {"exit1": True, "exit2":True, "exit3":True, "exit4":True}
entry_track = {"entry1": True, "entry2":True, "entry3":True, "entry4":True}


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

print("Iniciar simulacion")
generator.save_as_json("data_exit.json", 5, "Salida")
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

#Mirar cual es el proximo a salir
print("COLA")
print("")

exit_emergency.__str__()

print("PRIMER ELEMENTO")
print(exit_emergency.get_first())