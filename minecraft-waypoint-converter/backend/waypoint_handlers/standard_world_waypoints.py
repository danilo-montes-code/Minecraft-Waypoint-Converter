"""standard_world_waypoints.py

Contains a class that handles reading and writing waypoints to and from
a standardized format.
"""

from pathlib import Path

from pyfilehandlers.file_handler import FileHandler



class StandardWorldWaypoints:
    """
    A class that handles reading and writing waypoints to and from
    a standardized format. The data is for a single world/server.

    The standard format includes only waypoint data that is common
    between all waypoint mods. The format is as follows:

    ```
    DIMENSION_NAME_1:
        WAYPOINT_NAME_1:
            coordinates:
                x: float
                y: float
                z: float
            color: int,
            visible: bool
        WAYPOINT_NAME_2:
            ...
    DIMENSION_NAME_2:
        WAYPOINT_NAME_3:
            ...
        WAYPOINT_NAME_4:
            ...
    ```


    Attributes
    ----------
    world_name : str
        The name of the world/server.

    world_type : str
        Indication of what type of world the world is.

    waypoints_file : FileHandler
        Class to handle the file for this world's standardized waypoints.

    mod_name : str
        Name of the mod whose standardized waypoints are held in the file.
    """

    def __init__(
        self,
        world_name : str,
        world_type : str,
        mod_name : str
    ) -> None:
        """
        Initializes a StandardWorldWaypoints instance.
        

        Parameters
        ----------
        world_name : str
            The name of the world/server.

        world_type : str
            Indication of what type of world the world is.

        mod_name : str
            Name of the mod whose standardized waypoints are held in the file.
        """

        self.world_name : str = world_name
        self.world_type : str = world_type
        self.mod_name : str = mod_name


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

        standardized_waypoints_file_path : Path = Path(
            Path.cwd(), 
            'data',
            world_type,
        )

        self.waypoints_file = FileHandler(Path(
            standardized_waypoints_file_path,
            f'{mod_name}_{world_name}.yaml'
        ))


    def read_waypoints(self) -> dict:
        """
        Reads the waypoints from the file and returns the dict data.

        
        Return
        ------
        dict
            The waypoint data held in the file.
        """
        return self.waypoints_file.read()


    def write_waypoints(self, given_waypoints : dict) -> bool:
        """
        Writes the passed in waypoints to the file containing the
        standardized waypoint information.

        
        Parameters
        ----------
        given_waypoints : dict
            Properly formatted waypoints to write to the file.

        
        Return
        ------
        bool
            True,   if the file was successfully written to.
            False,  otherwise.
        """

        return self.waypoints_file.write(given_waypoints)
