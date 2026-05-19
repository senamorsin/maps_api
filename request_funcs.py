import math
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


def _haversine_meters(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    r = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def organization_at_point(ll: str, max_distance_m: float = 50.0):
    """Найти первую организацию рядом с точкой ll. Возвращает (name, address, ll_str) или None,
    если ничего не найдено или ближайшая организация дальше max_distance_m метров."""
    lon, lat = map(float, ll.split(','))
    try:
        geo_resp = requests.get(geocoder_server, params={
            'apikey': geocoder_key, 'geocode': ll, 'format': 'json',
        }, timeout=10)
        if not geo_resp:
            return None
        geo_features = geo_resp.json()['response']['GeoObjectCollection']['featureMember']
        if not geo_features:
            return None
        text = geo_features[0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
        response = requests.get(geosearch_server, params={
            'apikey': geosearch_key, 'text': text, 'lang': 'ru_RU',
            'll': ll, 'type': 'biz', 'results': 1,
        }, timeout=10)
        if not response:
            return None
        features = response.json().get('features', [])
    except requests.RequestException:
        return None
    if not features:
        return None
    org = features[0]
    org_lon, org_lat = org['geometry']['coordinates']
    if _haversine_meters(lon, lat, org_lon, org_lat) > max_distance_m:
        return None
    meta = org['properties']['CompanyMetaData']
    return meta.get('name', ''), meta.get('address', ''), f'{org_lon},{org_lat}'