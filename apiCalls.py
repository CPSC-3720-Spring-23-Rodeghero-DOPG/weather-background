import http.client, urllib.parse
import json
import requests
import urllib.request

def getCityCoords(city: str, state: str) -> list:
    conn = http.client.HTTPConnection('api.positionstack.com')

    params = urllib.parse.urlencode({
        'access_key': 'dbbedb2b43064fb0121ab645a874dbc4',
        'query': city,
        'region': state,
        'limit': 1,
    })

    conn.request('GET', '/v1/forward?{}'.format(params))

    res = conn.getresponse()
    data = json.load(res)
    return [data['data'][0]['latitude'], data['data'][0]['longitude']]

def getWeatherInfo(latitude: float, longitude: float) -> str:
    URL = 'https://api.weather.gov/points/{},{}/'.format(latitude, longitude)

    response = requests.get(URL)
    res = response.json()
    forecastURL = res['properties']['forecast']

    response = requests.get(forecastURL)
    res = response.json()
    return res['properties']['periods'][0]['shortForecast']

def getPopulationInfo(city: str, state: str)->float:
    census=urllib.request.urlopen(urllib.request.Request(f'https://api.census.gov/data/2021/acs/acs1?get=NAME,B01001_001E&for=place&in=state:{str(state).zfill(2)}&key={censusKey}'))
    censusBytes=census.read()
    censusStr=censusBytes.decode('utf8')
    census.close()
    censusJson=json.loads(censusStr)

    for cityArr in censusJson:
        if cityArr[0] == city:
            return cityArr[1]
        
    return 0