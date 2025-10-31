import csv
from datetime import datetime
from collections import defaultdict, Counter
from typing import NamedTuple, Optional

# --- Definiciones de NamedTuple (provistas en el enunciado) ---

Piloto = NamedTuple("Piloto", [("nombre", str), ("escuderia", str)])

CarreraFP = NamedTuple("CarreraFP", [
        ("fecha_hora", datetime), 
        ("circuito", str),                    
        ("pais", str), 
        ("seco", bool), # True si el asfalto estuvo seco, False si estuvo mojado
        ("tiempo", float), 
        ("podio", list[Piloto])])

# --- Ejercicio 1 ---

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
                # Parseo de los campos
                fecha_hora = datetime.strptime(row[0], FORMATO_FECHA)
                circuito = row[1]
                pais = row[2]
                seco = (row[3] == "Seco")
                tiempo = float(row[4])
                
                # Creación de los pilotos del podio
                p1 = Piloto(nombre=row[5], escuderia=row[6])
                p2 = Piloto(nombre=row[7], escuderia=row[8])
                p3 = Piloto(nombre=row[9], escuderia=row[10])
                podio = [p1, p2, p3]
                
                # Creación del objeto CarreraFP
                carrera = CarreraFP(fecha_hora, circuito, pais, seco, tiempo, podio)
                carreras.append(carrera)
                
    except FileNotFoundError:
        print(f"Error: No se encontró el fichero en la ruta {filename}")
    except Exception as e:
        print(f"Error durante la lectura o procesamiento del fichero: {e}")
        
    return carreras

# --- Ejercicio 2 ---

def maximo_dias_sin_ganar(carreras: list[CarreraFP], nombre_piloto: str) -> Optional[int]:
    """
    Devuelve el tiempo máximo (en días) que `nombre_piloto` estuvo sin ganar una carrera.
    Si el piloto no ha ganado al menos dos carreras, devuelve None.
    """
    # 1. Obtener todas las fechas en las que el piloto ganó (posición 0 del podio)
    fechas_victorias = []
    for c in carreras:
        if c.podio[0].nombre == nombre_piloto:
            fechas_victorias.append(c.fecha_hora)
            
    # 2. Si hay menos de 2 victorias, no se puede calcular un intervalo
    if len(fechas_victorias) < 2:
        return None
        
    # 3. Ordenar las fechas cronológicamente
    fechas_victorias.sort()
    
    # 4. Calcular el intervalo máximo entre victorias consecutivas
    max_dias = 0
    for i in range(len(fechas_victorias) - 1):
        fecha_victoria_1 = fechas_victorias[i]
        fecha_victoria_2 = fechas_victorias[i+1]
        
        # Cálculo de días según la observación del enunciado
        dias_entre_victorias = (fecha_victoria_2 - fecha_victoria_1).days
        
        if dias_entre_victorias > max_dias:
            max_dias = dias_entre_victorias
            
    return max_dias

# --- Ejercicio 3 ---

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

# --- Ejercicio 4 ---

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

# --- Ejercicio 5 ---

def piloto_racha_mas_larga_victorias_consecutivas(carreras: list[CarreraFP], año: Optional[int] = None) -> tuple[str, int]:
    """
    Devuelve el nombre del piloto que ha obtenido la racha de victorias 
    consecutivas más larga ese `año` y la longitud de esa racha.
    Si `año` es `None` entonces el resultado será sin restricción de año.
    """
    
    # 1. Filtrar las carreras por año si se proporciona
    carreras_a_procesar = carreras
    if año is not None:
        carreras_a_procesar = [c for c in carreras if c.fecha_hora.year == año]
        
    # Si no hay carreras para ese año, devolvemos una tupla vacía/nula
    if not carreras_a_procesar:
        return (None, 0)
        
    # 2. Ordenar las carreras cronológicamente (¡CRUCIAL para rachas!)
    carreras_ordenadas = sorted(carreras_a_procesar, key=lambda c: c.fecha_hora)
    
    # 3. Iterar para encontrar la racha más larga
    racha_max_global = ("", 0)   # (nombre_piloto, longitud_max)
    
    piloto_racha_actual = None
    longitud_racha_actual = 0
    
    for c in carreras_ordenadas:
        ganador_actual = c.podio[0].nombre
        
        if ganador_actual == piloto_racha_actual:
            longitud_racha_actual += 1
        else:
            piloto_racha_actual = ganador_actual
            longitud_racha_actual = 1
            
        if longitud_racha_actual > racha_max_global[1]:
            racha_max_global = (piloto_racha_actual, longitud_racha_actual)
            
    return racha_max_global

# --- Ejercicio 6 ---

def ultimos_ganadores_por_circuito(carreras: list[CarreraFP], n: int, estado: str) -> dict[str, list[str]]:
    """
    Devuelve un diccionario {circuito: [lista_ganadores]} con los ganadores
    de las últimas `n` carreras en ese circuito con el `estado` (Seco/Mojado) dado.
    Las listas están ordenadas de más reciente a más antigua.
    """
    
    # Convertir el parámetro 'estado' (string) a 'seco' (booleano)
    estado_booleano = (estado == "Seco")
    
    # 1. Agrupar todas las carreras por circuito
    carreras_por_circuito = defaultdict(list)
    for c in carreras:
        carreras_por_circuito[c.circuito].append(c)
        
    resultado = {}
    
    # 2. Procesar la lista de carreras para cada circuito
    for circuito, lista_carreras in carreras_por_circuito.items():
        
        # 3. Filtrar por el estado del asfalto (Seco/Mojado)
        carreras_filtradas = [c for c in lista_carreras if c.seco == estado_booleano]
        
        # 4. Ordenar las carreras filtradas por fecha (de más reciente a más antigua)
        carreras_ordenadas = sorted(carreras_filtradas, key=lambda c: c.fecha_hora, reverse=True)
        
        # 5. Coger solo las 'n' primeras carreras (las 'n' últimas cronológicamente)
        ultimas_n_carreras = carreras_ordenadas[:n]
        
        # 6. Extraer los nombres de los ganadores de esas 'n' carreras
        nombres_ganadores = [c.podio[0].nombre for c in ultimas_n_carreras]
        
        # 7. Añadir al diccionario solo si se encontraron ganadores para ese filtro
        if nombres_ganadores:
            resultado[circuito] = nombres_ganadores
            
    return resultado
