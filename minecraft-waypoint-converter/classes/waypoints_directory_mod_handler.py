"""waypoints_directory_mod_handler.py

Contains a class that handles reading and writing waypoints to and from
a waypoint mod that stores all waypoints in multiple directories.
Class is written as an abstract class.
"""


from .file_extension import FileExtension
from .waypoints_mod_handler import WaypointsModHandler

from abc import abstractmethod
from typing import Any

class DirectoryWaypointsModHandler(WaypointsModHandler):
    """
    A class that handles reading and writing waypoints to and from
    a waypoint mod that stores all waypoints in multiple directories.

    Attributes
    ----------
    base_directory_path : str
        the path to the directory where all waypoints are stored
    extension_of_files : FileExtension
        the extension that all files share
    """

    def __init__(self,
                 base_directory_path : str,
                 extension_of_files : FileExtension) -> None:
        """
        Creates an instance of a DirectoryWaypointsModHandler subclass.

        Parameters
        ----------
        base_directory_path : str
            the path to the directory where all waypoints are stored
        extension_of_files : FileExtension
            the extension that all files share
        """
        
        self.base_directory_path = base_directory_path
        self.extension_of_files = extension_of_files


    @abstractmethod
    def get_world_directory(self, world_name : str) -> str:
        """
        Gets the path of the directory that holds all world waypoints.

        Parameters
        ----------
        world_name : str
            the name of the world to get the directory from

        Returns
        -------
        str
            the path of the directory
        """
