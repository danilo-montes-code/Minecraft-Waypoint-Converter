"""waypoints_handler_lunar.py

Contains a class that handles reading and writing waypoints to and from
Lunar Client's waypoint mod.
"""


from .waypoints_file_mod_handler import FileWaypointsModHandler
from .file_json import JSONFile
from .useful_methods import (print_script_message, 
                             prompt_for_answer, 
                             select_list_options)

from typing import Any
import os
from pathlib import Path



class LunarWaypointsHandler(FileWaypointsModHandler):
    """
    A class that represents a set of waypoints for the Lunar Client
    waypoints mod.

    Lunar Client stores waypoints in the following format 
    (all waypoints in single JSON file):

    {
        "version" : int,
        "waypoints" : {
            "sp:worldName OR mp:serverName" : {
                "" : {
                    "waypointName" : {
                        "location" {
                            "x" : int,
                            "y" : int,
                            "z" : int
                        },
                        "visible" : bool,
                        "dimension" : int,
                        "color" : {
                            "value" : int,
                            "chroma" : bool (only if true),
                            "chromaSpeed" : "int" (only if not default),
                            "chromaType" : str (only if "shift")
                        },
                        "showBeam" : bool,
                        "showText" : bool
                    }
                }
            },
            ...
        }
    }

    world tags
        "sp:worldName" - singleplayer
        "mp:serverName" - multiplayer

    dimension tag (same for xaeros)
        -1 - nether
        0  - overworld
        1  - end

    Attributes
    ----------
    waypoints_file : FileHandler
        class that handles IO for the file in which Lunar Client stores
        its waypoints
    """

    def __init__(self,
                 different_file_path : str = None) -> None:
        """
        Creates an instance of LunarWaypointsHandler.

        Parameters
        ----------
        different_file_path : str, optional
            the path to the file where Lunar Client stores its waypoints
        """
        if not different_file_path:
            super().__init__(
                file_path = os.path.join(
                    Path.home(), 
                    '.lunarclient', 
                    'settings', 
                    'game',
                    'waypoints.json'
                ), 
                extension=JSONFile
            )

        else:
            super().__init__(
                file_path=different_file_path, 
                extension=JSONFile
            )

        data : dict = self.waypoints_file.read()
        self.waypoint_list : dict = data['waypoints']



    ####################################################################
    #####              WaypointsModHandler Overrides               #####
    ####################################################################

    def parse_world_name(world_name: str) -> str:
        # Lunar world name format is either
        # sp:WORLD_NAME
        # or
        # mp:WORLD_NAME
        return world_name[3:]


    def get_world_type(world_name : str) -> bool:
        return world_name[:2] == 'sp'


    def get_world_name(self, search_name : str) -> str | None:

        return self._get_specific_world_name(search_name=search_name)


    def _get_worlds(self) -> list[str]:
        return [world for world in self.waypoint_list.keys()]
    

    def _get_world_waypoints(self, world_name: str) -> dict:

        found_world = self._get_specific_world_name(search_name=world_name)

        if not found_world:
            raise Exception(
                'This should not happen, since the given world name is'
                ' the exact way it appears in the Lunar Client file.'
            )

        return self.waypoint_list[found_world][""]
    
    
    def _world_in_list(self, world_name: str) -> bool:
        # TODO is this method really needed?
        return False


    def _get_specific_world_name(self, search_name: str) -> str | None:

        matching_servers = self._get_matching_servers(search_name)

        if len(matching_servers) == 0:
            print_script_message(
                f'No servers matching the name "{search_name}" were found.'
            )
            return None

        if len(matching_servers) == 1:
            return matching_servers[0]
        
        return self._choose_server(matching_servers)


    def _get_matching_servers(self, search_name: str) -> list[str]:

        return list(
            filter(
                lambda server_name: search_name.lower() in server_name.lower(),
                self._get_worlds()
            )
        )


    def _choose_server(self, server_paths: list[str]) -> str:

        print_script_message('Multiple servers were found that include the given name.')
        print_script_message('Please select the number of the desired server.')

        server_choice : int = select_list_options(server_paths)

        return server_paths[server_choice - 1]
    

    def convert_from_mod_to_standard(self, world_name: str) -> dict:
        raise NotImplementedError()
    

    def _create_standardized_dict(self) -> dict:
        raise NotImplementedError()
    

    def convert_from_standard_to_mod(
            self, 
            standard_data : dict, 
            world_name : str
        ) -> bool:
        raise NotImplementedError()
    

    def _add_waypoints_to_mod(self, world_name: str, waypoints: list[str]) -> bool:
        raise NotImplementedError()



    ####################################################################
    #####            FileWaypointsModHandler Overrides             #####
    ####################################################################

    def read_waypoints(self) -> dict:
        return self.waypoints_file.read()
    

    def write(self, data : Any) -> bool:
        return self.waypoints_file.write(data)



    ####################################################################
    #####                       Other Methods                      #####
    ####################################################################

    def print_waypoints(self) -> None:
        """
        Prints the Lunar Client waypoints to the console.
        """

        self.waypoints_file.print()
