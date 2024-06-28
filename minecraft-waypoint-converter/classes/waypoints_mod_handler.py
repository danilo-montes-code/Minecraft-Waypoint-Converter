"""waypoints_mod_handler.py

Contains a class that handles reading and writing waypoints to and from
a waypoint mod.
Class is written as an abstract class.
"""



from abc import ABC, abstractmethod
from typing import Any



class WaypointsModHandler(ABC):
    """
    A class that handles reading and writing waypoints to and from
    a waypoint mod.

    Attributes
    ----------
    waypoint_list : dict
        the list of all the waypoints in all the worlds/servers
        that the mod has created waypoints for
    """

    def __init__(self) -> None: 
        """
        Creates an instance of a WaypointsModHandler subclass.
        """
        self.waypoint_list = {}



    ####################################################################
    #####                     Reading Methods                      #####
    ####################################################################

    @abstractmethod
    def _get_worlds(self) -> list[str]:
        """
        Retrieves a list of all the names of worlds/servers that the 
        mods has waypoints created for.

        Returns
        -------
        list[str]
            the list of the names of the worlds/servers
        """


    @abstractmethod
    def _get_world_waypoints(self, world_name : str) -> dict:
        """
        Retrieves a list of all the waypoints for a world which the mod 
        has waypoints created. Different subclasses of this class will
        implement different dict formats to return the waypoint data as.

        Parameters
        ----------
        world_name : str
            the name of the world/server to get waypoints from

        Returns
        -------
        dict
            a dict containing the world's waypoints'
        """


    @abstractmethod
    def world_in_list(self, world_name : str) -> bool:
        """
        Determines if the mod has waypoints created for the given
        world/server.

        Parameters
        ----------
        world_name : str
            the name of the world/server to check waypoints for

        Returns
        -------
        bool
            True,   if the mod has waypoints for the world/server
            False,  otherwise
        """


    @abstractmethod
    def _get_specific_world_name(self, search_name : str) -> str:
        """
        Obtains the file system name for the desired world/server. 
        Searches all world names using `search_name`, eventually 
        returning a single file system name for a world/server.

        Parameters
        ----------
        search_name : str
            part of the world/server name to find a server with

        Returns
        -------
        str
            the file system name for the desired world/server
        """


    @abstractmethod
    def _get_matching_servers(self, search_name : str) -> list[str]:
        """
        Obtains the file system names of all worlds/serves containing 
        the given `search_name`.

        Parameters
        ----------
        search_name : str
            part of the world/server name to find worlds with

        Returns
        -------
        list[str]
            the file system names for the found world/server
        """


    @abstractmethod
    def _choose_server(server_paths : list[str]) -> str:
        """
        Prompts user to choose the desired file system name for the 
        world from a list of possible worlds.

        Parameters
        ----------
        server_paths : list[str]
            file system names to choose from

        Returns
        -------
        str
            the file system name of the chosen world
        """



    ####################################################################
    #####                   Conversion Methods                     #####
    ####################################################################

    @abstractmethod
    def convert_from_mod_to_standard(self, world_name : str) -> dict:
        """
        Converts this mod's complete waypoint data to the standardized
        format.

        Returns
        -------
        dict
            a standardized formatted dict of a world's waypoints' 
            data that all waypoint mods share
        """


    @abstractmethod
    def _create_standardized_dict(self) -> dict:
        """
        Creates the dictionary with the world's waypoints in the
        standardized format.

        Returns
        -------
        dict
            the dict with the waypoint data as a standardized format
        """


    @abstractmethod
    def convert_from_standard_to_mod(self, standard_data : dict) -> bool:
        """
        Converts the standardized format to this mod's waypoint data.

        Parameters
        ----------
        standard_data : dict
            the standardized waypoint data to be converted

        Returns
        -------
        bool
            True,   if the conversion was successful,
            False,  otherwise
        """


    @abstractmethod
    def _add_waypoints_to_mod(self) -> bool:
        """
        Adds the given waypoints to the given world's waypoint list.
        Options for features that are specific to individual mods are
        not given any values, so they are left as default in class
        implementations of waypoint creation.

        Parameters
        ----------
        world_name : str
            the name of the world/server to add waypoints to
        waypoints : dict
            the waypoints to add to the world/server

        Returns
        -------
        bool
            True,   if the waypoints were added successfully
            False,  otherwise
        """
