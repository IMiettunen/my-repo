"""
This class implements the view panel component of the main_window.

It is responsible for the display of the tabs in the main window.
The view panel displays graphs and plots of the data, messages and images.

There are three tabs: Today, History and Compare.

Today:
    Displays the timeline of the current day.
    Display consist of the weather forecast and the weather and road data of the current day.

History:
    Displays the timeline between selected days.
    Display consist of the weather and road data between selected days.

Compare:
    Displays two different saved timelines between selected days that have been loaded to the application.
    Display consist of the weather and road data between selected days.

"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFileDialog

class ViewPanel(QWidget):

    def __init__(self,):
        super(ViewPanel, self).__init__()

        self.today_tab = QtWidgets.QWidget()
        self.history_tab = QtWidgets.QWidget()
        self.compare_tab = QtWidgets.QWidget()


    # NÄÄ KAIKKI SETUP FUNKTIOT PITÄÄ VARMAAN VAAN POISTAA JA KORVAA JOLLAIN MALLAI  def set_today_content(self, content):
    # JOKA SIT ASETTAA SEN SISÄLTÖNÄ OLEVAN WIDGETIN KYSEISEEN TABIIN
    # SE SISÄLTÖ SIT VOITAIS LUODA TUOL VIEWISSÄ NII NOUDATTAIS MVC MALLIA.
    # ELI SIIS SIIRTÄÄ TÄN NYKYSEN SCROLL AREAN YMPÄRILLE RAKENNETUN WIDGETIN VIEWIIN KOKONAAN


    def setup_today_tab(self):
        """
        Sets up the today tab.
        :return:
        """

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setGeometry(QtCore.QRect(0, 0, 1300, 900))
        scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        scroll_area.setWidgetResizable(True)

        scroll_area_layout = QtWidgets.QHBoxLayout()
        scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area_layout.addWidget(scroll_area)
        self.today_tab.setLayout(scroll_area_layout)

        #visualizer = DataVisualization()
        #buttons = visualizer.get_current_view()
        spacer_layout = QtWidgets.QHBoxLayout()
        horizontal_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        spacer_layout.addItem(horizontal_spacer)
        #spacer_layout.addWidget(buttons)
        spacer_layout.addItem(horizontal_spacer)

        content = QtWidgets.QWidget()
        content.setLayout(spacer_layout)
        scroll_area.setWidget(content)

        return self.today_tab


    def setup_history_tab(self):
        """
        Sets up the history tab.
        :return:
        """

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setGeometry(QtCore.QRect(0, 0, 1300, 900))
        scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        scroll_area.setWidgetResizable(True)

        scroll_area_layout = QtWidgets.QHBoxLayout()
        scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area_layout.addWidget(scroll_area)
        self.history_tab.setLayout(scroll_area_layout)

        # visualizer = DataVisualization()
        # buttons = visualizer.get_current_view()
        spacer_layout = QtWidgets.QHBoxLayout()
        horizontal_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        spacer_layout.addItem(horizontal_spacer)
        # spacer_layout.addWidget(buttons)
        spacer_layout.addItem(horizontal_spacer)

        content = QtWidgets.QWidget()
        content.setLayout(spacer_layout)
        scroll_area.setWidget(content)

        return self.history_tab


    def setup_compare_tab(self):
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setGeometry(QtCore.QRect(0, 0, 1300, 900))
        scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        scroll_area_layout = QtWidgets.QHBoxLayout()
        scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area_layout.addWidget(scroll_area)
        self.compare_tab.setLayout(scroll_area_layout)

        # visualizer = DataVisualization()
        # buttons = visualizer.get_current_view()
        spacer_layout = QtWidgets.QHBoxLayout()
        horizontal_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,
                                                  QtWidgets.QSizePolicy.Expanding)
        spacer_layout.addItem(horizontal_spacer)
        # spacer_layout.addWidget(buttons)
        spacer_layout.addItem(horizontal_spacer)

        content = QtWidgets.QWidget()
        content.setLayout(spacer_layout)
        scroll_area.setWidget(content)

        return self.compare_tab


    def get_view_panel(self):
        """
        Creates the view panel.
        :return: QTabWidget, view panel
        """
        view_panel = QtWidgets.QTabWidget()
        view_panel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        view_panel.addTab(self.setup_today_tab(), "")
        view_panel.setTabText(view_panel.indexOf(self.today_tab), "Today")
        view_panel.addTab(self.setup_history_tab(), "")
        view_panel.setTabText(view_panel.indexOf(self.history_tab), "History")
        view_panel.addTab(self.setup_compare_tab(), "")
        view_panel.setTabText(view_panel.indexOf(self.compare_tab), "Compare")
        view_panel.setCurrentIndex(0)


        return view_panel