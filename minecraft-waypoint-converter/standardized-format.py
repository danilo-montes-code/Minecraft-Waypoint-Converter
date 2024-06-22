from classes import *

import os, json
from pathlib import Path

########################################################################
#####                          Constants                           #####
########################################################################

HOME_DIR = Path.home()
APP_DATA = Path(os.getenv('APPDATA'))



########################################################################
#####                        Get Waypoints                         #####
########################################################################

def get_waypoints_lunar() -> None:

    waypoint_file_path = os.path.join(
        HOME_DIR, 
        '.lunarclient', 
        'settings', 
        'game',
        'waypoints.json'
    )

    lunar_waypoints = WaypointsLunar(
        file_path=waypoint_file_path
    )
    lunar_waypoints.print()
    


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

        print('> Multiple servers were found that include the given name.')
        print('> Please select the number of the desired server.')

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
        print(f'> No servers with the name "{server_name}" were found.')
        print('> Please enter a valid server name\n')

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
#####                            Main                              #####
########################################################################

def main() -> None: 
    print(HOME_DIR)
    print(APP_DATA)
    get_waypoints_lunar()
    get_waypoints_xaeros()



if __name__ == "__main__":
    main()