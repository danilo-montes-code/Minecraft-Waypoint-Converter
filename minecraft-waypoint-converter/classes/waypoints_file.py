"""waypoints_file.py

Contains a class that represents a set of waypoints from a mod that uses
a single file as its storage method.
Class is written as an abstract class.
"""


from .file_handler import FileHandler
from .file_extension import FileExtension
from .waypoints import Waypoints

from abc import abstractmethod
from typing import Any

class FileWaypoints(Waypoints):
    """
    A class that represents a set of waypoints in a world for a mod that
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
        Creates an instance of a FileWaypoints subclass.
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