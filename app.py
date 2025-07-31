import json
from models.estacion import Estacion
from typing import List
from urllib.parse import urlencode
from utils.scraping import run_playwright
from utils.combine import combinar_archivos_csv

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

ERROR_ESTACION_INVALIDA = "Error: La estación ingresada no es válida"
AGRUPANDO_ARCHIVOS = "Agrupando archivos descargados por año..."

def handle_descargar_y_agrupar():
    COD_ESTACION = input("Ingrese el código de la estación (ejemplo: 472D30C8): ")
    if not COD_ESTACION:
        print(ERROR_ESTACION_INVALIDA)
        exit(1)

    estaciones = cargar_estaciones("data/estaciones.json")
    estacion = buscar_estacion_por_codigo(estaciones, COD_ESTACION)

    if estacion is None:
        print("Error: Estación no encontrada")
        exit(1)

    url = crear_url_estacion(estacion)

    print("Iniciando descarga de datos...")
    print(url)
    run_playwright(url, estacion.nom)
    print(AGRUPANDO_ARCHIVOS)
    combinar_archivos_csv(estacion.nom)

def handle_descargar():
    COD_ESTACION = input("Ingrese el código de la estación (ejemplo: 472D30C8): ")
    if not COD_ESTACION:
        print(ERROR_ESTACION_INVALIDA)
        exit(1)

    estaciones = cargar_estaciones("data/estaciones.json")
    estacion = buscar_estacion_por_codigo(estaciones, COD_ESTACION)

    if estacion is None:
        print("Error: Estación no encontrada")
        exit(1)

    url = crear_url_estacion(estacion)

    print("Iniciando descarga de datos...")
    print(url)
    run_playwright(url, estacion.nom)

def handle_agrupar():
    print("NOTA: La estación debe haber sido descargada previamente.")
    NAME_ESTACION = input("Ingrese nombre de la estación (ejemplo: LUCMA): ")
    INDICE_ENCABEZADO = input("Ingrese N° de fila del encabezado (default: 11): ")
    if INDICE_ENCABEZADO.isdigit():
        INDICE_ENCABEZADO = int(INDICE_ENCABEZADO) - 1
    else:
        INDICE_ENCABEZADO = 10

    if not NAME_ESTACION:
        print(ERROR_ESTACION_INVALIDA)
        exit(1)
    print(AGRUPANDO_ARCHIVOS)
    combinar_archivos_csv(NAME_ESTACION, INDICE_ENCABEZADO)

def main():
    print("SCRAPING WEB SENAMHI")
    print("=====================================")
    print("1. Descargar datos de una estación y agrupar por año")
    print("2. Descargar datos de una estación")
    print("3. Agrupar datos de una estación por año")
    print("4. Salir")
    print("=====================================")

    try:

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            handle_descargar_y_agrupar()
        elif opcion == "2":
            handle_descargar()
        elif opcion == "3":
            handle_agrupar()
        elif opcion == "4":
            print("Saliendo...")
            exit(0)
        else:
            print("Opción no válida, saliendo...")
            exit(1)
    except KeyboardInterrupt:
        print("pipipipipipippipipi")
        print("Cerrando app :(")

if __name__ == "__main__":
    main()