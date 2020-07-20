import pygame
import shortestPathAlgorythm as alg
import time
class Frame(pygame.Rect):
    def __init__(self, x, y, blockWidth, color):
        pygame.Rect.__init__(self, x, y, blockWidth, blockWidth)
        self.isBlockade = False
        self.touched = False
        self.color = color

class Board:
    untouchedColor = (80,80,80)
    touchedColor = (170,170,170)
    startColor = (255,20,20)
    targetColor = (20,255,20)
    blockadeColor = (255,255,160)
    shortestWayColor = (130,255,130)

    def __init__(self, xSize, ySize, blockWidth, screen):
        self.start = (0, 0)
        self.target = (0, 0)
        self.framesToUpdate = []
        self.screen = screen
        self.frames = self.buildFrames(xSize, ySize, blockWidth)
        self.frameWidth = blockWidth

    def buildFrames(self, xSize, ySize, blockWidth):
        frames = []
        for x in range(0, xSize, blockWidth):
            row = []
            for y in range(0, ySize, blockWidth):
                self.framesToUpdate.append((int(x/blockWidth), int(y/blockWidth)))
                row.append(Frame(x, y, blockWidth, Board.untouchedColor))
            frames.append(row)
        return frames

    def getFrames(self):
        return self.frames

    def update(self):
        for x, y in self.framesToUpdate:
            pygame.draw.rect(screen, self.frames[x][y].color, self.frames[x][y])
        self.framesToUpdate.clear()

    def setFrame(self, x, y, type):

        if type == 1:
            self.frames[x][y].color = Board.blockadeColor
            self.frames[x][y].isBlockade = True
        elif type == 2:
            self.addTarget(x,y)
        elif type == 3:
            self.addStart(x,y)
        elif type == 4:
            self.touch(x,y)
        elif type == 5:
            self.frames[x][y].color = Board.shortestWayColor

        self.framesToUpdate.append((x,y))

    def addTarget(self, x, y):
        self.framesToUpdate.append((self.target[0], self.target[1]))
        self.frames[self.target[0]][self.target[1]].color = Board.untouchedColor
        self.target = (x,y)
        self.frames[x][y].color = Board.targetColor

    def addStart(self, x, y):
        self.framesToUpdate.append((self.start[0], self.start[1]))
        self.frames[self.start[0]][self.start[1]].color = Board.untouchedColor
        self.start = (x,y)
        self.frames[x][y].color = Board.startColor

    def touch(self, x, y):
        self.frames[x][y].color = Board.touchedColor
        self.frames[x][y].touched = True

    def convertToX(self, pos):
        x = int(pos[0]/self.frameWidth)
        return x
    def convertToY(self, pos):
        y = int(pos[1]/self.frameWidth)
        return y

def handleLeftClick(pos, board, frameWidth):
   board.setFrame(board.convertToX(pos), board.convertToY(pos), 1)

def handleRightClick(pos, board, frameWidth):
   board.setFrame(board.convertToX(pos), board.convertToY(pos),2)

def handleMiddleClick(pos, board, frameWidth):
   board.setFrame(board.convertToX(pos), board.convertToY(pos),3)


X_SIZE = 1280
Y_SIZE = 800
BLOCK_SIZE = 16

pygame.init()
screen = pygame.display.set_mode((X_SIZE, Y_SIZE))

board = Board(X_SIZE, Y_SIZE, BLOCK_SIZE, screen)
shortestPath = alg.ShortestPath(board)
calculate = False
calculated = False

while True:
    if pygame.mouse.get_pressed()[0]:
        handleLeftClick(pygame.mouse.get_pos(), board, BLOCK_SIZE)
    if pygame.mouse.get_pressed()[1]:
        handleMiddleClick(pygame.mouse.get_pos(), board, BLOCK_SIZE)
    if pygame.mouse.get_pressed()[2]:
        handleRightClick(pygame.mouse.get_pos(), board, BLOCK_SIZE)

    if calculate and not calculated:
            calculated = shortestPath.tick()
            time.sleep(0.1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == ord(" "):
                shortestPath.start()
                calculate = True



    board.update()
    pygame.display.update()

