from .file_handler import FileHandler
from .file_extension import FileExtension
from .waypoints import Waypoints

from abc import abstractmethod
from typing import Any

class FileWaypoints(Waypoints):

    def __init__(self,
                 file_path : str,
                 extension : FileExtension) -> None:
        self.waypoints_file = FileHandler(
            full_path=file_path, 
            extension=extension
        )


    @abstractmethod
    def read(self) -> None:
        pass

    @abstractmethod
    def write(self) -> None:
        pass