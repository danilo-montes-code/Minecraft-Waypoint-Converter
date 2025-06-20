"""waypoint_handler_xaeros.py

Contains a class that handles reading and writing waypoints to and from
the mod Xaero's Minimap.
"""

from pathlib import Path
import os

from pyfilehandlers.file_handler import FileHandler
from pyfilehandlers.file_txt import TxtFile
from pyfilehandlers.file_minecraft_dat import MinecraftDatFile
from lunapyutils import (
    print_script_message, 
    select_list_options,
    merge_dicts
)

from .waypoint_directory_mod_handler import DirectoryWaypointModHandler


from typing import override


class XaerosWaypointHandler(DirectoryWaypointModHandler):
    """
    A class that that handles reading and writing waypoints to and from
    the mod Xaero's Minimap.

    Xaero's Minimap stores all waypoints in a directory, defaulted to
    `%APPDATA%/.minecraft/xaero/minimap`. Within this directory, 
    there are subdirectories, one for each individual world/server. 
    A world/server directory contains up to three directories, named
    `dim%0`, `dim%-1`, and `dim%1`, for the Overworld, Nether, and End
    respectively. Each of these dimension directories contains a file named
    `mw$default_1.txt`, which contains the waypoints for that dimension.

    Xaero's Minimap also supports creating waypoint groups. 
    If a group is created, the first line of the file will be a line starting
    with "set", and the names of each group will follow, each separated by ":".
    The next three lines will be header comments, starting with "#",
    indicating the format of the waypoints in the file. 
    The format of waypoint storage in the text file is as follows 
    (example data is shown underneath the header lines):

    ```
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
    ```
    """

    def __init__(
        self,
        input_directory_path : Path = None,
        output_directory_path : Path = None
    ) -> None:
        """
        Initializes a XaerosWaypointHandler instance.
        By default, the output directory is set to the same as the input directory.

        
        Parameters
        ----------
        input_directory_path : pathlib.Path, optional
            The path to the directory where waypoints are stored, to be used as
            input to the converter.
            If not provided, defaults to `%APPDATA%/.minecraft/xaero/minimap`.

        output_directory_path : pathlib.Path, optional
            The path to the directory where waypoints are stored, to be used as
            output from the converter. If not provided, defaults to the same
            as `input_directory_path`.
        """

        input_dir = input_directory_path or Path(
            os.getenv('APPDATA'),
            '.minecraft',
            'xaero',
            'minimap'
        )

        output_dir = output_directory_path or input_dir

        super().__init__(
            input_directory_path = input_dir, 
            output_directory_path = output_dir, 
            extension_of_files='txt'
        )



    ####################################################################
    #####              WaypointsModHandler Overrides               #####
    ####################################################################

    @override
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


    @override
    def get_world_type(world_name : str) -> str:

        if world_name.startswith('Multiplayer_'):
            return 'multiplayer'

        if world_name.startswith('Realms_'):
            return 'realms'

        return 'singleplayer'


    @override
    def get_world_name(self, search_name : str) -> str | None:
        
        return self._get_specific_world_name(search_name=search_name)


    # TODO create dict and tuples of sp/mp worlds
    @override
    def _get_worlds(self) -> list[str]:

        worlds_with_created_wps = os.listdir(self.base_directory_path)
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
    

    @override
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

        world_dir = self._get_world_directory(world_name=found_world)

        waypoints = {
            'overworld' : {},
            'nether' : {},
            'end' : {}
        }

        for item in os.listdir(world_dir):

            item_path = os.path.join(world_dir, item)
            if not os.path.isdir(item_path):
                continue

            dimension = get_dimension_name(item)

            waypoint_file = FileHandler.exact_path(
                full_path=os.path.join(item_path, 'mw$default_1.txt'),
                extension=TxtFile
            )

            waypoint_file_data = waypoint_file.read()

            for line in waypoint_file_data:

                formatted_wp_dict = get_formatted_wp_dict(line_data=line)
                if not formatted_wp_dict:
                    continue

                waypoints[dimension][formatted_wp_dict['name']] = formatted_wp_dict

        return waypoints


    @override
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


    # TODO search tuples
    @override
    def _get_matching_servers(self, search_name : str) -> list[str]:

        return list(
            filter(
                lambda server_name: search_name.lower() in server_name.lower(),
                self._get_worlds()
            )
        )


    @override
    def _choose_server(self, server_paths : list[str]) -> str:
        
        print_script_message('(Xaero\'s): Multiple worlds were found that include the given text.')
        print_script_message('Please select the number of the desired server.')

        server_choice : int = select_list_options(server_paths)

        return server_paths[server_choice - 1]
    

    @override
    def convert_from_mod_to_standard(self, world_name : str) -> dict:
        
        standardized_dict = self._create_standardized_dict(world_name=world_name)

        standardized_dict = {
            key: value for (key, value) in standardized_dict.items() if value
        }

        return standardized_dict


    @override
    def _create_standardized_dict(self, world_name : str) -> dict:
        
        world_waypoints = self._get_world_waypoints(world_name=world_name)

        standardized_format = {
            'overworld' : {},
            'nether' : {},
            'end' : {}
        }

        for dimension in world_waypoints:
            for dimension_wp_name, dimension_wp_data in world_waypoints[dimension].items():
                
                standardized_format[dimension][dimension_wp_name] = {
                    'coordinates' : {
                        'x' : dimension_wp_data['x'],
                        'y' : dimension_wp_data['y'],
                        'z' : dimension_wp_data['z']
                    },
                    'color' : dimension_wp_data['color'],
                    'visible' : dimension_wp_data['disabled']
                }

        return standardized_format


    """
    Xaero's waypoint dict format
    {
        'DIMENSION_NAME' : {
            'WAYPOINT_NAME' : {
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
            },
            ...
        },
        ...
    }
    """
    @override
    def convert_from_standard_to_mod(
        self, 
        standard_data : dict,
        world_name : str
    ) -> bool:
        
        existing_waypoints = self._get_world_waypoints(world_name=world_name)
        wps_to_add = {
            'overworld' : {},
            'nether' : {},
            'end' : {}
        }

        for dimension, waypoints in standard_data.items():
            for wp_name, wp_data in waypoints.items():

                # remove duplicate waypoint names, despite Xaero's
                # support for duplicate waypoint names, to prevent
                # undesired waypoint duplication if converted multiple
                # times
                if wp_name in existing_waypoints:
                    print_script_message(f'Waypoint with name "{wp_name}" already exists, skipping...')
                    continue

                wps_to_add[dimension][wp_name] = self._create_mod_waypoint_dict(
                    standard_wp_dict=wp_data,
                    waypoint_name=wp_name
                )

        combined_waypoints = merge_dicts(existing_waypoints, wps_to_add)

        return  self._add_waypoints_to_mod(
                    world_name=world_name,
                    waypoints=combined_waypoints
                )


    @override
    def _add_waypoints_to_mod(self, 
                              world_name: str, 
                              waypoints: dict
    ) -> bool:

        dir_path = self._get_world_directory(world_name=world_name)
        
        output_files : dict[str, FileHandler] = {
            'overworld' : FileHandler.exact_path(
                full_path=os.path.join(dir_path, 'dim%0', 'mw$default_1.txt'),
                extension=TxtFile
            ),
            'nether' : FileHandler.exact_path(
                full_path=os.path.join(dir_path, 'dim%-1', 'mw$default_1.txt'),
                extension=TxtFile
            ),
            'end' : FileHandler.exact_path(
                full_path=os.path.join(dir_path, 'dim%1', 'mw$default_1.txt'),
                extension=TxtFile
            )
        }

        error_in_write = False

        for dimension, dimension_waypoints in waypoints.items():

            dimension : str

            write_successful = self._write_to_waypoint_file(
                waypoint_file=output_files[dimension],
                mod_formatted_waypoints=dimension_waypoints
            )

            if write_successful:
                print_script_message(f'{dimension.title()} waypoints written.')
            else:
                error_in_write = True
                print_script_message(f'Failure writing {dimension.title()} waypoints.')

        return not error_in_write


 
    @override
    def create_backup(self, world_name : str) -> bool:

        world_dir = self._get_world_directory(world_name=world_name)

        for item in os.listdir(world_dir):

            item_path = os.path.join(world_dir, item)
            if not os.path.isdir(item_path):
                continue

            # read file with FileHandler
            waypoint_file = FileHandler.exact_path(
                full_path=os.path.join(item_path, 'mw$default_1.txt'),
                extension=TxtFile
            )

            waypoint_file_data = waypoint_file.read()

            backup_file = FileHandler.exact_path(
                full_path=Path(
                    os.getcwd(),
                    'minecraft-waypoint-converter',
                    'data',
                    'backups',
                    self.get_datetime(),
                    'xaero\'s minimap',
                    world_name,
                    item,
                    'mw$default_1.txt'
                ),
                extension=TxtFile
            )

            if not backup_file.write(data = waypoint_file_data):
                print_script_message('Error creating Xaero\'s Minimap backup file.')
                return False

        return True



    ####################################################################
    #####          DirectoryWaypointsModHandler Overrides          #####
    ####################################################################

    @override
    def _get_world_directory(self, world_name : str) -> str:

        return os.path.join(self.base_directory_path, world_name)
    
    

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
            'x' : int(standard_wp_dict['coordinates']['x']),
            'y' : int(standard_wp_dict['coordinates']['y']),
            'z' : int(standard_wp_dict['coordinates']['z']),
            'color' : int(standard_wp_dict['color']),
            'disabled' : not bool(standard_wp_dict['visible']),
            'type' : 0, # default
            'set' : 'gui.xaero_default', # default
            'rotate_on_tp' : False, # default
            'tp_yaw' : 0, # default
            'visibility_type' : 0, # default
            'destination' : False # default
        }

        return xaeros_dict
    

    def _write_to_waypoint_file(
            self,
            waypoint_file : FileHandler,
            mod_formatted_waypoints : dict
        ) -> bool:

        lines_to_write = self._get_headers_(waypoint_file=waypoint_file)

        for wp_name, wp_data in mod_formatted_waypoints.items():

            line_format = \
                f'waypoint:{wp_name}:{wp_data['initials']}:{wp_data['x']}:' \
                f'{wp_data['y']}:{wp_data['z']}:{wp_data['color']}:' \
                f'{str(wp_data['disabled']).lower()}:{wp_data['type']}:{wp_data['set']}:' \
                f'{str(wp_data['rotate_on_tp']).lower()}:{wp_data['tp_yaw']}:' \
                f'{wp_data['visibility_type']}:{str(wp_data['destination']).lower()}'.strip()
            
            lines_to_write.append(line_format)

        return waypoint_file.write(data=lines_to_write)       
        

    def _get_headers_(
            self,
            waypoint_file : FileHandler,
        ) -> list[str]:

        if waypoint_file.is_empty():
            return []
        
        file_lines : list[str] = waypoint_file.read()

        return [line.strip() for line in file_lines if not line.startswith('waypoint')]
    