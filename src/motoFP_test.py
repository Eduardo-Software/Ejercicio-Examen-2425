import motoFP as fp 
import json          

RUTA_DATOS = "../data/mundial_motofp.csv"

def main():
    """
    Función principal que ejecuta todos los tests del examen.
    """
    print("Cargando datos desde " + RUTA_DATOS)
    carreras = fp.lee_carreras(RUTA_DATOS)
    
    if not carreras:
        print("Error: No se pudieron cargar los datos. Abortando tests.")
        return
    print(f"Datos cargados. {len(carreras)} carreras en total.\n")
    
    # Test Ejercicio 1
    print("### Test lee_carreras ###")
    print(f"Número de carreras leídas: {len(carreras)}")
    print("\nLas dos primeras son:")
    print(f"\t{carreras[0]}")
    print(f"\t{carreras[1]}")
    print("Las dos últimas son:")
    print(f"\t{carreras[-2]}")
    print(f"\t{carreras[-1]}")
    print("-" * 40 + "\n")

    # Test Ejercicio 2
    print("### Test maximo_dias_sin_ganar ###")
    print(f"Para Marc Marquez: {fp.maximo_dias_sin_ganar(carreras, 'Marc Marquez')}")
    print(f"Para Jorge Martin: {fp.maximo_dias_sin_ganar(carreras, 'Jorge Martin')}")
    print(f"Para Freddy Mercuri: {fp.maximo_dias_sin_ganar(carreras, 'Freddy Mercuri')}")
    print("-" * 40 + "\n")

    # Test Ejercicio 3
    print("### Test piloto_mas_podios_por_circuito ###")
    res_e3 = fp.piloto_mas_podios_por_circuito(carreras)
    print(json.dumps(res_e3, indent=4, ensure_ascii=False))
    print("-" * 40 + "\n")

    # Test Ejercicio 4
    print("### Test escuderias_con_solo_un_piloto ###")
    res_e4 = fp.escuderias_con_solo_un_piloto(carreras)
    print(res_e4)
    print("-" * 40 + "\n")

if __name__ == "__main__":
    main()