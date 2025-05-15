import os
import csv

# Cambia esto a la ruta donde están tus CSVs
carpeta_entrada = "Mollepata/original"
carpeta_salida = os.path.join("Mollepata")
os.makedirs(carpeta_salida, exist_ok=True)

for nombre_archivo in os.listdir(carpeta_entrada):
    if not nombre_archivo.endswith(".csv"):
        continue

    ruta_archivo = os.path.join(carpeta_entrada, nombre_archivo)
    
    with open(ruta_archivo, encoding="utf-8") as f:
        lineas = f.readlines()

    if len(lineas) < 13:
        print(f"⚠️ Archivo {nombre_archivo} no tiene suficientes líneas, se omite.")
        continue

    headers = "AÑO / MES / DÍA,TEMPERATURA (°C) MAX, TEMPERATURA (°C) MIN,HUMEDAD RELATIVA (%),PRECIPITACIÓN (mm/día) TOTAL".split(',')

    data_lines = lineas[12:]

    filas = []
    for i in range(0, len(data_lines), 2):
        primera = data_lines[i].strip()
        segunda = data_lines[i+1].strip() if i+1 < len(data_lines) else ''
        combinada = primera + segunda
        filas.append(combinada.split(','))

    ruta_salida = os.path.join(carpeta_salida, nombre_archivo)

    with open(ruta_salida, "w", newline='', encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(headers)
        writer.writerows(filas)

    print(f"✅ Procesado y guardado: {nombre_archivo}")
