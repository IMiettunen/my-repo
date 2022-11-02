from PyQt5.QtWidgets import *
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import datetime as dt
import matplotlib.dates as mdates
import random as rand
import matplotlib as plt


dates = ['01,09,2022','02,09,2022','03,09,2022',
            '04,09,2022','05,09,2022','06,09,2022',
            '07,09,2022','08,09,2022','09,09,2022',
            '10,09,2022','11,09,2022','12,09,2022',
            '13,09,2022','14,09,2022','15,09,2022',
            '16,09,2022','17,09,2022','18,09,2022',
            '19,09,2022','20,09,2022','21,09,2022',
            '22,09,2022','23,09,2022','24,09,2022',
            '25,09,2022','26,09,2022','27,09,2022',
            '28,09,2022','29,09,2022','30,09,2022',]

hour_rain = {   
    '08:00': 1.0, 
    '09:00': 3.5, 
    '10:00': 2.0, 
    '11:00': 4.0, 
    '12:00': 5.5, 
    '13:00': 0.0   
} 

hour_temp = {
    '08:00':8, 
    '09:00':10, 
    '10:00':12, 
    '11:00':13, 
    '12:00':17, 
    '13:00':15
} 

daily_rain = []

daily_temp = []

def rand_rain():
    while len(daily_rain)<30:
       daily_rain.append(round(rand.uniform(0.0, 5.5),1))

def rand_temp():
    while len(daily_temp)<30:
       daily_temp.append(rand.randint(-3, 18)) 

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax1 = fig.add_subplot()
        self.ax2 = self.ax1.twinx()
        #self.figure = fig
        
        super().__init__(fig)

class MatplotlibWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        RBlayout = QGridLayout()
        self.timespan = 'month'

        monthRB = QRadioButton("month")
        monthRB.setChecked(True)
        #monthRB.country = "Australia"
        monthRB.toggled.connect(self.onClickedMonth)
        RBlayout.addWidget(monthRB, 0, 0)

        sixhRB = QRadioButton("6h")
        #sixhRB.country = "China"
        sixhRB.toggled.connect(self.onClickedSix)
        RBlayout.addWidget(sixhRB, 0, 1)

        hlayout.addLayout(RBlayout)

        self.rainButton = QPushButton("Rain")
        hlayout.addWidget(self.rainButton)
        self.tempButton = QPushButton("Temp")
        hlayout.addWidget(self.tempButton)
        self.bothButton = QPushButton("Both")
        hlayout.addWidget(self.bothButton)
        vlayout.addLayout(hlayout)
        self.x = [dt.datetime.strptime(d,'%d,%m,%Y').date() for d in dates]
        self.xhours = [dt.datetime.strptime(h,'%H:%M') for h in list(hour_rain.keys())]

        rand_temp()
        rand_rain()
        # canvas gets created during init once
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        vlayout.addWidget(self.sc)
        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)
        self.draw_temp()
        self.draw_rain()
        self.draw_temp_rain()
        self.tempButton.pressed.connect(self.draw_temp)
        self.rainButton.pressed.connect(self.draw_rain)
        self.bothButton.pressed.connect(self.draw_temp_rain)
        self.show()

    def draw_rain(self):
        #Draw barchart of rain
        if self.timespan =='month':
            y = daily_rain 
            self.sc.ax1.cla()
            self.sc.ax2.set_visible(False)
            self.sc.ax1.bar(self.x,y)
            self.sc.ax1.grid(True, linestyle='--', color = 'b')
            self.sc.ax1.set_ylabel('mm', color='b', rotation=0)
            self.sc.ax1.set_title('Rain')     
            self.format_xaxis()
            self.sc.draw()
        else:
            y = list(hour_rain.values())

            self.sc.ax1.cla()
            self.sc.ax2.set_visible(False)
            self.sc.ax1.bar(self.xhours, y, width=0.01)
            self.sc.ax1.grid(True, linestyle='--', color = 'b')
            self.sc.ax1.set_ylabel('mm', color='b', rotation=0)
            self.sc.ax1.set_title('Rain')     
            self.format_xaxis()
            self.sc.draw()


    def draw_temp(self):
        #Draw linegraph of temperature
        if self.timespan =='month':
            y = daily_temp
            self.sc.ax1.cla()
            self.sc.ax2.set_visible(False)
            self.sc.ax1.plot(self.x, y,'r-')
            self.sc.ax1.grid(True, linestyle='--', color = 'r')
            self.sc.ax1.set_ylabel('°C', color='r', rotation=0)
            #plt.ylabel('Temperature in °C') #Jos molemmat graafit piirretään, niin tää otsikko menee oikealle
            self.sc.ax1.set_title('Temperature')
            self.format_xaxis()
            self.sc.draw()
        else:
            y = list(hour_temp.values())

            self.sc.ax1.cla()
            self.sc.ax2.set_visible(False)
            self.sc.ax1.plot(self.xhours, y, 'r-')
            self.sc.ax1.grid(True, linestyle='--', color = 'r')
            self.sc.ax1.set_ylabel('°C', color='r', rotation=0)
            self.sc.ax1.set_title('Temperature')     
            self.format_xaxis()
            self.sc.draw()
           

    def draw_temp_rain(self):
        #Draw linegraph for temperature and bar chart for rain amount in same figure
        if self.timespan =='month':
            y1 = daily_temp
            y2 = daily_rain

            self.sc.ax1.cla()
            self.sc.ax2.cla()
            self.sc.ax2.set_visible(True)

            #Accessing the y-axes in self's figure and creating second y-axis thah shares x-axis with the first one
            ax1 = self.sc.ax1
            ax2 = self.sc.ax2
            ax1.set_zorder(1) # brings ax1 to front
            ax1.patch.set_visible(False)

            # Plot line graph with red line and bar chart with blue bars, add labels to axes
            ax1.plot(self.x, y1,'r-', label="Temperature")
            ax2.bar(self.x, y2, label="Rain")
            ax1.set_ylabel('°C', color='r', rotation=0)
            ax2.set_ylabel('mm', color='b', rotation=0)

            #Setting secondary y-axis ticks on a wanted 0.5 frequency
            start, end = ax2.get_ylim()
            ax2.yaxis.set_ticks(np.arange(start, end, 1.0))

            # Figure styling + Combined lables box
            ax1.grid(True, linestyle='--', color = 'r')
            #ax2.grid(True, linestyle='--', color = 'b')
            #ax1.legend(frameon=True)
            lines, labels = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines + lines2, labels + labels2,frameon = True)

            self.format_xaxis()

            self.sc.draw()
        else:
            y1 = list(hour_temp.values())
            y2 = list(hour_rain.values())

            self.sc.ax1.cla()
            self.sc.ax2.cla()
            self.sc.ax2.set_visible(True)

            #Accessing the y-axes in self's figure and creating second y-axis thah shares x-axis with the first one
            ax1 = self.sc.ax1
            ax2 = self.sc.ax2
            ax1.set_zorder(1) # brings ax1 to front
            ax1.patch.set_visible(False)

            # Plot line graph with red line and bar chart with blue bars, add labels to axes
            ax1.plot(self.xhours, y1,'r-', label="Temperature")
            ax2.bar(self.xhours, y2, width=0.01, label="Rain")
            ax1.set_ylabel('°C', color='r', rotation=0)
            ax2.set_ylabel('mm', color='b', rotation=0)

            #Setting secondary y-axis ticks on a wanted 0.5 frequency
            start, end = ax2.get_ylim()
            ax2.yaxis.set_ticks(np.arange(start, end, 0.5))

            # Figure styling + Combined lables box
            ax1.grid(True, linestyle='--', color = 'r')
            #ax2.grid(True, linestyle='--', color = 'b')
            #ax1.legend(frameon=True)
            lines, labels = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines + lines2, labels + labels2,frameon = True)

            self.format_xaxis()
            self.sc.draw()

    def format_xaxis(self):
        if self.timespan =='month':
            # X-axis formatting to show dates the wanted way and setting borders to sensible visible are
            self.sc.ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
            self.sc.ax1.xaxis.set_major_locator(mdates.DayLocator())
            self.sc.ax1.set_xlabel('Date')
            self.sc.figure.autofmt_xdate()

            #Set x-axis boundaries with one extra day in both ends
            self.sc.ax1.set_xbound(self.x[0]-dt.timedelta(days=1), self.x[len(self.x)-1]+dt.timedelta(days=1))
        else:
            hours = list(hour_rain.keys())
            x = [dt.datetime.strptime(h,"%H:%M") for h in hours]
            self.sc.ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
            #self.sc.ax1.xaxis.set_major_locator(mdates.DayLocator())
            self.sc.ax1.set_xlabel('Time')
            self.sc.figure.autofmt_xdate()

            self.sc.ax1.set_xbound(x[0]-dt.timedelta(hours=1), x[len(x)-1]+dt.timedelta(hours=1))
            

    def onClickedMonth(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.timespan = 'month'
            self.draw_temp_rain()
        else:
            pass
 
    def onClickedSix(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.timespan = 'sixhours'
            self.draw_temp_rain()
        else:
            pass

app = QApplication([])
window = MatplotlibWidget()
app.exec_()


"""
hour_rain = {   
    '08:00': 1.0, 
    '09:00': 3.5, 
    '10:00': 2.0, 
    '11:00': 4.0, 
    '12:00': 5.5, 
    '13:00': 0.0   
} 

hour_temp = {
    '08:00':8, 
    '09:00':10, 
    '10:00':12, 
    '11:00':13, 
    '12:00':17, 
    '13:00':15
} 

hours = [hour_rain.keys()]
y = [hour_rain.values()]
format = "%H:%M"
x = [dt.datetime.strptime(h,format).date() for h in hours]


hours= [hour_temp.keys()]
y= [hour_temp.values()]
format = "%H:%M"
x = [dt.datetime.strptime(h,format).date() for h in hours]
"""



