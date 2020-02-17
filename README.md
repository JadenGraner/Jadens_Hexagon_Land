#Jadens_Hexagon_Land
A simple early-stage game based around castles and monsters (monsters yet to come)
It uses Perlin Noise Terrain Generation for the map, and I created a chunk loading system to make the game run efficiently with large map sizes, and I really build the game to be very expandable, theoretically it would be relatively easy to mod in buildings, terrains, and resources

Chop down trees, build structures, grow a small village all in this amazing new game...

It's not really great because I've only been working on it for three days(and it's not done), but I should probably show my work some more so I thought I'd post it
I'd like to keep working on it and maybe turn it into a real game one day but we'll see how that goes

Requires Numpy, Pygame, Sys, And Noise

Simple Game rules:
Pressing enter in Forests gives you Wood, right now buildings only cost 100 Wood, Buildings require 1 Person to work them

Each Tick: People Require Houses,
1 Person: moves into 1 House,
Houses: require 1 Food and 1 Wood,
Foresters: require 1 Person, produce 2 Wood,
Crop require: 1 Person, Fields Produce 2 Food,
Mines require: 1 Person, Produce 1 Stone

Terrains Are:
Blue: Water
Yellow: Sand
Light Green: Plains
Dark Green: Forest


Controls are:
F       To focus the camera on the player
G       To lock the camera on the player
WASD    To move the camera around
B       To Toggle The Build Menu
Enter   To select a building in menu or run "action" on players current tile
←→     To Traverse the player left and Right
↑↓      In combination with ←→ To travel diagonally up and down (Sorry, I know it's horrible)
esc     To exit build window or the game

Building Codes are:
Ho	House. Each hold two people
Fo	Forester. Chops down trees
Mi	Mine. Mines Stone
Wa	Wall. Does nothing
Cr	Crop. Grows food
Fi	Fishing(hut?). Does nothing
St	Storage. Each hold 480 Resource of each type


JGraner Corporation 2020
