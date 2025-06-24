"""main.py

Driver script for Minecraft Waypoint Converter.
"""


from PyQt6.QtWidgets import QApplication

from frontend.gui import MinecraftWaypointConverterMainWindow



def main() -> None:
    """
    Main function to run the Minecraft Waypoint Converter GUI.
    """
    
    app = QApplication([])
    main_window = MinecraftWaypointConverterMainWindow()
    main_window.show()
    app.exec()


if __name__ == "__main__":
    main()