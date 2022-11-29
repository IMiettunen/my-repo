import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
import json


class UiMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def get_today_tab(self):
        self.today_tab = QtWidgets.QWidget()
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setGeometry(QtCore.QRect(0, 0, 1300, 900))
        scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        scroll_area_layout = QtWidgets.QHBoxLayout()
        scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area_layout.addWidget(scroll_area)
        self.today_tab.setLayout(scroll_area_layout)

        today_view_spacer_layout = QtWidgets.QHBoxLayout()
        today_view_content_layout = QtWidgets.QVBoxLayout()  #Tän sisään today tabille tuleva roina

        title_layout = QtWidgets.QHBoxLayout()
        city_name_label = QtWidgets.QLabel("City name")
        font = QtGui.QFont()
        font.setPointSize(18)
        city_name_label.setFont(font)
        city_name_label.setFixedWidth(200)
        city_name_label.setAlignment(QtCore.Qt.AlignLeft)
        title_layout.addWidget(city_name_label)

        update_button_layout = QtWidgets.QHBoxLayout()
        update_button_layout.setSpacing(18)
        self.today_update_button_label = QtWidgets.QLabel("Last updated 00.00")
        self.today_update_button_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter | QtCore.Qt.AlignTrailing)
        update_button_layout.addWidget(self.today_update_button_label)

        self.today_update_push_button = QtWidgets.QPushButton("Update")
        self.today_update_push_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        update_button_layout.addWidget(self.today_update_push_button)

        title_layout.addLayout(update_button_layout)
        today_view_content_layout.addLayout(title_layout)

        vertical_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        today_view_content_layout.addItem(vertical_spacer)

        horizontal_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        today_view_spacer_layout.addItem(horizontal_spacer)
        today_view_spacer_layout.addLayout(today_view_content_layout)
        today_view_spacer_layout.addItem(horizontal_spacer)

        scroll_area.setLayout(today_view_spacer_layout)

        return self.today_tab


    def get_history_tab(self):
        self.history_tab = QtWidgets.QWidget()
        self.history_scroll_area = QtWidgets.QScrollArea(self.history_tab)
        self.history_scroll_area.setGeometry(QtCore.QRect(0, 0, 1300, 870))
        self.history_scroll_area.setWidgetResizable(True)
        self.history_scroll_area_contents = QtWidgets.QWidget()
        self.history_scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 1300, 868))
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.history_scroll_area_contents)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(0, 0, 1300, 61))
        self.history_scroll_area_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.history_scroll_area_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.history_scroll_area_layout.setContentsMargins(325, 18, 325, 6)
        self.history_title_layout = QtWidgets.QHBoxLayout()
        self.history_city_name_label = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.history_city_name_label.sizePolicy().hasHeightForWidth())
        # self.history_city_name_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.history_city_name_label.setFont(font)
        self.history_city_name_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.history_city_name_label.setAutoFillBackground(False)
        self.history_city_name_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.history_city_name_label.setText("City name")
        self.history_title_layout.addWidget(self.history_city_name_label)
        self.history_save_button_layout = QtWidgets.QHBoxLayout()
        self.history_save_button_layout.setSpacing(18)
        self.history_save_button_label = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.history_save_button_label.sizePolicy().hasHeightForWidth())
        # self.history_save_button_label.setSizePolicy(sizePolicy)
        self.history_save_button_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.history_save_button_label.setText("Save timeline with these settings")
        self.history_save_button_layout.addWidget(self.history_save_button_label)
        self.history_save_push_button = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.history_save_push_button.clicked.connect(self.save_timeline)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.history_save_push_button.sizePolicy().hasHeightForWidth())
        # self.history_save_push_button.setSizePolicy(sizePolicy)
        self.history_save_push_button.setText("Save")
        self.history_save_button_layout.addWidget(self.history_save_push_button)
        self.history_title_layout.addLayout(self.history_save_button_layout)
        self.history_scroll_area_layout.addLayout(self.history_title_layout)
        self.history_scroll_area.setWidget(self.history_scroll_area_contents)

        return self.history_tab

    def save_timeline(self):
        settings = self.get_current_settings()
        # Save data of all the graphs and plots, messages, etc. with the settings

        data = {
            "settings": settings,
            "data": None,
        }

        title = settings["city"] + " " + settings["start date"] + " - " + settings["end date"]
        f = open("data/saves/" + title + ".json", "w")
        json.dump(data, f)
        f.close()


    def get_compare_tab(self):
        self.compare_tab = QtWidgets.QWidget()
        self.compare_tab.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.compare_scroll_area = QtWidgets.QScrollArea(self.compare_tab)
        self.compare_scroll_area.setGeometry(QtCore.QRect(0, 0, 1300, 870))
        self.compare_scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.compare_scroll_area_contents = QtWidgets.QWidget()
        self.compare_scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 1300, 868))
        self.compare_scroll_area_contents.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.compare_scroll_area_contents)
        #self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 1300, 61))
        self.compare_scroll_area_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.compare_scroll_area_layout.setContentsMargins(25, 18, 25, 6)
        self.compare_scroll_area_layout.setSpacing(25)
        self.left_compare_title_layout = QtWidgets.QHBoxLayout()
        self.left_compare_city_name_label = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.left_compare_city_name_label.sizePolicy().hasHeightForWidth())
        # self.left_compare_city_name_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.left_compare_city_name_label.setFont(font)
        self.left_compare_city_name_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.left_compare_city_name_label.setAutoFillBackground(False)
        self.left_compare_city_name_label.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.left_compare_city_name_label.setText("City name")

        self.left_compare_title_layout.addWidget(self.left_compare_city_name_label)
        self.left_compare_load_timeline_button_layout = QtWidgets.QHBoxLayout()
        self.left_compare_load_timeline_button_layout.setSpacing(18)
        self.left_compare_load_timeline_label = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.left_compare_load_timeline_label.sizePolicy().hasHeightForWidth())
        # self.left_compare_load_timeline_label.setSizePolicy(sizePolicy)
        self.left_compare_load_timeline_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.left_compare_load_timeline_label.setText("Load timeline")
        self.left_compare_load_timeline_button_layout.addWidget(self.left_compare_load_timeline_label)
        self.left_compare_load_timeline_push_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.left_compare_load_timeline_push_button.sizePolicy().hasHeightForWidth())
        self.left_compare_load_timeline_push_button.clicked.connect(self.load_saved_timeline)
        # self.left_compare_load_timeline_push_button.setSizePolicy(sizePolicy)
        self.left_compare_load_timeline_push_button.setText("Load")
        self.left_compare_load_timeline_button_layout.addWidget(self.left_compare_load_timeline_push_button)
        self.left_compare_title_layout.addLayout(self.left_compare_load_timeline_button_layout)
        self.compare_scroll_area_layout.addLayout(self.left_compare_title_layout)
        self.compare_separator_line = QtWidgets.QFrame(self.horizontalLayoutWidget_4)
        self.compare_separator_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.compare_separator_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.compare_scroll_area_layout.addWidget(self.compare_separator_line)


        self.right_compare_title_layout = QtWidgets.QHBoxLayout()
        self.right_compare_city_name_label = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.right_compare_city_name_label.sizePolicy().hasHeightForWidth())
        # self.right_compare_city_name_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.right_compare_city_name_label.setFont(font)
        self.right_compare_city_name_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.right_compare_city_name_label.setAutoFillBackground(False)
        self.right_compare_city_name_label.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.right_compare_city_name_label.setText("City name")
        self.right_compare_title_layout.addWidget(self.right_compare_city_name_label)
        self.right_compare_load_timeline_button_layout = QtWidgets.QHBoxLayout()
        self.right_compare_load_timeline_button_layout.setSpacing(18)
        self.right_compare_load_timeline_label = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.right_compare_load_timeline_label.sizePolicy().hasHeightForWidth())
        # self.right_compare_load_timeline_label.setSizePolicy(sizePolicy)
        self.right_compare_load_timeline_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.right_compare_load_timeline_label.setText("Load timeline")
        self.right_compare_load_timeline_button_layout.addWidget(self.right_compare_load_timeline_label)
        self.right_compare_load_timeline_push_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.right_compare_load_timeline_push_button.sizePolicy().hasHeightForWidth())
        # self.right_compare_load_timeline_push_button.setSizePolicy(sizePolicy)
        self.right_compare_load_timeline_push_button.setText("Load")
        self.right_compare_load_timeline_button_layout.addWidget(self.right_compare_load_timeline_push_button)
        self.right_compare_title_layout.addLayout(self.right_compare_load_timeline_button_layout)
        self.compare_scroll_area_layout.addLayout(self.right_compare_title_layout)
        self.compare_scroll_area.setWidget(self.compare_scroll_area_contents)

        return self.compare_tab


    def load_saved_timeline(self):
        response = QFileDialog.getOpenFileName(
            caption='Select saved timeline',
            directory=os.getcwd()+'/data/saves',
            filter='JSON files (*.json)',
            initialFilter='JSON files (*.json)'
        )
        if response:
            f = open(response[0], "r")
            data = json.load(f)
            f.close()
            print(data)

            # Display data

    def get_view_panel(self):
        self.view_panel = QtWidgets.QTabWidget()
        #self.view_panel.resize(QtCore.QRect(300, 0, 1300, 900))
        self.view_panel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.view_panel.addTab(self.get_today_tab(), "")
        self.view_panel.setTabText(self.view_panel.indexOf(self.today_tab), "Today")
        # self.view_panel.addTab(self.get_history_tab(), "")
        # self.view_panel.setTabText(self.view_panel.indexOf(self.history_tab), "History")
        # self.view_panel.addTab(self.get_compare_tab(), "")
        # self.view_panel.setTabText(self.view_panel.indexOf(self.compare_tab), "Compare")
        #
        # self.view_panel.setCurrentIndex(0)
        # self.view_panel.currentChanged.connect(self.set_timeline_selection_visibility)
        # self.set_timeline_selection_visibility()

        return self.view_panel

    def get_side_panel(self):
        side_panel = QtWidgets.QWidget(self)
        side_panel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        side_panel.setGeometry(QtCore.QRect(0, 0, 300, 900))
        side_panel.setMinimumWidth(300)
        side_panel.setMaximumWidth(300)
        side_panel.setMinimumHeight(900)
        side_panel_items = QtWidgets.QWidget(side_panel)
        side_panel_items.setGeometry(QtCore.QRect(0, 0, 300, 900))
        side_panel_items_layout = QtWidgets.QVBoxLayout(side_panel_items)
        side_panel_items_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        side_panel_items_layout.setContentsMargins(18, 6, 18, 0)
        side_panel_items_layout.setSpacing(18)

        application_title_label = QtWidgets.QLabel("Road Watch")
        font = QtGui.QFont()
        font.setPointSize(20)
        application_title_label.setFont(font)
        application_title_label.setContentsMargins(6, 0, 6, 0)
        side_panel_items_layout.addWidget(application_title_label)

        city_selection_layout = QtWidgets.QVBoxLayout()
        city_label = QtWidgets.QLabel("Select city")
        city_label.setContentsMargins(0, 0, 0, 6)
        font = QtGui.QFont()
        font.setPointSize(14)
        city_label.setFont(font)
        city_selection_layout.addWidget(city_label)
        self.city_selection_combo_box = QtWidgets.QComboBox()
        self.city_selection_combo_box.addItems(["Helsinki", "Espoo", "Tampere", "Vantaa", "Oulu"])
        self.city_selection_combo_box.currentIndexChanged.connect(self.city_selection_combo_box_changed)
        city_selection_layout.addWidget(self.city_selection_combo_box)
        city_selection = QtWidgets.QWidget()
        city_selection.setLayout(city_selection_layout)
        side_panel_items_layout.addWidget(city_selection)

        data_selection_layout = QtWidgets.QVBoxLayout()
        #data_selection_layout.setSpacing(5)
        data_selection_label = QtWidgets.QLabel("Select data")
        data_selection_label.setFont(font)
        data_selection_label.setContentsMargins(0, 0, 0, 6)
        data_selection_layout.addWidget(data_selection_label)

        self.weather_info_checkbox = QtWidgets.QCheckBox("Weather info")
        self.weather_info_checkbox.stateChanged.connect(self.weather_info_checkbox_changed)
        data_selection_layout.addWidget(self.weather_info_checkbox)

        self.road_info_checkbox = QtWidgets.QCheckBox("Road info")
        self.road_info_checkbox.stateChanged.connect(self.select_all_sub_selections)
        data_selection_layout.addWidget(self.road_info_checkbox)

        road_info_sub_selection_layout = QtWidgets.QVBoxLayout()
        road_info_sub_selection_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        road_info_sub_selection_layout.setContentsMargins(18, 0, 0, 0)
        road_info_sub_selection_layout.setSpacing(5)

        self.road_camera_checkbox = QtWidgets.QCheckBox("Road camera")
        self.road_camera_checkbox.stateChanged.connect(self.change_sub_selection_state)
        road_info_sub_selection_layout.addWidget(self.road_camera_checkbox)

        self.traffic_messages_checkbox = QtWidgets.QCheckBox("Traffic messages")
        self.traffic_messages_checkbox.stateChanged.connect(self.change_sub_selection_state)
        road_info_sub_selection_layout.addWidget(self.traffic_messages_checkbox)

        self.road_maintenance_checkbox = QtWidgets.QCheckBox("Road maintenance")
        self.road_maintenance_checkbox.stateChanged.connect(self.change_sub_selection_state)
        road_info_sub_selection_layout.addWidget(self.road_maintenance_checkbox)

        self.road_condition_checkbox = QtWidgets.QCheckBox("Road condition")
        self.road_condition_checkbox.stateChanged.connect(self.change_sub_selection_state)
        road_info_sub_selection_layout.addWidget(self.road_condition_checkbox)

        self.road_info_sub_selection_checkboxes = [self.road_camera_checkbox, self.traffic_messages_checkbox, self.road_maintenance_checkbox, self.road_condition_checkbox]

        data_selection_layout.addLayout(road_info_sub_selection_layout)
        data_selection = QtWidgets.QWidget()
        data_selection.setLayout(data_selection_layout)
        side_panel_items_layout.addWidget(data_selection)

        save_favourite_layout = QtWidgets.QHBoxLayout()
        save_favourite_layout.setSpacing(18)
        save_favourite_label = QtWidgets.QLabel("Save as favourite")
        save_favourite_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        save_favourite_layout.addWidget(save_favourite_label)

        self.save_favourite_push_button = QtWidgets.QPushButton("Save")
        self.save_favourite_push_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.save_favourite_push_button.clicked.connect(self.set_favourite_settings)
        save_favourite_layout.addWidget(self.save_favourite_push_button)
        save_favourite = QtWidgets.QWidget()
        save_favourite.setLayout(save_favourite_layout)
        side_panel_items_layout.addWidget(save_favourite)

        menu_line_1 = QtWidgets.QFrame()
        menu_line_1.setFrameShape(QtWidgets.QFrame.HLine)
        menu_line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        menu_line_1.setContentsMargins(12, 0, 12, 0)
        side_panel_items_layout.addWidget(menu_line_1)

        favourite_selection_layout = QtWidgets.QVBoxLayout()
        favourite_label = QtWidgets.QLabel("Favourite views")
        favourite_label.setContentsMargins(0, 0, 0, 6)
        favourite_label.setFont(font)
        favourite_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        favourite_selection_layout.addWidget(favourite_label)

        self.favourite_selection_combo_box = QtWidgets.QComboBox()
        self.favourite_selection_combo_box.setCurrentText("Select view")
        self.initialize_favourite_selection_combo_box() # Adds saved favourites to the combo box
        self.favourite_selection_combo_box.currentIndexChanged.connect(self.load_favourite_settings)
        favourite_selection_layout.addWidget(self.favourite_selection_combo_box)
        favourite_selection = QtWidgets.QWidget()
        favourite_selection.setLayout(favourite_selection_layout)
        side_panel_items_layout.addWidget(favourite_selection)

        timeline_selection_layout = QtWidgets.QVBoxLayout()
        timeline_selection_layout.setSpacing(24)

        menu_line_2 = QtWidgets.QFrame(side_panel_items)
        menu_line_2.setFrameShape(QtWidgets.QFrame.HLine)
        menu_line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        menu_line_2.setContentsMargins(0, 24, 0, 24)
        timeline_selection_layout.addWidget(menu_line_2)

        timeline_label = QtWidgets.QLabel("Select timeline")
        timeline_label.setFont(font)
        timeline_selection_layout.addWidget(timeline_label)

        date_selections_layout = QtWidgets.QHBoxLayout()
        date_selections_layout.setSpacing(8)

        start_date_selection_layout = QtWidgets.QVBoxLayout()
        start_date_label = QtWidgets.QLabel("Start date")
        start_date_selection_layout.addWidget(start_date_label)
        self.start_date_edit = QtWidgets.QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        date = QtCore.QDate.currentDate()
        self.start_date_edit.setDate(date)
        self.start_date_edit.setMaximumDate(date)
        self.start_date_edit.dateChanged.connect(self.set_max_min_dates)
        start_date_selection_layout.addWidget(self.start_date_edit)
        date_selections_layout.addLayout(start_date_selection_layout)

        end_date_selection_layout = QtWidgets.QVBoxLayout()
        end_date_label = QtWidgets.QLabel("End date")
        end_date_selection_layout.addWidget(end_date_label)
        self.end_date_edit = QtWidgets.QDateEdit(side_panel_items)
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(date)
        self.end_date_edit.setMinimumDate(date)
        self.end_date_edit.setMaximumDate(date)
        self.end_date_edit.dateChanged.connect(self.set_max_min_dates)
        end_date_selection_layout.addWidget(self.end_date_edit)

        date_selections_layout.addLayout(end_date_selection_layout)
        timeline_selection_layout.addLayout(date_selections_layout)

        self.timeline_selection = QtWidgets.QWidget()
        self.timeline_selection.setLayout(timeline_selection_layout)
        side_panel_items_layout.addWidget(self.timeline_selection)

        spacerItem = QtWidgets.QSpacerItem(300, 200, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        side_panel_items_layout.addItem(spacerItem)

        return side_panel



    def clear_all_info_selections(self):
        self.weather_info_checkbox.setChecked(not QtCore.Qt.Checked)
        self.road_info_checkbox.setChecked(not QtCore.Qt.Checked)

    def city_selection_combo_box_changed(self):
        self.favourite_selection_combo_box.setCurrentIndex(0)
        self.clear_all_info_selections()


    def weather_info_checkbox_changed(self):
        self.favourite_selection_combo_box.setCurrentIndex(0)

    def select_all_sub_selections(self):
        if self.road_info_checkbox.checkState() == QtCore.Qt.PartiallyChecked:
            self.road_info_checkbox.blockSignals(True)
            self.road_info_checkbox.setCheckState(QtCore.Qt.Checked)
            self.road_info_checkbox.blockSignals(False)

        for checkbox in self.road_info_sub_selection_checkboxes:
            if checkbox.isChecked() != self.road_info_checkbox.isChecked():
                checkbox.blockSignals(True)
                checkbox.setChecked(not checkbox.isChecked())
                checkbox.blockSignals(False)

    def change_sub_selection_state(self):
        self.favourite_selection_combo_box.setCurrentIndex(0)

        sub_selections_checked = len(list(filter(lambda cb: cb.isChecked(), self.road_info_sub_selection_checkboxes)))
        if sub_selections_checked == 0:
            self.road_info_checkbox.blockSignals(True)
            self.road_info_checkbox.setCheckState(not QtCore.Qt.Checked)
            self.road_info_checkbox.blockSignals(False)
        elif 0 < sub_selections_checked < 4:
            self.road_info_checkbox.blockSignals(True)
            self.road_info_checkbox.setCheckState(QtCore.Qt.PartiallyChecked)
            self.road_info_checkbox.blockSignals(False)
        else:
            self.road_info_checkbox.blockSignals(True)
            self.road_info_checkbox.setCheckState(QtCore.Qt.Checked)
            self.road_info_checkbox.blockSignals(False)

    def set_max_min_dates(self):
        min_end_date = self.start_date_edit.date()
        self.end_date_edit.setMinimumDate(min_end_date)

        max_start_date = self.end_date_edit.date()
        self.start_date_edit.setMaximumDate(max_start_date)

    def set_timeline_selection_visibility(self):
        if self.view_panel.currentIndex() == 1:
            self.timeline_selection.show()
        else:
            self.timeline_selection.hide()

    def get_current_settings(self):
        # return dict of settings
        return {
            "city": self.city_selection_combo_box.currentText(),
            "weather info": self.weather_info_checkbox.isChecked(),
            "road info": {
                "road camera": self.road_camera_checkbox.isChecked(),
                "traffic messages": self.traffic_messages_checkbox.isChecked(),
                "road maintenance": self.road_maintenance_checkbox.isChecked(),
                "road condition": self.road_condition_checkbox.isChecked(),
            },
            "start date": (self.start_date_edit.date().toString(QtCore.Qt.ISODate) if self.view_panel.currentIndex() == 1 else None),
            "end date": (self.end_date_edit.date().toString(QtCore.Qt.ISODate) if self.view_panel.currentIndex() == 1 else None),
        }

    def set_favourite_settings(self):
        selection = self.get_current_settings()

        key = selection['city']
        path = "data\settings\settings.json"
        f = open(path, "r")
        settings = json.load(f)
        f.close()

        settings[key] = selection
        f = open(path, "w")
        json.dump(settings, f)
        f.close()

        self.favourite_selection_combo_box.setCurrentText(key)

        for i in range(self.favourite_selection_combo_box.count()):
            if self.favourite_selection_combo_box.itemText(i) == key:
                return
        self.favourite_selection_combo_box.addItem(key)


    def load_favourite_settings(self):
        path = "data\settings\settings.json"
        f = open(path, "r")
        settings = json.load(f)
        f.close()
        key = self.favourite_selection_combo_box.currentText()
        if key == "Select view":
            return

        self.city_selection_combo_box.setCurrentText(key)
        self.weather_info_checkbox.setChecked(settings[key]["weather info"])
        self.road_camera_checkbox.setChecked(settings[key]["road info"]["road camera"])
        self.traffic_messages_checkbox.setChecked(settings[key]["road info"]["traffic messages"])
        self.road_maintenance_checkbox.setChecked(settings[key]["road info"]["road maintenance"])
        self.road_condition_checkbox.setChecked(settings[key]["road info"]["road condition"])

        self.favourite_selection_combo_box.setCurrentText(key)


    def initialize_favourite_selection_combo_box(self):
        path = "data\settings\settings.json"
        f = open(path, "r")
        settings = json.load(f)
        f.close()
        for key in settings.keys():
            self.favourite_selection_combo_box.addItem(key)



    def setup_ui(self):

        hBox = QtWidgets.QHBoxLayout(self)
        hBox.setContentsMargins(0, 1, 0, 0)
        hBox.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        hBox.addWidget(self.get_side_panel())
        hBox.addWidget(self.get_view_panel())

        frame = QtWidgets.QFrame(self)
        frame.setLayout(hBox)
        self.setCentralWidget(frame)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.setGeometry(0, 0, 1600, 900)
        self.setMinimumSize(QtCore.QSize(1600, 900))
        self.setWindowTitle("Road Watch")


def main():
    app = QApplication(sys.argv)
    window = UiMainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()