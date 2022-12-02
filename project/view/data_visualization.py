"""
This class visualizes the data for the user.

It works as a view for the application.
It only has access to the controller.
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap

from graph import GraphWidget
from project.model.apirequests import*

class DataVisualization(QWidget):
    def __init__(self):
        super().__init__()


    def get_view(self, settings, view):

        if view == 0:
            return self.get_current_view(settings)
        elif view == 1:
            return self.get_history_view(settings)
        else:
            return self.get_saved_view()


    def get_current_view(self, settings):
        vBox = QtWidgets.QVBoxLayout(self)
        #Tätä käytetään today tabilla (Jos current settingseis ei oo start tai end datea)
        weatherForecast = weather_forecast('TAMPERE')

        #Tätä käytetään history ja compare tabeilla (Jos current settingseis on start tai end datea)
        weatherData = weather_daily_measurements('TAMPERE', start_time=datetime.now() - timedelta(days=14),
                               end_time=datetime.now() - timedelta(days=1))

        graphObserved = GraphWidget(weatherData)
        graphForecast = GraphWidget(weatherForecast)
        vBox.addWidget(graphForecast)
        vBox.addWidget(graphObserved)
        if weather_cameras("TAMPERE"):
            label = QLabel(self)
            pixmap = QPixmap('../weather_cam.jpg')
            label.setPixmap(pixmap)
            vBox.addWidget(label)
            #self.resize(pixmap.width(), pixmap.height())


        foo = QtWidgets.QWidget()
        foo.setLayout(vBox)
        return foo

    def get_history_view(self, settings):
        pass

    def get_saved_view(self):
        pass