"""waypoints_handler_xaeros.py

Contains a class that handles reading and writing waypoints to and from
Xaero's Minimap mod.
"""


from .file_extension import FileExtension
from .file_txt import TxtFile
from .waypoints_directory_mod_handler import DirectoryWaypointsModHandler
from .useful_methods import (print_script_message, 
                             select_list_options)

from typing import Type, Any
from pathlib import Path
import os




class XaerosWaypointsHandler(DirectoryWaypointsModHandler):
    """
    A class that that handles reading and writing waypoints to and from
    Xaero's Minimap mod.

    Xaero's Minimap stores all waypoints in a directory. Within this
    directory, there are subdirectories, each for an individual
    world/server. Within these folders are the waypoints for each 
    individual world/server. This folder has separate folders for each 
    dimension, labeled `dim%<DIMENSION_INT>`. Each dimension folder
    has a single file, `mw$default_1.txt` that holds the waypoint data.

    Xaero's supports creating waypoint groups. If a group is created,
    the list of groups will be the first line, separated by :, 
    followed by the header comments to indicate the waypoint format. 
    The format of waypoint storage in the text file is as follows 
    (header line is consistent, so example data is shown underneath 
    the header lines):

    sets:gui.xaero_default:02 Homes:01 Portals:20 Ocean Monuments:10 Caves:21 Pillager Outposts:30 Ancient Cities:04 Biomes
    #
    #waypoint:name:initials:x:y:z:color:disabled:type:set:rotate_on_tp:tp_yaw:visibility_type:destination
    #
    waypoint:gold farm portal:G:-295:91:158:3:false:0:01 Portals:false:0:0:false
    waypoint:ocean mon II:O:191:63:-5332:2:false:0:20 Ocean Monuments:false:0:0:false
    waypoint:ocean mon:O:126:63:-6313:12:false:0:20 Ocean Monuments:false:0:0:false
    waypoint:return to nether:R:-13802:25:34418:11:false:0:10 Caves:false:0:0:false
    waypoint:far cave:F:-1287:70:5142:5:false:0:10 Caves:false:0:0:false
    waypoint:cave:C:-619:65:1100:11:false:0:10 Caves:false:0:0:false
    waypoint:Ancient City I:A:-13787:-47:34454:10:false:0:30 Ancient Cities:false:0:0:false
    waypoint:Swamp I:A:-1861:71:-5968:5:false:0:04 Biomes:false:0:0:false
    waypoint:Mushroom Fields I:M:106:76:-833:4:false:0:04 Biomes:false:0:0:false
    waypoint:Frozen Ocean I:F:2950:63:3151:8:false:0:04 Biomes:false:0:0:false
    waypoint:Dark Oak I:D:-1296:79:5025:2:false:0:04 Biomes:false:0:0:false
    waypoint:village home:V:-381:68:1070:0:false:0:gui.xaero_default:false:0:0:false
    """

    def __init__(self,
                 different_directory_path : str = None) -> None:
        """
        Creates an instance of XaerosWaypointsHandler.

        Parameters
        ----------
        different_file_path : str, optional
            the path to the directory where Xaero's Minimap 
            stores its waypoints
        """
        if not different_directory_path:
            super().__init__(
                base_directory_path=Path(
                    os.path.join(
                        os.getenv('APPDATA'),
                        '.minecraft',
                        'XaeroWaypoints'
                    )
                ), 
                extension_of_files=TxtFile
            )

        else:
            super().__init__(
                base_directory_path=different_directory_path,
                extension_of_files=TxtFile
            )



    ####################################################################
    #####              WaypointsModHandler Overrides               #####
    ####################################################################

    def parse_world_name(world_name : str) -> str:
        # Xaero's world name format is:
        # just the name of the world for singleplayer
        # Multiplayer_SERVER_NAME for multiplayer
        # Realms_REALMS_IP for realms
        
        if world_name.startswith('Multiplayer_'):
            return world_name[12:]
        
        if world_name.startswith('Realms_'):
            return world_name[7:]
        
        return world_name


    def get_world_type(world_name : str) -> str:

        if world_name.startswith('Multiplayer_'):
            return 'multiplayer'

        if world_name.startswith('Realms_'):
            return 'realms'

        return 'singleplayer'


    def get_world_name(self, search_name : str) -> str | None:
        
        return self._get_specific_world_name(search_name=search_name)


    def _get_worlds(self) -> list[str]:
    
        return [dir_name for dir_name in os.listdir(self.base_directory_path)]


    def _get_world_waypoints(self, world_name : str) -> dict:
        
        found_world = self._get_specific_world_name(search_name=world_name)

        if not found_world:
            raise Exception(
                'This should not happen, since the given world name is'
                ' the exact way it appears in the Xaero\'s dir.'
            )

        world_dir = os.path.join(self.base_directory_path, found_world)

        waypoints = {
            'overworld' : [],
            'nether' : [],
            'end' : []
        }

        for item in os.listdir(world_dir):

            item_path = os.path.join(world_dir, item)

            if not os.path.isdir(item_path):
                continue

            print(item_path)

            # get dimension from item
            # read file with FileHandler
            # save data in waypoints dict


        raise NotImplementedError()


    def _world_in_list(self, world_name : str) -> bool:
        # TODO is this method really needed?
        return False


    def _get_specific_world_name(self, search_name : str) -> str | None:
        
        matching_servers = self._get_matching_servers(search_name=search_name)

        if len(matching_servers) == 0:
            print_script_message(
                f'No servers matching the name "{search_name}" were found.'
            )
            return None

        if len(matching_servers) == 1:
            return matching_servers[0]

        return self._choose_server(matching_servers)


    def _get_matching_servers(self, search_name : str) -> list[str]:

        return list(
            filter(
                lambda server_name: search_name.lower() in server_name.lower(),
                self._get_worlds()
            )
        )


    def _choose_server(self, server_paths : list[str]) -> str:
        
        print_script_message('Multiple servers were found that include the given name.')
        print_script_message('Please select the number of the desired server.')

        server_choice : int = select_list_options(server_paths)

        return server_paths[server_choice - 1]
    

    def convert_from_mod_to_standard(self, world_name : str) -> dict:
        
        standardized_dict = self._create_standardized_dict(world_name=world_name)

        standardized_dict = {
            key: value for (key, value) in standardized_dict.items() if value
        }

        return standardized_dict


    def _create_standardized_dict(self, world_name : str) -> dict:
        
        world_waypoints = self._get_world_waypoints(world_name=world_name)

        standardized_format = {
            'overworld' : {},
            'nether' : {},
            'end' : {}
        }

        for waypoint in world_waypoints:
            pass

        raise NotImplementedError()


    def convert_from_standard_to_mod(
        self, 
        standard_data : dict,
        world_name : str,
        testing : bool = False
    ) -> bool:
        raise NotImplementedError()


    def _add_waypoints_to_mod(self, 
                              world_name: str, 
                              waypoints: dict
    ) -> bool:
        raise NotImplementedError()



    ####################################################################
    #####          DirectoryWaypointsModHandler Overrides          #####
    ####################################################################

    def get_world_directory(self, world_name : str) -> str:
        raise NotImplementedError()
    


    ####################################################################
    #####                       Other Methods                      #####
    ####################################################################

