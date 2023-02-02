from OpenGL.GL import *

class Cell():
    def __init__(self, *args):
        self.id = args[0]
        self.point = args[1]
        self.state = 'Free'
        self.h = 0
        self.g = 0
        self.d = 0
        self.idf = 0
        self.ids = []
        
    def IsInsideObstacle(self, obstacle):
        hInters = 0
        vInters = 0
        point1 = [min([vertex[0] for vertex in obstacle]), min([vertex[1] for vertex in obstacle])]
        point2 = [max([vertex[0] for vertex in obstacle]), max([vertex[1] for vertex in obstacle])]
        if not (point1[1] <= self.point[1] <= point2[1]) and not (point1[0] <= self.point[0] <= point2[0]): return False
        for i in range(len(obstacle)):
            point1 = obstacle[i]
            point2 = obstacle[(i + 1) if (i + 1) < len(obstacle) else 0]
            if not (min([point1[1],point2[1]]) <= self.point[1] <= max([point1[1],point2[1]])) and \
               not (min([point1[0],point2[0]]) <= self.point[0] <= max([point1[0],point2[0]])): continue 
            if point2[0] == point1[0]:
                if (point1[1] < self.point[1] <= point2[1] or point2[1] < self.point[1] <= point1[1]) and point2[0] > self.point[0]: hInters += 1
            elif point2[1] == point1[1]:
                if (point1[0] < self.point[0] <= point2[0] or point2[0] < self.point[0] <= point1[0]) and point2[1] > self.point[1]: vInters += 1
            else:
                y = point1[1] + ((point2[1] - point1[1])/(point2[0] - point1[0]))*(self.point[0] - point1[0])
                if (point1[1] < y <= point2[1] or point2[1] < y <= point1[1]) and y > self.point[1]: vInters += 1
                x = point1[0] + ((point2[0] - point1[0])/(point2[1] - point1[1]))*(self.point[1] - point1[1])
                if (point1[0] < x <= point2[0] or point2[0] < x <= point1[0]) and x > self.point[0]: hInters += 1
        return False if (vInters % 2) == 0 and (hInters % 2) == 0 else True
    
    def Draw(self, color, delta):
        glBegin(GL_QUADS)
        glColor3fv(color)
        glVertex3f(self.point[0] + delta, self.point[1] + delta, 0.0)
        glVertex3f(self.point[0] - delta, self.point[1] + delta, 0.0)
        glVertex3f(self.point[0] - delta, self.point[1] - delta, 0.0)
        glVertex3f(self.point[0] + delta, self.point[1] - delta, 0.0)
        glEnd()

class OccupancyGrid():
    def __init__(self, *args):
        map = args[0]
        self.__minPoint = (map.MinX, map.MinY)
        self.__maxPoint = (map.MaxX, map.MaxY)
        self.__cells = []
        self.__startID = 0
        self.__goalID = 0
        self.__delta = args[1]
        self.__solution = []
        self.__visited = []
        self.__possible = []
        self.__nCols = int((self.__maxPoint[0] - self.__minPoint[0])/self.__delta[0])
        point = [self.__minPoint[0] + self.__delta[0]/2,
                 self.__minPoint[1] + self.__delta[1]/2]
        cellID = 0
        while(point[1] <= (self.__maxPoint[1] - self.__delta[1]/2)):
            while(point[0] <= (self.__maxPoint[0] - self.__delta[0]/2)):
                self.__cells.append(Cell(cellID, (point[0], point[1])))
                cellID += 1
                point[0] += self.__delta[0]
            point = [self.__minPoint[0] + self.__delta[0]/2,
                     point[1] + self.__delta[1]]
        self.UpdateCellsState(map)
        self.CellsConnections()

    def UpdateCellsState(self, map):
        for cell in self.__cells:
            for obstacle in map.Obstacles:
                if cell.IsInsideObstacle(obstacle):
                    cell.state = 'Obstacle'
                    break
                
    def CellsConnections(self):
        for cell in self.__cells:
            if (cell.id == 0):
                cell.ids.append(cell.id + 1)
                cell.ids.append(cell.id + self.__nCols)
                cell.ids.append(cell.id + self.__nCols + 1)
            elif (cell.id == self.__nCols - 1):
                cell.ids.append(cell.id - 1)
                cell.ids.append(cell.id + self.__nCols - 1)
                cell.ids.append(cell.id + self.__nCols)
            elif (cell.id == len(self.__cells) - self.__nCols):
                cell.ids.append(cell.id - self.__nCols)
                cell.ids.append(cell.id - self.__nCols + 1)
                cell.ids.append(cell.id + 1)
            elif (cell.id == len(self.__cells) - 1):
                cell.ids.append(cell.id - self.__nCols - 1)
                cell.ids.append(cell.id - self.__nCols)
                cell.ids.append(cell.id - 1)
            elif not (cell.id % self.__nCols):
                cell.ids.append(cell.id - self.__nCols)
                cell.ids.append(cell.id - self.__nCols + 1)
                cell.ids.append(cell.id + 1)
                cell.ids.append(cell.id + self.__nCols)
                cell.ids.append(cell.id + self.__nCols + 1)
            elif not ((cell.id + 1) % (self.__nCols)):
                cell.ids.append(cell.id - self.__nCols - 1)
                cell.ids.append(cell.id - self.__nCols)
                cell.ids.append(cell.id - 1)
                cell.ids.append(cell.id + self.__nCols - 1)
                cell.ids.append(cell.id + self.__nCols)
            elif (cell.id < self.__nCols):
                cell.ids.append(cell.id - 1)
                cell.ids.append(cell.id + 1)
                cell.ids.append(cell.id + self.__nCols - 1)
                cell.ids.append(cell.id + self.__nCols)
                cell.ids.append(cell.id + self.__nCols + 1)
            elif (cell.id > len(self.__cells) - self.__nCols):
                cell.ids.append(cell.id - self.__nCols - 1)
                cell.ids.append(cell.id - self.__nCols)
                cell.ids.append(cell.id - self.__nCols + 1)
                cell.ids.append(cell.id - 1)
                cell.ids.append(cell.id + 1)
            else:
                cell.ids.append(cell.id - self.__nCols - 1)
                cell.ids.append(cell.id - self.__nCols)
                cell.ids.append(cell.id - self.__nCols + 1)
                cell.ids.append(cell.id - 1)
                cell.ids.append(cell.id + 1)
                cell.ids.append(cell.id + self.__nCols - 1)
                cell.ids.append(cell.id + self.__nCols)
                cell.ids.append(cell.id + self.__nCols + 1)


    def DefineStartGoalCell(self, point, button, screenSize):
        id = 0
        point = [self.__minPoint[0] + ((self.__maxPoint[0] - self.__minPoint[0])/screenSize[0])*point[0], 
                 self.__minPoint[1] + ((self.__maxPoint[1] - self.__minPoint[1])/screenSize[1])*(screenSize[1] - point[1])]
        for cell in self.__cells:
            d = ((point[0] - cell.point[0]) ** 2 + (point[1] - cell.point[1]) ** 2) ** (1/2)
            if d < (((self.__delta[0]) ** 2 + (self.__delta[1]) ** 2) ** (1/2))*0.5:
                id = cell.id
                break
        if button[0]: self.__startID = id
        elif button[2]: self.__goalID = id
        self.AStarAlgorithm()

    def AStarAlgorithm(self):
        self.__possible = []
        self.__visited = []
        self.__solution = []
        startCell = self.__cells[self.__startID]
        goalCell = self.__cells[self.__goalID]
        if startCell.state == 'Obstacle' or goalCell.state == 'Obstacle': return
        for cell in self.__cells: 
            cell.h = ((goalCell.point[0] - cell.point[0]) ** 2 + (goalCell.point[1] - cell.point[1]) ** 2) ** (1/2)
        tmpCell = startCell
        self.__possible.append(tmpCell)
        while(tmpCell.id != self.__goalID):
            if not self.__possible: break
            tmpCell = self.__possible.pop(0)
            self.__visited.append(tmpCell)
            for cellID in tmpCell.ids:
                possibleNextCell = self.__cells[cellID]
                if possibleNextCell.state == 'Obstacle': continue
                g = tmpCell.g + ((tmpCell.point[0] - possibleNextCell.point[0]) ** 2 + (tmpCell.point[1] - possibleNextCell.point[1]) ** 2) ** (1/2)
                if not [cell for cell in self.__possible if cell == possibleNextCell] and \
                   not [cell for cell in self.__visited if cell == possibleNextCell] : 
                    possibleNextCell.idf = tmpCell.id
                    possibleNextCell.g = g
                    possibleNextCell.d = possibleNextCell.g + possibleNextCell.h
                    self.__possible.append(possibleNextCell)
                    self.__possible.sort(key=lambda cell: cell.d)
                elif(g <= possibleNextCell.g):
                    possibleNextCell.idf = tmpCell.id
                    possibleNextCell.g = g
                    possibleNextCell.d = possibleNextCell.g + possibleNextCell.h
        if(tmpCell.id == self.__goalID):
            cell = self.__visited[-1] if self.__startID != self.__goalID else goalCell
            self.__solution.append(cell)
            while(cell.id != startCell.id):
                cell = self.__cells[cell.idf]
                self.__solution.append(cell)


    def Draw(self):
        # Drawing obstacle cells
        for cell in self.__cells:
            if cell.state == 'Free': continue
            cell.Draw((0.4,0.4,0.4), self.__delta[0]/2)
        
        # Drawing visited cells
        for cell in self.__visited:
            cell.Draw((0.7,0.7,1), self.__delta[0]/4)
        
        # Drawing possible next cells
        for cell in self.__possible:
            cell.Draw((0.7,1,1), self.__delta[0]/4)
        
        #Draw solution path
        glLineWidth(5)
        glBegin(GL_LINE_STRIP)
        glColor3f(0,1,0)
        for cell in self.__solution:
            glVertex3f(cell.point[0], cell.point[1], 0.0)
        glEnd()
        
        # Drawing start cell
        self.__cells[self.__startID].Draw((0,1,0), self.__delta[0]/4)
        
        # Drawing goal cell
        self.__cells[self.__goalID].Draw((1,0,0), self.__delta[0]/4)