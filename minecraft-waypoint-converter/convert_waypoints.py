"""
Minecraft Waypoint Converter

Converts Minecraft waypoints between various mods. 

Dependencies:
* pyfilehandlers
* lunapyutils
* amulet_nbt
* argparse
"""
    
import os
from pathlib import Path

import argparse
from lunapyutils import (
    prompt_for_answer,
    print_script_message,
    select_list_options
)
from pyfilehandlers.file_handler import FileHandler

from waypoint_handlers.waypoint_mod_handler import WaypointModHandler
from waypoint_handlers.waypoint_handler_lunar import LunarWaypointHandler
from waypoint_handlers.waypoint_handler_xaeros import XaerosWaypointHandler
from waypoint_handlers.standard_world_waypoints import StandardWorldWaypoints


MOD_CLASSES : dict[str, WaypointModHandler] = {
    'lunar client'      : None,
    'xaero\'s minimap'  : None
}



########################################################################
#####                    Get World/Server Info                     #####
########################################################################

def get_world_name() -> str:
    """
    Prompts the user to enter the name of the world to get waypoints from.
    """

    return prompt_for_answer(
        'What is the name of the singleplayer world or multiplayer server IP?' \
        ' (Only part of the name is necessary,' \
        ' ex. "best" will find "best world")'
    )


def get_mod_names(mod_options : tuple[str]) -> tuple[str]:

    print_script_message('Select the mod to convert from: ')
    from_mod : str = mod_options[select_list_options(mod_options) - 1]

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

    from_mod_handler = MOD_CLASSES[from_mod]
    to_mod_handler = MOD_CLASSES[to_mod]

    create_backups(
        from_mod_handler=from_mod_handler,
        from_mod_world_name=from_mod_world_name,
        to_mod_handler=to_mod_handler,
        to_mod_world_name=to_mod_world_name
    )
    
    world_name, world_type = get_world_info(from_mod, from_mod_world_name)

    # TODO v2
    # get waypoints from both mods, combine into one dict, save this dict
    # to the standard yaml, then save to to_mod
    # rather than only converting the from_mod into the standard yaml
    

    # TODO v2 end

    standard_file = StandardWorldWaypoints(
        world_name=world_name,
        world_type=world_type,
        mod_name=from_mod
    )
    
    standardized_waypoints = from_mod_handler.convert_from_mod_to_standard(
        world_name=from_mod_world_name
    )

    standard_file.write_waypoints(given_waypoints=standardized_waypoints)

    to_mod_handler.create_backup(world_name=to_mod_world_name)

    conversion_successful = to_mod_handler.convert_from_standard_to_mod(
        standard_data=standardized_waypoints,
        world_name=to_mod_world_name
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
            world_name = LunarWaypointHandler.parse_world_name(mod_world_name)
            world_type = LunarWaypointHandler.get_world_type(mod_world_name)
            
        case 'xaero\'s minimap':
            world_name = XaerosWaypointHandler.parse_world_name(mod_world_name)
            world_type = XaerosWaypointHandler.get_world_type(mod_world_name)

    return world_name, world_type


def create_backups(
    from_mod_handler : WaypointModHandler,
    from_mod_world_name : str,
    to_mod_handler : WaypointModHandler,
    to_mod_world_name : str
) -> bool:
    """
    Creates backups of the waypoint files.

    Returns
    -------
    bool
        True,   if the backup creations were successful
        False,  otherwise
    """

    return  (from_mod_handler.create_backup(world_name=from_mod_world_name) 
    and     to_mod_handler.create_backup(world_name=to_mod_world_name))



########################################################################
#####                            Driver                            #####
########################################################################

def run_driver(convert_here : bool) -> None:
    """
    Runs the convertion functionality of the script.

    Parameters
    ----------
    convert_here : bool
        True,   if the user wishes to convert files within this dir
        False,  otherwise
    """

    from_mod, to_mod = get_mod_names(mod_options=(
        'lunar client',
        'xaero\'s minimap'
    ))

    # TODO v2 - user chooses from dropdown list, rather than getting the
    # name of the world, for each mod

    world_name = get_world_name()

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
    
    # TODO v2 end
    
    if convert_here:
        MOD_CLASSES[from_mod].convert_here()
        MOD_CLASSES[to_mod].convert_here()

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

def init_parser() -> argparse.Namespace:
    """
    Initializes the command line argument parser.

    Returns
    -------
    argparse.Namespace
        the argument parser object that has been instantiated
    """

    parser = argparse.ArgumentParser(
        description='Converts waypoints between Minecraft mods'
    )

    parser.add_argument(
        '--convert-here',
        action='store_true'
    ) 

    return parser.parse_args()
    

def setup_classes(convert_here : bool) -> None:

    if convert_here:

        dir_path = os.path.join(
            os.getcwd(),
            'minecraft-waypoint-converter',
            'data',
            'convert-here'
        )

        MOD_CLASSES['lunar client'] = LunarWaypointHandler(
            different_file_path=os.path.join(
                dir_path,
                'lunar client',
                'waypoints.json'
            )
        )
        MOD_CLASSES['xaero\'s minimap'] = XaerosWaypointHandler(
            different_directory_path=os.path.join(
                dir_path,
                'xaero\'s minimap'
            )
        )


def main() -> None:
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    args = init_parser()

    if args.convert_here:
        print_script_message('Running script using mode: convert-here')
    else:
        print_script_message('Running script using mode: standard')
        
    setup_classes(args.convert_here)

    # default functionality of script
    run_driver(args.convert_here)
    
    return



def testing():

    servers_file = FileHandler(
        Path(
            os.getenv('APPDATA'),
            '.minecraft',
            'servers.dat'
        )
    )

    data = servers_file.read()

    for server in data.tag['servers']:
        print(f'{server['name']} (ip: {server['ip']})')

    exit()



if __name__ == "__main__":

    testing()
    # main()