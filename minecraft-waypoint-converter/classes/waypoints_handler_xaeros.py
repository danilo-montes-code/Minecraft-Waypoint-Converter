"""waypoints_handler_xaeros.py

Contains a class that handles reading and writing waypoints to and from
Xaero's Minimap mod.
"""


from .file_handler import FileHandler
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

        def get_dimension_name(dir_name : str) -> str:
            """
            Gets the name of the dimension from the name of the
            directory.

            Parameters
            ----------
            dir_name : str
                the name of the directory to get the dimension from

            Returns
            -------
            str
                the name of the dimension
            """

            dir_name = dir_name.replace('dim%', '')

            try:
                dimension_int = int(dir_name)

                # unaware of custom dimension ints
                dimensions = ['overworld', 'end', 'nether']
                return dimensions[dimension_int]
            
            except (IndexError, ValueError):
                print_script_message(f'Dimension in folder {dir_name} is invalid')
                return 'filler_dimension'
            
        
        def get_formatted_wp_dict(line_data : str) -> dict | None:
            """
            Creates the formatted waypoint dict from the line.

            Parameters
            ----------
            line_data : str
                the line from the file

            Returns
            -------
            dict
                the formatted waypoint dict,
                None,   if the line does not contain waypoint data
                        or upon error
            """
            if line_data.startswith('sets') or line_data.startswith('#'):
                return None
                
            line_data = line_data.split(':')

            try:
                waypoint_format = {
                    'name' : line_data[1], 
                    'initials' : line_data[2],
                    'x' : line_data[3],
                    'y' : line_data[4],
                    'z' : line_data[5],
                    'color' : line_data[6],
                    'disabled' : line_data[7],
                    'type' : line_data[8],
                    'set' : line_data[9], 
                    'rotate_on_tp' : line_data[10], 
                    'tp_yaw' : line_data[11], 
                    'visibility_type' : line_data[12],
                    'destination' : line_data[13]
                }

                return waypoint_format

            except (ValueError, IndexError):
                print_script_message(f'Error in line parsing: {line_data}')
                return None


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

            dimension = get_dimension_name(item)

            # read file with FileHandler
            waypoint_file = FileHandler.exact_path(
                full_path=os.path.join(item_path, 'mw$default_1.txt'),
                extension=TxtFile
            )

            waypoint_file_data = waypoint_file.read()

            for line in waypoint_file_data:

                formatted_wp_dict = get_formatted_wp_dict(line_data=line)
                if not formatted_wp_dict:
                    continue

                waypoints[dimension].append(formatted_wp_dict)

        return waypoints


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

        for dimension in world_waypoints:
            for dimension_waypoint in world_waypoints[dimension]:
                
                wp_name = dimension_waypoint['name']

                standardized_format[dimension][wp_name] = {
                    'coordinates' : {
                        'x' : dimension_waypoint['x'],
                        'y' : dimension_waypoint['y'],
                        'z' : dimension_waypoint['z']
                    },
                    'color' : dimension_waypoint['color'],
                    'visible' : dimension_waypoint['disabled']
                }

        return standardized_format


    """
    waypoint_format = {
        'name' : line_data[1], 
        'initials' : line_data[2],
        'x' : line_data[3],
        'y' : line_data[4],
        'z' : line_data[5],
        'color' : line_data[6],
        'disabled' : False, # default
        'type' : 0, # default
        'set' : 'gui.xaero_default', # default
        'rotate_on_tp' : False, # default
        'tp_yaw' : 0, # default
        'visibility_type' : 0, # default
        'destination' : False # default
    }
    """
    def convert_from_standard_to_mod(
        self, 
        standard_data : dict,
        world_name : str,
        testing : bool = False
    ) -> bool:
        
        existing_waypoints = self._get_world_waypoints(world_name=world_name)
        wps_to_add = {
            'overworld' : {},
            'nether' : {},
            'end' : {}
        }

        for dimension, waypoints in standard_data.items():
            for wp_name, wp_data in waypoints.items():

                wps_to_add[dimension][wp_name] = self._create_mod_waypoint_dict(
                    standard_wp_dict=wp_data,
                    waypoint_name=wp_name
                )

        combined_waypoints = {**existing_waypoints, **wps_to_add}

        if testing:
            from json import dumps
            print(dumps(combined_waypoints, indent=2))
            return False
        
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

    def _create_mod_waypoint_dict(
            self, 
            standard_wp_dict : dict, 
            waypoint_name : str
        ) -> dict:

        xaeros_dict = {
            'name' : waypoint_name, 
            'initials' : waypoint_name[0].title(),
            'x' : standard_wp_dict['coordinates']['x'],
            'y' : standard_wp_dict['coordinates']['y'],
            'z' : standard_wp_dict['coordinates']['z'],
            'color' : standard_wp_dict['color'],
            'disabled' : standard_wp_dict['visible'],
            'type' : 0, # default
            'set' : 'gui.xaero_default', # default
            'rotate_on_tp' : False, # default
            'tp_yaw' : 0, # default
            'visibility_type' : 0, # default
            'destination' : False # default
        }

        return xaeros_dict