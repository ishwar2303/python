from flask import Flask, request, Response
import json
import requests

app = Flask(__name__)

@app.route('/weather', methods=['POST'])
def getWeatherDetails():
    args = request.json
    assert args.get('city'), 'City Required'
    assert args.get('output_format'), 'Output Format Required'

    city = args.get('city')
    output_format = args.get('output_format')

    json_res = weatherAPIFromRapidAPI(city)

    location = json_res['location']
    latitude = location['lat']
    longitude = location['lon']
    location_name = location['name'] + ' ' + location['country']
    temperature = json_res['current']['temp_c']

    assert output_format == 'json' or output_format == 'xml', 'Output Format can only be json or xml'

    if output_format == 'json':
        res_json = {
            'Weather': temperature,
            'Latitude': latitude,
            'Longitude': longitude,
            'City': location_name
        }
        return Response(json.dumps(res_json), mimetype='text/json')
    
    if output_format == 'xml':
        res_xml = (
            f'<?xml version="1.0" encoding="UTF-8" ?>'
            f'<root>'
            f'<Temperature>{temperature}</Temperature>'
            f'<City>{location_name}</City>'
            f'<Latitude>{latitude}</Latitude>'
            f'<Longitude>{longitude}</Longitude>'
            f'</root>'
        )
        return Response(res_xml, mimetype='text/xml')


def weatherAPIFromRapidAPI(city):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q": city}
    headers = {
        "X-RapidAPI-Key": "31371bc5c3msh34f399b07961d46p192883jsn2ba7562e3194",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

# Checking Data from RapidApi
# @app.route('/rapid-weather-api', methods=['GET'])
# def getWeatherData(): 
#     json_data = weatherAPIFromRapidAPI('Mumbai')
#     return json_data

if __name__ == '__main__':
    app.run(debug=True)
