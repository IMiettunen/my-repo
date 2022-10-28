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

# minlon, minlat, maxlon, maxlat
FMISIDS = {"TAMPERE": "101123", "HELSINKI": "101007", "OULU": "101789", "TURKU": "100948", "LAPPEENRANTA": "101247"}


# Ota selvää parametreistä ja korjaa
def weather_data(city, end_time=datetime.now(), start_time=datetime.now()-timedelta(days=1), timestep="30"):
    start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = fmi_base_url + fmi_queries[1] + "&fmisid=" + FMISIDS[city] + "&timestep=" + timestep + "&starttime" \
        "=" + start + "&endtime=" + end

    return url


# URL toimii?
def weather_forecast(city, end_time=datetime.now()+timedelta(days=1), start_time=datetime.now(), timestep="30"):
    start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = fmi_base_url + fmi_queries[0] + "&latlon=" + fmi_coordinates[city] + "&timestep=" + timestep + "&starttime" \
        "=" + start + "&endtime=" + end + "&parameters=temperature,windspeedms"

    return url


def road_data():
    pass


def road_forecast():
    pass
