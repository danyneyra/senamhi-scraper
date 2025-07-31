# 📡 Scraper de Datos Hidrometeorológicos del SENAMHI - Perú

Este proyecto permite **descargar automáticamente los archivos CSV** de datos Hidrometeorológicos históricos del sitio web del **SENAMHI** (Servicio Nacional de Meteorología e Hidrología del Perú) para cualquier estación meteorológica del país. Utiliza `Playwright` para automatizar la descarga de archivos que están protegidos por CAPTCHA.

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
├── data
  ├── estaciones.json
├── download/
├── utils/
  ├── combine.py
  ├── scraping.py
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
python -m venv .venv
source .venv/bin/activate     # En Linux/macOS
.venv\Scripts\activate        # En Windows

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

Verás el siguiente menú interactivo:

```
SCRAPING WEB SENAMHI
=====================================
1. Descargar datos de una estación y agrupar por año
2. Descargar datos de una estación
3. Agrupar datos de una estación por año
4. Salir
=====================================
Seleccione una opción:
```

Dependiendo de la opción elegida, se te pedirá ingresar el **código** o el **nombre** de la estación. Puedes obtener estos datos desde el archivo `estaciones.json`.

Por ejemplo, para descargar y agrupar datos de la estación Quiruvilca:

```
Seleccione una opción: 1
Ingrese el código de la estación (ejemplo: 4727319A):
```

El programa descargará automáticamente todos los archivos CSV disponibles y los organizará por año en la carpeta `download/`.

## 📁 Archivos generados

Todos los archivos `.csv` descargados se almacenan organizadamente dentro de la carpeta `download/`. Puedes procesarlos posteriormente con herramientas como Excel, pandas, etc.

## 📝 Notas adicionales

- **Git:** Para clonar el repositorio necesitas tener [Git](https://git-scm.com/) instalado en tu sistema. Puedes verificarlo ejecutando `git --version` en la terminal.

- **Activación del entorno virtual en Windows:**  
  Si al ejecutar `.venv\Scripts\activate` en PowerShell ves el error:

  ```
  Activate.ps1 no se puede cargar porque la ejecución de scripts está deshabilitada en este sistema.
  ```

  Debes permitir la ejecución de scripts. Abre PowerShell como administrador y ejecuta:

  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

  Luego intenta activar el entorno virtual nuevamente.

- **Consideraciones adicionales:**
  - Asegúrate de tener conexión a internet para instalar dependencias y navegadores.
  - Si usas otro shell (como CMD), la activación se realiza con `.venv\Scripts\activate.bat`.
  - Si tienes problemas con permisos, ejecuta la terminal como administrador.
  - Revisa que tu versión de Python sea 3.8 o superior (`python --version`).

---

## 🧠 Notas técnicas

- El sitio web del SENAMHI requiere resolver un CAPTCHA para cada descarga mensual de CSV. Por eso se utiliza `Playwright` para automatizar la navegación y descarga. [Senamhi](https://www.senamhi.gob.pe/?p=estaciones)
- El archivo `estaciones.json` actúa como un catálogo completo de todas las estaciones meteorológicas disponibles en Perú, incluyendo nombre, código y coordenadas.


---

> Proyecto creado con ❤️ para facilitar el acceso a datos hidrometeorológicos históricos del SENAMHI Perú.
