#Librarys
import time
import argparse
import random
import copy
import os.path
from os import path
from Tkinter import *

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class Puzzle(object):

    def __init__(self, filename):
        file = open(filename, 'r') 
        try:
            with open(filename , 'r') as f:
                first_line = f.readline()
                dimensions = map(int, first_line.strip().split(','))
                self.blocks = [[None for i in range(dimensions[0])] for j in range(dimensions[1])]
                self.edges_horizontal = [[False for i in range(dimensions[0]+1)] for j in range(dimensions[1]+1)]
                self.edges_vertical = [[False for i in range(dimensions[0]+1)] for j in range(dimensions[1]+1)]
                
                i = -1
                j = 0
                for line in f:
                    for c in line:
                        i = i+1
                        if c == '.':
                            continue
                        elif is_int(c):
                            self.blocks[j][i] = int(c)
                    i = -1
                    j = j+1
        except:
            print('Puzzle File Incorrectly Formatted')
            exit()
    
    def checkPointsEdges(self, i, j):
        drawnLines = [None] * 4

        if i-1 >= 0:
            drawnLines[0] = self.edges_vertical[i-1][j]
        if i+1 <= GRID_NUMBER_X:
            drawnLines[1] = self.edges_vertical[i][j]
        if j-1 >= 0:
            drawnLines[2] = self.edges_horizontal[i][j-1]
        if j+1 <= GRID_NUMBER_Y:
            drawnLines[3] = self.edges_horizontal[i][j]

        return drawnLines.count(True)

    def checkBoxEdges(self, i, j):
        edgesDrawn = 0

        if self.edges_horizontal[i][j]:
            edgesDrawn = edgesDrawn + 1
        if self.edges_horizontal[i+1][j]:
            edgesDrawn = edgesDrawn + 1
        if self.edges_vertical[i][j]:
            edgesDrawn = edgesDrawn + 1
        if self.edges_vertical[i][j+1]:
            edgesDrawn = edgesDrawn + 1
        
        return edgesDrawn

    def checkBoxComplete(self, i, j):
        if self.blocks[i][j] == None:
            return False
        return self.blocks[i][j] <= self.checkBoxEdges(i, j)

class DrawPuzzle(object):
    
    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=CANVAS_SIZE_X, height = CANVAS_SIZE_Y)
        self.canvas.pack()
        for i in range(0, GRID_NUMBER_Y+1):
            for j in range(0, GRID_NUMBER_X+1):
                xCoord = CANVAS_BOUNDARY_SIZE + j*CANVAS_BLOCK_SIZE
                yCoord = CANVAS_BOUNDARY_SIZE + i*CANVAS_BLOCK_SIZE
                self.canvas.create_oval(xCoord, yCoord, xCoord+CIRCLE_SIZE, yCoord+CIRCLE_SIZE, fill="black")

                #Draws numbers in (about) middle of block if number exists
                if j < GRID_NUMBER_X and i < GRID_NUMBER_Y and blocks[i][j] != None:
                    self.canvas.create_text(xCoord+CANVAS_BLOCK_SIZE/1.75, yCoord+CANVAS_BLOCK_SIZE/1.75, text=str(blocks[i][j]))
        
        self.canvas.update()
        time.sleep(0.5)
        self.drawBasics()

    def drawEdge(self, iOld, jOld, iNew, jNew):

        #Moving horizontal
        if iOld == iNew:
            xCoord = CANVAS_BOUNDARY_SIZE + jOld*CANVAS_BLOCK_SIZE + CIRCLE_SIZE/2 + LINE_SIZE/2
            yCoord = CANVAS_BOUNDARY_SIZE + iOld*CANVAS_BLOCK_SIZE + CIRCLE_SIZE/2 + LINE_SIZE/2

            if jOld < jNew:
                self.canvas.create_line(xCoord, yCoord, xCoord+CANVAS_BLOCK_SIZE, yCoord, width=LINE_SIZE, fill="red")
            elif jOld > jNew:
                self.canvas.create_line(xCoord-CANVAS_BLOCK_SIZE, yCoord, xCoord, yCoord, width=LINE_SIZE, fill="red")

        #Moving vertical
        elif jOld == jNew:
            xCoord = CANVAS_BOUNDARY_SIZE + jOld*CANVAS_BLOCK_SIZE + CIRCLE_SIZE/2 + LINE_SIZE/2
            yCoord = CANVAS_BOUNDARY_SIZE + iOld*CANVAS_BLOCK_SIZE + CIRCLE_SIZE/2 + LINE_SIZE/2
            
            if iOld < iNew:
                self.canvas.create_line(xCoord, yCoord, xCoord, yCoord+CANVAS_BLOCK_SIZE, width=LINE_SIZE, fill="red")
            elif iOld > iNew:
                self.canvas.create_line(xCoord, yCoord-CANVAS_BLOCK_SIZE, xCoord, yCoord, width=LINE_SIZE, fill="red")

    def drawEdges(self):

        for i in range(len(edges_horizontal)):
            for j in range(len(edges_horizontal[i])):
                if edges_horizontal[i][j]:
                    xCoord = CANVAS_BOUNDARY_SIZE + j*CANVAS_BLOCK_SIZE + CIRCLE_SIZE/2 + LINE_SIZE/2
                    yCoord = CANVAS_BOUNDARY_SIZE + i*CANVAS_BLOCK_SIZE + CIRCLE_SIZE/2 + LINE_SIZE/2
                    self.canvas.create_line(xCoord, yCoord, xCoord+CANVAS_BLOCK_SIZE, yCoord, width=LINE_SIZE)

        for i in range(len(edges_vertical)):
            for j in range(len(edges_vertical[i])):
                if edges_vertical[i][j]:
                    xCoord = CANVAS_BOUNDARY_SIZE + j*CANVAS_BLOCK_SIZE + CIRCLE_SIZE/2 + LINE_SIZE/2
                    yCoord = CANVAS_BOUNDARY_SIZE + i*CANVAS_BLOCK_SIZE + CIRCLE_SIZE/2 + LINE_SIZE/2
                    self.canvas.create_line(xCoord, yCoord, xCoord, yCoord+CANVAS_BLOCK_SIZE, width=LINE_SIZE)
        
        self.canvas.update()

    def drawBasics(self):
        for i in range(0, GRID_NUMBER_Y):
            for j in range(0, GRID_NUMBER_X):

                #Can add logic for 2s if need be later
                if blocks[i][j] == 3:

                    #Check for 0,3 in cardinal direction to 3
                    if i-1 >= 0:
                        self.checkCardinal3(i, j, blocks[i-1][j], horizontalEdges = True, checkForward = False)

                    if i+1 < GRID_NUMBER_X:
                        self.checkCardinal3(i, j, blocks[i+1][j], horizontalEdges = True, checkForward = True)

                    if j-1 >= 0:
                        self.checkCardinal3(i, j, blocks[i][j-1], horizontalEdges = False, checkForward = False)

                    if j+1 < GRID_NUMBER_Y:
                        self.checkCardinal3(i, j, blocks[i][j+1], horizontalEdges = False, checkForward = True)

                    #Check for 0,3 diagonal to 3
                    if i-1 >= 0 and j-1 >= 0:
                        if blocks[i-1][j-1] == 0:
                            edges_horizontal[i][j] = True
                            edges_vertical[i][j] = True
                        if blocks[i-1][j-1] == 3:
                            edges_horizontal[i+1][j] = True
                            edges_vertical[i][j+1] = True

                    if i-1 >= 0 and j+1 < GRID_NUMBER_Y:
                        if blocks[i-1][j+1] == 0:
                            edges_horizontal[i][j] = True
                            edges_vertical[i][j+1] = True
                        if blocks[i-1][j+1] == 3:
                            edges_horizontal[i+1][j] = True
                            edges_vertical[i][j] = True

                    if i+1 < GRID_NUMBER_X and j-1 >= 0:
                        if blocks[i+1][j-1] == 0:
                            edges_horizontal[i+1][j] = True
                            edges_vertical[i][j] = True
                        if blocks[i+1][j-1] == 3:
                            edges_horizontal[i][j] = True
                            edges_vertical[i][j+1] = True

                    if i+1 < GRID_NUMBER_X and j+1 < GRID_NUMBER_Y:
                        if blocks[i+1][j+1] == 0:
                            edges_horizontal[i+1][j] = True
                            edges_vertical[i][j+1] = True
                        if blocks[i+1][j+1] == 3:
                            edges_horizontal[i][j] = True
                            edges_vertical[i][j] = True

        self.drawEdges()

    def checkCardinal3(self, i, j, otherBox, horizontalEdges, checkForward = True):

        if otherBox == 0:

            if horizontalEdges:
                edges_vertical[i][j] = True
                edges_vertical[i][j+1] = True

                i1 = i if checkForward else i+1
                i2 = i+1 if checkForward else i

                edges_horizontal[i1][j] = True
                edges_horizontal[i2][j-1] = True
                edges_horizontal[i2][j+1] = True
                
            else:
                edges_horizontal[i][j] = True
                edges_horizontal[i+1][j] = True

                j1 = j if checkForward else j+1
                j2 = j+1 if checkForward else j

                edges_vertical[i][j1] = True
                edges_vertical[i-1][j2] = True
                edges_vertical[i+1][j2] = True

        elif otherBox == 3:

            if horizontalEdges:
                edges_horizontal[i][j] = True
                edges_horizontal[i+1][j] = True
            else:
                edges_vertical[i][j] = True
                edges_vertical[i][j+1] = True

class Ants(object):

    def __init__(self, puzzle, puzzleDisplay):

        self.startingPoints = []
        self.puzzle = puzzle
        self.puzzleDisplay = puzzleDisplay

        for i in range(0, GRID_NUMBER_Y+1):
            for j in range(0, GRID_NUMBER_X+1):

                if self.puzzle.checkPointsEdges(i, j) == 1:
                    self.startingPoints.append([i,j])
                    xCoord = CANVAS_BOUNDARY_SIZE + j*CANVAS_BLOCK_SIZE -1.5
                    yCoord = CANVAS_BOUNDARY_SIZE + i*CANVAS_BLOCK_SIZE -1.5
                    self.puzzleDisplay.canvas.create_oval(xCoord, yCoord, xCoord+CIRCLE_SIZE+3, yCoord+CIRCLE_SIZE+3, fill="red", outline="")
        
        #print(self.startingPoints)
        self.puzzleDisplay.canvas.update()  

    def findPath(self):  
        randomNum = random.randint(0, len(self.startingPoints)-1)
        randomStartingPoint = self.startingPoints[randomNum]
        iStart = randomStartingPoint[0]
        jStart = randomStartingPoint[1]
        iCur = iStart
        jCur = jStart
        firstIteration = True

        ant_puzzle = self.puzzle
        ant_edges_horizontal = self.puzzle.edges_horizontal
        ant_edges_vertical = self.puzzle.edges_vertical

        while True:
        
            #print(str(iCur)+","+str(jCur))
            validMoves = []

            #Check valid moves
            if (iCur-1 >= 0 
            and not ant_edges_vertical[iCur-1][jCur]
            and ant_puzzle.checkPointsEdges(iCur-1, jCur) < 2
            and (iCur-1 < 0 or jCur-1 < 0 or not ant_puzzle.checkBoxComplete(iCur-1, jCur-1))
            and (iCur-1 < 0  or jCur+1 > GRID_NUMBER_Y or not ant_puzzle.checkBoxComplete(iCur-1, jCur))):
                validMoves.append([iCur-1, jCur])
                
            if (iCur+1 <= GRID_NUMBER_X 
            and not ant_edges_vertical[iCur][jCur]
            and ant_puzzle.checkPointsEdges(iCur+1, jCur) < 2
            and (iCur+1 > GRID_NUMBER_X or jCur-1 < 0 or not ant_puzzle.checkBoxComplete(iCur, jCur-1))
            and (iCur+1 > GRID_NUMBER_X or jCur+1 > GRID_NUMBER_Y or not ant_puzzle.checkBoxComplete(iCur, jCur))):
                validMoves.append([iCur+1, jCur])

            if (jCur-1 >= 0
            and not ant_edges_horizontal[iCur][jCur-1]
            and ant_puzzle.checkPointsEdges(iCur, jCur-1) < 2
            and (iCur-1 < 0 or jCur-1 < 0 or not ant_puzzle.checkBoxComplete(iCur-1, jCur-1))
            and (iCur+1 > GRID_NUMBER_X or jCur-1 < 0 or not ant_puzzle.checkBoxComplete(iCur, jCur-1))):
                validMoves.append([iCur, jCur-1])

            if (jCur+1 <= GRID_NUMBER_Y 
            and not ant_edges_horizontal[iCur][jCur]
            and ant_puzzle.checkPointsEdges(iCur, jCur+1) < 2
            and (iCur-1 < 0  or jCur+1 > GRID_NUMBER_Y or not ant_puzzle.checkBoxComplete(iCur-1, jCur))
            and (iCur+1 > GRID_NUMBER_X or jCur+1 > GRID_NUMBER_Y or not ant_puzzle.checkBoxComplete(iCur, jCur))):
                validMoves.append([iCur, jCur+1])

            if (iCur == iStart and jCur == jStart and not firstIteration) or len(validMoves) == 0:
                #print("NO VALID MOVES END ANT")
                break

            randomNum = random.randint(0, len(validMoves)-1)
            randomValidMove = validMoves[randomNum]
            #print(validMoves)
            iNew = randomValidMove[0]
            jNew = randomValidMove[1]

            #Moving horizontal
            if iCur == iNew:
                if jCur < jNew:
                    ant_edges_horizontal[iCur][jCur] = True
                elif jCur > jNew:
                    ant_edges_horizontal[iNew][jNew] = True

            #Moving vertical
            elif jCur == jNew:
                if iCur < iNew:
                    ant_edges_vertical[iCur][jCur] = True
                elif iCur > iNew:
                    ant_edges_vertical[iNew][jNew] = True

            self.puzzleDisplay.drawEdge(iCur, jCur, iNew, jNew)

            #Move along already drawn lines
            while (ant_puzzle.checkPointsEdges(iNew, jNew) == 2 
            and not (iNew == iStart and jNew == jStart)):

                #print(str(iCur)+","+str(jCur))

                if (iNew-1 >= 0 
                and iNew-1 != iCur 
                and ant_edges_vertical[iNew-1][jNew]):
                    iCur = iNew
                    jCur = jNew
                    iNew = iNew-1
                    continue

                if (iNew+1 <= GRID_NUMBER_X 
                and iNew+1 != iCur
                and ant_edges_vertical[iNew][jNew]):
                    iCur = iNew
                    jCur = jNew
                    iNew = iNew+1
                    continue
                    
                if (jNew-1 >= 0 
                and jNew-1 != jCur
                and ant_edges_horizontal[iNew][jNew-1]):
                    iCur = iNew
                    jCur = jNew
                    jNew = jNew-1
                    continue

                if (jNew+1 <= GRID_NUMBER_Y 
                and jNew+1 != jCur
                and ant_edges_horizontal[iNew][jNew]):
                    iCur = iNew
                    jCur = jNew
                    jNew = jNew+1
                    continue

            iCur = iNew
            jCur = jNew
            firstIteration = False

        totalEdges = 0
        for edges in ant_edges_horizontal:
            totalEdges += edges.count(True)
        for edges in ant_edges_vertical:
            totalEdges += edges.count(True)
        return [totalEdges, ant_puzzle]

#Global Graphic Sizes
CANVAS_BLOCK_SIZE = 60
CIRCLE_SIZE = 5
LINE_SIZE = 2
CANVAS_BOUNDARY_SIZE = 5

#Arguement Parser, requires a filename for puzzle
parser = argparse.ArgumentParser(description='Solve a Loops Puzzle')
parser.add_argument('filename', help='name of puzzle file required to solve')
args = parser.parse_args()

#Generates puzzle from file
FILE_NAME = args.filename
if not path.exists(FILE_NAME):
    print('File not found')
    exit()
puzzle = Puzzle(FILE_NAME)

blocks = puzzle.blocks
edges_horizontal = puzzle.edges_horizontal
edges_vertical = puzzle.edges_vertical

#TODO: CLEAN UP THIS SECTION SO THAT PUZZLE CREATED IS GETTING PASSED INTO PUZZLE DISPLAY
GRID_NUMBER_Y = len(blocks)
GRID_NUMBER_X = len(blocks[0])
CANVAS_SIZE_X = CANVAS_BOUNDARY_SIZE*2 + CANVAS_BLOCK_SIZE*GRID_NUMBER_X
CANVAS_SIZE_Y = CANVAS_BOUNDARY_SIZE*2 + CANVAS_BLOCK_SIZE*GRID_NUMBER_Y

#Draw Puzzle
puzzleDisplay = DrawPuzzle()  
firstAnts = Ants(puzzle, puzzleDisplay)

path = firstAnts.findPath()
# print(path)
# puzzleDisplay.drawEdges(path[1].edges_horizontal, path[1].edges_vertical)

puzzleDisplay.root.mainloop()

#Pseduo code for ACO
"""
board = initialiseBoard(file_name)
board.basicMoves()

while iter < MAX_ITERATION or not bestSolution.complete
    for ant in ants
        ant.findRoute()
    for ant in ants
        if ant.route.complete
            break
        else if ant.route.fitness > max_fitness
            bestRoute = ant.route
            maxFitness = ant.route.fitness
    board.updatePheromones(ants.route)
"""