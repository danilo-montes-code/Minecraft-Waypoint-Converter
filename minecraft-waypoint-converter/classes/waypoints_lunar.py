from .file_extension import FileExtension
from .file_json import JSONFile
from .waypoints import Waypoints

from typing import Type, Any



class WaypointsLunar(Waypoints):

    def __init__(self,
                 file_path : str) -> None:
        super().__init__(file_path=file_path, extension=JSONFile)


    def read(self) -> dict:
        return self.file.read()
    
    def write(self, data : Any) -> bool:
        return self.file.write(data)
    
    def print(self) -> None:
        self.file.print()