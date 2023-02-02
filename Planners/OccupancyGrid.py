from OpenGL.GL import *
from Tools.Points import Point3D

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
        point1 = Point3D(min([vertex.x for vertex in obstacle]), min([vertex.y for vertex in obstacle]), 0.0)
        point2 = Point3D(max([vertex.x for vertex in obstacle]), max([vertex.y for vertex in obstacle]), 0.0)
        if not ((point1.y <= self.point.y <= point2.y) and (point1.x <= self.point.x <= point2.x)): return False
        for i in range(len(obstacle)):
            point1 = Point3D(obstacle[i]) 
            point2 = Point3D(obstacle[(i + 1) if (i + 1) < len(obstacle) else 0])
            if point2.x == point1.x:
                if (min([point1.y, point2.y]) < self.point.y <= max([point1.y, point2.y])) and point2.x > self.point.x: hInters += 1
            elif point2.y != point1.y:
                x = point1.x + ((point2.x - point1.x)/(point2.y - point1.y))*(self.point.y - point1.y)
                if (min([point1.x, point2.x]) < x <= max([point1.x, point2.x])) and x > self.point.x: hInters += 1
        return (hInters % 2) != 0
    
    def Draw(self, color, delta):
        glBegin(GL_QUADS)
        glColor3fv(color)
        glVertex3f(self.point.x + delta, self.point.y + delta, 0.0)
        glVertex3f(self.point.x - delta, self.point.y + delta, 0.0)
        glVertex3f(self.point.x - delta, self.point.y - delta, 0.0)
        glVertex3f(self.point.x + delta, self.point.y - delta, 0.0)
        glEnd()

class OccupancyGrid():
    def __init__(self, *args):
        map = args[0]
        self.__minPoint = map.MinPoint
        self.__maxPoint = map.MaxPoint
        self.__cells = []
        self.__startID = 0
        self.__goalID = 0
        self.__delta = Point3D(args[1][0], args[1][1], 0.0)
        self.__solution = []
        self.__visited = []
        self.__possible = []
        self.__nCols = int((self.__maxPoint.x - self.__minPoint.x)/self.__delta.x)
        self.InitialiseCells()
        self.UpdateCellsState(map)
   
    def InitialiseCells(self):
        point = Point3D(self.__minPoint.x + self.__delta.x/2,
                        self.__minPoint.y + self.__delta.y/2,
                        0.0)
        cellID = 0
        while(point.y <= (self.__maxPoint.y - self.__delta.y/2)):
            while(point.x <= (self.__maxPoint.x - self.__delta.x/2)):
                self.__cells.append(Cell(cellID, Point3D(point)))
                cellID += 1
                point.x += self.__delta.x
            point = Point3D(self.__minPoint.x + self.__delta.x/2, point.y + self.__delta.y, 0.0)
        self.CellsConnections()
            
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

    def UpdateCellsState(self, map):
        for cell in self.__cells:
            for obstacle in map.Obstacles:
                if cell.IsInsideObstacle(obstacle):
                    cell.state = 'Obstacle'
                    break
                
    
    def DefineStartGoalCell(self, point, button, screenSize):
        id = 0
        point = Point3D(self.__minPoint.x + ((self.__maxPoint.x - self.__minPoint.x)/screenSize[0])*point[0], 
                        self.__minPoint.y + ((self.__maxPoint.y - self.__minPoint.y)/screenSize[1])*(screenSize[1] - point[1]), 
                        0.0)
        for cell in self.__cells:
            d = point.Distance(cell.point)
            if d < (((self.__delta.x) ** 2 + (self.__delta.y) ** 2) ** (1/2))*0.5:
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
            cell.h = cell.point.Distance(goalCell.point)
        tmpCell = startCell
        self.__possible.append(tmpCell)
        while(tmpCell.id != self.__goalID):
            if not self.__possible: break
            tmpCell = self.__possible.pop(0)
            self.__visited.append(tmpCell)
            for cellID in tmpCell.ids:
                possibleNextCell = self.__cells[cellID]
                if possibleNextCell.state == 'Obstacle': continue
                g = tmpCell.g + tmpCell.point.Distance(possibleNextCell.point)
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
            cell.Draw((0.4,0.4,0.4), self.__delta.x/2)
        # Drawing visited cells
        for cell in self.__visited:
            cell.Draw((0.7,0.7,1), self.__delta.x/4)
        # Drawing possible next cells
        for cell in self.__possible:
            cell.Draw((0.7,1,1), self.__delta.x/4)
        #Draw solution path
        glLineWidth(5)
        glBegin(GL_LINE_STRIP)
        glColor3f(0,1,0)
        for cell in self.__solution:
            glVertex3f(cell.point.x, cell.point.y, cell.point.z)
        glEnd()
        # Drawing start cell
        self.__cells[self.__startID].Draw((0,1,0), self.__delta.x/4)
        # Drawing goal cell
        self.__cells[self.__goalID].Draw((1,0,0), self.__delta.x/4)