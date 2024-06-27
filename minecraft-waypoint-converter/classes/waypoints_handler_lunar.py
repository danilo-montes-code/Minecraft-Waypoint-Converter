"""waypoints_handler_lunar.py

Contains a class that handles reading and writing waypoints to and from
Lunar Client's waypoint mod.
"""


from .file_json import JSONFile
from .waypoints_file_mod_handler import FileWaypointsModHandler
from .useful_methods import (print_script_message, 
                             prompt_for_answer, 
                             select_list_options)

from typing import Any



class LunarWaypointsHandler(FileWaypointsModHandler):
    """
    A class that represents a set of waypoints for the Lunar Client
    waypoints mod.

    Attributes
    ----------
    waypoints_file : FileHandler
        class that handles IO for the file in which the waypoints
        are stored
    """

    def __init__(self,
                 file_path : str) -> None:
        super().__init__(file_path=file_path, extension=JSONFile)
        data : dict = self.waypoints_file.read()
        self.waypoint_list : dict = data['waypoints']

    ####################################################################
    #####                   Waypoints Overrides                    #####
    ####################################################################

    def get_worlds(self) -> list[str]:
        return [world for world in self.waypoint_list.keys()]
    

    def get_world_waypoints(self, world_name: str) -> dict:

        if not self.world_in_list(world_name):
            print('Given world not in world list')
            return None

        found_world = self.get_specific_world_name(world_name)

        for world, waypoints in self.waypoint_list.items():

            # will be exact world name, no risk of different server being found
            if world == found_world:
                return waypoints[""]

        return None


    def add_world_waypoints(self, world_name: str, waypoints: list[str]) -> bool:
        pass
    
    
    def world_in_list(self, world_name: str) -> bool:

        for world in self.waypoint_list.keys():
            if world_name in world:
                return True
            
        return False


    def get_specific_world_name(self, search_name: str) -> str:

        matching_servers = self.get_matching_servers(search_name)

        while len(matching_servers) == 0:
            print_script_message(
                f'No servers with the name "{server_name}" were found.' \
                'Please enter a valid server name\n'
            )

            server_name = prompt_for_answer(
                'What is the name of the singleplayer world or multiplayer server IP?' \
                ' (Only part of the name is necessary,' \
                ' ex. "best" will find "best world")'
            )
            matching_servers = self.get_matching_servers(server_name)

        if len(matching_servers) == 1:
            return matching_servers[0]
        
        return self.choose_server(matching_servers)

    

    def get_matching_servers(self, search_name: str) -> list[str]:

        return list(
            filter(
                lambda server_name: search_name.lower() in server_name.lower(),
                self.get_worlds()
            )
        )


    def choose_server(server_paths: list[str]) -> str:

        print_script_message('Multiple servers were found that include the given name.')
        print_script_message('Please select the number of the desired server.')

        server_choice : int = select_list_options(server_paths)

        return server_paths[server_choice - 1]
    


    ####################################################################
    #####                 File Waypoints Overrides                 #####
    ####################################################################

    def read(self) -> dict:
        return self.waypoints_file.read()
    

    def write(self, data : Any) -> bool:
        # convert from YAML standard format to Lunar format
        return self.waypoints_file.write(data)
    


    ####################################################################
    #####                       Other Methods                      #####
    ####################################################################

    def print(self) -> None:
        self.waypoints_file.print()

    