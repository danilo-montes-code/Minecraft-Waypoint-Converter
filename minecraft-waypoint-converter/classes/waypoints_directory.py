from .file_handler import FileHandler
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