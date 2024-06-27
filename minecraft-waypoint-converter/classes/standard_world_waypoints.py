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
    world_type : bool
        indication of what type of world the world is:
        True - singleplayer,
        False - multiplayer
    waypoints : list[dict]
        the list of all the waypoints in the world/server
    waypoints_file : FileHandler
        class to handle the file for this world's standardized waypoints
    """

    def __init__(self,
                 world_name : str,
                 world_type : bool) -> None:
        """
        Creates an instance of a StandardWorldWaypoints subclass.
        
        Parameters
        ----------
        world_name : str
            the name of the world/server
        world_type : int
            indication of what type of world the world is:
            True - singleplayer,
            False - multiplayer
        """

        self.world_name : str = world_name
        self.world_type : bool = world_type
        self.waypoints : list[dict] = []

        # standardized_waypoints_file_path : str = os.path.join(
        #     os.getcwd(), 'minecraft-waypoint-converter', 'data'
        # )

        # Format preserved for if number of world types becomes
        # more than just 2
        
        # match world_type:
        #     case 0:
        #         standardized_waypoints_file_path = os.path.join(
        #             standardized_waypoints_file_path,
        #             'singleplayer'
        #         )

        #     case 1:
        #         standardized_waypoints_file_path = os.path.join(
        #             standardized_waypoints_file_path,
        #             'multiplayer'
        #         )

        standardized_waypoints_file_path : str = os.path.join(
            os.getcwd(), 'minecraft-waypoint-converter', 'data',
            'singleplayer' if world_type else 'multiplayer',
            world_name
        )

        self.waypoints_file = FileHandler.exact_path(
            full_path=os.path.join(
                standardized_waypoints_file_path,
                world_name
            ),
            extension=YAMLFile
        )



    def read_waypoints(self) -> list[dict]:
        return self.waypoints_file.read()

    def write_waypoints(self, given_waypoints : list[dict]) -> bool:
        return self.waypoints_file.write(given_waypoints)
    