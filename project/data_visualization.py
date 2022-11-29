from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

from graph import GraphWidget

class DataVisualization(QWidget):
    def __init__(self):
        super().__init__()

    def get_current_view(self):
        vBox = QtWidgets.QVBoxLayout(self)

        graph = GraphWidget()
        vBox.addWidget(graph)

        foo = QtWidgets.QWidget()
        foo.setLayout(vBox)
        return foo