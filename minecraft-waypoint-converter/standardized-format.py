from classes import *

import os, json
from pathlib import Path

########################################################################
#####                          Constants                           #####
########################################################################

HOME_DIR = Path.home()




def get_waypoints_lunar() -> None:
    file_path = os.path.join(
        HOME_DIR, 
        '.lunarclient', 
        'settings', 
        'game',
        'waypoints.json'
    )

    lunar_waypoints = WaypointsLunar(
        file_path=file_path, 
        extension=JSONFile
    )
    lunar_waypoints.print()
    


def get_waypoints_xaeros() -> None:
    file_path = os.path.join(
        HOME_DIR, 
        '.lunarclient', 
        'settings', 
        'game',
        'waypoints.json'
    )


def main() -> None:
    get_waypoints_lunar()



if __name__ == "__main__":
    main()