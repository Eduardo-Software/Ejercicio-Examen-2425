import csv
from datetime import datetime
from collections import defaultdict, Counter
from typing import NamedTuple, Optional

Piloto = NamedTuple("Piloto", [("nombre", str), ("escuderia", str)])

CarreraFP = NamedTuple("CarreraFP", [
        ("fecha_hora", datetime), 
        ("circuito", str),                    
        ("pais", str), 
        ("seco", bool), # True si el asfalto estuvo seco, False si estuvo mojado
        ("tiempo", float), 
        ("podio", list[Piloto])])

# Ejercicio 1

def lee_carreras(filename: str) -> list[CarreraFP]:
    """
    Recibe la ruta de un fichero CSV y devuelve una lista de tuplas de tipo CarreraFP
    conteniendo todos los datos almacenados en el fichero.
    """
    carreras = []

    FORMATO_FECHA = "%Y-%m-%d %H:%M"

    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            
            for row in reader:
                fecha_hora = datetime.strptime(row[0], FORMATO_FECHA)
                circuito = row[1]
                pais = row[2]
                seco = (row[3] == "Seco")
                tiempo = float(row[4])
                
                p1 = Piloto(nombre=row[5], escuderia=row[6])
                p2 = Piloto(nombre=row[7], escuderia=row[8])
                p3 = Piloto(nombre=row[9], escuderia=row[10])
                podio = [p1, p2, p3]
                
                carrera = CarreraFP(fecha_hora, circuito, pais, seco, tiempo, podio)
                carreras.append(carrera)
                
    except FileNotFoundError:
        print(f"Error: No se encontró el fichero en la ruta {filename}")
    except Exception as e:
        print(f"Error durante la lectura o procesamiento del fichero: {e}")
        
    return carreras

# Ejercicio 2

def maximo_dias_sin_ganar(carreras: list[CarreraFP], nombre_piloto: str) -> Optional[int]:
    """
    Devuelve el tiempo máximo (en días) que `nombre_piloto` estuvo sin ganar una carrera.
    Si el piloto no ha ganado al menos dos carreras, devuelve None.
    """
    fechas_victorias = []
    for c in carreras:
        if c.podio[0].nombre == nombre_piloto:
            fechas_victorias.append(c.fecha_hora)
            
    if len(fechas_victorias) < 2:
        return None
        
    fechas_victorias.sort()
    
    max_dias = 0
    for i in range(len(fechas_victorias) - 1):
        fecha_victoria_1 = fechas_victorias[i]
        fecha_victoria_2 = fechas_victorias[i+1]
        
        # Cálculo de días según la observación del enunciado
        dias_entre_victorias = (fecha_victoria_2 - fecha_victoria_1).days
        
        if dias_entre_victorias > max_dias:
            max_dias = dias_entre_victorias
            
    return max_dias

# Ejercicio 3

def piloto_mas_podios_por_circuito(carreras: list[CarreraFP]) -> dict[str, str]:
    """
    Devuelve un diccionario que a cada circuito le hace corresponder el nombre
    del piloto que más veces ha estado en el podio en ese circuito.
    """
    conteo_podios = defaultdict(Counter)
    
    for c in carreras:
        circuito = c.circuito
        for piloto in c.podio:
            conteo_podios[circuito][piloto.nombre] += 1
            
    resultado = {}
    for circuito, conteo_de_pilotos in conteo_podios.items():
        piloto_max = max(conteo_de_pilotos, key=conteo_de_pilotos.get)
        resultado[circuito] = piloto_max
        
    return resultado

# Ejercicio 4

def escuderias_con_solo_un_piloto(carreras: list[CarreraFP]) -> list[str]:
    """
    Devuelve una lista con las escuderías que solo tienen un piloto.
    """
    pilotos_por_escuderia = defaultdict(set)
    
    for c in carreras:
        for piloto in c.podio:
            pilotos_por_escuderia[piloto.escuderia].add(piloto.nombre)
            
    escuderias_unicas = []
    for escuderia, nombres_pilotos in pilotos_por_escuderia.items():
        if len(nombres_pilotos) == 1:
            escuderias_unicas.append(escuderia)
            
    return sorted(escuderias_unicas)