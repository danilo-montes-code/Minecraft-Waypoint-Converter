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
    
    """

    def __init__(self,
                 base_directory_path : str,
                 extension_of_files : FileExtension) -> None:
        self.base_directory_path = base_directory_path
        self.extension_of_files = extension_of_files


    @abstractmethod
    def read_file(self, world_name : str) -> None:
        pass

    @abstractmethod
    def write_file(self, world_name : str) -> None:
        pass