from os import listdir
from OpenGL.GL import *

class MapReader():
    def __init__(self, *arg):
        self.__border = []
        self.__obstacles = []
        self.mapID = arg[0] if arg else 1
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
                        vertex = (float(pointTxt[0])/100, float(pointTxt[1])/100, 0.0)
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
    def MinX(self):
        return min([vertex[0] for vertex in self.__border])
    
    @property
    def MaxX(self):
        return max([vertex[0] for vertex in self.__border])
    
    @property
    def MinY(self):
        return min([vertex[1] for vertex in self.__border])
    
    @property
    def MaxY(self):
        return max([vertex[1] for vertex in self.__border])
    
    @property
    def Obstacles(self):
        return self.__obstacles


    def NextMap(self, mapID):
        nMaps = len(listdir('Resources/Maps/'))
        mapID = 1 if mapID > nMaps else nMaps if mapID <= 0 else mapID
        self.__init__(mapID)


    def Draw(self):
        glBegin(GL_QUADS)
        glColor3f(1,1,1)
        for vertex in self.__border:
            glVertex3fv(vertex)
        glEnd()
        for obstacle in self.__obstacles:
            glLineWidth(3)
            glBegin(GL_LINE_LOOP)
            glColor3f(0.4,0.4,0.4)
            for vertex in obstacle:
                glVertex3fv(vertex)
            glEnd()