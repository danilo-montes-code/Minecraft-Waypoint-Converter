"""standard_world_waypoints.py

Contains a class that hanldes reading and writing waypoints to and from
a standardized format.
"""

from .file_handler import FileHandler
from .file_yaml import YAMLFile

from typing import Any
import os

class StandardWorldWaypoints():
    """
    A class that represents a set of waypoints in a single world or server.

    Attributes
    ----------
    world_name : str
        the name of the world/server
    world_type : int
        indication of what type of world the world is:
        0 - singleplayer,
        1 - multiplayer
    waypoints : list[dict]
        the list of all the waypoints in the world/server
    waypoints_file : FileHandler
        class to handle the file for this world's standardized waypoints
    """

    def __init__(self,
                 world_name : str,
                 world_type : int) -> None:
        """
        Creates an instance of a StandardWorldWaypoints subclass.
        
        Parameters
        ----------
        world_name : str
            the name of the world/server
        world_type : int
            indication of what type of world the world is:
            0 - singleplayer,
            1 - multiplayer
        """
        self.world_name : str = world_name
        self.world_type : int = world_type
        self.waypoints : list[dict] = []

        standardized_waypoints_file_path : str = os.path.join(
            os.getcwd(), 'minecraft-waypoint-converter', 'data'
        )
        match world_type:
            case 0:
                standardized_waypoints_file_path = os.path.join(
                    standardized_waypoints_file_path,
                    'singleplayer'
                )

            case 1:
                standardized_waypoints_file_path = os.path.join(
                    standardized_waypoints_file_path,
                    'multiplayer'
                )
        self.waypoints_file = FileHandler(
            full_path=os.path.join(
                standardized_waypoints_file_path,
                world_name
            ),
            extension=YAMLFile
        )


    def read(self) -> list[dict]:
        return self.waypoints_file.read()

    def write(self, given_waypoints : list[dict]) -> bool:
        return self.waypoints_file.write(given_waypoints)