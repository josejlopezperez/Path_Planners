from OpenGL.GL import *
from Tools.Points import Point3D

class Cell():
    def __init__(self, *args):
        self.id = args[0]
        self.point = args[1]
        self.state = 'Free'
        self.f = {'h':0.0, 'g':0.0}
        self.cellFather = 0
        self.cellSons = []
    
    @property
    def Function(self):
        return self.f['g'] + self.f['h']
        
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
        self.__startCell = Cell(0, Point3D(0,0,0))
        self.__goalCell = Cell(0, Point3D(0,0,0))
        self.__delta = Point3D(args[1][0], args[1][1], 0.0)
        self.__solution = []
        self.__visited = []
        self.__possible = []
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
        self.__startCell = self.__cells[0]
        self.__goalCell = self.__cells[0]
        self.CellsConnections()
            
    def CellsConnections(self):
        nCols = int((self.__maxPoint.x - self.__minPoint.x)/self.__delta.x)
        for cell in self.__cells:
            if (cell.id == 0):
                cell.cellSons.append(self.__cells[cell.id + 1])
                cell.cellSons.append(self.__cells[cell.id + nCols])
                cell.cellSons.append(self.__cells[cell.id + nCols + 1])
            elif (cell.id == nCols - 1):
                cell.cellSons.append(self.__cells[cell.id - 1])
                cell.cellSons.append(self.__cells[cell.id + nCols - 1])
                cell.cellSons.append(self.__cells[cell.id + nCols])
            elif (cell.id == len(self.__cells) - nCols):
                cell.cellSons.append(self.__cells[cell.id - nCols])
                cell.cellSons.append(self.__cells[cell.id - nCols + 1])
                cell.cellSons.append(self.__cells[cell.id + 1])
            elif (cell.id == len(self.__cells) - 1):
                cell.cellSons.append(self.__cells[cell.id - nCols - 1])
                cell.cellSons.append(self.__cells[cell.id - nCols])
                cell.cellSons.append(self.__cells[cell.id - 1])
            elif not (cell.id % nCols):
                cell.cellSons.append(self.__cells[cell.id - nCols])
                cell.cellSons.append(self.__cells[cell.id - nCols + 1])
                cell.cellSons.append(self.__cells[cell.id + 1])
                cell.cellSons.append(self.__cells[cell.id + nCols])
                cell.cellSons.append(self.__cells[cell.id + nCols + 1])
            elif not ((cell.id + 1) % (nCols)):
                cell.cellSons.append(self.__cells[cell.id - nCols - 1])
                cell.cellSons.append(self.__cells[cell.id - nCols])
                cell.cellSons.append(self.__cells[cell.id - 1])
                cell.cellSons.append(self.__cells[cell.id + nCols - 1])
                cell.cellSons.append(self.__cells[cell.id + nCols])
            elif (cell.id < nCols):
                cell.cellSons.append(self.__cells[cell.id - 1])
                cell.cellSons.append(self.__cells[cell.id + 1])
                cell.cellSons.append(self.__cells[cell.id + nCols - 1])
                cell.cellSons.append(self.__cells[cell.id + nCols])
                cell.cellSons.append(self.__cells[cell.id + nCols + 1])
            elif (cell.id > len(self.__cells) - nCols):
                cell.cellSons.append(self.__cells[cell.id - nCols - 1])
                cell.cellSons.append(self.__cells[cell.id - nCols])
                cell.cellSons.append(self.__cells[cell.id - nCols + 1])
                cell.cellSons.append(self.__cells[cell.id - 1])
                cell.cellSons.append(self.__cells[cell.id + 1])
            else:
                cell.cellSons.append(self.__cells[cell.id - nCols - 1])
                cell.cellSons.append(self.__cells[cell.id - nCols])
                cell.cellSons.append(self.__cells[cell.id - nCols + 1])
                cell.cellSons.append(self.__cells[cell.id - 1])
                cell.cellSons.append(self.__cells[cell.id + 1])
                cell.cellSons.append(self.__cells[cell.id + nCols - 1])
                cell.cellSons.append(self.__cells[cell.id + nCols])
                cell.cellSons.append(self.__cells[cell.id + nCols + 1])

    def UpdateCellsState(self, map):
        for cell in self.__cells:
            for obstacle in map.Obstacles:
                if cell.IsInsideObstacle(obstacle):
                    cell.state = 'Obstacle'
                    break
                
    
    def DefineStartGoalCell(self, point, button):
        id = sorted(self.__cells, key=lambda cell: point.Distance(cell.point))[0].id
        if button[0]: self.__startCell = self.__cells[id]
        elif button[2]: self.__goalCell = self.__cells[id]
        self.AStarAlgorithm()

    def AStarAlgorithm(self):
        self.__possible = []
        self.__visited = []
        self.__solution = []
        if self.__startCell.state == 'Obstacle' or self.__goalCell.state == 'Obstacle': return
        for cell in self.__cells: 
            cell.f['h'] = cell.point.Distance(self.__goalCell.point)
        tmpCell = self.__startCell
        self.__possible.append(tmpCell)
        while(tmpCell != self.__goalCell):
            if not self.__possible: break
            tmpCell = self.__possible.pop(0)
            self.__visited.append(tmpCell)
            for nextCell in tmpCell.cellSons:
                if nextCell.state == 'Obstacle': continue
                g = tmpCell.f['g'] + tmpCell.point.Distance(nextCell.point)
                if not (nextCell in self.__possible or nextCell in self.__visited): 
                    nextCell.cellFather = tmpCell
                    nextCell.f['g'] = g
                    self.__possible.append(nextCell)
                    self.__possible.sort(key=lambda cell: cell.Function)
                elif(g < nextCell.f['g']):
                    nextCell.cellFather = tmpCell
                    nextCell.f['g'] = g
        if(tmpCell == self.__goalCell):
            cell = self.__visited[-1] if self.__startCell != self.__goalCell else self.__goalCell
            self.__solution.append(cell)
            while(cell != self.__startCell):
                cell = cell.cellFather
                self.__solution.append(cell)


    def Draw(self):
        for cell in self.__cells:
            if cell.state == 'Free': continue
            cell.Draw((0.4,0.4,0.4), self.__delta.x/2)
        for cell in self.__visited:
            cell.Draw((0.7,0.7,1), self.__delta.x/4)
        for cell in self.__possible:
            cell.Draw((0.7,1,1), self.__delta.x/4)
        glLineWidth(5)
        glBegin(GL_LINE_STRIP)
        glColor3f(0,1,0)
        for cell in self.__solution:
            glVertex3f(cell.point.x, cell.point.y, cell.point.z)
        glEnd()
        self.__startCell.Draw((0,1,0), self.__delta.x/4)
        self.__goalCell.Draw((1,0,0), self.__delta.x/4)