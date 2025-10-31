import motoFP as fp  # Importamos el módulo con nuestras funciones
import json          # Para imprimir diccionarios de forma legible

# Ruta al fichero de datos, subiendo un nivel (..) y entrando en 'data'
RUTA_DATOS = "../data/mundial_motofp.csv"

def main():
    """
    Función principal que ejecuta todos los tests del examen.
    """
    
    # --- Carga de datos ---
    # Leemos los datos una sola vez al inicio
    print("Cargando datos desde " + RUTA_DATOS)
    carreras = fp.lee_carreras(RUTA_DATOS)
    
    if not carreras:
        print("Error: No se pudieron cargar los datos. Abortando tests.")
        return
    print(f"Datos cargados. {len(carreras)} carreras en total.\n")
    
    # --- Test Ejercicio 1 ---
    print("### Test lee_carreras ###")
    print(f"Número de carreras leídas: {len(carreras)}")
    print("\nLas dos primeras son:")
    print(f"\t{carreras[0]}")
    print(f"\t{carreras[1]}")
    print("Las dos últimas son:")
    print(f"\t{carreras[-2]}")
    print(f"\t{carreras[-1]}")
    print("-" * 40 + "\n")

    # --- Test Ejercicio 2 ---
    print("### Test maximo_dias_sin_ganar ###")
    print(f"Para Marc Marquez: {fp.maximo_dias_sin_ganar(carreras, 'Marc Marquez')}")
    print(f"Para Jorge Martin: {fp.maximo_dias_sin_ganar(carreras, 'Jorge Martin')}")
    print(f"Para Freddy Mercuri: {fp.maximo_dias_sin_ganar(carreras, 'Freddy Mercuri')}")
    print("-" * 40 + "\n")

    # --- Test Ejercicio 3 ---
    print("### Test piloto_mas_podios_por_circuito ###")
    res_e3 = fp.piloto_mas_podios_por_circuito(carreras)
    # Usamos json.dumps para una impresión formateada del diccionario
    print(json.dumps(res_e3, indent=4, ensure_ascii=False))
    print("-" * 40 + "\n")

    # --- Test Ejercicio 4 ---
    print("### Test escuderias_con_solo_un_piloto ###")
    res_e4 = fp.escuderias_con_solo_un_piloto(carreras)
    print(res_e4)
    print("-" * 40 + "\n")

    # --- Test Ejercicio 5 ---
    print("### Test piloto_racha_mas_larga_victorias_consecutivas ###")
    print(f"Para año=2024: {fp.piloto_racha_mas_larga_victorias_consecutivas(carreras, 2024)}")
    print(f"Para año=None: {fp.piloto_racha_mas_larga_victorias_consecutivas(carreras, None)}")
    print("-" * 40 + "\n")

    # --- Test Ejercicio 6 ---
    print("### Test ultimos_ganadores_por_circuito ###")
    
    print('\nPara n=2 y estado="Seco"')
    res_e6_seco = fp.ultimos_ganadores_por_circuito(carreras, n=2, estado="Seco")
    print(json.dumps(res_e6_seco, indent=4, ensure_ascii=False))
    
    print('\nPara n=2 y estado="Mojado"')
    res_e6_mojado = fp.ultimos_ganadores_por_circuito(carreras, n=2, estado="Mojado")
    print(json.dumps(res_e6_mojado, indent=4, ensure_ascii=False))
    print("-" * 40 + "\n")

# --- Punto de entrada principal ---
if __name__ == "__main__":
    main()