import asyncio
import zendriver as zd
from settings import SUCCESS, ERROR, PROCESSING, TIMEOUT_SECONDS, POLL_INTERVAL
from src.query_handler import QueryModeHandler, CSVManager, get_user_query_mode, get_station_code
from src.exceptions import IframeNotFoundError, TableNotFoundError, SelectNotFoundError
from src.station_service import create_station_url, get_headers_for_station

async def wait_for_in_node(node, selector, poll_interval=POLL_INTERVAL):
    """Espera a que un elemento aparezca dentro de un nodo específico"""
    try:
        countdown = TIMEOUT_SECONDS  # seconds
        while True:
            elem = await node.query_selector(selector)
            if elem:
                return elem
            await asyncio.sleep(poll_interval)
            countdown -= poll_interval
            if countdown <= 0:
                break
    except asyncio.TimeoutError:
        print(f"Timeout waiting for selector: {selector}")
        return None

async def setup_page_and_iframe(browser, url: str):
    """Configura la página inicial y obtiene el iframe"""
    page = await browser.get(url)

    # Hacer clic en la pestaña de tabla
    tab = await page.wait_for(selector='a#tabla-tab')
    await tab.click()

    # Esperar al iframe que contiene la tabla
    iframe_with_table = await page.wait_for(selector='iframe#contenedor')
    if not iframe_with_table:
        raise IframeNotFoundError(f"{ERROR} Iframe contenedor no encontrado")
    
    print(f"{SUCCESS} Iframe contenedor encontrado")
    
    # Esperar a que la tabla inicial esté disponible
    async with asyncio.timeout(TIMEOUT_SECONDS):
        table_found = await wait_for_in_node(iframe_with_table, "table#dataTable")
    
    if not table_found:
        raise TableNotFoundError(f"{ERROR} Tabla inicial no encontrada en iframe")
    
    return page, iframe_with_table

async def get_select_options(page):
    """Obtiene las opciones del select"""
    select_found = await page.wait_for(selector="select#CBOFiltro")
    if not select_found:
        raise SelectNotFoundError(f"{ERROR} Select CBOFiltro no encontrado")
    
    select_html = await select_found.get_html()
    return select_html

async def process_option(page, iframe_with_table, option, csv_manager, save_individual=True):
    """Procesa una opción específica del select"""
    print(f"\n{PROCESSING} Procesando opción: {option['text']} ({option['value']})")
    
    # Seleccionar la opción
    option_select = await page.query_selector(f"option[value='{option['value']}']")
    if not option_select:
        print(f"{ERROR} No se pudo encontrar la opción: {option['value']}")
        return False
    
    await option_select.select_option()
    print(f"{SUCCESS} Opción seleccionada exitosamente")

    # Esperar actualización de la tabla
    await asyncio.sleep(2)

    try:
        # Buscar tabla actualizada
        updated_table = await wait_for_in_node(iframe_with_table, "table#dataTable")
        
        if not updated_table:
            print(f"{ERROR} No se pudo encontrar la tabla actualizada para opción: {option['value']}")
            return False
        
        # Obtener HTML de la tabla
        table_html = await updated_table.get_html()
        
        # Guardar datos
        if save_individual:
            csv_manager.save_individual_file(table_html, option['value'])
        else:
            csv_manager.add_table_data(table_html, option['value'])

        return True
        
    except Exception as e:
        print(f"{ERROR} Error procesando opción {option['value']}: {e}")
        return False

async def main():
    # Obtener código de estación y verificar
    print(f"{SUCCESS} Bienvenido al sistema de scraping del SENAMHI")
    query_station = get_station_code()
    if not query_station:
        print(f"{ERROR} Código de estación inválido o no encontrado")
        return

    # Mostrar información de la estación
    print(f"{SUCCESS} Estación encontrada: {query_station.name} ({query_station.code})")

    headers = get_headers_for_station(query_station)
    station_name = query_station.name.replace(" ", "")

    # Obtener modo de consulta
    query_params = get_user_query_mode(station_name)

    print(f"\n🚀 Iniciando scraping a la estación {query_station.name} en modo: {query_params['mode'].upper()}")

    browser = await zd.start()
    
    try:
        # Configurar página e iframe
        url_station = create_station_url(query_station)
        page, iframe_with_table = await setup_page_and_iframe(browser, url_station)

        # Obtener opciones del select
        select_html = await get_select_options(page)
        
        # Configurar manejadores
        query_handler = QueryModeHandler()
        query_handler.load_options(select_html)
        
        csv_manager = CSVManager(station_name)
        csv_manager.headers = headers
        csv_manager.start_line = 1 if query_station.status == "AUTOMATICA" else 2

        # Mostrar años disponibles
        available_years = query_handler.get_available_years()
        print(f"📅 Años disponibles: {available_years}")
        
        # Filtrar opciones según el modo
        if query_params['mode'] == 'month':
            filtered_options = query_handler.filter_by_month(query_params['year'], query_params['month'])
            save_individual = True
        elif query_params['mode'] == 'year':
            filtered_options = query_handler.filter_by_year(query_params['year'])
            save_individual = not query_params['consolidated']
        elif query_params['mode'] == 'period':
            filtered_options = query_handler.filter_by_period(query_params['start_year'], query_params['end_year'])
            save_individual = not query_params['consolidated']
        
        if not filtered_options:
            print(f"{ERROR} No se encontraron opciones para los criterios especificados")
            return
        
        print(f"\n📊 Se procesarán {len(filtered_options)} opciones")
        
        # Procesar opciones filtradas
        successful_count = 0
        for i, option in enumerate(filtered_options, 1):
            print(f"\n--- Procesando {i}/{len(filtered_options)} ---")

            success = await process_option(page, iframe_with_table, option, csv_manager, save_individual=save_individual)
            if success:
                successful_count += 1
        
        # Guardar archivo consolidado si es necesario
        if not save_individual and query_params.get('filename'):
            csv_manager.save_consolidated_file(query_params['filename'])
        
        print(f"\n🎉 Proceso completado: {successful_count}/{len(filtered_options)} opciones procesadas exitosamente")
        
    except Exception as e:
        print(f"{ERROR} Error durante el proceso: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Pausa para verificación visual
        print("🔍 Manteniendo navegador abierto 2 segundos para verificación...")
        await asyncio.sleep(2)
        await browser.stop()

if __name__ == '__main__':
    asyncio.run(main())