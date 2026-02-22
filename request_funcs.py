import requests
from keys import geocoder_key, static_key, geosearch_key

static_server = 'https://static-maps.yandex.ru/v1'
geocoder_server = 'https://geocode-maps.yandex.ru/1.x'
geosearch_server = 'https://search-maps.yandex.ru/v1'


def ll_from_address(address: str) -> str:
    """Получение долготы и широты по адресу"""

    params = {
        'apikey': geocoder_key,
        'geocode': address,
        'format': 'json'
    }
    response = requests.get(geocoder_server, params=params)
    if not response:
        raise RuntimeError(f'Ошибка при выполнении запроса: {response.status_code} {response.reason}')
    json_response = response.json()
    features = json_response['response']['GeoObjectCollection']['featureMember']
    if not features:
        raise RuntimeError('Адрес не найден')
    most_relevant = features[0]
    return most_relevant['GeoObject']['Point']['pos'].replace(' ', ',')


def image_from_params(**params) -> bytes:
    """Получение изображения по параметрам"""
    print(params)
    params['apikey'] = static_key
    if 'pt' in params and params['pt'] == '':
        del params['pt']
    response = requests.get(static_server, params=params)
    print(response.reason)
    if not response:
        raise RuntimeError(f'Ошибка при выполнении запроса: {response.status_code} {response.reason}')
    return response.content

def full_adderss_from_geocode(ll: str, add_mail_index=False) -> str:
    """Получение полного адреса по координатам"""
    params = {
        'apikey': geocoder_key,
        'geocode': ll,
        'format': 'json'
    }
    response = requests.get(geocoder_server, params=params)
    if not response:
        raise RuntimeError(f'Ошибка при выполнении запроса: {response.status_code} {response.reason}')
    json_response = response.json()
    features = json_response['response']['GeoObjectCollection']['featureMember']
    if not features:
        raise RuntimeError('Адрес не найден')
    most_relevant = features[0]
    mail_index = most_relevant['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
    if add_mail_index:
        return f'{most_relevant["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]}, индекс: {mail_index}'
    return most_relevant['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']