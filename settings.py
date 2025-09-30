# SENAMHI Scraper - Configuración Simple

# Configuración básica del proyecto
PROJECT_NAME = "SENAMHI Scraper"
VERSION = "1.0.0"

# URLs
BASE_URL = "https://www.senamhi.gob.pe/mapas/mapa-estaciones-2/map_red_graf.php"

# Timeouts (en segundos)
PAGE_TIMEOUT = 30
ELEMENT_TIMEOUT = 10
TIMEOUT_SECONDS = 30
POLL_INTERVAL = 0.5

# Configuración de archivos
CSV_SEPARATOR = ";"
CSV_ENCODING = "utf-8"
OUTPUT_DIR = "output"
CSV_DIR = "output/csv"
LOGS_DIR = "output/logs"
REPORTS_DIR = "output/reports"

# Datos
STATIONS_FILE = "data/estaciones.json"

# Mensajes de estado
SUCCESS = "✅"
ERROR = "❌"
PROCESSING = "🔄"
INFO = "ℹ️"
WARNING = "⚠️"