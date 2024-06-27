"""waypoints_directory.py

Contains a class that represents a set of waypoints from a mod that uses
a directory as its storage method.
Class is written as an abstract class.
"""


from .file_extension import FileExtension
from .waypoints import Waypoints

from abc import abstractmethod
from typing import Any

class DirectoryWaypoints(Waypoints):

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