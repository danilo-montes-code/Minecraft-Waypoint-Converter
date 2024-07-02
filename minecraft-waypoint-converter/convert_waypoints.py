"""
Minecraft Waypoint Converter

Converts Minecraft waypoints between various mods. 

Dependencies:
* ruamel.yaml
"""



from classes import *
from classes.waypoints_mod_handler import WaypointsModHandler

import os, json, sys
from pathlib import Path




########################################################################
#####                          Constants                           #####
########################################################################

HOME_DIR = Path.home()
APP_DATA = Path(os.getenv('APPDATA'))

MOD_CLASSES : dict[str, WaypointsModHandler] = {
    'lunar client'      : LunarWaypointsHandler() or None,
    'xaero\'s minimap'  : XaerosWaypointsHandler() or None
}


########################################################################
#####                        Get Waypoints                         #####
########################################################################


def get_waypoints_xaeros() -> None:

    def search_for_server_waypoints(server_name : str) -> list[str]:

        matching_servers : list[Path] = []

        waypoint_lists = os.listdir(xaeros_folder_path)
        matching_servers : list[Path] = \
            list(
                filter(
                    lambda dir_name: server_name.lower() in dir_name.lower(), 
                    waypoint_lists
                )
            )
        
        return matching_servers



    def choose_server(server_paths : list[str]) -> str:

        print_script_message('Multiple servers were found that include the given name.')
        print_script_message('Please select the number of the desired server.')

        server_choice : int = select_list_options(server_paths)

        return server_paths[server_choice - 1]


    xaeros_folder_path = os.path.join(
        APP_DATA,
        '.minecraft',
        'XaeroWaypoints'
    )

    server_name = prompt_for_answer(
        'What is the name of the singleplayer world or multiplayer server IP?' \
        ' (Only part of the name is necessary,' \
        ' ex. "best" will find "best world")'
    )

    matching_servers = search_for_server_waypoints(server_name)

    while len(matching_servers) == 0:
        print_script_message(f'No servers with the name "{server_name}" were found.')
        print_script_message('Please enter a valid server name\n')

        server_name = prompt_for_answer(
            'What is the name of the singleplayer world or multiplayer server IP?' \
            ' (Only part of the name is necessary,' \
            ' ex. "best" will find "best world")'
        )
        matching_servers = search_for_server_waypoints(server_name)

    print(matching_servers)

    if len(matching_servers) == 1:
        server_waypoints_dir = matching_servers[0]
    else:
        server_waypoints_dir = choose_server(matching_servers)

    print(server_waypoints_dir)

    # get server dir from server_waypoints_dir

    # load waypoints file

    # TODO chance xaeros to handle dir instead of single file

    # xaero_waypoints = WaypointsXaeros(
    #     file_path=file_path
    # )


    


########################################################################
#####                     Write to Waypoints                       #####
########################################################################








########################################################################
#####                    Get World/Server Info                     #####
########################################################################

def get_world_name() -> str:

    return prompt_for_answer(
        'What is the name of the singleplayer world or multiplayer server IP?' \
        ' (Only part of the name is necessary,' \
        ' ex. "best" will find "best world")'
    )


def get_mod_names(mod_options : tuple[str]) -> tuple[str]:

    print_script_message('Select the mod to convert from: ')
    from_mod : str = mod_options[select_list_options(mod_options) - 1]

    print()

    print_script_message('Select the mod to convert to: ')
    to_mod : str = mod_options[select_list_options(mod_options) - 1]

    if from_mod == to_mod:
        print_script_message(
            'The mods to export from and import to can not be the same mod. '
            'Please select two different mods.'
        )
        return get_mod_names(mod_options)

    return from_mod, to_mod
    

def get_world_file_name(
        world_name : str, 
        mod_name : str,
    ) -> str | None:
    """
    Gets the file system name of the world as it appears for the given
    mod.
    
    Parameters
    ----------
    world_name : str
        the name of the world to search for
    mod_name : str
        the name of the mod to check

    Returns
    -------
    str
        the name of the world on the file system for the mod,
        None if the world is not on the file system
    """

    return MOD_CLASSES[mod_name].get_world_name(search_name=world_name)



########################################################################
#####                         Conversion                           #####
########################################################################

def convert_waypoints(
        from_mod : str, 
        to_mod : str, 
        from_mod_world_name : str,
        to_mod_world_name : str
    ) -> bool:
    """
    Converts the waypoints from one mod to another.
    
    Parameters
    ----------
    from_mod : str
        the mod to convert from
    to_mod : str
        the mod to convert to
    from_mod_world_name : str
        the name of the world for the mod to convert from
    to_mod_world_name : str
        the name of the world for the mod to convert to

    Returns
    -------
    bool
        True,   if the conversion was successful,
        False,  otherwise
    """

    # create standard_world_wps instance

    from_mod_handler = MOD_CLASSES[from_mod]
    to_mod_handler = MOD_CLASSES[to_mod]
    
    world_name, world_type = get_world_info(from_mod, from_mod_world_name)

    standard_file = StandardWorldWaypoints(
        world_name=world_name,
        world_type=world_type,
        mod_name=from_mod
    )
    
    
    # from_mod - get waypoints of world in std mod wp format,
    #            convert wps to standard format dict
    standardized_waypoints = from_mod_handler.convert_from_mod_to_standard(
        world_name=from_mod_world_name
    )


    # from_mod -> std_world_wps - save to standard yaml file
    standard_file.write_waypoints(given_waypoints=standardized_waypoints)

    # to_mod - convert wps to std mop wp format,
    #          add wps to world in mod's files
    conversion_successful = to_mod_handler.convert_from_standard_to_mod(
        standard_data=standardized_waypoints,
        world_name=to_mod_world_name,
        testing=True
    )

    return conversion_successful


def get_world_info(mod_name : str, mod_world_name : str) -> tuple[str, bool]:
    """
    Gets the world name and type.

    Parameters
    ----------
    mod_name : str
        the name of the mod to use to get the data
    mod_world_name : str
        the name of the world to get the data of

    Returns
    -------
    tuple[str, str]
        the name of the world and the world type
    """

    world_name : str = None
    world_type : str = None

    match mod_name:
        
        case 'lunar client':
            world_name = LunarWaypointsHandler.parse_world_name(mod_world_name)
            world_type = LunarWaypointsHandler.get_world_type(mod_world_name)
            
        case 'xaero\'s minimap':
            world_name = XaerosWaypointsHandler.parse_world_name(mod_world_name)
            world_type = XaerosWaypointsHandler.get_world_type(mod_world_name)

    return world_name, world_type



########################################################################
#####                            Driver                            #####
########################################################################

def run_driver() -> None:

    # get world/server name
    world_name = get_world_name()

    # get convert from and to mod names
    from_mod, to_mod = get_mod_names(mod_options=(
        'lunar client',
        'xaero\'s minimap'
    ))

    # get file system names for world/server in both from and to mods
    world_name_in_from_mod = get_world_file_name(world_name, from_mod)
    world_name_in_to_mod   = get_world_file_name(world_name, to_mod)

    if not world_name_in_from_mod or not world_name_in_to_mod:
        print_script_message(
            f'Given world not in {from_mod}'
        ) if not world_name_in_from_mod \
        else print_script_message(
            f'Given world not in {to_mod}'
        )
        return

    # convert from to
    if convert_waypoints(
        from_mod=from_mod,
        from_mod_world_name=world_name_in_from_mod,
        to_mod=to_mod,
        to_mod_world_name=world_name_in_to_mod
    ):
        print_script_message('Conversion successful!')

    else:
        print_script_message('Conversion unsuccessful.')

    return



########################################################################
#####                            Main                              #####
########################################################################

def determine_options(number_max : int) -> int:

    if len(sys.argv) == 1:
        return 0

    elif len(sys.argv) == 2:

        try:
            option = int(sys.argv[1])
            if option < 1 or option > number_max:
                raise IndexError
            
            return option

        except ValueError:
            print('Given choice is not a number.\n')

        except IndexError:
            print('Given choice is not in the range of options.\n')

    else:
        print('Incorrect number of args')
        
    return -1


def main() -> None: 

    option = determine_options(6)

    if option == -1:
        return
    

    # default functionality of script
    if option == 0:
        run_driver()

        wps_lunar = MOD_CLASSES['lunar client']._get_world_waypoints(
            world_name="kidnamedsoub"
        )

        wps_xaeros = MOD_CLASSES['xaero\'s minimap']._get_world_waypoints(
            world_name="kidnamedsoub"
        )

        print('Separate lunar and xaeros lists')
        # for wp_name in wps_lunar.keys():
        #     print(wp_name)

        for dimension in wps_xaeros.keys():
            for wp in wps_xaeros[dimension].keys():
                print(wp)



    # get lunar wps file
    elif option == 1:
        MOD_CLASSES['lunar client'].print_waypoints()

        

    # get kidnamedsoub wps
    elif option == 2:
        wps_lunar = MOD_CLASSES['lunar client']._get_world_waypoints(
            world_name="kidnamedsoub"
        )

        wps_xaeros = MOD_CLASSES['xaero\'s minimap']._get_world_waypoints(
            world_name="kidnamedsoub"
        )

        print('Separate lunar and xaeros lists')
        for wp_name in wps_lunar.keys():
            print(wp_name)

        for dimension in wps_xaeros.keys():
            for wp in wps_xaeros[dimension].keys():
                print(wp)
        # print(
        #     json.dumps(
        #         wps, 
        #         indent=2
        #     )
        # )


    # choosing from multiple lunar worlds
    elif option == 3:
        print(
            MOD_CLASSES['lunar client']._get_specific_world_name(
                '2020'
            )
        )


    # xaeros
    elif option == 4:
        xaeros = MOD_CLASSES['xaero\'s minimap']
        print(
            json.dumps(
                xaeros._get_world_waypoints('soub'),
                indent=2
            )
        )


    elif option == 5:
        xaeros = MOD_CLASSES['xaero\'s minimap']
        print(
            json.dumps(
                xaeros.convert_from_mod_to_standard('soub'),
                indent=2
            )
        )


    elif option == 6:
        pass



    # TODO cmd line args for FROM TO formats
    # ex py ... .py lunar xaeros
    
    return



if __name__ == "__main__":
    main()