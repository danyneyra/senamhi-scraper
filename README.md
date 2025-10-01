# 🌦️ SENAMHI Data Scraper

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-green.svg)](https://pydantic.dev/)
[![Zendriver](https://img.shields.io/badge/Zendriver-Latest-orange.svg)](https://zendriver.dev/)

> **Automatiza la descarga de datos meteorológicos históricos del SENAMHI con bypass automático de Cloudflare Turnstile**

Este proyecto permite **descargar datos hidrometeorológicos históricos** en archivos CSV organizados por **Mes, Año o Rangos de años** desde el sitio web oficial del **SENAMHI** (Servicio Nacional de Meteorología e Hidrología del Perú). Utiliza tecnología avanzada con `Zendriver` para superar automáticamente las protecciones de Cloudflare Turnstile.

## 📚 Tabla de Contenidos

- [✨ Características](#-características)
- [🎯 Modos de Consulta](#-modos-de-consulta)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🚀 Instalación](#-instalación)
- [⚡ Uso Rápido](#-uso-rápido)
- [💡 Ejemplos de Uso](#-ejemplos-de-uso)
- [🔄 Flujo de Ejecución](#-flujo-de-ejecución)
- [🛠️ Configuración Avanzada](#️-configuración-avanzada)
- [🔧 Troubleshooting](#-troubleshooting)
- [⚠️ Limitaciones](#️-limitaciones)
- [📄 Licencia](#-licencia)

## ✨ Características

### 🚀 Funcionalidades Principales
- 🛡️ **Bypass automático de Cloudflare Turnstile** - Acceso garantizado sin intervención manual
- 🔄 **Tres modos de consulta flexibles** - Month, Year, Period con opciones avanzadas
- 📊 **Exportación inteligente** - CSV organizados con nombres descriptivos
- 🎯 **Interfaz interactiva amigable** - Validaciones en tiempo real
- 📋 **Modelos Pydantic tipados** - Validación automática de datos
- 🔧 **Configuración centralizada** - Personalización fácil en `settings.py`


## 🎯 Modos de Consulta

### 1. Modo Month (Mensual)
Descarga datos de un mes específico.
- **Entrada**: Año y mes
- **Salida**: Un archivo CSV individual
- **Ejemplo**: `TICAPAMPA-202409.csv`

### 2. Modo Year (Anual)
Descarga todos los meses de un año completo.
- **Entrada**: Año
- **Opciones**: Archivos individuales o consolidado
- **Salida**: 12 archivos separados o 1 archivo consolidado
- **Ejemplo**: `TICAPAMPA-2024.csv`

### 3. Modo Period (Periodo)
Descarga datos de múltiples años.
- **Entrada**: Año inicial y final
- **Opciones**: Archivos individuales o consolidado
- **Salida**: Múltiples archivos o 1 archivo consolidado
- **Ejemplo**: `TICAPAMPA-2020-2025.csv`

## 📁 Estructura del Proyecto

```
senamhi_scraper/
├── 📄 main.py                    # 🚀 Script principal ejecutable
├── 📄 run_scraper.py            # 🎮 Interfaz interactiva (recomendado)
├── ⚙️ settings.py               # ✨ Configuración centralizada
├── 📋 requirements.txt          # 📦 Dependencias del proyecto
├── 📖 README.md                # 📚 Documentación completa
│
├── 📁 src/                      # 🏗️ Código fuente modular
│   ├── 🚨 exceptions.py        # Excepciones personalizadas
│   ├── 🎯 query_handler.py     # Manejador principal de consultas
│   ├── 🌐 html_utils.py        # Utilidades para parsing HTML
│   ├── 🏭 station_service.py   # Servicio de gestión de estaciones
│   └── 📁 models/              # 🏛️ Modelos de datos con Pydantic
│       ├── 📄 __init__.py      
│       ├── 🏢 station.py       # Modelo Station + validaciones
│       ├── 🔍 query.py         # Modelos de consultas y respuestas
│       └── 📊 data_schema.py   # Esquemas CSV y validadores
│
├── 📁 data/                     # 💾 Datos del proyecto
│   └── 🗄️ estaciones.json      # Base de datos de estaciones
│
├── 📁 output/                   # 📈 Archivos generados
│   └── 📊 *.csv                # Datos meteorológicos descargados
│                               # Estructura: ESTACION-YYYYMM.csv
│
└── 📁 .venv/                    # 🐍 Entorno virtual (opcional)
    └── 📦 [dependencias aisladas]
```

## 🚀 Instalación

### Requisitos
- **Python 3.8+** (recomendado 3.11+)
- **zendriver** - Automatización web avanzada
- **beautifulsoup4** - Parsing HTML
- **pydantic** - Validación de datos y modelos tipados


### 1. Clonar repositorio
```bash
git clone https://github.com/danyneyra/senamhi-scraper.git
cd senamhi-scraper
```

### 2. Crea un entorno virtual
```bash
python -m venv .venv
```

### 3. Ingresar en el entorno virtual
```bash
.venv\Scripts\activate        # En Windows
source .venv/bin/activate     # En Linux/macOS
```

### 4. Instalar librerías desde requirements.txt (Recomendado)
```bash
pip install -r requirements.txt
```


## ⚡ Uso Rápido

### Método 1: Script Interactivo (Recomendado)
```bash
python run_scraper.py
```

### Método 2: Script Principal
```bash
python main.py
```

## 💡 Ejemplos de Uso

### Consultar un mes específico
```
Modo: 1 (Month)
Año: 2024
Mes: 9
→ Genera: output/TICAPAMPA-202409.csv
```

### Consultar año completo (archivos separados)
```
Modo: 2 (Year)
Año: 2024
¿Archivo único?: n
→ Genera: output/TICAPAMPA-202401.csv, TICAPAMPA-202402.csv, etc.
```

### Consultar año completo (archivo consolidado)
```
Modo: 2 (Year)
Año: 2024
¿Archivo único?: s
→ Genera: output/TICAPAMPA-2024.csv
```

### Consultar periodo (archivo consolidado)
```
Modo: 3 (Period)
Año inicial: 2020
Año final: 2025
¿Archivo único?: s
→ Genera: output/TICAPAMPA-2020-2025.csv
```

### 📊 Casos de Uso Comunes

#### 🌡️ Análisis de Tendencias Climáticas
```bash
# Descargar últimos 10 años para análisis de tendencias
Modo: 3 (Period) | Años: 2015-2024 | Consolidado: Sí
# Resultado: Archivo único con datos históricos completos
```

#### 📈 Estudios de Variabilidad Estacional
```bash
# Descargar año completo en archivos separados
Modo: 2 (Year) | Año: 2024 | Consolidado: No
# Resultado: 12 archivos CSV (uno por mes)
```

#### 🔍 Verificación de Datos Específicos
```bash
# Consultar un mes particular para validación
Modo: 1 (Month) | Año: 2024 | Mes: 09
# Resultado: Datos específicos de septiembre 2024
```

## 📋 Formato de Salida

### 📄 Archivos Individuales
Cada archivo contiene los datos del mes correspondiente:
- **Formato**: CSV con separador `;`
- **Encoding**: UTF-8
- **Nomenclatura**: `NOMBRE_ESTACION-YYYYMM.csv`
- **Ejemplo**: `TICAPAMPA-202409.csv`

### 📦 Archivos Consolidados
Consolida toda la información en un solo archivo:
- **Formato**: CSV con separador `;`
- **Encoding**: UTF-8 
- **Nomenclatura**: `NOMBRE_ESTACION-YYYY.csv` o `CODIGO_ESTACION-YYYY-YYYY.csv`
- **Contenido**: Datos ordenados cronológicamente


## 🔄 Flujo de Ejecución

1. **Inicialización**: Configuración del navegador y parámetros
2. **Navegación**: Acceso a la página y resolución de Cloudflare
3. **Configuración**: Clic en pestaña de tabla y localización de iframe
4. **Extracción**: Obtención de opciones del select
5. **Filtrado**: Aplicación de criterios según modo de consulta
6. **Procesamiento**: Iteración sobre opciones filtradas
7. **Exportación**: Generación de archivos CSV
8. **Finalización**: Limpieza y cierre del navegador

## Manejo de Errores

El sistema incluye manejo robusto de errores:
- **Timeouts configurables** para elementos web
- **Reintentos automáticos** para operaciones fallidas
- **Validación de datos** antes del procesamiento

## 🔧 Troubleshooting

### Errores Comunes

#### 🚫 "Iframe contenedor no encontrado"
```bash
# Soluciones:
- Verificar conexión a internet estable
- Revisar si SENAMHI cambió la estructura del sitio
- Aumentar timeout en settings.py: PAGE_TIMEOUT = 45
- Verificar que Cloudflare se resolvió correctamente
```

#### 🚫 "Select CBOFiltro no encontrado" 
```bash
# Soluciones:
- Confirmar que la estación tiene datos disponibles
- Verificar código de estación en data/estaciones.json
- Revisar consola del navegador para errores JavaScript
- Probar con una estación diferente
```

#### 🚫 "No se encontraron opciones para los criterios"
```bash
# Soluciones:
- Verificar que el año/periodo existe en los datos
- Consultar años disponibles primero
- Revisar formato de fecha (YYYYMM)
- Probar con un rango de fechas más amplio
```

#### 🚫 Errores de Validación Pydantic
```bash
# Ejemplos:
ValidationError: Latitude must be between -90 and 90
ValidationError: El código de estación no puede estar vacío

# Solución: Verificar datos de entrada según los modelos
```

## ⚠️ Limitaciones

- **Dependencia externa**: Sujeto a cambios en el sitio web de SENAMHI
- **Conexión requerida**: Necesita internet estable durante la operación
- **Navegador activo**: El navegador debe permanecer abierto durante el scraping
- **Cloudflare**: Puede requerir verificación adicional ocasionalmente
- **Rate limiting**: Respetar los límites del servidor de SENAMHI

## 🛠️ Configuración Avanzada

### Personalizar settings.py
```python
# Timeouts personalizados
PAGE_TIMEOUT = 45        # Tiempo de carga de página
ELEMENT_TIMEOUT = 15     # Tiempo de espera de elementos
POLL_INTERVAL = 0.3      # Intervalo de polling

# Directorios personalizados
OUTPUT_DIR = "mi_output"
CSV_DIR = "mi_output/datos_csv"
LOGS_DIR = "mi_output/registros"

# CSV personalizado
CSV_SEPARATOR = ","       # Cambiar a coma si prefieres
CSV_ENCODING = "utf-8"   # Encoding de archivos
```

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
  - Revisa que tu versión de Python sea 3.11 o superior (`python --version`).


## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la **Licencia MIT**.

```
MIT License - Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

##

<div align="center">
Desarollado con 💜 para la comunidad meteorológica peruana. <br/>
Facilitando el acceso a datos hidrometeorológicos históricos del SENAMHI
</div>
