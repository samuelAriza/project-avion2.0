import queue_priority
import json
import generator
from datetime import datetime
import time
from tqdm import tqdm

#Funcion initialize que crea los archivos json necesarios que usan otras funciones como argumento para funcionar. Crea los archivos json necesarios y por defecto les anade uno par de corchetes
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
exit_track = [True]
entry_track = [True]


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

#Se llama la funcion save_as_json del generador. save_as_json("nombre_archivo.json", # de aviones a generar, tipo: Salida | Llegada)
generator.save_as_json("data_exit.json", 15, "Salida")
generator.save_as_json("data_entry.json", 15, "Llegada")

#Permitir el ingreso de un avion antes de la simulacion y guardarlo en su archivo correspondiente segun el tipo asignado
option = input("Desea ingresar algun avion? y or n\n")
print("\n")

if(option == "y"):
    aerolinea = input("Nombre aerolinea\n")
    numero_vuelo = input("Numero de vuelo\n")
    tipo_vuelo = input("Tipo de vuelo. Salida o Entrada\n")
    aeropuerto_salida = input("Aeropuerto de salida\n")
    aeropuerto_llegada = input("Aeropuerto de llegada\n")
    ciudad_origen = input("Ciudad origen\n")
    ciudad_destino = input("Ciudad destino\n")
    hora = input("Hora\n")
    hora = int(hora)
    minutos = input("Minutos\n")
    minutos = int(minutos)
    duracion = input("Duracion\n")
    duracion = int(duracion)
    prioridad = input("Prioridad : Emergencia, Militar, Comercial o Especial \n")
    estado = input("Estado : On time, Delayed, Canceelled\n")

    register = {
        "aerolinea": aerolinea,
        "numero_vuelo": numero_vuelo,
        "tipo_vuelo": tipo_vuelo,  
        "aeropuerto_salida": aeropuerto_salida,
        "aeropuerto_llegada": aeropuerto_llegada,
        "ciudad_origen": ciudad_origen,
        "ciudad_destino":  ciudad_destino,
        "hora": datetime(2023, 3, 17, hora, minutos).strftime('%Y-%m-%d %H:%M'),
        "duracion": duracion,
        "prioridad": prioridad,
        "estado": estado
    }
    if(tipo_vuelo == "Salida"):
        with open("data_exit.json", "r+") as file:
            data = json.load(file)
        data.append(register)
        with open("data_exit.json", "w") as file:
            json.dump(data, file, indent=4)
    else:
        with open("entry_exit.json", "r+") as file:
            data = json.load(file)
        data.append(register)
        with open("entry_exit.json", "w") as file:
            json.dump(data, file, indent=4)

#!! Iniciar la simulacion !!
print("Iniciar simulacion\n")

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

#Funcion firsts coge los primeros de cada cola para organizarlos segun la hora, resuelve por prioridad en caso de que haya algun empate de hora; resuelve segun la prioridad. Realiza penalizacion de los aviones de salida que estan retrasados
def firsts(value, value_1, value_2, value_3, type):
    def get_first():
        array = []
        assign_track = []
    
        array.append(value.get_first())
        array.append(value_1.get_first())
        array.append(value_2.get_first())
        array.append(value_3.get_first())

        for i in range(0, len(array)):
            if(len(array[i]) != 0):
                assign_track.append(array[i])

        assign_track = sorted(assign_track, key=lambda x: x["hora"])
        return assign_track
    assign_track = get_first()

    #Realizar castigo para los aviones que estan Delayed
    if type == "exit":
        tipo = "salida"
    else:
        tipo = "llegada"
    if (len(assign_track) > 0):
        if(assign_track[0]["tipo_vuelo"] == "Salida"):
            while(assign_track[0]["estado"] == "Delayed"):

                for i in range(0, len(assign_track)):
                    print(f'| Avion {assign_track[i]["numero_vuelo"]} | Hora de {tipo} : {assign_track[i]["hora"]}')
                print("\n")
                if(assign_track[0]["prioridad"] == "Emergencia"):
                    value.penalization(type)
                elif(assign_track[0]["prioridad"] == "Especial"):
                    value_1.penalization(type)
                elif(assign_track[0]["prioridad"] == "Militar"):
                    value_2.penalization(type)
                else:
                    value_3.penalization(type)
                assign_track = get_first()
                print("Penalizacion realizada\n")
                print("Cola nueva\n")

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

    if(len(assign_track) > 0):
        print("-"*60)
        for i in range(0, len(assign_track)):
            if(type == "exit"):
                print(f'| Avion {assign_track[i]["numero_vuelo"]} | Hora de salida : {assign_track[i]["hora"]}')
            else:
                print(f'| Avion {assign_track[i]["numero_vuelo"]} | Hora de llegada : {assign_track[i]["hora"]}')
        print("\n")
        if(type == "exit"):
            print("Proximo avion de salida")
            print(f'| Avion {assign_track[0]["numero_vuelo"]} | Hora de salida : {assign_track[0]["hora"]}')
        else:
            print("Proximo avion de llegada")
            print(f'| Avion {assign_track[0]["numero_vuelo"]} | Hora de salida : {assign_track[0]["hora"]}')
        print("\n")
        return assign_track, len(assign_track)
    else:
        return [], 0

#Asignar pistas para aviones de salida. Llama a la funcion first y realiza el control de las pistas
def assign_track(value, value_1, value_2, value_3, type):

    flag = True
    
    while(flag == True):
        assign_track, length = firsts(value, value_1, value_2, value_3, type)
        if (length > 0):
            if(exit_track[0] == True):
                exit_track[0] = False
                print(f'Pista : {0} Asignada a avion con numero de vuelo :  {assign_track[0]["numero_vuelo"]}')
                if(type == "exit"):
                    for i in tqdm(range(0, 100), total=100, desc="Despegando ..."):
                        time.sleep(0.04)
                    print("\n")
                    print(f'Avion con numero de vuelo {assign_track[0]["numero_vuelo"]} | Despegue completado\n')
                else: 
                    for i in tqdm(range(0, 100), total=100, desc="Aterrizando ..."):
                        time.sleep(0.04)
                    print("\n")
                    print(f'Avion con numero de vuelo {assign_track[0]["numero_vuelo"]} | Aterrizaje completado')

                print("-"*60)
                print("\n")
                priority = assign_track[0]["prioridad"]
                if(priority == "Emergencia"):
                    value.unglue()
                    print(f'Aviones de emergencia en lista de espera :  | {value.get_size()}\n')
                elif (priority == "Especial"):
                    value_1.unglue()
                    print(f'Aviones de especial en lista de espera :  | {value_1.get_size()}\n')

                elif(priority == "Militar"):
                    value_2.unglue()
                    print(f'Aviones de militar en lista de espera :  | {value_2.get_size()}\n')
                else:
                    value_3.unglue()
                    print(f'Aviones de comercial en lista de espera :  | {value_3.get_size()}\n')
                exit_track[0] = True
        else:
            flag = False
            break

print("Aviones de salida\n")
assign_track(exit_emergency, exit_special, exit_military, exit_commercial, "exit")
print("\n")

print("Aviones de llegada\n")
assign_track(entry_emergency, entry_special, entry_military, entry_commercial, "entry")
