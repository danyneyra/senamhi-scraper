import settings
import re
from typing import List, Optional
from bs4 import BeautifulSoup

# Constante para el parser HTML
HTML_PARSER = 'html.parser'

def extract_select_options(html_content: str, select_id: Optional[str] = None, select_name: Optional[str] = None) -> List[dict]:
    """
    Extrae los valores y textos de las opciones de un select.
    
    Args:
        html_content (str): El contenido HTML que contiene el select
        select_id (str, optional): ID del select a buscar
        select_name (str, optional): Atributo name del select a buscar
        
    Returns:
        List[dict]: Lista de diccionarios con 'value' y 'text' de cada opción
        
    Raises:
        ValueError: Si no se encuentra ningún select con los criterios especificados
    """
    
    soup = BeautifulSoup(html_content, HTML_PARSER)
    
    # Buscar el select específico
    select_element = None
    
    if select_id:
        select_element = soup.find('select', id=select_id)
    elif select_name:
        select_element = soup.find('select', attrs={'name': select_name})
    else:
        # Si no se especifica ID ni name, tomar el primer select
        select_element = soup.find('select')
    
    if not select_element:
        if select_id:
            criteria = f"ID '{select_id}'"
        elif select_name:
            criteria = f"name '{select_name}'"
        else:
            criteria = "algún select"
        raise ValueError(f"No se encontró ningún select con {criteria}")
    
    # Extraer todas las opciones
    options = select_element.find_all('option')
    
    result = []
    
    for i, option in enumerate(options):
        option_data = {
            'value': option.get('value', ''),
            'text': option.get_text(strip=True),
            'selected': option.has_attr('selected'),
            'disabled': option.has_attr('disabled')
        }
        
        result.append(option_data)
    
    return result

def _date_format(date_str: str) -> Optional[tuple]:
    """Verifica si una cadena es una fecha válida en formato YYYY-MM-DD o YYYY/MM/DD, y extraer año, mes, día"""
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str) or re.match(r'^\d{4}/\d{2}/\d{2}$', date_str):
        year, month, day = date_str.split('-') if '-' in date_str else date_str.split('/')
        if 1 <= int(month) <= 12 and 1 <= int(day) <= 31:
            return int(year), int(month), int(day)
    return None

def _process_table_row(row, row_index, separator):
    cells = row.find_all(['td', 'th'])
    row_data = []

    for cell_idx, cell in enumerate(cells):
        cell_text = cell.get_text(strip=True)
        cell_text = re.sub(r'\s+', ' ', cell_text)
        if separator in cell_text:
            cell_text = f'"{cell_text}"'

        if row_index > 0 and cell_idx == 0:
            date_format = _date_format(cell_text)
            if date_format is None:
                print(f"⚠️  Advertencia: La primera celda de la fila {row_index + 1} no es una fecha válida: '{cell_text}'")
                return None
            year, month, day = date_format
            row_data.extend([f"{year:04d}", f"{month:02d}", f"{day:02d}"])
        else:
            row_data.append("0.0" if cell_text == "S/D" else cell_text)
    return row_data if row_data and any(cell.strip() for cell in row_data) else None

def html_table_to_csv(html_content: str, separator: str = settings.CSV_SEPARATOR, start_line: Optional[int] = 0) -> str:
    """
    Convierte una tabla HTML a formato CSV usando BeautifulSoup y retorna directamente el contenido CSV como string.
    
    Args:
        html_content (str): El contenido HTML que contiene la tabla
        separator (str): Separador a usar (por defecto ';')
        
    Returns:
        str: Contenido CSV como string
    """
    soup = BeautifulSoup(html_content, HTML_PARSER)
    table = soup.find('table')
    if not table:
        return ""

    csv_lines = []
    rows = table.find_all('tr')

    for row_index, row in enumerate(rows):
        if start_line and row_index < start_line:
            continue
        row_data = _process_table_row(row, row_index, separator)
        if row_data:
            csv_lines.append(separator.join(row_data))

    return '\n'.join(csv_lines)
