import numpy as np
import pygame
import sys
# import time

#My Modules:
import Terrain_Generation
import Assets

# Initialize Pygame
pygame.init()
Display_Width,Display_Height = 1280,720
cx,cy = Display_Width//2,Display_Height//2
screen = pygame.display.set_mode((Display_Width,Display_Height))
clock = pygame.time.Clock()


#Some World Parameters
Chunk_Size = 8
World_Border = 16

#Generate World Terrain Base
Chunk_List,Chunk_Check,Structures,Grid_Size,Chunk_Grid_Size = Terrain_Generation.Chunk_Initialize(Chunk_Size,World_Border)

#Generate Assets
Terrain_List,Sprite_List = Assets.Initialize_Assets()



# Tile Info
global r
r = 30 # Tile Radius (height)
rd2 = r/2 #Radius/2 just for optimization
r2 = r*2 # Diameter? (height)
rf = (r*(np.sqrt(3)/2)) #Hexagon width radius
rf2 = (r*(np.sqrt(3)/2))*2 #Hexagon Width Diameter
rf12 = (r*(np.sqrt(3)/2))/2 #Hexagon Quadrent (stupid)

Control_Mode = 'Move' #Move, Build, One Day: UI
Constant_Track = False #Constantly track Player?

#Simple Camera Class For Top Down View
class Camera:
    def __init__(self,pos=(0,0)):
        self.pos = list(pos)

    def Update (self,dt,Key):
        s = dt*400

        if Key[pygame.K_w]:
            self.pos[1] += s

        if Key[pygame.K_s]:
            self.pos[1] -= s

        if Key[pygame.K_a]:
            self.pos[0] += s

        if Key[pygame.K_d]:
            self.pos[0] -= s

#ThiS Class Contains Plater Data (most of which has been migrated Elsewhere or doesn't exist yet)
class Player:
    def __init__(self,pos=(0,0)):
        self.pos = list(pos)

    def Update (self,Key):


        #Annoying Six-Direction Movement System
        if self.pos[1]%2 == 0 :

            if Key[pygame.K_UP] and Key[pygame.K_RIGHT]:
                self.pos[1] -= 1

            elif Key[pygame.K_DOWN] and Key[pygame.K_LEFT]:
                self.pos[1] += 1
                self.pos[0] -= 1

            elif Key[pygame.K_UP] and Key[pygame.K_LEFT]:
                self.pos[1] -= 1
                self.pos[0] -= 1

            elif Key[pygame.K_DOWN] and Key[pygame.K_RIGHT]:
                self.pos[1] += 1

            elif Key[pygame.K_LEFT]:
             self.pos[0] -= 1

            elif Key[pygame.K_RIGHT]:
                self.pos[0] += 1

        elif self.pos[1]%2 == 1 :

            if Key[pygame.K_UP] and Key[pygame.K_RIGHT]:
                self.pos[1] -= 1
                self.pos[0] += 1

            elif Key[pygame.K_DOWN] and Key[pygame.K_LEFT]:
                self.pos[1] += 1

            elif Key[pygame.K_UP] and Key[pygame.K_LEFT]:
                self.pos[1] -= 1

            elif Key[pygame.K_DOWN] and Key[pygame.K_RIGHT]:
                self.pos[1] += 1
                self.pos[0] += 1

            elif Key[pygame.K_LEFT]:
             self.pos[0] -= 1

            elif Key[pygame.K_RIGHT]:
                self.pos[0] += 1


        #Check Position To Ensure plater is on the map
        if self.pos[0] < 0:
            self.pos[0] = 0

        if self.pos[0] > Grid_Size-1:
            self.pos[0] = Grid_Size-1

        if self.pos[1] < 0:
            self.pos[1] = 0

        if self.pos[1] > Grid_Size-1:
            self.pos[1] = Grid_Size-1

        global Terrain
        if Key[pygame.K_RETURN]: # When Action Button Is Pressed
            global Current_Chunk
            global Structures
            global Terrain_List
            global Sprite_List
            global UI
            Terrain = Get_Terrain(self.pos[0],self.pos[1],Current_Chunk) # Current Terrain of current chunk
            Structure = Structures[x,y] # Get Structure being stood on
            Assets.Asset_Action(Terrain_List,Sprite_List,UI,Terrain,Structures) # Run Action Checker

# This Class Contains The Code For Showing The Build Menue/Entering Build Mode
class Build_UI:
    def __init__(self,Highlighted=0):
        global Sprite_List
        self.Highlighted = Highlighted

    def Update(self,Key):
        global Sprite_List
        pygame.draw.polygon(screen,(255,255,255),( (Display_Width-50,Display_Height-50),(Display_Width-50,Display_Height),(50,Display_Height),(50,Display_Height-50) ), 0) #Starting top right

        #Highlight Selection
        if Key[pygame.K_LEFT]:
         self.Highlighted -= 1

        elif Key[pygame.K_RIGHT]:
            self.Highlighted += 1

        elif Key[pygame.K_UP]:
         self.Highlighted -= 1

        elif Key[pygame.K_DOWN]:
            self.Highlighted += 1

        #Make Sure Highlighted Object Actually Exists
        if self.Highlighted < 1:
            self.Highlighted = 1

        elif self.Highlighted > len(Sprite_List)-1:
            self.Highlighted = len(Sprite_List)-1

        # Attempt To Build
        if Key[pygame.K_RETURN]:
            if Structures[Play.pos[0],Play.pos[1]] == 0:

                Building = Sprite_List[self.Highlighted]

                # Check To See If Each Of The Resources That The Building Costs Can Be Afforded
                Afford_Needed = len(Building['Materials'])
                Afford = 0
                for i,Material in enumerate(Building['Materials']):
                    if UI.Resource_Name_Count(Material) >= Building['Cost'][i]:
                        Afford += 1
                # If All Resources Can Be Afforced Subtract Resources From Storage And Place Building
                if Afford_Needed == Afford:
                    for i,Material in enumerate(Building['Materials']):
                        if UI.Resource_Name_Count(Material) >= Building['Cost'][i]:
                            Structures[Play.pos[0],Play.pos[1]] += self.Highlighted
                            UI.Move_Resources(Material,-Building['Cost'][i])

        for i in range(1,len(Sprite_List)): #Render Sprites to select building to build
            if i == self.Highlighted:
                Highlight = True
            else:
                Highlight = False
            # print(Building_Sprite)
            x = 75+(i*50)
            y = Display_Height-25
            text,textRect = Assets.Check_Sprite(Sprite_List,i,x,y,Highlight)
            # text,textRect = Assets.Sprites(Building_Sprite,x,y,Highlight)
            screen.blit(text,textRect)


# This Class Contains The Current Number Of Resources And Displays Them In The Top Right Of The Screen
class Resourc_UI:
    def __init__(self,Resources=('Food','Water','Wood','Stone','People'),Resource_Count=(10,10,100,0,0),Base_Resource_Cap=120,Base_People_Cap=0):
        self.Resources = list(Resources)
        self.Resource_Count = list(Resource_Count)
        self.Resource_Cap = Base_Resource_Cap
        self.Base_Resource_Cap = Base_Resource_Cap
        self.People_Cap = Base_People_Cap
        self.Base_People_Cap = Base_People_Cap
        self.Busy_People = 0
    def Move_Resources(self,Type,Amount): # Change Resource Count By Type and Number
        if Type == 'Food':
            self.Resource_Count[0] += Amount
        elif Type == 'Water':
            self.Resource_Count[1] += Amount
        elif Type == 'Wood':
            self.Resource_Count[2] += Amount
        elif Type == 'Stone':
            self.Resource_Count[3] += Amount
    def Resource_Name_Count(self,Type): #Get Resource Count By Name, For Convenience
        if Type == 'Food':
            return(self.Resource_Count[0])
        elif Type == 'Water':
            return(self.Resource_Count[1])
        elif Type == 'Wood':
            return(self.Resource_Count[2])
        elif Type == 'Stone':
            return(self.Resource_Count[3])
        elif Type == 'People':
            return(self.Resource_Count[4])

    def Update(self): #Draw Resource Window
        pygame.draw.polygon(screen,(255,255,255),( (Display_Width,0),(Display_Width,100),(Display_Width-200,100),(Display_Width-200,0) ), 0) #Starting top right
        for i,Resource in enumerate(self.Resources):
            if (self.Resource_Count[i] > self.Resource_Cap) and i < 4:
                self.Resource_Count[i] = self.Resource_Cap
            elif (self.Resource_Count[i] > self.People_Cap) and i > 4:
                self.Resource_Count[i] = self.People_Cap

            x = Display_Width-100
            # y = 15+(i*25)
            y = (((100)/len(self.Resources))*i)+10
            if i < 4:
                Ending = '/'+str(self.Resource_Cap)
            else:
                Ending = '/'+str(self.People_Cap)+'('+str(self.Busy_People)+')'
            Full_Caption = str(Resource)+'='+str(self.Resource_Count[i])+Ending
            tempcolor = (255,255,255)
            font = pygame.font.Font('freesansbold.ttf', 16)
            text = font.render(Full_Caption, True, (0,0,0), tempcolor)
            textRect = text.get_rect()
            textRect.center=(x,y)
            screen.blit(text,textRect)

#This Class Runs Infrequent Updates So The Game Doesn't Run Too Slowly
#It Handles: Buildings Gathering Resources, Number Of People With Jobs, And Number Of Storage Buildings
class Infrequent_Updates:
    def __init__(self):
        self.Lazy_People = 0
        self.Busy_People = 0

    def Update(self): # Assigns People Jobs, Has Buildings Collect Materials, Checks Storage Buildings Of People and Resources
        self.Lazy_People = UI.Resource_Count[4]
        self.Busy_People = 0
        Storage = 0
        People_Cap = 0
        for x in range(Grid_Size):# Simple Check Structures, Check Resources, Check people, Do Action Loop
            for y in range(Grid_Size):
                if Structures[x,y] == 1:
                    if (UI.Resource_Name_Count('Wood') > 0) and (UI.Resource_Name_Count('Food') > 0):
                        UI.Move_Resources('Wood',-1)
                        UI.Move_Resources('Food',-1)
                        People_Cap += 1
                elif Structures[x,y] == 2:
                    if UI.Resource_Count[0] >= 1:
                        if self.Lazy_People > 0:
                            self.Lazy_People -= 1
                            self.Busy_People += 1
                            UI.Move_Resources('Wood',2)
                        # UI.Move_Resources('Food',-1)
                elif Structures[x,y] == 3:
                    if UI.Resource_Count[0] >= 1:
                        if self.Lazy_People > 0:
                            self.Lazy_People -= 1
                            self.Busy_People += 1
                            UI.Move_Resources('Stone',1)
                        # UI.Move_Resources('Food',-1)
                elif Structures[x,y] == 5:
                    if UI.Resource_Count[0] >= 1:
                        if self.Lazy_People > 0:
                            self.Lazy_People -= 1
                            self.Busy_People += 1
                            UI.Move_Resources('Food',2)
                elif Structures[x,y] == 7:
                    Storage += 1
        UI.Resource_Cap = UI.Base_Resource_Cap + (Storage*480) #Storage per Building
        UI.People_Cap = UI.Base_People_Cap + (People_Cap*2) #People per House
        UI.Busy_People = self.Busy_People
        if UI.People_Cap > UI.Resource_Count[4]: #Add Person To Town When Space Is Avalible
            UI.Resource_Count[4] += 1

#Camera Class
Cam = Camera((0,0))

#Player Class
Play = Player((0,0))

#Resource Window
UI = Resourc_UI()

#Build Window
Build = Build_UI()

#Infrequent Update Tracker
Infq = Infrequent_Updates()

def Switch_Mode(): #Switch From Building To playing (One day add main menue stuff)
    global Control_Mode
    if Control_Mode == 'Move':
        Control_Mode = 'Build'
    elif Control_Mode == 'Build':
        Control_Mode = 'Move'

def Tile_Distance(x,y): # Keeps Track Of Position Because of Hexagon Map
    if (y % 2 == 0):
        X = x*SIMPLEMISTERY1 +SIMPLEMISTERY2 #Simple Precalculated Numbers Used For FPS Efficiency
        Y = y*rf2+r
    else:
        X = x*SIMPLEMISTERY1 +SIMPLEMISTERY3 #Simple Precalculated Numbers Used For FPS Efficiency
        Y = y*rf2+r
    return(X,Y)

def Track_Player(x,y): # Does what It says doesn't it?
    X,Y = Tile_Distance(Play.pos[0],Play.pos[1])

    Cam.pos[0],Cam.pos[1] = -X+rf2+Display_Width//2,-Y+rf2+Display_Height//2

def Get_Terrain(x,y,chunk): #Get The Tile Being Stood On (Because Of The Chunk System)
    global Chunk_Size
    global Chunk_List
    Terrain = Chunk_List[x%Chunk_Size,y%Chunk_Size,chunk]
    return(Terrain)


def PlayerSprite(x,y): #Should Be Migrated To Assets
    pygame.draw.rect(screen,(255,0,255), ( x-rf12, y-rf12, rf12, rf12 ) )


#Precalculations For FPS Speedups:
SIMPLEMISTERY1 = rf2+5
SIMPLEMISTERY2 = rf-2
SIMPLEMISTERY3 = +rf*2

#Speed of Infrequent Updates
Tick_Speed = 10
Tick = 0

while True:
    Tick += 1
    for event in pygame.event.get():

        # UNIVERSAL KEY PRESSES
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if Control_Mode == 'Move':
                    pygame.quit()
                    sys.exit()

            if event.key == pygame.K_TAB: # DEBUG
                px,py = Play.pos[0],Play.pos[1]
                print('Terrain',Get_Terrain(px,py,Current_Chunk))
                print('Chunk Generated:',Chunk_Check[Current_Chunk])
                print('Structures',Structures[px,py])

            if event.key == pygame.K_b: # DEBUG
                Switch_Mode()

            if event.key == pygame.K_f: # DEBUG
                Track_Player(Play.pos[0],Play.pos[1])


            if event.key == pygame.K_g: # DEBUG
                Constant_Track = not Constant_Track

    dt = clock.tick()/1000
    pygame.display.set_caption('Hexagon_Land - FPS: %.2f'%clock.get_fps())

    screen.fill((0,0,0))


    #This Section Handles Chunks And Loads Tiles To The Screen
    def Singlify(x,y): #Flatten 2D Values
        Max_Width = 15 #16
        n = (y*Max_Width)+x+y
        return(n)

    def Doublify(n): #UnFlatten 2D Values
        Max_Width = 16
        y = n//Max_Width
        x = (n%Max_Width)
        # print('HOLDUP NIGGA')
        return(x,y)


    #Render Distance Stuff
    Render_Distance = 2 #1-12?
    Render_DistanceX = Render_Distance
    Render_DistanceY = Render_Distance//2

    # Current Whole Chunk
    Current_Chunk_X = Play.pos[0]//Chunk_Size
    Current_Chunk_Y = Play.pos[1]//Chunk_Size

    Current_Chunk = Singlify(Current_Chunk_X,Current_Chunk_Y)

    Render_List = [] # Empty list to be filled with chunks to be rendered

    #Position within current chunk
    Position_In_Chunk_X = Play.pos[0]%Chunk_Size
    Position_In_Chunk_Y = Play.pos[1]%Chunk_Size



    for x in range(-Render_DistanceX,Render_DistanceX+1): #New Render Distance Renderer (Rectangular)
        for y in range(-Render_DistanceY,Render_DistanceY+1):

            X,Y = Current_Chunk_X+x,Current_Chunk_Y+y
            if X >= 0 and X < World_Border:
                if Y >= 0 and Y < World_Border:
                    Render_List = np.append(Render_List, Singlify(X,Y))

    for Chunk in Render_List: #Generate Chunks That Are Trying To Be Displated But Arent' Populated Yet
        Chunk = int(Chunk)
        if Chunk_Check[Chunk] == False:
            Chunk_X,Chunk_Y = Doublify(Chunk)
            Chunk_List[:,:,Chunk] = Terrain_Generation.Generate_Chunk(Chunk_X,Chunk_Y,Chunk_Size)
            Chunk_Check[Chunk] = True

    for Chunk in Render_List:
        # print('DEBUG: CHUNK? :',Chunk)
        Chunk = int(Chunk)
        Chunk_Terrain = Chunk_List[:,:,Chunk]
        Current_Chunk_X,Current_Chunk_Y = Doublify(Chunk) #Convert singlet chunk into 2D object for next two lines
        for x in range(Chunk_Size*Current_Chunk_X, Chunk_Size*Current_Chunk_X+Chunk_Size): #Render at location of chunk from start of chunk to end
            for y in range(Chunk_Size*Current_Chunk_Y, Chunk_Size*Current_Chunk_Y+Chunk_Size): #Render at location of chunk from start of chunk to end

                In_Chunk_X,In_Chunk_Y = x%Chunk_Size,y%Chunk_Size

                X,Y = Tile_Distance(x,y) # Switch From Tile Count To Tile Pixel Location
                X,Y = X+Cam.pos[0],Y+Cam.pos[1] #Camera Movement

                Display_Buffer = rf2
                if (X<Display_Width+Display_Buffer and X>0-Display_Buffer and Y<Display_Height+Display_Buffer and Y>0-Display_Buffer): # Only Render Tiles on-screen

                    TColor,THex = Assets.Check_Terrain(Terrain_List,Chunk_Terrain[In_Chunk_X,In_Chunk_Y],X,Y) # Render Terrain Tiles
                    pygame.draw.polygon(screen,TColor,(THex), 0)


                    if Structures[x,y] > 0: # Render Structure Assets
                        text,textRect = Assets.Check_Sprite(Sprite_List,Structures[x,y],X,Y,False)
                        screen.blit(text,textRect)



                    if (Play.pos[0] == x and Play.pos[1] == y): #Render Player
                        PlayerSprite(X,Y)

    Key = pygame.key.get_pressed()

    #Send Key Inputs To Class In Speficied Mode
    if (Control_Mode == 'Build'):
        Build.Update(Key)
        if Key[pygame.K_ESCAPE]:
            Switch_Mode()
    elif (Control_Mode == 'Move'):
        Play.Update(Key)
        if Key[pygame.K_ESCAPE]:
            print('main menu, kj lol')
            # pygame.quit()
            # sys.exit()

    #Update UI
    UI.Update()

    #Update Screen
    pygame.display.flip()

    #Update Camera
    Cam.Update(dt,Key)

    #Update Infrequent Updates If Tick Is Correct
    if Tick%Tick_Speed == 0:
        Infq.Update()

    #Update Camera If Tracking Player
    if Constant_Track == True:
        Track_Player(Play.pos[0],Play.pos[1])
