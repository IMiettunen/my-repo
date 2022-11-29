from PyQt5.QtWidgets import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.widgets import CheckButtons
import datetime as dt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import random as rand
import matplotlib.markers
import PyQt5.QtCore


forecast = {
    'Tampere': {
        'Times': [dt.datetime(2022, 11, 28, 0, 0), dt.datetime(2022, 11, 28, 1, 0), dt.datetime(2022, 11, 28, 2, 0),
                  dt.datetime(2022, 11, 28, 3, 0), dt.datetime(2022, 11, 28, 4, 0), dt.datetime(
                      2022, 11, 28, 5, 0), dt.datetime(2022, 11, 28, 6, 0),
                  dt.datetime(2022, 11, 28, 7, 0), dt.datetime(2022, 11, 28, 8, 0), dt.datetime(
                      2022, 11, 28, 9, 0), dt.datetime(2022, 11, 28, 10, 0),
                  dt.datetime(2022, 11, 28, 11, 0), dt.datetime(2022, 11, 28, 12, 0), dt.datetime(
                      2022, 11, 28, 13, 0), dt.datetime(2022, 11, 28, 14, 0),
                  dt.datetime(2022, 11, 28, 15, 0), dt.datetime(2022, 11, 28, 16, 0), dt.datetime(
                      2022, 11, 28, 17, 0), dt.datetime(2022, 11, 28, 18, 0),
                  dt.datetime(2022, 11, 28, 19, 0), dt.datetime(2022, 11, 28, 20, 0), dt.datetime(
                      2022, 11, 28, 21, 0), dt.datetime(2022, 11, 28, 22, 0),
                  dt.datetime(2022, 11, 28, 23, 0)],

        'Temperature': {
            'values': [4, 4, 3, 3, 3, 4, 4, 5, 5, 6, 7, 7, 8, 9, 9, 11, 12, 12, 10, 9, 8, 7, 6, 5],
            'unit': 'xx'
        },

        'Windspeedms': {
            'values': [6, 7, 8, 7, 8, 7, 6, 5, 3, 3, 1, 2, 1, 2, 2, 3, 4, 5, 6, 7, 6, 7, 8, 8],
            'unit': 'xx'
        }
    }
}
observed = {
    'Tampere': {
        'Times': [],

        'Temperature': {
            'values': [],
            'unit': 'degC'
        },
        'Wind': {
            'values': [],
            'unit': 'm/s'
        },
        'Cloud': {
            'values': [],
            'unit': '1/8'
        }
    }
}
hour_rain_temp_wind = {
    '00:00': [1.0, 4, 6],
    '01:00': [3.5, 4, 7],
    '02:00': [2.0, 3, 8],
    '03:00': [4.0, 3, 7],
    '04:00': [5.5, 3, 8],
    '05:00': [0.0, 4, 7],
    '06:00': [5.5, 4, 6],
    '07:00': [0.0, 5, 5],
    '08:00': [1.0, 5, 3],
    '09:00': [3.5, 6, 3],
    '10:00': [2.0, 7, 1],
    '11:00': [4.0, 7, 2],
    '12:00': [5.5, 8, 1],
    '13:00': [0.0, 9, 2],
    '14:00': [1.0, 9, 2],
    '15:00': [3.5, 11, 3],
    '16:00': [2.0, 12, 4],
    '17:00': [4.0, 12, 5],
    '18:00': [5.5, 10, 6],
    '19:00': [0.0, 9, 7],
    '20:00': [1.0, 8, 6],
    '21:00': [3.5, 7, 7],
    '22:00': [2.0, 6, 8],
    '23:00': [4.0, 5, 8]
}


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self):  # , parent=None, width=5, height=4, dpi=100
        fig = Figure()  # figsize=(width, height), dpi=dpi
        self.ax1 = fig.add_subplot()
        self.ax2 = self.ax1.twinx()
        self.ax3 = self.ax1.twinx()
        self.ax3.spines.right.set_position(("axes", 1.05))
        #self.ax3.set_ylim(1, 20)
        self.figure = fig
        plt.subplots_adjust(left=0.01, bottom=0.01,
                            right=0.99, top=0.99, wspace=0, hspace=0)
        plt.margins(2)
        self.ax1.patch.set_alpha(0.0)
        fig.patch.set_facecolor('grey')
        self.figure.patch.set_alpha(0.1)

        super().__init__(fig)


class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        RBlayout = QGridLayout()
        self.span = 12
        self.data = forecast
        # self.xData = [dt.datetime.strptime(h, '%H:%M')for h in data["Tampere"]["Times"]]
        self.xData = self.data["Tampere"]["Times"]

        twoRB = QRadioButton("2h")
        twoRB.toggled.connect(self.onClicked)
        RBlayout.addWidget(twoRB, 0, 0)

        fourRB = QRadioButton("4h")
        fourRB.toggled.connect(self.onClicked)
        RBlayout.addWidget(fourRB, 0, 1)

        sixRB = QRadioButton("6h")
        sixRB.toggled.connect(self.onClicked)
        RBlayout.addWidget(sixRB, 0, 2)

        eightRB = QRadioButton("8h")
        eightRB.toggled.connect(self.onClicked)
        RBlayout.addWidget(eightRB, 0, 3)

        twelveRB = QRadioButton("12h")
        twelveRB.setChecked(True)
        twelveRB.toggled.connect(self.onClicked)
        RBlayout.addWidget(twelveRB, 0, 4)

        hlayout.addLayout(RBlayout)

        self.tempButton = QPushButton("Temp")
        hlayout.addWidget(self.tempButton)
        self.rainButton = QPushButton("Rain")
        hlayout.addWidget(self.rainButton)
        self.windButton = QPushButton("Wind")
        hlayout.addWidget(self.windButton)
        self.allButton = QPushButton("All")
        hlayout.addWidget(self.allButton)
        vlayout.addLayout(hlayout)

        # canvas gets created during init once
        self.sc = MplCanvas()  # self, width=500, height=400, dpi=100
        vlayout.addWidget(self.sc)

        self.setLayout(vlayout)

        self.draw_graph()

        self.tempButton.pressed.connect(lambda: self.draw_graph(
            [1.0, 0.2, 0.2], [True, False, False], ['bold', 'normal', 'normal']))
        self.rainButton.pressed.connect(lambda: self.draw_graph(
            [0.2, 1.0, 0.2], [False, True, False], ['normal', 'bold', 'normal']))
        self.windButton.pressed.connect(lambda: self.draw_graph(
            [0.2, 0.2, 1.0], [False, False, True], ['normal', 'normal', 'bold']))
        self.allButton.pressed.connect(lambda: self.draw_graph())

        self.setMinimumSize(450, 100)
        #self.resize(650, 400)

        self.setWindowFlags(PyQt5.QtCore.Qt.FramelessWindowHint)
        self.setAttribute(PyQt5.QtCore.Qt.WA_TranslucentBackground)

        self.show()

    def format_yData(self, forecast):
        #time = forecast['Tampere']['Times']
        temperature = forecast["Tampere"]["Temperature"]["values"]
        wind = forecast["Tampere"]["Windspeedms"]["values"]
        #forecast['Tampere']['Times'] = lista
        # forecast['Tampere']['Temperature'].get('values) = lista
        # forecast['Tampere']['Wind'].get('values') = lista

        return temperature, wind

    def get_limits(self):
        # Gets x-axis limits from ongoing hour(rounded down) and chosen forecast length
        # returns indexes for start and finish
        #now = dt.datetime.now().hour()
        now = dt.datetime.now().replace(microsecond=0, second=0, minute=0, day=28)
        start = list(self.data["Tampere"]["Times"]).index(now)

        return start, start + self.span

    def draw_graph(self, alphas=[1.0, 1.0, 1.0], grids=[False, False, False], font=['bold', 'bold', 'bold']):
        # Draw linegraph for temperature and scattered chart for wind and bar chart for rain

        y3 = [i[0] for i in hour_rain_temp_wind.values()]  # Rain
        x = self.xData
        width = 0.01

        # Y-axis data, y1 = temperature, y2 = wind
        #y1, y2 = self.format_yData(forecast)
        y1 = forecast["Tampere"]["Temperature"]["values"]
        y2 = forecast["Tampere"]["Windspeedms"]["values"]

        ax1 = self.sc.ax1
        ax2 = self.sc.ax2
        ax3 = self.sc.ax3
        ax1.cla()
        ax2.cla()
        ax3.cla()

        ax3.spines.right.set_position(("axes", 1.05))
        ax2.set_visible(True)

        ax1.set_zorder(1)  # brings ax1 to front
        ax1.patch.set_visible(False)

        # Plot line graph with red line and bar chart with blue bars, add labels to axes
        ax1.plot(x, y1, 'r-', label="Temperature", alpha=alphas[0])
        # matplotlib.markers.CARETRIGHT
        ax2.scatter(x, y2, marker='4',
                    alpha=alphas[2],  color='k', label="Wind")
        ax3.bar(x, y3, width=width, label="Rain", alpha=alphas[1])
        ax1.set_ylabel('°C', loc='top', color='r',
                       fontweight=font[0], alpha=alphas[0], rotation=0)
        ax2.set_ylabel('m/s',  loc='top', color='k',
                       fontweight=font[2], alpha=alphas[2], rotation=0)

        ax3.set_ylabel('mm',  loc='top', color='b',
                       fontweight=font[1], alpha=alphas[1], rotation=0)

        # Setting limits and frequency to y-axes
        #start, end = ax1.get_ylim()
        ax1.yaxis.set_ticks(np.arange(-4, 19, 2))
        start2, end2 = ax2.get_ylim()
        ax2.yaxis.set_ticks(np.arange(0, end2, 1))
        start3, end3 = ax3.get_ylim()
        ax3.yaxis.set_ticks(np.arange(0, end3, 1))

        # Figure styling + Combined lables box
        if grids[0]:
            # , linestyle='--', color = 'r'
            ax1.grid(grids[0], linestyle='--', color='r')
        if grids[1]:
            ax2.grid(grids[1], linestyle='--', color='b')
        if grids[2]:
            ax3.grid(grids[2], linestyle='--', color='black')
        # ax1.legend(frameon=True)
        line, label = ax1.get_legend_handles_labels()
        line2, label2 = ax2.get_legend_handles_labels()
        line3, label3 = ax3.get_legend_handles_labels()
        ax1.legend(line + line2 + line3, label + label2 + label3,
                   frameon=True, loc='best')  # , bbox_to_anchor=(0.5, 0.0, 0.5, 0.5)
        ax1.spines['top'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax3.spines['top'].set_visible(False)

        self.format_xaxis()

    def format_xaxis(self):
        start, end = self.get_limits()
        #x = self.xData[start:end+1]
        x_axis = self.xData[start:end+1]
        #self.xData = [dt.datetime.strptime(h,'%H:%M') for h in list(self.data.keys())]

        self.sc.ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        self.sc.ax1.set_xlabel('Time')
        self.sc.figure.autofmt_xdate()
        self.sc.ax1.set_xbound(x_axis[0] - dt.timedelta(minutes=10),
                               x_axis[len(x_axis)-1] + dt.timedelta(minutes=10))

        self.sc.draw()

    def onClicked(self):
        radioButton = self.sender()
        span = radioButton.text()[:-1]
        # radioButton.isChecked()
        self.span = int(span)
        self.format_xaxis()


# app = QApplication([])
# graph = GraphWidget(forecast)
# app.exec_()
