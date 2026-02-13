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
    return most_relevant['GeoObject']['Point']['pos']


def image_from_params(**params) -> bytes:
    """Получение изображения по параметрам"""

    params['apikey'] = static_key
    response = requests.get(static_server, params=params)
    if not response:
        raise RuntimeError(f'Ошибка при выполнении запроса: {response.status_code} {response.reason}')
    return response.content