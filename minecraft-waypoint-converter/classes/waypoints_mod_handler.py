"""waypoints_mod_handler.py

Contains a class that hanldes reading and writing waypoints to and from
a waypoint mod.
Class is written as an abstract class.
"""


from abc import ABC, abstractmethod
from typing import Any

class WaypointsModHandler(ABC):
    """
    A class that represents a set of waypoints in a world.

    Attributes
    ----------
    waypoints : list[dict]
        the list of all the waypoints in the world/server 
    """

    def __init__(self) -> None: 
        """
        Creates an instance of a WaypointsModHandler subclass.
        """
        self.waypoints = []


    @abstractmethod
    def get_worlds(self) -> list[str]:
        """
        Retrieves a list of all the names of worlds/servers that the 
        mods has waypoints created for.

        Returns
        -------
        list[str]
            the list of the names of the worlds/servers
        """


    @abstractmethod
    def get_world_waypoints(self, world_name : str) -> list[dict]:
        """
        Retrieves a list of all the waypoints for a world which the mod 
        has waypoints created. The data contained has only the data
        points that are common between all waypoint mods. These
        attributes are:
        - name : str
        - coordinates : { x : float, y : float, z : float }
        - dimension : int (-1 = nether, 0 = overworld, 1 = end)
        - color : hex
        - visible : bool

        Parameters
        ----------
        world_name : str
            the name of the world/server to get waypoints from

        Returns
        -------
        list[dict]
            a list of a world's waypoints' generalized data that all 
            waypoint mods share
        """
        

    @abstractmethod
    def add_world_waypoints(self, 
                            world_name : str,
                            waypoints : list[dict]) -> bool:
        """
        Adds the given waypoints to the given world's waypoint list.
        Options for features that are specific to individual mods are
        not given any values, so they are left as default in class
        implementations of waypoint creation.

        Parameters
        ----------
        world_name : str
            the name of the world/server to add waypoints to
        waypoints : list[dict]
            the waypoints to add to the world/server

        Returns
        -------
        bool
            True,   if the waypoints were added successfully
            False,  otherwise
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
    def get_specific_world_name(self, search_name : str) -> str:
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
    def get_matching_servers(self, search_name : str) -> list[str]:
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
    def choose_server(server_paths : list[str]) -> str:
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