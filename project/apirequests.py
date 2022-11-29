"""
This file fetches data from digitraffic and the fmi

For data, a start and end time are required.

For a forecast, the end time of the forecast is required.

Requests are parsed into python dict containers and returned.
"""

from datetime import datetime
from datetime import timedelta
import requests
from collections import Counter
import operator
from fmiopendata.wfs import download_stored_query


fmi_queries = ["fmi::forecast::harmonie::surface::point::multipointcoverage",
               "fmi::observations::weather::multipointcoverage"]
fmi_coordinates = {"TAMPERE": "61.49911,23.78712", "HELSINKI": "60.192059,24.945831", "OULU": "65.01236,25.46816",
                   "TURKU": "60.45451,22.26482", "LAPPEENRANTA": "61.05871,28.18871"}
# minlon, minlat, maxlon, maxlat
fmi_bbox = {"TAMPERE": "23.652361,61.435179,23.865908,61.520098",
                         "HELSINKI": "24.785044,60.134141,25.172312,60.286969",
                         "OULU": "25.398253,64.987359,25.562361,65.037538",
                         "TURKU": "22.197470,60.422136,22.344069,60.474289",
                         "LAPPEENRANTA": "28.106238,61.025745,28.272406,61.071282"}

digitrafi_maintenance_base_url = "https://tie.digitraffic.fi/api/maintenance/v1/tracking/routes?endFrom="

# minlon, minlat, maxlon, maxlat
FMISIDS = {"TAMPERE": "101124",
           "HELSINKI": "100971",
           "OULU": "101786",
           "TURKU": "101065",
           "LAPPEENRANTA": "101237"}

# Kaupunkien nimet pitää ehkä vaihtaa muotoon esim. "Tampere"
digitrafi_coordinates = {"TAMPERE": "23.652361,61.435179,23.865908,61.520098",
                         "HELSINKI": "24.785044,60.134141,25.172312,60.286969",
                         "OULU": "25.398253,64.987359,25.562361,65.037538",
                         "TURKU": "22.197470,60.422136,22.344069,60.474289",
                         "LAPPEENRANTA": "28.106238,61.025745,28.272406,61.071282"}


def weather_data(city, end_time=datetime.now() - timedelta(days=1), start_time=datetime.now() - timedelta(days=2),
                 timestep="60"):
    start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    data = download_stored_query(fmi_queries[1],
                                 args=["bbox=" + fmi_bbox[city], "timestep=" + timestep, "starttime=" + start,
                                       "endtime=" + end, "parameters=t2m,ws_10min,n_man", "timeseries=True"])
    return data.data


def weather_forecast(city, end_time=datetime.now()+timedelta(days=1), start_time=datetime.now(), timestep="60"):
    start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    data = download_stored_query(fmi_queries[0],
                                 args=["latlon=" + fmi_coordinates[city], "timestep=" + timestep, "starttime=" + start,
                                       "endtime=" + end, "parameters=temperature,windspeedms", "timeseries=True"])
    return data.data


def road_data(city, end_time=datetime.now() + timedelta(days=1), start_time=datetime.now(), task_name="",
              situation_type=""):
    start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    maintenance_data = get_maintenance_data(city, start, end, task_name)
    traffic_messages = get_traffic_messages(situation_type, city)
    road_condition = get_road_condition(city)
    return maintenance_data, traffic_messages, road_condition


def get_maintenance_data(city, start, end, task_name=""):
    coordinates = digitrafi_coordinates[city].split(",")
    url = digitrafi_maintenance_base_url + start + "&endBefore=" + end \
          + "&xMin=" + coordinates[0] + "&yMin=" + coordinates[1] + "&xMax=" + coordinates[2] \
          + "&yMax=" + coordinates[3] + "&taskId=" + task_name + "&domain=state-roads"
    response = requests.get(url)
    # the searched data is converted into a dictionary
    maintenance_data_temp = response.json()
    maintenance_data = format_maintenance_data(city, maintenance_data_temp)
    return maintenance_data


def format_maintenance_data(city, maintenance_data):
    data = {"tasks": [], "startTime": [], "endTime": []}

    for features in maintenance_data['features']:
        data["tasks"].append(features['properties']['tasks'])
        data["startTime"].append(features['properties']['startTime'])
        data["endTime"].append(features['properties']['endTime'])

    maintenance_data = {city: data}
    return maintenance_data


def get_traffic_messages(situation_type, city):
    url = "https://tie.digitraffic.fi/api/traffic-message/v1" \
          "/messages?inactiveHours=0&includeAreaGeometry=false&situationType="\
          + situation_type
    response = requests.get(url)
    all_traffic_messages = response.json()
    # Find all messages from the area (location_code)
    city_messages = format_traffic_messages(city, all_traffic_messages)

    return city_messages


def format_traffic_messages(city, all_traffic_messages):
    coordinates = digitrafi_coordinates[city].split(",")
    coordinates = [float(c) for c in coordinates]
    messages = {"situationType": [], "name": [], "comment": []}

    for feature in all_traffic_messages['features']:
        if feature['geometry'] != None:
            for coords in feature['geometry']['coordinates']:
                if type(coords) == list:
                    for cordPair in coords:
                        if len(cordPair) == 2:
                            if cordPair[0] > coordinates[0] and cordPair[0] < coordinates[2] and cordPair[1] > coordinates[1] and cordPair[0] < coordinates[3]:
                                messages["situationType"].append(feature['properties']['situationType'])
                                messages["name"].append(feature['properties']['announcements'][0]['features'][0]['name'])
                                messages["comment"].append(feature['properties']['announcements'][0]['comment'])
                                break

    traffic_msg = {city: messages}
    return traffic_msg


def get_road_condition(city):
    coordinates = digitrafi_coordinates[city].split(",")
    url = "https://tie.digitraffic.fi/api/v3/data/road-conditions/" \
          + coordinates[0] + "/" + coordinates[1] + "/" + coordinates[2] + "/" + coordinates[3]
    response = requests.get(url)
    # the searched data is converted into a dictionary
    all_condition_data = response.json()
    condition_data = parse_road_condition(city, all_condition_data)
    return condition_data


def parse_road_condition(city, condition_data):
    conditions = {"0h": {"daylight": [], "roadTemperature": [],
                         "overallRoadCondition": []},
                  "2h": {"daylight": [], "roadTemperature": [],
                         "overallRoadCondition": [],
                         "precipitationCondition": [], "roadCondition": []},
                  "4h": {"daylight": [], "roadTemperature": [],
                         "overallRoadCondition": [],
                         "precipitationCondition": [], "roadCondition": []},
                  "6h": {"daylight": [], "roadTemperature": [],
                         "overallRoadCondition": [],
                         "precipitationCondition": [], "roadCondition": []},
                  "12h": {"daylight": [], "roadTemperature": [],
                          "overallRoadCondition": [],
                          "precipitationCondition": [], "roadCondition": []}}

    for weatherData in condition_data['weatherData']:
        for roadConditions in weatherData['roadConditions']:
            conditions[roadConditions['forecastName']]["daylight"].append(roadConditions['daylight'])
            conditions[roadConditions['forecastName']]["roadTemperature"] += [float(roadConditions['roadTemperature'])]
            conditions[roadConditions['forecastName']]["overallRoadCondition"].append(roadConditions['overallRoadCondition'])
            if roadConditions['forecastName'] != "0h":
                conditions[roadConditions['forecastName']]["precipitationCondition"].append(roadConditions['forecastConditionReason']['precipitationCondition'])
                conditions[roadConditions['forecastName']]["roadCondition"].append(roadConditions['forecastConditionReason']['roadCondition'])

    for data in conditions.values():
        temp_daylight = Counter(data["daylight"])
        avg_daylight = max(temp_daylight.items(), key=operator.itemgetter(1))[0]
        data["daylight"] = [avg_daylight]

        avg_roadTemp = sum(data["roadTemperature"]) / len(data["roadTemperature"])
        data["roadTemperature"] = [avg_roadTemp]

        temp_ovcond = Counter(data["overallRoadCondition"])
        avg_ovcond = max(temp_ovcond.items(), key=operator.itemgetter(1))[0]
        data["overallRoadCondition"] = [avg_ovcond]

        if "precipitationCondition" in data:
            temp_precip = Counter(data["precipitationCondition"])
            avg_precip = max(temp_precip.items(), key=operator.itemgetter(1))[0]
            data["precipitationCondition"] = [avg_precip]

        if "roadCondition" in data:
            temp_rd = Counter(data["roadCondition"])
            avg_rd = max(temp_rd.items(), key=operator.itemgetter(1))[0]
            data["roadCondition"] = [avg_rd]

    current_cond = {city: conditions}
    return current_cond
