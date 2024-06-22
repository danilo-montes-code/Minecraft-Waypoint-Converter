from .file_handler import FileHandler
from .file_extension import FileExtension

from abc import ABC, abstractmethod
from typing import Any

class Waypoints(ABC):

    def __init__(self, 
                 file_path : str,
                 extension : FileExtension) -> None:
        self.file = FileHandler(full_path=file_path, extension=extension)

    @abstractmethod
    def read(self) -> Any:
        pass

    @abstractmethod
    def write(self, data : Any) -> Any:
        pass