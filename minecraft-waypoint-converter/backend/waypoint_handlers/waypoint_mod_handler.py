"""waypoint_mod_handler.py

Contains a class that handles reading and writing waypoints to and from
a waypoint mod.
Class is written as an abstract class.
"""

from abc import ABC, abstractmethod
from datetime import datetime



class WaypointModHandler(ABC):
    """
    A class that handles reading and writing waypoints to and from
    a waypoint mod.

    
    Attributes
    ----------
    waypoint_list : dict
        The list of all the waypoints in all the worlds/servers
        that the mod has created waypoints for. Formatted in the
        standard waypoint save format used in `StandardWorldWaypoints`.

    time_created : datetime.datetime
        The date and time that the instance was created.
    """

    def __init__(self) -> None: 
        """
        Initializes a WaypointModHandler instance.
        """
        self.waypoint_list = {}
        self.time_created = datetime.now()



    ####################################################################
    #####                     Static Methods                       #####
    ####################################################################

    @staticmethod
    @abstractmethod
    def parse_world_name(world_name : str) -> str:
        """
        Parses the world name from the file system name and leaves only 
        the general name of the world.

        
        Parameters
        ----------
        world_name : str
            The name to parse.

            
        Returns
        -------
        str
            The parsed world name.
        """


    @staticmethod
    @abstractmethod
    def get_world_type(world_name : str) -> str:
        """
        Gets whether the world is singleplayer or multiplayer.

        
        Parameters
        ----------
        world_name : str
            The world to determine.

        
        Returns
        -------
        str
            The type of the world.
        """



    ####################################################################
    #####                     Reading Methods                      #####
    ####################################################################

    @abstractmethod
    def get_world_name(self, search_name : str) -> str | None:
        """
        Finds and returns the desired world's name on the file system
        for the mod.

        
        Parameters
        ----------
        search_name : str
            Part of the world name to be searched for.

            
        Returns
        -------
        str
            The file system name of the world.
            None if the world is not found.
        """


    @abstractmethod
    def _get_worlds(self) -> list[str]:
        """
        Retrieves a list of all the names of worlds/servers that the 
        mods has waypoints created for.

        
        Returns
        -------
        list[str]
            The list of the names of the worlds/servers.
        """


    @abstractmethod
    def _get_world_waypoints(self, world_name : str) -> dict:
        """
        Retrieves a list of all the waypoints for a world which the mod 
        has waypoints created. Subclasses of this class will
        implement the dict format following the format of their
        respective mod.

        
        Parameters
        ----------
        world_name : str
            The name of the world/server to get waypoints from.

            
        Returns
        -------
        dict
            A dict containing the world's waypoints.
        """


    @abstractmethod
    def _get_specific_world_name(self, search_name : str) -> str | None:
        """
        Obtains the file system name for the desired world/server. 
        Searches all world names using `search_name`, eventually 
        returning a single file system name for a world/server.

        
        Parameters
        ----------
        search_name : str
            Part of the world/server name to find a server with.

            
        Returns
        -------
        str
            The file system name for the desired world/server.
            None if the world was not in the mod's files.
        """


    @abstractmethod
    def _get_matching_servers(self, search_name : str) -> list[str]:
        """
        Obtains the file system names of all worlds/serves containing 
        the given `search_name`.

        
        Parameters
        ----------
        search_name : str
            Part of the world/server name to find worlds with.

            
        Returns
        -------
        list[str]
            The file system names for the found world/server.
        """


    @abstractmethod
    def _choose_server(self, server_paths : list[str]) -> str:
        """
        Prompts user to choose the desired file system name for the 
        world from a list of possible worlds.

        
        Parameters
        ----------
        server_paths : list[str]
            File system names to choose from.

            
        Returns
        -------
        str
            The file system name of the chosen world.
        """



    ####################################################################
    #####                   Conversion Methods                     #####
    ####################################################################

    @abstractmethod
    def convert_from_mod_to_standard(self, world_name : str) -> dict:
        """
        Converts this mod's complete waypoint data to the standardized
        format.

        
        Parameters
        ----------
        world_name : str
            Name of the world to get waypoints for, as it appears in the
            mod's file system.

            
        Returns
        -------
        dict
            A standardized formatted dict of a world's waypoints' 
            data that all waypoint mods share.
        """


    @abstractmethod
    def _create_standardized_dict(self, world_name : str) -> dict:
        """
        Creates the dictionary with the world's waypoints in the
        standardized format.


        Parameters
        ----------
        world_name : str
            Name of the world to get waypoints for, as it appears in the
            mod's file system.

            
        Returns
        -------
        dict
            The dict with the waypoint data as a standardized format.
        """


    @abstractmethod
    def convert_from_standard_to_mod(
        self, 
        standard_data : dict,
        world_name : str    
    ) -> bool:
        """
        Converts the standardized format to this mod's waypoint data.

        
        Parameters
        ----------
        standard_data : dict
            The standardized waypoint data to be converted.

        world_name : str
            The name of the world/server to add waypoints to.

        testing : bool
            True,   if the method is being tested.
            False,  otherwise.

            
        Returns
        -------
        bool
            True,   if the conversion was successful.
            False,  otherwise.
        """


    @abstractmethod
    def _add_waypoints_to_mod(self, 
                              world_name: str, 
                              waypoints: dict
    ) -> bool:
        """
        Adds the given waypoints to the given world's waypoint list.
        Options for features that are specific to individual mods are
        not given any values, so they are left as default in class
        implementations of waypoint creation.

        
        Parameters
        ----------
        world_name : str
            The name of the world to add waypoints to.

        waypoints : dict
            Waypoint data to add to the world's waypoint list.

            
        Returns
        -------
        bool
            True,   if the waypoints were added successfully.
            False,  otherwise.
        """


    @abstractmethod
    def convert_here(self) -> None:
        """
        Changes the base directory to the predefined directory
        `minecraft-waypoint-converter/data/convert-here`
        """


    @abstractmethod
    def create_backup(self, world_name : str) -> bool:
        """
        Creates a backup of the waypoint data and stores it in
        `minecraft-waypoint-converter/data/backups`

        
        Parameters
        ----------
        world_name : str
            The name of the world to save a backup of.

            
        Returns
        -------
        bool
            True,   if the backup creation was successful.
            False,  otherwise.
        """



    ####################################################################
    #####                      Other Methods                       #####
    ####################################################################

    def get_datetime(self) -> str:
        """
        Gets the datetime from this instance and returns a 
        human readable string with relevant information.
        """

        return self.time_created.strftime("%Y.%m.%d-%H.%M.%S")
