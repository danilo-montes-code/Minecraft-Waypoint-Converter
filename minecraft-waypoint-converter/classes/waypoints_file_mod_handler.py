"""waypoints_file_mod_handler.py

Contains a class that handles reading and writing waypoints to and from
a waypoint mod that stores all waypoints in a single file.
Class is written as an abstract class.
"""



from .file_handler import FileHandler
from .file_extension import FileExtension
from .waypoints_mod_handler import WaypointsModHandler

from abc import abstractmethod
from pathlib import Path
import os



class FileWaypointsModHandler(WaypointsModHandler):
    """
    A class that handles reading and writing waypoints to and from
    a waypoint mod that stores all waypoints in a single file.

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

        Parameters
        ----------
        file_path : str
            the full path of the waypoints file
        extension : FileExtension
            the extension of said file
        """

        self.waypoints_file = FileHandler.exact_path(
            full_path=file_path, 
            extension=extension
        )
        super().__init__()



    @abstractmethod
    def read_full_waypoint_file(self) -> dict:
        """
        Reads and returns the data held within the waypoints file.

        Returns
        -------
        dict
            the data held within the file
        """
        

    @abstractmethod
    def write_to_full_waypoint_file(self) -> None:
        """
        Writes to the data held within the waypoints file.
        """
    
    
    @abstractmethod
    def change_path(self, new_path : str) -> None:
        """
        Changes the path to the file where waypoints are stored.

        Parameters
        ----------
        new_path : str
            the path to the file where all waypoints are stored
        """
