from os import listdir
from OpenGL.GL import *
from Tools.Points import Point3D

class MapReader():
    def __init__(self, *args):
        self.__border = []
        self.__obstacles = []
        nMaps = len(listdir('Resources/Maps/'))
        self.mapID = 1 if not args else 1 if args[0] > nMaps else nMaps if args[0] <= 0 else args[0]
        with open(f'Resources/Maps/{str(self.mapID)}.txt') as f:
            lines = f.readlines()
            obstacle = []
            isBorder = False
            isObstacle = False
            for line in lines:
                if not isBorder and not isObstacle:
                    if '[BORDER]' in line: isBorder = True
                    elif '[OBSTACLE]' in line: isObstacle = True
                    continue
                else:
                    pointTxt = line.split()
                    if len(pointTxt) == 2:
                        vertex = Point3D(float(pointTxt[0])/100, float(pointTxt[1])/100, 0.0)
                        if isBorder: self.__border.append(vertex)
                        else: obstacle.append(vertex)
                    else:
                        if isBorder: isBorder = False
                        else:
                            self.__obstacles.append(obstacle)
                            isObstacle = False
                            obstacle = []
            if obstacle: self.__obstacles.append(obstacle)
                            
    @property
    def MinPoint(self):
        point = Point3D(min([vertex.x for vertex in self.__border]),
                        min([vertex.y for vertex in self.__border]),
                        min([vertex.z for vertex in self.__border]))
        return point
    
    @property
    def MaxPoint(self):
        point = Point3D(max([vertex.x for vertex in self.__border]),
                        max([vertex.y for vertex in self.__border]),
                        max([vertex.z for vertex in self.__border]))
        return point
    
    @property
    def Width(self):
        return self.MaxPoint.x - self.MinPoint.x
    
    @property
    def Height(self):
        return self.MaxPoint.y - self.MinPoint.y
    
    @property
    def OrthoPoints(self):
        point1 = self.MinPoint
        point2 = self.MaxPoint
        if self.Width > self.Height:
            point1.y -= (self.Width - self.Height)/2
            point2.y += (self.Width - self.Height)/2
        else:
            point1.x -= (self.Height - self.Width)/2
            point2.x += (self.Height - self.Width)/2
        return point1, point2
    
    @property
    def Obstacles(self):
        return self.__obstacles


    def DrawBorder(self):
        glBegin(GL_QUADS)
        glColor3f(1,1,1)
        for vertex in self.__border:
            glVertex3fv(vertex.ToVector)
        glEnd()


    def DrawObstacles(self):
        for obstacle in self.__obstacles:
            glLineWidth(3)
            glBegin(GL_LINE_LOOP)
            glColor3f(0.0,0.0,0.0)
            for vertex in obstacle:
                glVertex3fv(vertex.ToVector)
            glEnd()