# Minecraft Waypoint Converter
Converts waypoints between various Minecraft waypoint mods. Given a mod to import from, and a mod to export to, waypoints from the former will be converted to the latter and added as new waypoints.



# Running the Script
0. Enusre you have Python installed on your machine
    * Windows tutorial: https://gist.github.com/danilo-montes/2a2239035e689dfeafa0b7a59fed8c60

1. Download the source files
    * Go to latest version in Releases
    * Download the zip file of the source code
    * Extract folder to desired location

2. Find extracted folder in File Explorer

3. Double click the folder, and copy the path to the folder from the bar

4. Open command prompt

5. Type the command `cd`, hit space, paste the path you just copied, and hit enter

6. Type the command `pipenv shell`

7. Type the command `py minecraft-waypoint-converter\convert-waypoints.py` (you can hit shift while typing to autofill)
    * For Unix-based systems, use `py minecraft-waypoint-converter/convert-waypoints.py`

8. You are now running the script!


# Usage
Once executing the run command, as described in step 7 above, the script will begin. Answer the questions as they appear.

`> What is the name of the singleplayer world or multiplayer server IP? (Only part of the name is necessary, ex. "best" will find "best world"):` \
Here, enter part of or the entire server name. Entering "my" will find worlds or servers like "my world", "friendsandmyserver.serverminer.com", and "crummycat.aternos.me". NOTE: in v1 of this script, you MUST have already created waypoints at least once before for the world/server. This is so that the files for those worlds can be created. This is set to change in the next version.

`> Select the mod to convert from:` \
Here, choose the mod that you want to export waypoints from.

`> Select the mod to convert to:` \
Here, choose the mod that you want to import waypoint to.

The script will continue and notify the user of any errors in running, or if the user needs to specify a world out of a few options. After converting, the script will notify the user if the conversion was fully successful.

## Command line arguments
The user might wish to copy their world's waypoint files into a separate location, so if anything goes wrong, the original data is not lost. They might also have someone else send their waypoint files to the user, who can then convert it using the script and send back the results. In this case, you can supply the optional argument `--convert-here` when running the script (run `py minecraft-waypoint-converter\convert-waypoints.py --convert-here`). This will make the script look into the `minecraft-waypoint-converter\data\convert-here` folder for the file(s) to convert, so create this folder and then put the necessary files or folders in there.

For example, Xaero's Minimap stores waypoints in a folder that has the name of the world or server in it, like `\.minecraft\XaeroWaypoints\Countries and Kingdoms`. You would copy the entire folder and paste the copy into `convert`, so the folder path would be `minecraft-waypoint-converter\data\convert-here\Countries and Kingdoms`. The finished conversion will also appear in `minecraft-waypoint-converter\data\convert-here`.

# Currently Supported Mods
- Xaero's Minimap
- Lunar Client Waypoints


## Mod Features

| Mod Features                           | Lunar Client | Xaero's Minimap |
| :------------------------------------- | :----------: | :-------------: |
| Name waypoint                          | ✓            | ✓              |
| Specify waypoint dimension             | ✓            | ✓              |
| Color waypoint                         | ✓            | ✓              |
| Toggle waypoint visibility             | ✓            | ✓              |
| Create waypoints with duplicate names* |              | ✓              |
| Show waypoint beam in game             | ✓            |                |
| Show waypoint text in game             | ✓            |                |

\* Note that despite support for waypoints with duplicate names, this tool skips any duplicate named waypoints to avoid undesirably duplicated waypoints when converting multiple times between the same two mods

# Planned Features
__v2__
- Additional world name choosing option: singleplayer worlds and multiplayer servers are polled and presented as options, so you don't have to have created waypoints for the files to exist

__v3__
- GUI to make use more user accessible