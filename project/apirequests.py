"""
This file fetches data from digitraffic and the fmi

For data, a start and end time are required.

For a forecast, the end time of the forecast is required.

Requests are parsed into python dict containers and returned.
"""

from datetime import datetime
from datetime import timedelta
import requests

fmi_base_url = "https://opendata.fmi.fi/wfs?request=getfeature&version=2.0.0&storedquery_id="
fmi_queries = ["fmi::forecast::harmonie::surface::point::timevaluepair", "fmi::observations::weather::timevaluepair"]
fmi_coordinates = {"TAMPERE": "61.49911,23.78712", "HELSINKI": "60.192059,24.945831", "OULU": "65.01236,25.46816",
                   "TURKU": "60.45451,22.26482", "LAPPEENRANTA": "61.05871,28.18871"}

digitrafi_maintenance_base_url = "https://tie.digitraffic.fi/api/maintenance/v1/tracking/routes?endFrom="

# minlon, minlat, maxlon, maxlat
fmi_bboxes = {"TAMPERE": "", "HELSINKI": "", "OULU": "", "TURKU": "", "LAPPEENRANTA": ""}


digitrafi_coordinates = {"TAMPERE": "23.652361,61.435179,23.865908,61.520098",
                         "HELSINKI": "24.785044,60.134141,25.172312,60.286969",
                         "OULU": "25.398253,64.987359,25.562361,65.037538",
                         "TURKU": "22.197470,60.422136,22.344069,60.474289",
                         "LAPPEENRANTA": "28.106238,61.025745,28.272406,61.071282"}
digitrafi_location_codes = {"TAMPERE": "408", "HELSINKI": "73", "OULU": "291",
                            "TURKU": "418", "LAPPEENRANTA": "213"}

# Ota selvää parametreistä ja korjaa
def weather_data(city, end_time=datetime.now(), start_time=datetime.now()-timedelta(days=1), timestep="30"):
    start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = fmi_base_url + fmi_queries[1] + "&latlon=" + fmi_coordinates[city] + "&timestep=" + timestep + "&starttime" \
        "=" + start + "&endtime=" + end + "&parameters=temperature,windspeedms"

    return url


# URL toimii?
def weather_forecast(city, end_time=datetime.now()+timedelta(days=1), start_time=datetime.now(), timestep="30"):
    start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = fmi_base_url + fmi_queries[0] + "&latlon=" + fmi_coordinates[city] + "&timestep=" + timestep + "&starttime" \
        "=" + start + "&endtime=" + end + "&parameters=temperature,windspeedms"

    return url


def road_data(city, end_time=datetime.now()+timedelta(days=1), start_time=datetime.now(), task_name="", situation_type="", location_code=""):
    start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    maintenance_data = get_maintenance_data(city, start, end, task_name)
    traffic_messages = get_traffic_messages(situation_type, location_code)
    return maintenance_data, traffic_messages


def get_maintenance_data(city, start, end, task_name):
    coordinates = digitrafi_coordinates[city].split(",")
    url = digitrafi_maintenance_base_url + start + "&endBefore=" + end \
          + "&xMin=" + coordinates[0] + "&yMin=" + coordinates[1] + "&xMax=" + coordinates[2] \
          + "&yMax=" + coordinates[3] + "&taskId=" + task_name + "&domain=state-roads"
    response = requests.get(url)
    # the searched data is converted into a dictionary
    maintenance_data = response.json()
    # print(maintenance_data['features'][0]['properties']['tasks'])
    return maintenance_data


def get_traffic_messages(situation_type, location_code):
    url = "https://tie.digitraffic.fi/api/traffic-message/v1" \
          "/messages?inactiveHours=0&includeAreaGeometry=false&situationType="\
          + situation_type
    response = requests.get(url)
    all_traffic_messages = response.json()
    # Find all messages from the area (location_code)
    # all_traffic_messages['features'][0]['properties']['tasks']
    pass


def road_condition(city):
    coordinates = digitrafi_coordinates[city].split(",")
    url = "https://tie.digitraffic.fi/api/v3/data/road-conditions/" \
          ""+coordinates[0]+"/"+coordinates[1]+"/"+coordinates[2]+"/"+coordinates[3]
    response = requests.get(url)
    # the searched data is converted into a dictionary
    condition_data = response.json()
    # print(condition_data['weatherData'][0]['roadConditions'][0]['forecastName'])
    # print(condition_data['weatherData'][0]['roadConditions'][0]['roadTemperature'])
    return condition_data
