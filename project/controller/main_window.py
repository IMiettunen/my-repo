"""
This class is the main window of the application.

It works as a controller for the application.
It's responsible for the communication between the view and the model.
It's the only class that has access to the model and the view.

"""

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
import json
import pathlib

from project.controller.components.side_panel import SidePanel
from project.controller.components.view_panel import ViewPanel



class UiMainWindow(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()

        self.folder = pathlib.Path.cwd()

        self.today_tab_content = QtWidgets.QWidget()
        self.history_tab_content = QtWidgets.QWidget()
        self.compare_tab_content_left = QtWidgets.QWidget()
        self.compare_tab_content_right = QtWidgets.QWidget()

        self.setup_ui()


    def setup_ui(self):
        """
        Sets up the main window
        :return:
        """

        hBox = QtWidgets.QHBoxLayout(self)
        hBox.setContentsMargins(0, 1, 0, 0)
        hBox.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.side_panel_object = SidePanel()
        self.side_panel_widget = self.side_panel_object.get_side_panel()
        hBox.addWidget(self.side_panel_widget)

        self.side_panel_object.search_push_button.clicked.connect(self.search_with_selected_data)
        self.side_panel_object.save_timeline_push_button.clicked.connect(self.save_timeline)
        self.side_panel_object.load_timeline_push_button_1.clicked.connect(self.display_timeline_left)
        self.side_panel_object.load_timeline_push_button_2.clicked.connect(self.display_timeline_right)

        self.view_panel_object = ViewPanel()
        self.view_panel_widget = self.view_panel_object.get_view_panel()
        self.view_panel_widget.currentChanged.connect(self.change_tab)
        hBox.addWidget(self.view_panel_widget)

        frame = QtWidgets.QFrame(self)
        frame.setLayout(hBox)
        self.setCentralWidget(frame)

        self.setGeometry(0, 0, 1600, 900)
        self.setMinimumSize(QtCore.QSize(1600, 900))
        self.setWindowTitle("Road Watch")


    def change_tab(self):
        """
        Connects tab change in view panel to side panel
        :return: None
        """

        self.side_panel_object.set_tab_index(self.view_panel_widget.currentIndex())
        print("change tab")


    def search_with_selected_data(self):
        """
        Connects search button in side panel to view panel
        :return: None
        """

        # controller kutsuu modelia eli apirequestia parametreilla ja saa takaisin dataa
        # sen jälkeen controller kutsuu data visualizationia eli viewiä saadulla datalla ja saa takaisin kuvaajia
        # sitten controller näyttää datan.

        # VIEW JA MODEL EIVÄT SAA KOSKAAN KOMMUNIKOIDA SUORAAN KESKENÄÄN

        print("search with selected data")


        settings = self.side_panel_object.get_current_settings()

        # tässä kohtaa kutsuu modelia ja hankkii datan
        # sen jäkeen kutsuu viewiä ja näyttää datan



    def save_timeline(self):
        """
        Saves the timeline in json format
        :return:
        """

        print("save timeline")

        settings = self.side_panel_object.get_current_settings()
        # Save data of all the graphs and plots, messages, etc. with the settings

        data = {
            "settings": settings,
            "data": None,
        }

        title = settings["city"] + " " + settings["startDate"] + " - " + settings["endDate"]
        path = self.folder / 'controller' / 'saves' / 'timelines' / title + ".json"
        f = open(path, "w")
        f.write(json.dumps(data, indent=4))
        f.close()


    def load_timeline(self):
        """
        Loads timeline in json format
        :return:
        """

        print("load timeline")

        path = self.folder / 'controller' / 'saves' / 'timelines'
        response = QFileDialog.getOpenFileName(
            caption='Select saved timeline',
            directory=str(path),
            filter='JSON files (*.json)',
            initialFilter='JSON files (*.json)'
        )
        if response and response[0] != '':
            f = open(response[0], "r")
            data = json.load(f)
            f.close()
            print(data)

    def display_timeline_left(self):
        """
        Loads the timeline in json format and requests visualization from the view
        Displays the timeline in the left compare tab
        :return: None
        """

        timeline = self.load_timeline()
        # Display data


    def display_timeline_right(self):
        """
        Loads the timeline in json format and requests visualization from the view
        Displays the timeline in the right compare tab
        :return: None
        """

        timeline = self.load_timeline()
        # Display data



def main():
    app = QApplication(sys.argv)
    window = UiMainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
