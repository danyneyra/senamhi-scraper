
# 📡 Scraper de Datos Meteorológicos del SENAMHI - Perú

Este proyecto permite **descargar automáticamente los archivos CSV** de datos meteorológicos históricos del sitio web del **SENAMHI** (Servicio Nacional de Meteorología e Hidrología del Perú) para cualquier estación meteorológica del país. Utiliza `Playwright` para automatizar la descarga de archivos que están protegidos por CAPTCHA.

## 🚀 Características

- Descarga todos los archivos CSV históricos (por mes y año) de una estación específica.
- Supera el uso de CAPTCHA usando Playwright.
- Utiliza un archivo `estaciones.json` que contiene:
  - Códigos de estaciones
  - Nombres
  - Coordenadas geográficas
  - Tipo de estación
- Guarda todos los archivos descargados en la carpeta `download`.

## 📂 Estructura del proyecto

```
senamhi-scraper/
├── app.py
├── estaciones.json
├── download/
├── requirements.txt
└── README.md
```

## 🧰 Requisitos

- Python 3.8 o superior
- [Playwright](https://playwright.dev/python/)
- Navegador Chromium (se instala automáticamente con Playwright)

## ⚙️ Instalación

```bash
# 1. Clona este repositorio
git clone https://github.com/danyneyra/senamhi-scraper.git
cd senamhi-scraper

# 2. Crea un entorno virtual
python -m venv venv
source venv/bin/activate     # En Linux/macOS
venv\Scripts\activate        # En Windows

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Instala los navegadores para Playwright
playwright install
```

## ▶️ Uso

Ejecuta el script principal:

```bash
python app.py
```

Se te pedirá que ingreses el **código de la estación**. Puedes obtener este código desde el archivo `estaciones.json`.

Por ejemplo, Estación de Quiruvilca:

```bash
Ingrese el código de estación: 4727319A
```

El programa descargará automáticamente todos los archivos CSV disponibles (organizados por mes y año) a la carpeta `download/`.

## 📁 Archivos generados

Todos los archivos `.csv` descargados se almacenan organizadamente dentro de la carpeta `download/`. Puedes procesarlos posteriormente con herramientas como Excel, pandas, etc.

## 🧠 Notas técnicas

- El sitio web del SENAMHI requiere resolver un CAPTCHA para cada descarga mensual de CSV. Por eso se utiliza `Playwright` para automatizar la navegación y descarga.
- El archivo `estaciones.json` actúa como un catálogo completo de todas las estaciones meteorológicas disponibles en Perú, incluyendo nombre, código y coordenadas.


---

> Proyecto creado con ❤️ para facilitar el acceso a datos meteorológicos históricos del SENAMHI Perú.
