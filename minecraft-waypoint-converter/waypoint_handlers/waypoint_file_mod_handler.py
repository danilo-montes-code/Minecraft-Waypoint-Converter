"""waypoint_file_mod_handler.py

Contains a class that handles reading and writing waypoints to and from
a waypoint mod that stores all waypoints in a single file.
Class is written as an abstract class.
"""

from abc import abstractmethod
from pathlib import Path

from pyfilehandlers.file_handler import FileHandler

from .waypoint_mod_handler import WaypointModHandler



class FileWaypointModHandler(WaypointModHandler):
    """
    A class that handles reading and writing waypoints to and from
    a waypoint mod that stores all waypoints in a single file.

    
    Attributes
    ----------
    input_waypoint_file : FileHandler
        Class that handles IO for the file in which the waypoints
        are stored, to be used as input to the converter.

    output_waypoint_file : FileHandler
        Class that handles IO for the file in which the waypoints
        are stored, to be used as output from the converter.
    """

    def __init__(
        self,
        input_file_path : Path,
        output_file_path : Path
    ) -> None:
        """
        Initializes a FileWaypointModHandler instance.

        
        Parameters
        ----------
        input_file_path : pathlib.Path
            The full path of the waypoint file to be used as 
            input to the converter.

        output_file_path : pathlib.Path
            The full path of the waypoint file to be used as 
            output from the converter.
        """

        super().__init__()
        self.input_waypoint_file = FileHandler(input_file_path)
        self.output_waypoint_file = FileHandler(output_file_path)


    @abstractmethod
    def read_full_waypoint_file(self) -> dict:
        """
        Reads and returns the data held within the waypoints file.

        
        Returns
        -------
        dict
            The data held within the file.
        """
        

    @abstractmethod
    def write_to_full_waypoint_file(self) -> None:
        """
        Writes to the data held within the waypoints file.
        """
    