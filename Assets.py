import pygame
import numpy as np

def Initialize_Assets(): #Does what it says
    Terrain_List = Initialize_Terrain()
    Sprite_List = Initialise_Sprites()

    return(Terrain_List,Sprite_List)

def Initialize_Terrain(): # List Of Avalable Terrains And Their Values (Easily Expandable)
    Terrain_List = (
    {
        'Tag':0,
        'Name':'Water',
        'Color':(0,0,255),
        'Action':'Water'
    },
    {
        'Tag':1,
        'Name':'Desert',
        'Color':(235,204,52),
        'Action':'None'
    },
    {
        'Tag':2,
        'Name':'Plains',
        'Color':(0,150,0),
        'Action':'None'
    },
    {
        'Tag':3,
        'Name':'Forest',
        'Color':(0,100,0),
        'Action':'Wood'
    }
    )
    return(Terrain_List)

def Initialise_Sprites(): # List Of Avalable Building Sprites and their values (easily expandable)
    Sprite_List = (
    {
        'Tag':0,
        'Name':'Empty'
    },
    {
        'Tag':1,
        'Name':'House',
        'Symbol':'Ho',
        'Cost':(100,),
        'Materials':('Wood',)
    },
    {
        'Tag':2,
        'Name':'Forester',
        'Symbol':'Fo',
        'Cost':(100,),
        'Materials':('Wood',)
    },
    {
        'Tag':3,
        'Name':'Mine',
        'Symbol':'Mi',
        'Cost':(100),
        'Materials':('Wood',)
    },
    {
        'Tag':4,
        'Name':'Wall',
        'Symbol':'Wa',
        'Cost':(100,),
        'Materials':('Wood',)
    },
    {
        'Tag':5,
        'Name':'Crop',
        'Symbol':'Cr',
        'Cost':(100,),
        'Materials':('Wood',)
    },
    {
        'Tag':6,
        'Name':'Fishing',
        'Symbol':'Fi',
        'Cost':(100,),
        'Materials':('Wood',)
    },
    {
        'Tag':7,
        'Name':'Storage',
        'Symbol':'St',
        'Cost':(100,),
        'Materials':('Wood',)
    }
    )
    return(Sprite_List)


def Check_Terrain(Terrain_List,Level,x,y): #Actually Render Terrain
    Terrain = Terrain_List[int(Level)]
    return(Compile_Terrain(Terrain,x,y))


def Compile_Terrain(Terrain,x,y): #Compile Terrain Tile
    #Duplicate, Oops
    r = 30 # Tile Radius (height)
    rd2 = r/2 #Radius/2 just for optimization
    rf = (r*(np.sqrt(3)/2)) #Hexagon width radius
    Hex1 = [x,y-r]
    Hex2 = [x+rf,y-rd2]
    Hex3 = [x+rf,y+rd2]
    Hex4 = [x,y+r]
    Hex5 = [x-rf,y+rd2]
    Hex6 = [x-rf,y-rd2]
    Hex = (Hex1,Hex2,Hex3,Hex4,Hex5,Hex6)
    return(Terrain['Color'],Hex)


def Check_Sprite(Sprite_List,Level,x,y,Highlight=False): #Actually Render Sprite

    if Highlight == True:
        Color = 255,0,0
    else:
        Color = 255,255,255
    Sprite = Sprite_List[Level]
    return(Compile_sprite(Sprite,Color,x,y))

def Compile_sprite(Sprite,Color,x,y): #Compile Spite Info
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(Sprite['Symbol'], True, (0,0,0), Color)
    textRect = text.get_rect()
    textRect.center=(x,y)
    return(text,textRect)


def Asset_Action(Terrain_List,Sprite_List,UI,Terrain,Sprite,Modifiers='None'): #Does that it says
    Action1 = Terrain_List[int(Terrain)]['Action']
    if Action1 == 'Wood':
        UI.Move_Resources('Wood',1)
    elif Action1 == 'Water':
        UI.Move_Resources('Water',1)
    elif Action1 == 'Food':
        UI.Move_Resources('Food',1)
    elif Action1 == 'Stone':
        UI.Move_Resources('Stone',1)
