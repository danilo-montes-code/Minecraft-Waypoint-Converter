"""waypoints_handler_xaeros.py

Contains a class that handles reading and writing waypoints to and from
Xaero's Minimap mod.
"""


from .file_extension import FileExtension
from .file_txt import TxtFile
from .waypoints_mod_handler import WaypointsModHandler

from typing import Type, Any



class XaerosWaypointsHandler(WaypointsModHandler):

    def __init__(self,
                 file_path : str) -> None:
        super().__init__(file_path=file_path, extension=TxtFile)


    def read(self) -> dict:
        return self.file.read()

    def write(self, data : Any) -> bool:
        return self.file.write(data)

    def print(self) -> None:
        self.file.print()

    def _get_worlds(self) -> list[str]:
        pass