import copy

POSSIBLE_DIMENSIONS = [(0,-1),(0,1),(1,0),(-1,0)]
class ShortestPath:
    class Path:
        def __init__(self, steps):
            self.steps = steps

    def __init__(self, board):
        self.board = board

    def start(self):
        self.paths = []
        self.paths.append(ShortestPath.Path([self.board.start]))

    def finish(self, path):
        for x,y in path.steps:
            self.board.setFrame(x,y,5)

    def tick(self):
        newPaths = []
        for path in self.paths:
            newStep = []
            rebranchNeeded = False
            lastX, lastY = path.steps[-1]
            for nextX, nextY in POSSIBLE_DIMENSIONS:
                if self.board.target == (lastX + nextX, lastY + nextY):
                    path.steps.append((lastX + nextX, lastY + nextY))
                    self.finish(path)
                    return True

                if not self.board.frames[lastX + nextX][lastY + nextY].isBlockade and not self.board.frames[lastX + nextX][lastY + nextY].touched:
                    self.board.setFrame(lastX + nextX, lastY + nextY, 4)
                    inBoard = 0 < lastX + nextX and 0 < lastY + nextY and len(self.board.frames)-1 > lastX + nextX and len(self.board.frames[len(self.board.frames)-1])-1 > lastY + nextY
                    if inBoard:
                        if rebranchNeeded:
                            newPath = ShortestPath.Path(copy.deepcopy(path.steps))
                            newPath.steps.append((lastX + nextX, lastY + nextY))
                            newPaths.append(newPath)
                        else:
                            rebranchNeeded = True
                            newStep = (lastX + nextX, lastY + nextY)
            if newStep:
                path.steps.append(newStep)
        self.paths = self.paths + newPaths
        return False




