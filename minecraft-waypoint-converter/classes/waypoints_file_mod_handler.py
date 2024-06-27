"""waypoints_file_mod_handler.py

Contains a class that handles reading and writing waypoints to and from
a waypoint mod that stores all waypoints in a single file.
Class is written as an abstract class.
"""


from .file_handler import FileHandler
from .file_extension import FileExtension
from .waypoints_mod_handler import WaypointsModHandler

from abc import abstractmethod
from typing import Any

class FileWaypointsModHandler(WaypointsModHandler):
    """
    A class that represents a set of waypoints for a mod that
    stores all world and server waypoints in a single file.

    Attributes
    ----------
    waypoints_file : FileHandler
        class that handles IO for the file in which the waypoints
        are stored
    """

    def __init__(self,
                 file_path : str,
                 extension : FileExtension) -> None:
        """
        Creates an instance of a FileWaypointsModHandler subclass.
        """
        self.waypoints_file = FileHandler(
            full_path=file_path, 
            extension=extension
        )
        super().__init__()


    @abstractmethod
    def read(self) -> dict:
        """
        Reads and returns the dictionary data held within 
        the waypoints file.
        """
        

    @abstractmethod
    def write(self) -> None:
        """
        Writes to the dictionary data held within the waypoints file.
        """