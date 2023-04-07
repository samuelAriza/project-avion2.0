import json
import random
from datetime import datetime

airlines = ["LATAM", "Avianca", "Delta", "United", "American Airlines"]
airports = ["LIM", "BOG", "MIA", "JFK", "LAX", "MAD"]
city = {"MDE": "Medellin", "LIM": "Lima", "BOG" : "Bogotá", "MIA": "Miami", "JFK": "Nueva York", "LAX" : "Los Ángeles", "MAD": "Madrid"}

priority = ["Comercial", "Militar", "Emergencia", "Especial"]

def save_as_json(filename, number, type):
    with open(filename, "r+") as file:
        data = json.load(file)

    for i in range(number):
        value = ""
        if(type == "Salida"):
            airport_exit = "MDE"
            airport = random.choice(airports)
        else:
            airport_exit = random.choice(airports)
            airport = "MDE"

        register = {
            "aerolinea": random.choice(airlines),
            "numero_vuelo": "LA" + str(i+1),
            "tipo_vuelo": type,  
            "aeropuerto_salida": airport_exit,
            "aeropuerto_llegada": airport,
            "ciudad_origen": city[airport_exit],
            "ciudad_destino":  city[airport],
            "hora": datetime(2023, 3, 17, random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)).strftime('%Y-%m-%d %H:%M:%S'),
            "duracion": random.randint(60, 360),
            "prioridad": random.choice(priority),
            "estado": random.choice(["On time", "Delayed", "Cancelled"])
        }
        data.append(register)

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

save_as_json("data_exit.json", 5, "Salida")
save_as_json("data_entry.json", 5, "Llegada")


