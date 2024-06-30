"""standard_world_waypoints.py

Contains a class that handles reading and writing waypoints to and from
a standardized format.
"""



from .file_handler import FileHandler
from .file_yaml import YAMLFile

from typing import Any
import os



class StandardWorldWaypoints():
    """
    A class that handles reading and writing waypoints to and from
    a standardized format. The data is for a single world/server.

    The standard format includes only waypoint data that is common
    between all waypoint mods. The format is as follows:

    {
        'DIMENSION_NAME_1' : {
            'WAYPOINT_NAME_1' : {
                'coordinates' : {
                    'x' : float,
                    'y' : float,
                    'z' : float
                },
                'color' : int,
                'visible : bool
            },
            'WAYPOINT_NAME_2' : {
                ...
            }
        },
        'DIMENSION_NAME_2' : {
            'WAYPOINT_NAME_3' : {
                ...
            },
            'WAYPOINT_NAME_4' : {
                ...
            }
        }
    }


    Attributes
    ----------
    world_name : str
        the name of the world/server
    world_type : bool
        indication of what type of world the world is:
        True - singleplayer,
        False - multiplayer
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


        # Format preserved for if number of world types becomes
        # more than just 2


        # standardized_waypoints_file_path : str = os.path.join(
        #     os.getcwd(), 'minecraft-waypoint-converter', 'data'
        # )

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
        )

        self.waypoints_file = FileHandler.exact_path(
            full_path=os.path.join(
                standardized_waypoints_file_path,
                f'{world_name}.yaml'
            ),
            extension=YAMLFile
        )



    def read_waypoints(self) -> dict:
        """
        Reads the waypoints from the file and returns the dict data.

        Return
        ------
        dict
            the waypoint data held in the file
        """
        
        return self.waypoints_file.read()


    def write_waypoints(self, given_waypoints : dict) -> bool:
        """
        Writes the passed in waypoints to the file containing the
        standardized waypoint information.

        Parameters
        ----------
        given_waypoints : dict
            properly formatted waypoints to write to the file

        Return
        ------
        bool
            True,   if the file was successfully written to,
            False,  otherwise
        """

        return self.waypoints_file.write(given_waypoints)
