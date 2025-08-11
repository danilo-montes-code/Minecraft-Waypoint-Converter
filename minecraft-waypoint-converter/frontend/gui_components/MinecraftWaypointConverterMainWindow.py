from PyQt6.QtWidgets import QMainWindow, QWidget

class MinecraftWaypointConverterMainWindow(QMainWindow):
    """
    A class that creates the GUI for Minecraft Waypoint Converter.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minecraft Waypoint Converter")

        container = QWidget()
        self.setCentralWidget(container)