"""gui.py

Contains a class that creates the GUI for Minecraft Waypoint Converter.
"""

# from PyQt6.QtWidgets import (
#     QMainWindow,
#     QWidget,
#     QComboBox,
# )
# from PyQt6 import uic, QtWidgets
# import sys
# from pathlib import Path

# basedir = Path(__file__).parent
# print(basedir)


# app = QtWidgets.QApplication(sys.argv)

# window = uic.loadUi(Path(
#     basedir,
#     "MinecraftWaypointConverterMainWindow.ui"
#     # ".ui"
# ))
# window.show()
# app.exec()










from test import Ui_MainWindow

import sys
from PyQt6 import QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()













# class MinecraftWaypointConverterMainWindow(QMainWindow):
#     """
#     A class that create the GUI for Minecraft Waypoint Converter.
#     """
    
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Minecraft Waypoint Converter")

#         container = QWidget()
#         self.setCentralWidget(container)