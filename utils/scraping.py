from playwright.sync_api import sync_playwright
import os

def run_playwright(url: str, name: str):
    try:
        with sync_playwright() as p:
            print("Abriendo explorador...")
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Ir a la página inicial
            page.goto(url)

            # Dar clic en el Tabla
            page.click("a#tabl")

            # Esperar que se resuelva el reCAPTCHA (automáticamente si invisible)
            page.wait_for_timeout(1500)  # puede necesitar ajustarse

            # Extraer captcha visible
            captcha_text = page.locator("span[style*='font-size:xxx-large']").inner_text()

            # Ingresar captcha y enviar
            page.fill("#captchaInput", captcha_text)
            page.click("button#entrar")  # id exacto puede variar

            # Esperar redirección o validación
            page.wait_for_timeout(1500)

            # Obtener todas las opciones del select
            options = page.eval_on_selector_all("select#CBOFiltro > option", "els => els.map(e => ({ value: e.value, text: e.textContent }))")
            
            # Esperar que el iframe cargue
            frame = page.frame(name="contenedor")
            if not frame:
                print("Error: No se pudo encontrar Frame")
                exit(1)

            # Esperar que el botón esté visible dentro del iframe
            frame.wait_for_selector("#export2", state="visible", timeout=10000)

            # Se seleccionará periodo por periodo y se irá descargando
            for option in options:
                # Seleccionar periodo
                page.select_option("#CBOFiltro", value=option["value"])

                # Esperar un tiempo
                page.wait_for_timeout(2000)

                # Click para descargar (con manejo de descarga)
                with page.expect_download() as download_info:
                    frame.click("#export2")

                # Guardar el archivo descargado
                download = download_info.value
                save_path = os.path.join(os.getcwd(), f"download/{name}/{option["text"]}.csv")
                download.save_as(save_path)
                print("Archivo descargado en:", save_path)

            browser.close()
    except KeyboardInterrupt:
        print("Cerrando app :(")