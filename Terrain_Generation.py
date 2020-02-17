import numpy as np
import noise


def Chunk_Initialize(Chunk_Size,World_Border): #Start Chunk Terrain System
    #Create Important Values
    Full_Grid = Chunk_Size*World_Border
    Chunk_Grid_Size = World_Border*World_Border

    #Create Important Lists
    Structures = np.zeros((Full_Grid,Full_Grid),dtype=int) #Structures
    Chunk_List = np.zeros((Chunk_Size,Chunk_Size,Chunk_Grid_Size),dtype=float) #Chunks
    Chunk_Check = np.full((Chunk_Grid_Size),False,dtype=bool) #Chunk Generated Check

    #Populate First Chunk
    Chunk_List[:,:,0] = Generate_Chunk(0,0,Chunk_Size)
    Chunk_Check[0] = True

    return(Chunk_List,Chunk_Check,Structures,Full_Grid,Chunk_Grid_Size)


def Generate_Chunk(Chunk_X,Chunk_Y,Chunk_Size): #Generate Chunks

    #Create Empty Chunk
    Chunk = np.zeros((Chunk_Size,Chunk_Size),dtype=int) # 0=Water,1=Desert, 2=Plains, 3=Forest

    #Perlin noise Characteristics
    shape = (Chunk_Size,Chunk_Size)
    scale = 10.0
    octaves = 6 #Smoothness
    persistence = 0.5 #Scatteredness (dont change)
    lacunarity = 2.0 #Fractalness? (don't change)

    #Float Value Chunk For Generating int chunk values
    Grid = np.zeros(shape)

    #Unused, could change water Height  (Now thinking of riging ocean gameplay option)
    Threshold = 1

    for x in range(Chunk_Size*Chunk_X, Chunk_Size*Chunk_X+Chunk_Size): #Render at location of chunk from start of chunk to end
        for y in range(Chunk_Size*Chunk_Y, Chunk_Size*Chunk_Y+Chunk_Size): #Render at location of chunk from start of chunk to end
            #Chunk Scale XY Values
            X = x%Chunk_Size
            Y = y%Chunk_Size

            Grid[X,Y] = noise.pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=Chunk_Size, repeaty=Chunk_Size, base=0)

    #Converting Fload Grid To Chunk Terrain Values
    for x in range(Chunk_Size):
        for y in range(Chunk_Size):
            if (Grid[x,y] > Threshold*0.38):
                Chunk[x,y] = 3
            elif (Grid[x,y] > Threshold*0.3):
                Chunk[x,y] = 3
            elif (Grid[x,y] > Threshold*0.175):
                Chunk[x,y] = 2
            elif (Grid[x,y] > Threshold*0.1):
                Chunk[x,y] = 2
            elif (Grid[x,y] > Threshold*-0.05): #0.05
                Chunk[x,y] = 1

    return(Chunk)
