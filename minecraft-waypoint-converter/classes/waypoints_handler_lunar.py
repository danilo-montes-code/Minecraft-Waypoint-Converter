"""waypoints_handler_lunar.py

Contains a class that handles reading and writing waypoints to and from
Lunar Client's waypoint mod.
"""


from .waypoints_file_mod_handler import FileWaypointsModHandler
from .file_json import JSONFile
from .file_handler import FileHandler
from .file_dat_minecraft import MinecraftDatFile
from .useful_methods import (print_script_message, 
                             select_list_options,
                             merge_dicts)

from typing import Any
import os
from pathlib import Path



class LunarWaypointsHandler(FileWaypointsModHandler):
    """
    A class that handles reading and writing waypoints to and from
    Lunar Client's waypoint mod.

    Lunar Client stores waypoints in the following format 
    (all waypoints in single JSON file):

    {
        "version" : int,
        "waypoints" : {
            "sp:worldName OR mp:serverName" : {
                "" : {
                    "waypointName" : {
                        "location" {
                            "x" : float,
                            "y" : float,
                            "z" : float
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

    Lunar Client does NOT allow for duplicate waypoint names.

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

        file_path = different_file_path or os.path.join(
            Path.home(), 
            '.lunarclient', 
            'settings', 
            'game',
            'waypoints.json'
        )

        super().__init__(
            file_path = file_path, 
            extension=JSONFile
        )

        try:
            data : dict = self.read_full_waypoint_file()
            self.waypoint_list : dict = data['waypoints']

        except TypeError:
            # if the file is not found, do not create the waypoint list
            print_script_message(f'No file found at {file_path}')
            return None



    ####################################################################
    #####              WaypointsModHandler Overrides               #####
    ####################################################################

    def parse_world_name(world_name: str) -> str:
        # Lunar world name format is either
        # sp:WORLD_NAME
        # or
        # mp:WORLD_NAME
        return world_name[3:]


    def get_world_type(world_name : str) -> str:
        # does not account for realms, since I am unaware of realms format
        return 'singleplayer' if world_name[:2] == 'sp' else 'multiplayer'


    def get_world_name(self, search_name : str) -> str | None:

        return self._get_specific_world_name(search_name=search_name)


    def _get_worlds(self) -> list[str]:

        worlds_with_created_wps = list(self.waypoint_list.keys())
        worlds_singleplayer = os.listdir(os.path.join(
            os.getenv('APPDATA'),
            '.minecraft',
            'saves'
        ))
        worlds_multiplayer_file = FileHandler(
            extension=MinecraftDatFile,
            full_path=os.path.join(
                os.getenv('APPDATA'),
                '.minecraft',
                'servers.dat'
            )
        )
        worlds_multiplayer = []

        for server in worlds_multiplayer_file.read()['servers']:
            worlds_multiplayer.append(f'{server['name']} (ip: {server['ip']})')

        return worlds_with_created_wps + worlds_singleplayer + worlds_multiplayer

    

    def _get_world_waypoints(self, world_name: str) -> dict:

        found_world = self._get_specific_world_name(search_name=world_name)

        if not found_world:
            raise Exception(
                'This should not happen, since the given world name is'
                ' the exact way it appears in the Lunar Client file.'
            )

        return self.waypoint_list[found_world][""]


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

        print_script_message('(Lunar Client): Multiple worlds were found that include the given text.')
        print_script_message('Please select the number of the desired server.')

        server_choice : int = select_list_options(server_paths)

        return server_paths[server_choice - 1]
    

    def convert_from_mod_to_standard(self, world_name: str) -> dict:
        
        standardized_dict = self._create_standardized_dict(world_name=world_name)

        standardized_dict = {
            key: value for (key, value) in standardized_dict.items() if value
        }

        return standardized_dict
    

    def _create_standardized_dict(self, world_name: str) -> dict:

        world_waypoints = self._get_world_waypoints(world_name=world_name)

        standardized_format = {
            'overworld' : {},
            'nether' : {},
            'end' : {}
        }

        for wp_name, wp_data in world_waypoints.items():

            # verify duplicate names are not overriden
            dimension = 'filler_dimension'

            match wp_data['dimension']:

                case 0:
                    dimension = 'overworld'

                case -1:
                    dimension = 'nether'

                case 1:
                    dimension = 'end'

                # other dimension
                case _:
                    pass


            color = wp_data['color']['value'] if 'color' in wp_data else 0

            standardized_format[dimension][wp_name] = {
                'coordinates' : {
                    'x' : wp_data['location']['x'],
                    'y' : wp_data['location']['y'],
                    'z' : wp_data['location']['z']
                },
                'color' : color,
                'visible' : wp_data['visible']
            }

        return standardized_format
    

    def convert_from_standard_to_mod(
            self, 
            standard_data : dict, 
            world_name : str
        ) -> bool:
        
        existing_waypoints = self._get_world_waypoints(world_name=world_name)
        wps_to_add = {}

        for dimension, waypoints in standard_data.items():
            for wp_name, wp_data in waypoints.items():

                # remove duplicate waypoint names because Lunar does not
                # support duplicate waypoint names
                if wp_name in existing_waypoints:
                    print_script_message(f'Waypoint with name "{wp_name}" already exists, skipping...')
                    continue

                wps_to_add[wp_name] = self._create_mod_waypoint_dict(
                    standard_wp_dict=wp_data,
                    dimension=dimension
                )

        combined_waypoints = merge_dicts(existing_waypoints, wps_to_add)
        
        return  self._add_waypoints_to_mod(
                    world_name=world_name,
                    waypoints=combined_waypoints
                )

    
    def _add_waypoints_to_mod(
            self, 
            world_name: str, 
            waypoints: dict
        ) -> bool:

        error_in_write = False

        full_wp_data = self.read_full_waypoint_file()

        full_wp_data['waypoints'][world_name][""] = waypoints

        write_successful = self.write_to_full_waypoint_file(data=full_wp_data)

        if write_successful:
            print_script_message(f'Waypoints written.')
        else:
            error_in_write = True
            print_script_message(f'Failure writing waypoints.')

        return not error_in_write


    def change_path(self, new_path : str) -> None:
        self.file_path = os.path.join(
            new_path, 
            'lunar client', 
            'waypoints.json'
        )
        return


    def create_backup(self, world_name : str) -> bool:
        data : dict = self.read_full_waypoint_file()
        backup_file = FileHandler.exact_path(
            full_path=Path(
                os.getcwd(),
                'minecraft-waypoint-converter',
                'data',
                'backups',
                self.get_datetime(),
                'lunar client',
                'waypoints.json'
            ),
            extension=JSONFile
        )

        if not backup_file.write(data=data):
            print_script_message('Error creating Lunar Client backup file.')
            return False

        return True



    ####################################################################
    #####            FileWaypointsModHandler Overrides             #####
    ####################################################################

    def read_full_waypoint_file(self) -> dict:
        return self.waypoints_file.read()
    

    def write_to_full_waypoint_file(self, data : Any) -> bool:
        return self.waypoints_file.write(data)



    ####################################################################
    #####                       Other Methods                      #####
    ####################################################################

    def print_waypoints(self) -> None:
        """
        Prints the Lunar Client waypoints to the console.
        """

        self.waypoints_file.print()


    def _create_mod_waypoint_dict(
            self, 
            standard_wp_dict : dict, 
            dimension : str
        ) -> dict:
        """
        Creates the waypoint dict in the format of Lunar Client.

        Parameters
        ----------
        standard_wp_dict : dict
            the standardized waypoint data
        dimension : str
            the dimension currently being handled

        Returns
        -------
        dict
            the waypoints formatted in the way of Lunar Client
        """
        
        dimension_int : int

        match dimension:
            case 'overworld':
                dimension_int = 0

            case 'nether':
                dimension_int = -1

            case 'end':
                dimension_int = 1

            # have not tested modded dimensions, so don't know
            # what int they get 
            case _:
                dimension_int = 2


        lunar_dict = {
            'location' : {
                'x' : float(standard_wp_dict['coordinates']['x']),
                'y' : float(standard_wp_dict['coordinates']['y']),
                'z' : float(standard_wp_dict['coordinates']['z'])
            },
            'visible' : bool(standard_wp_dict['visible']),
            'dimension' : int(dimension_int),
            'color' : {
                'value' : int(standard_wp_dict['color'])
            },
            'showBeam' : True,
            'showText' : True
        }

        return lunar_dict
    