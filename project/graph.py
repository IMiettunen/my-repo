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

# Testdata containing hourly weather forecast (Location, Time, Temperature, windspeed)
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

        'windspeedms': {
            'values': [6, 7, 8, 7, 8, 7, 6, 5, 3, 3, 1, 2, 1, 2, 2, 3, 4, 5, 6, 7, 6, 7, 8, 8],
            'unit': 'xx'
        }
    }
}

# Testdata containing daily averages for a month (Location, Time, Temperature, windspeed, cloudcoverage)
observed = {
    'Tampere': {
        'Times': [dt.datetime(2022, 11, 1, 0, 0), dt.datetime(2022, 11, 2, 0, 0),
                  dt.datetime(2022, 11, 3, 0, 0),
                  dt.datetime(2022, 11, 4, 0, 0), dt.datetime(
                      2022, 11, 5, 0, 0),
                  dt.datetime(2022, 11, 6, 0, 0), dt.datetime(
                      2022, 11, 7, 0, 0),
                  dt.datetime(2022, 11, 8, 0, 0), dt.datetime(
                      2022, 11, 9, 0, 0),
                  dt.datetime(2022, 11, 10, 0, 0), dt.datetime(
                      2022, 11, 11, 0, 0),
                  dt.datetime(2022, 11, 12, 0, 0), dt.datetime(
                      2022, 11, 13, 0, 0),
                  dt.datetime(2022, 11, 14, 0, 0), dt.datetime(
                      2022, 11, 15, 0, 0),
                  dt.datetime(2022, 11, 16, 0, 0), dt.datetime(
                      2022, 11, 17, 0, 0),
                  dt.datetime(2022, 11, 18, 0, 0), dt.datetime(
                      2022, 11, 19, 0, 0),
                  dt.datetime(2022, 11, 20, 0, 0), dt.datetime(
                      2022, 11, 21, 0, 0),
                  dt.datetime(2022, 11, 22, 0, 0), dt.datetime(
                      2022, 11, 23, 0, 0),
                  dt.datetime(2022, 11, 24, 0, 0), dt.datetime(
                      2022, 11, 25, 0, 0),
                  dt.datetime(2022, 11, 26, 0, 0), dt.datetime(
                      2022, 11, 27, 0, 0),
                  dt.datetime(2022, 11, 28, 0, 0), dt.datetime(
                      2022, 11, 29, 0, 0),
                  dt.datetime(2022, 11, 30, 0, 0)],

        'Temperature': {
            'values': [4, 4, 3, 3, 3, 4, 4, 5, 5, 6, 7, 7, 8, 9, 9, 11, 12, 12, 10, 9, 8, 7, 6, 5, 4, 5, 6, 5, 8, 6],
            'unit': 'degC'
        },
        'windspeedms': {
            'values': [6, 7, 8, 7, 8, 7, 6, 5, 3, 3, 1, 2, 1, 2, 2, 3, 4, 5, 6, 7, 6, 7, 8, 8, 1, 2, 2, 3, 4, 5],
            'unit': 'm/s'
        },
        'Cloud': {
            'values': [6, 7, 8, 7, 8, 7, 6, 5, 3, 2, 1, 1, 0, 0, 0, 3, 4, 5, 4, 6, 7, 7, 8, 8, 0, 0, 3, 4, 5, 4],
            'unit': '1/8'
        }
    }
}


class MplCanvas(FigureCanvasQTAgg):
    """A control which can be used to embded a matplotlib figure.

    Args:
        FigureCanvasQTAgg (class): A class MplCanvas inherits
    """

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
        # self.ax1.patch.set_alpha(0.0)
        # fig.patch.set_facecolor('grey')
        # self.figure.patch.set_alpha(0.1)

        super().__init__(fig)


class GraphWidget(QWidget):
    """Widget containing MPLCanvas to visualize weather data in graph

    Args:
        QWidget (Class): Class that GraphWidget inherits
    """

    def __init__(self, data):
        super().__init__()
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        radioButtonLayout = QGridLayout()
        self.span = 12

        # Data to be shown in graph
        self.data = data
        self.city = list(self.data.keys())[0]
        self.dataKeys = list(self.data[list(self.data.keys())[0]].keys())
        self.xData = list(self.data[self.city].values())[0]
        self.dataTypeForecast = True

        # Buttons to select what data is highlighted
        hlayout.addLayout(radioButtonLayout)
        self.tempButton = QPushButton("Temp")
        self.windButton = QPushButton("Wind")
        self.allButton = QPushButton("All")

        hlayout.addWidget(self.tempButton)
        hlayout.addWidget(self.windButton)
        vlayout.addLayout(hlayout)

        # Create buttons and radiobuttons according to visualized data
        if len(self.dataKeys) == 3:
            print("LEN DATAKEYS: ", len(self.dataKeys))
            self.dataTypeForecast = True
            twoRB = QRadioButton("2h")
            twoRB.toggled.connect(self.onClicked)
            radioButtonLayout.addWidget(twoRB, 0, 0)

            fourRB = QRadioButton("4h")
            fourRB.toggled.connect(self.onClicked)
            radioButtonLayout.addWidget(fourRB, 0, 1)

            sixRB = QRadioButton("6h")
            sixRB.toggled.connect(self.onClicked)
            radioButtonLayout.addWidget(sixRB, 0, 2)

            eightRB = QRadioButton("8h")
            eightRB.toggled.connect(self.onClicked)
            radioButtonLayout.addWidget(eightRB, 0, 3)

            twelveRB = QRadioButton("12h")
            twelveRB.setChecked(True)
            twelveRB.toggled.connect(self.onClicked)
            radioButtonLayout.addWidget(twelveRB, 0, 4)

        else:
            self.dataTypeForecast = False
            self.cloudButton = QPushButton("Clouds")
            hlayout.addWidget(self.cloudButton)
            self.cloudButton.pressed.connect(lambda: self.draw_graph(
                [0.2, 0.2, 1.0], [False, False, True], ['normal', 'normal', 'bold']))

        hlayout.addWidget(self.allButton)

        # Create canvas and set it to layout
        self.sc = MplCanvas()
        vlayout.addWidget(self.sc)
        self.setLayout(vlayout)
        self.draw_graph()

        # Buttonactions to select what data is highlighet in graph
        self.tempButton.pressed.connect(lambda: self.draw_graph(
            [1.0, 0.2, 0.2], [True, False, False], ['bold', 'normal', 'normal']))
        self.windButton.pressed.connect(lambda: self.draw_graph(
            [0.2, 1.0, 0.2], [False, True, False], ['normal', 'bold', 'normal']))
        self.allButton.pressed.connect(lambda: self.draw_graph())

        self.setMinimumSize(450, 100)
        #self.resize(650, 400)

        # SET VISIBILITY OF WIDGET "WINDOW"
        # self.setWindowFlags(PyQt5.QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(PyQt5.QtCore.Qt.WA_TranslucentBackground)

        self.show()

    def draw_graph(self, alphas=[1.0, 1.0, 1.0], grids=[False, False, False], font=['bold', 'bold', 'bold']):
        """This functions draws the graph. Line chart for temperature and scattered chart for wind and cloudcoverage if necessary

        Args:
            alphas (list, float): Tells what data is highlighted. Defaults to [1.0, 1.0, 1.0] (All visible).
            grids (list, bool): Tells what data is highlighted with grid. Defaults to [False, False, False].
            font (list, bool): Tells what data is higlighted with bold font. Defaults to ['bold', 'bold', 'bold'].
        """

        x = self.xData
        self.sc.ax1.cla()
        self.sc.ax2.cla()
        self.sc.ax3.cla()

        # Y-axis data, y1 = temperature, y2 = wind
        y1 = self.data[list(self.data.keys())[0]][self.dataKeys[1]]["values"]
        y2 = self.data[list(self.data.keys())[0]][self.dataKeys[2]]["values"]

        ax1 = self.sc.ax1
        ax1.set_zorder(1)  # brings ax1 to front
        ax1.patch.set_visible(False)
        ax1.plot(x, y1, 'r-', label="Temperature", alpha=alphas[0])
        ax1.set_ylabel('°C', loc='top', color='r',
                       fontweight=font[0], alpha=alphas[0], rotation=0)
        start, end = ax1.get_ylim()
        ax1.yaxis.set_ticks(np.arange(round(start - 2), round(end + 2), 2))
        ax1.spines['top'].set_visible(False)
        if grids[0]:
            ax1.grid(grids[0], linestyle='--', color='r')

        ax2 = self.sc.ax2
        ax2.set_visible(True)
        ax2.scatter(x, y2, marker='4',
                    alpha=alphas[1],  color='k', label="Wind")
        ax2.set_ylabel('m/s',  loc='top', color='k',
                       fontweight=font[1], alpha=alphas[1], rotation=0)
        start2, end2 = ax2.get_ylim()
        ax2.yaxis.set_ticks(np.arange(0, end2, 1))
        ax2.spines['top'].set_visible(False)
        if grids[1]:
            ax2.grid(grids[1], linestyle='--', color='black')

        # If shown data is observed data (not forecast) also third y-axis is shown for cloud coverage
        if not self.dataTypeForecast:
            y3 = self.data[self.city][self.dataKeys[3]]["values"]
            ax3 = self.sc.ax3
            ax3.spines.right.set_position(("axes", 1.05))
            ax3.scatter(x, y3, marker="o", label="Clouds", alpha=alphas[2])
            ax3.set_ylabel('/8',  loc='top', color='b',
                           fontweight=font[2], alpha=alphas[2], rotation=0)
            #ax3.yaxis.set_ticks(np.arange(0, 8,1))
            ax3.set_ylim(0, 8.33)
            ax3.spines['top'].set_visible(False)
            if grids[2]:
                ax3.grid(grids[2], linestyle='--', color='b')

        # Legends and labels according to shown data type
        # ax1.legend(frameon=True)
        line, label = ax1.get_legend_handles_labels()
        line2, label2 = ax2.get_legend_handles_labels()
        if self.dataTypeForecast:
            ax1.legend(line + line2, label + label2, frameon=True, loc='best')
            self.sc.ax3.set_visible(False)
        else:
            line3, label3 = ax3.get_legend_handles_labels()
            ax1.legend(line + line2 + line3, label + label2 +
                       label3, frameon=True, loc='best')
            ax3.set_visible(True)

        self.format_xaxis()

    def get_limits(self):
        """Searches limit values for x-axis according to wanted forecast length and returns their indexes

        Returns:
            int, int: indexes of values that limit x-axis
        """
        now = dt.datetime.now().replace(day=28, hour=10, microsecond=0, second=0, minute=0)
        startIndex = self.xData.index(now)
        end = now + dt.timedelta(hours=self.span)
        endIndex = self.xData.index(end)

        return startIndex, endIndex

    def format_xaxis(self):
        """Formats x-axis according to shown data and timewindow. 
        """
        if self.dataTypeForecast:
            # Formats x-axis when visualizin forecast data
            # limits axis +-10minutes to show all datapoints properly
            start, end = self.get_limits()
            x_axis = self.xData[start:end+1]
            self.sc.ax1.xaxis.set_major_formatter(
                mdates.DateFormatter("%H:%M"))
            self.sc.ax1.set_xlabel('Time')
            self.sc.figure.autofmt_xdate()
            self.sc.ax1.set_xbound(x_axis[0] - dt.timedelta(minutes=10),
                                   x_axis[len(x_axis)-1] + dt.timedelta(minutes=10))

        else:
            # Format x-axis when visualizing observed data (Daily average)
            # Limits x-axis +- 0.2 days to show all datapoints properly
            self.sc.ax1.xaxis.set_major_formatter(
                mdates.DateFormatter("%d/%m/%Y"))
            self.sc.ax1.set_xlabel('Date')
            limL = mdates.date2num(self.xData[0])
            limR = mdates.date2num(self.xData[len(self.xData)-1])
            self.sc.ax1.set_xbound(limL-0.2, limR+0.2)
            # Tick frequency and tick label visibility
            self.sc.ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
            # every Nth tick shown
            N = 2
            [l.set_visible(False) for (i, l) in enumerate(
                self.sc.ax1.xaxis.get_ticklabels()) if i % N != 0]
            self.sc.figure.autofmt_xdate(rotation=60)

        self.sc.draw()

    def update(self, data):
        """Updates visualized data when user requests.

        Args:
            data (dict): New dataset
        """
        self.data = data
        self.city = list(data.keys())[0]
        self.dataKeys = list(data[list(data.keys())[0]].keys())
        self.xData = list(data[self.city].values())[0]
        self.draw_graph()

    def onClicked(self):
        """Sets proper timespan to x-axis according to selected radiobutton
        """
        radioButton = self.sender()
        span = radioButton.text()[:-1]
        # radioButton.isChecked()
        self.span = int(span)
        self.format_xaxis()

#app = QApplication([])
#graph = GraphWidget(forecast)
#graph = GraphWidget(observed)
#app.exec_()
