import requests
from bs4 import BeautifulSoup

# Creando sesión
session = requests.Session()

# URL de la página que deseas scrapear
url = 'https://www.senamhi.gob.pe/mapas/mapa-estaciones-2/map_red_graf.php?cod=101004&estado=AUTOMATICA&tipo_esta=M&cate=EMA&cod_old='

# Realizando la solicitud GET
response = session.get(url)
# Verificando el estado de la respuesta
if response.status_code == 200:
    # Analizando el contenido HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Capturando código captcha
    captcha_span = soup.find('span', style='color: red; font-size:xxx-large')
    if captcha_span:
        captcha_code = captcha_span.text.strip()
        print(f'Captcha code: {captcha_code}')
    else:
        print('Captcha code not found.')
    print('Cookies before captcha:', session.cookies.get_dict())

    # Enviar captcha a servidor para generar cookies
    
    url_captcha = 'https://www.senamhi.gob.pe/mapas/mapa-estaciones-2/captcha/config/check.php'
    data_captcha = {
        'captchaInput': captcha_code,
        'captcha': captcha_code,
        'action': 'validarUsuario'
    }
    headers = {
        'Referer': url,
    }
    response_captcha = session.post(url_captcha, data=data_captcha, headers=headers)
    # Verificando el estado de la respuesta
    if response_captcha.status_code == 200:
        print('Captcha sent successfully.')
    else:
        print('Failed to send captcha.')
    print(response_captcha.text)

    print('Cookies after captcha:', session.cookies.get_dict())

    # Seleccionar periodo a descargar
    filter = '202505'
    url_csv = f'https://www.senamhi.gob.pe/mapas/mapa-estaciones-2/_dt_est_tp_0s3n@mH1.php?estaciones=101004&t_e=M&CBOFiltro={filter}&estado=AUTOMATICA&cod_old=EMA&cate_esta=&alt=199&export2='
    
    response_csv = session.get(url_csv)
    # Verificando el estado de la respuesta
    if response_csv.status_code == 200:
        print('CSV file downloaded successfully.')
        with open('data.csv', 'wb') as f:
            f.write(response_csv.content)
    else:
        print('Failed to download CSV file.')


    #print(soup.prettify())