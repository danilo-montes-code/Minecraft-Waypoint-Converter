"""waypoint_directory_mod_handler.py

Contains a class that handles reading and writing waypoints to and from
a waypoint mod that stores all waypoints in multiple directories.
Class is written as an abstract class.
"""

from abc import abstractmethod, ABC
from pathlib import Path

from .waypoint_mod_handler import WaypointModHandler



class DirectoryWaypointModHandler(WaypointModHandler, ABC):
    """
    A class that handles reading and writing waypoints to and from
    a waypoint mod that stores its waypoints in multiple directories.

    
    Attributes
    ----------
    input_directory_path : pathlib.Path
        The path to the directory where waypoints are stored, to be used as
        input to the converter.

    output_directory_path : pathlib.Path
        The path to the directory where waypoints are stored, to be used as
        output from the converter.

    extension_of_files : str
        The extension that all files share.
    """

    def __init__(
        self,
        input_directory_path : Path,
        output_directory_path : Path,
        extension_of_files : str
    ) -> None:
        """
        Initializes a DirectoryWaypointModHandler instance.

        
        Parameters
        ----------
        input_directory_path : pathlib.Path
            The path to the directory where waypoints are stored, to be used as
            input to the converter.

        output_directory_path : pathlib.Path
            The path to the directory where waypoints are stored, to be used as
            output from the converter.

        extension_of_files : str
            The extension that all files share.
        """
        
        super().__init__()
        self.input_directory_path = input_directory_path
        self.output_directory_path = output_directory_path
        self.extension_of_files = extension_of_files


    @abstractmethod
    def _get_world_directory(self, world_name : str) -> str:
        """
        Gets the path of the directory that holds all world waypoints.


        Parameters
        ----------
        world_name : str
            The name of the world to get the directory from.

            
        Returns
        -------
        str
            The path of the directory.
        """
