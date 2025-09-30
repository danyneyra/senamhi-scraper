import settings
from typing import List, Dict
import re
import os
from src.html_utils import extract_select_options, html_table_to_csv
from src.models.station import Station
from src.station_service import find_station_by_code

class QueryModeHandler:
    """
    Maneja los diferentes modos de consulta: Month, Year, Period
    """
    
    def __init__(self):
        self.available_options: List[Dict[str, str]] = []
        
    def load_options(self, select_html: str) -> None:
        """
        Carga las opciones disponibles del select
        """
        self.available_options = extract_select_options(select_html)
        print(f"{settings.SUCCESS} {len(self.available_options)} opciones cargadas")
        
    def get_valid_options(self) -> List[Dict[str, str]]:
        """
        Filtra opciones válidas (que tienen valor y formato correcto YYYYMM)
        """
        valid_options = []
        for option in self.available_options:
            value = option['value'].strip()
            if value and re.match(r'^\d{6}$', value):  # Formato YYYYMM
                valid_options.append(option)
        return valid_options
        
    def filter_by_month(self, year: int, month: int) -> List[Dict[str, str]]:
        """
        Filtra opciones por año y mes específico
        """
        target_value = f"{year:04d}{month:02d}"
        valid_options = self.get_valid_options()
        
        filtered = [opt for opt in valid_options if opt['value'] == target_value]
        
        print(f"📅 Filtro por mes {year}/{month}: {len(filtered)} opciones encontradas")
        return filtered
        
    def filter_by_year(self, year: int) -> List[Dict[str, str]]:
        """
        Filtra opciones por año completo
        """
        year_str = str(year)
        valid_options = self.get_valid_options()
        
        filtered = [opt for opt in valid_options if opt['value'].startswith(year_str)]
        
        print(f"📅 Filtro por año {year}: {len(filtered)} opciones encontradas")
        return filtered
        
    def filter_by_period(self, start_year: int, end_year: int) -> List[Dict[str, str]]:
        """
        Filtra opciones por periodo de años
        """
        valid_options = self.get_valid_options()
        filtered = []
        
        for option in valid_options:
            year = int(option['value'][:4])
            if start_year <= year <= end_year:
                filtered.append(option)
                
        print(f"📅 Filtro por periodo {start_year}-{end_year}: {len(filtered)} opciones encontradas")
        return filtered
        
    def get_available_years(self) -> List[int]:
        """
        Obtiene lista de años disponibles
        """
        valid_options = self.get_valid_options()
        years = set()
        
        for option in valid_options:
            year = int(option['value'][:4])
            years.add(year)
            
        return sorted(years)

class CSVManager:
    """
    Maneja la creación y escritura de archivos CSV
    """
    
    def __init__(self, filename: str, output_dir: str = settings.CSV_DIR):
        self.filename = filename
        self.output_dir = os.path.join(output_dir, filename)
        self.csv_data_buffer = []
        self.headers = []
        self.start_line = 1  # Línea inicial para procesar (después de encabezados)

        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def add_table_data(self, table_html: str, option_value: str) -> None:
        """
        Añade datos de una tabla al buffer
        """
        try:
            csv_content = html_table_to_csv(table_html, separator=settings.CSV_SEPARATOR, start_line=self.start_line)
            if csv_content:
                processed_lines = self._process_csv_lines(csv_content)
                # Comprobar si el buffer ya tiene encabezados
                if not self.csv_data_buffer and self.headers:
                    self.csv_data_buffer.append(settings.CSV_SEPARATOR.join(self.headers))  # Añadir encabezados al inicio
                self.csv_data_buffer.extend(processed_lines)
                print(f"{settings.SUCCESS} Datos añadidos al buffer para periodo {option_value}: {len(processed_lines)} filas")
        except Exception as e:
            print(f"{settings.ERROR} Error procesando tabla para {option_value}: {e}")

    def _process_csv_lines(self, csv_content: str) -> List[str]:
        """
        Procesa las líneas CSV añadiendo el periodo
        """
        lines = csv_content.split('\n')
        processed_lines = []

        for line in lines:
            if line.strip():
                processed_lines.append(line)
                    
        return processed_lines
            
    def save_individual_file(self, table_html: str, option_value: str) -> str:
        """
        Guarda una tabla individual en un archivo CSV
        """
        filename = f"{self.filename}-{option_value}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            csv_content = html_table_to_csv(table_html, separator=settings.CSV_SEPARATOR, start_line=self.start_line)
            if csv_content:
                with open(filepath, 'w', encoding=settings.CSV_ENCODING) as f:
                    f.write(settings.CSV_SEPARATOR.join(self.headers) + "\n" + csv_content)
                print(f"{settings.SUCCESS} Archivo individual guardado: {filename}")
                return filepath
        except Exception as e:
            print(f"{settings.ERROR} Error guardando archivo {filename}: {e}")
        
        return ""
        
    def save_consolidated_file(self, filename: str) -> str:
        """
        Guarda todos los datos del buffer en un archivo consolidado
        """
        if not self.csv_data_buffer:
            print(f"{settings.ERROR} No hay datos en el buffer para guardar")
            return ""
            
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding=settings.CSV_ENCODING) as f:
                f.write('\n'.join(self.csv_data_buffer))

            print(f"{settings.SUCCESS} Archivo consolidado guardado: {filename}")
            print(f"📊 Contiene {len(self.csv_data_buffer)} líneas")
            return filepath
            
        except Exception as e:
            print(f"{settings.ERROR} Error guardando archivo consolidado: {e}")
            return ""
            
    def clear_buffer(self):
        """
        Limpia el buffer de datos
        """
        self.csv_data_buffer.clear()

def get_station_code() -> Station | None:
    """
    Solicita al usuario el código de la estación meteorológica
    """
    while True:
        print("\n" + "="*50)
        print("🔍 INGRESE EL CÓDIGO DE LA ESTACIÓN")
        code = input("Código (ejemplo: 472D30C8): ").strip()
        
        if code == "":
            continue

        station = find_station_by_code(code)
        return station

def get_user_query_mode(filename: str) -> Dict:
    """
    Solicita al usuario el modo de consulta
    """
    print("\n" + "="*50)
    print("🔍 SELECCIONA EL MODO DE CONSULTA")
    print("="*50)
    print("1. Month  - Descargar un mes específico (YYYY-MM)")
    print("2. Year   - Descargar todo un año")
    print("3. Period - Descargar un periodo de años (YYYY-YYYY)")
    print("="*50)
    
    while True:
        mode = input("Ingresa el número del modo (1-3): ").strip()
        
        if mode == "1":
            return get_month_params(filename)
        elif mode == "2":
            return get_year_params(filename)
        elif mode == "3":
            return get_period_params(filename)
        else:
            print(f"{settings.ERROR} Opción inválida. Por favor ingresa 1, 2 o 3.")

def get_month_params(filename: str) -> Dict:
    """
    Obtiene parámetros para consulta mensual
    """
    print("\n📅 Modo MONTH seleccionado")
    
    while True:
        try:
            year_input = input("Ingresa el año (ej: 2024): ").strip()
            year = int(year_input)
            if year < 2000 or year > 2050:
                print(f"{settings.ERROR} Año inválido. Debe estar entre 2000 y 2050.")
                continue
                
            month_input = input("Ingresa el mes (1-12): ").strip()
            month = int(month_input)
            if month < 1 or month > 12:
                print(f"{settings.ERROR} Mes inválido. Debe estar entre 1 y 12.")
                continue
                
            return {
                "mode": "month",
                "year": year,
                "month": month,
                "filename": f"{filename}-{year:04d}{month:02d}.csv"
            }
            
        except ValueError:
            print(f"{settings.ERROR} Por favor ingresa números válidos.")

def get_year_params(filename: str) -> Dict:
    """
    Obtiene parámetros para consulta anual
    """
    print("\n📅 Modo YEAR seleccionado")
    
    while True:
        try:
            year_input = input("Ingresa el año (ej: 2024): ").strip()
            year = int(year_input)
            if year < 2000 or year > 2050:
                print(f"{settings.ERROR} Año inválido. Debe estar entre 2000 y 2050.")
                continue
                
            save_mode = input("¿Guardar como archivo único? (s/n): ").strip().lower()
            consolidated = save_mode in ['s', 'si', 'y', 'yes', 'true', '1']

            return {
                "mode": "year",
                "year": year,
                "consolidated": consolidated,
                "filename": f"{filename}-{year}.csv" if consolidated else None
            }
            
        except ValueError:
            print(f"{settings.ERROR} Por favor ingresa un número válido.")

def get_period_params(filename: str) -> Dict:
    """
    Obtiene parámetros para consulta de periodo
    """
    print("\n📅 Modo PERIOD seleccionado")
    
    while True:
        try:
            start_year_input = input("Ingresa el año inicial (ej: 2020): ").strip()
            start_year = int(start_year_input)
            
            end_year_input = input("Ingresa el año final (ej: 2025): ").strip()
            end_year = int(end_year_input)
            
            if start_year > end_year:
                print(f"{settings.ERROR} El año inicial no puede ser mayor que el final.")
                continue

            if start_year < 2000 or end_year > 2050:
                print(f"{settings.ERROR} Los años deben estar entre 2000 y 2050.")
                continue
                
            save_mode = input("¿Guardar como archivo único? (s/n): ").strip().lower()
            consolidated = save_mode in ['s', 'si', 'y', 'yes']
            
            return {
                "mode": "period",
                "start_year": start_year,
                "end_year": end_year,
                "consolidated": consolidated,
                "filename": f"{filename}-{start_year}-{end_year}.csv" if consolidated else None
            }
            
        except ValueError:
            print(f"{settings.ERROR} Por favor ingresa números válidos.")