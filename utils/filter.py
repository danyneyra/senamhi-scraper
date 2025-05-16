import os
import pandas as pd
from collections import defaultdict

# Ruta de la carpeta que contiene los CSV
carpeta = 'Mollepata'

# Obtener todos los archivos CSV
archivos_csv = [f for f in os.listdir(carpeta) if f.endswith('.csv')]

# Agrupar archivos por año
archivos_por_anio = defaultdict(list)
for archivo in archivos_csv:
    if '-' in archivo:
        anio = archivo.split('-')[0]
        archivos_por_anio[anio].append(archivo)

# Leer y combinar archivos por año
for anio, archivos in archivos_por_anio.items():
    dataframes = []
    for archivo in archivos:
        ruta_completa = os.path.join(carpeta, archivo)
        # Leer encabezado desde la línea 11 (índice 10)
        encabezado = pd.read_csv(ruta_completa, skiprows=0, nrows=1, header=None).iloc[0].tolist()
        # Leer datos desde la línea 12 (índice 11) en adelante
        df = pd.read_csv(ruta_completa, skiprows=1, header=None, names=encabezado, sep=',', engine='python')
        dataframes.append(df)

    # Concatenar y guardar
    df_anual = pd.concat(dataframes, ignore_index=True)
    salida = os.path.join(carpeta, f'{carpeta}_{anio}_completo.csv')
    df_anual.to_csv(salida, index=False)
    print(f'Archivo combinado guardado: {salida}')
