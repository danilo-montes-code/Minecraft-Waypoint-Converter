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

    lunar_waypoints_file = FileHandler.existing_file(file_path, JSONFile)
    lunar_waypoints : dict = lunar_waypoints_file.read()
    print(json.dumps(lunar_waypoints, indent=2))
    



def main() -> None:
    get_waypoints_lunar()



if __name__ == "__main__":
    main()