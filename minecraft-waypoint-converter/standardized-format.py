"""
Minecraft Waypoint Converter

Converts Minecraft waypoints between various mods. 

Dependencies:
* ruamel.yaml
"""


from classes import *

import os, json, sys
from pathlib import Path

########################################################################
#####                          Constants                           #####
########################################################################

HOME_DIR = Path.home()
APP_DATA = Path(os.getenv('APPDATA'))

LUNAR_FILE = LunarWaypointsHandler(
    file_path = os.path.join(
        HOME_DIR, 
        '.lunarclient', 
        'settings', 
        'game',
        'waypoints.json'
    )
) or None
# XAERO_DIR = 


########################################################################
#####                        Get Waypoints                         #####
########################################################################

def get_waypoints_lunar() -> None:

    LUNAR_FILE.print()

    '''
    Lunar Client waypoint file attributes

    - all waypoints in single file
    - JSON

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
            }
        }
    }
    
    world tags
        "sp:worldName" - singleplayer
        "mp:serverName" - multiplayer

    dimension tag (same for xaeros)
        -1 - nether
        0  - overworld
        1  - end
    '''
    


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
#####                         Conversion                           #####
########################################################################

def convert_waypoints(from_mod, to_mod, world_name):
    pass



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

    print_script_message('Select the mod to convert to: ')
    to_mod : str = mod_options[select_list_options(mod_options) - 1]

    return from_mod, to_mod
    

def verify_world_in_mod_dir(
        world_name : str, 
        mod_name : str,
    ) -> bool:
    """
    
    Parameters
    ----------

    Returns
    -------
    
    """

    # from mod_name, get proper directory/file


    # get list of world/server names in said location

    # iterate through and return true if world_name is found

    # return false, if world_name was not found
    pass



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

    option = determine_options(3)

    if option == -1:
        return
    
    # default, no args
    if option == 0:

        # get world/server name
        world_name = get_world_name()

        # get convert from and to mod names
        from_mod, to_mod = get_mod_names(mod_options=(
            'lunar client',
            'xaero\'s minimap'
        ))

        # verify world/server name in both from and to mods
        world_in_from_mod = verify_world_in_mod_dir(world_name, from_mod)
        world_in_to_mod   = verify_world_in_mod_dir(world_name, to_mod)

        if not world_in_from_mod or not world_in_to_mod:
            print(
                f'Given world not in {from_mod}'
            ) if not world_in_from_mod \
            else print(
                f'Given world not in {to_mod}'
            )

        # convert from to
        convert_waypoints(from_mod, to_mod, world_name)
        
        





    elif option == 1:
        get_waypoints_lunar()

    elif option == 2:
        print(
            json.dumps(
                LUNAR_FILE.get_world_waypoints(world_name="kidnamedsoub"), 
                indent=2
            )
        )

    elif option == 3:
        print(HOME_DIR)
        print(APP_DATA)
        get_waypoints_xaeros()


    # TODO cmd line args for FROM TO formats
    # ex py ... .py lunar xaeros

    

    return



if __name__ == "__main__":
    main()