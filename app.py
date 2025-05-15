import json
from models.estacion import Estacion
from typing import List
from urllib.parse import urlencode
from boot import run_playwright

def cargar_estaciones(path: str) -> List[Estacion]:
    with open(path, 'r', encoding="utf-8") as archivo:
        datos_json = json.load(archivo)
    return [Estacion(**item) for item in datos_json]

def buscar_estacion_por_codigo(estaciones: List[Estacion], codigo: str) -> Estacion | None:
    for est in estaciones:
        if est.cod == codigo:
            return est
    return None

def crear_url_estacion(estacion: Estacion) -> str:
    url_base = "https://www.senamhi.gob.pe/mapas/mapa-estaciones-2/map_red_graf.php"
    params = {
        "cod": estacion.cod,
        "estado": estacion.estado,
        "tipo_esta": estacion.ico,
        "cate": estacion.cate,
        "cod_old": estacion.cod_old
    }
    return f"{url_base}?{urlencode(params)}"

def main():
    print("SCRAPING WEB SENAMHI")
    COD_ESTACION = input("Ingrese el código de la estación: ")

    if not COD_ESTACION:
        print("Error: La estación ingresada no es válida")
        exit(1)
        
    estaciones = cargar_estaciones("data/estaciones.json")
    estacion = buscar_estacion_por_codigo(estaciones, COD_ESTACION)

    if estacion is None:
        print("Error: Estación no encontrada")
        exit(1)

    url = crear_url_estacion(estacion)
    print(url)

    run_playwright(url, estacion.nom)

if __name__ == "__main__":
    main()