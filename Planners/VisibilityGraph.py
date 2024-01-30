import math
from OpenGL.GL import *
import random
from Tools.Points import *

class Node():
    def __init__(self, *args):
        self.id = args[0]
        self.point = args[1]
        self.state = 'Free'
        self.f = {'h':0.0, 'g':0.0}
        self.nodeFather = 0
        self.nodeSons = []

    @property
    def Function(self):
        return self.f['g'] + self.f['h']

    def CheckConnections(self, map):
        nodeSons = []
        point1 = self.point
        for nodeSon in self.nodeSons:
            flag = False
            point2 = nodeSon.point
            for obstacle in map.Obstacles:
                for i in range(len(obstacle)):
                    point3 = Point3D(obstacle[i])   
                    point4 = Point3D(obstacle[(i + 1) if (i + 1) < len(obstacle) else 0])
                    if point1 == point3 or point1 == point4 or point2 == point3 or point2 == point4:
                        continue
                    if DoIntersect(point1,point2,point3,point4):
                        flag = True
                        break
                if flag: break
            if not flag: nodeSons.append(nodeSon)
        self.nodeSons = nodeSons

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

    def Draw(self, color):
        glBegin(GL_POLYGON)
        glColor3fv(color)
        for i in range(50):
            point = Point3D(0.15 * math.cos(i * 2 * math.pi / 50) + self.point.x,
                            0.15 * math.sin(i * 2 * math.pi / 50) + self.point.y,
                            0.0 + self.point.z)
            glVertex3fv(point.ToVector)
        glEnd()


class VG():
    def __init__(self, *args):
        self.__map = args[0]
        self.__minPoint = self.__map.MinPoint
        self.__maxPoint = self.__map.MaxPoint
        self.__nodes = []
        self.__startNode = Node(0, Point3D(0,0,0))
        self.__goalNode = Node(0, Point3D(0,0,0))
        self.__solution = []
        self.__visited = []
        self.__possible = []
        self.InitialiseNodes()

    def InitialiseNodes(self):
        id = 1
        for obstacle in self.__map.Obstacles:
            for vertex in obstacle:
                self.__nodes.append(Node(id, vertex))
                id +=1
        point = Point3D(random.uniform(self.__minPoint.x + 1, self.__maxPoint.x - 1),
                        random.uniform(self.__minPoint.y + 1, self.__maxPoint.y - 1),
                        0)
        self.__startNode = Node(0, point)
        point = Point3D(random.uniform(self.__minPoint.x + 1, self.__maxPoint.x - 1),
                        random.uniform(self.__minPoint.y + 1, self.__maxPoint.y - 1),
                        0)
        self.__goalNode = Node(id, point)
        self.NodesConnections()

    def NodesConnections(self):
        nodesList = [self.__startNode] + self.__nodes + [self.__goalNode]
        for node in nodesList:
            node.nodeSons = [nodeSon for nodeSon in nodesList if nodeSon != node]
            node.CheckConnections(self.__map)

    def DefineStartGoal(self, point, button):
        if button[0]: 
            self.__startNode.point = point
        elif button[2]: 
            self.__goalNode.point = point
        self.NodesConnections()
        self.AStarAlgorithm()

    def AStarAlgorithm(self):
        self.__possible = []
        self.__visited = []
        self.__solution = []
        if self.__startNode.state == 'Obstacle' or self.__goalNode.state == 'Obstacle': return
        for node in [self.__startNode] + self.__nodes:
            node.f['h'] = node.point.Distance(self.__goalNode.point)
        tmpNode = self.__startNode
        self.__possible.append(tmpNode)
        while(tmpNode != self.__goalNode):
            if not self.__possible: break
            tmpNode = self.__possible.pop(0)
            self.__visited.append(tmpNode)
            for nextNode in tmpNode.nodeSons:
                if nextNode.state == 'Obstacle': continue
                g = tmpNode.f['g'] + tmpNode.point.Distance(nextNode.point)
                if not (nextNode in self.__possible or nextNode in self.__visited): 
                    nextNode.nodeFather = tmpNode
                    nextNode.f['g'] = g
                    self.__possible.append(nextNode)
                    self.__possible.sort(key=lambda node: node.Function)
                elif(g < nextNode.f['g']):
                    nextNode.nodeFather = tmpNode
                    nextNode.f['g'] = g
        if(tmpNode == self.__goalNode):
            node = self.__visited[-1] if self.__startNode != self.__goalNode else self.__goalNode
            self.__solution.append(node)
            while(node != self.__startNode):
                node = node.nodeFather
                self.__solution.append(node)

    def Draw(self):
        for node in self.__nodes:
            if node.state == 'Obstacle': continue
            node.Draw((0.4,0.4,0.4))
            for nodeSon in node.nodeSons:
                glLineWidth(0.5)
                glBegin(GL_LINE_STRIP)
                glColor4f(0.4,0.4,0.4,0.1)
                glVertex3f(nodeSon.point.x, nodeSon.point.y, nodeSon.point.z)
                glVertex3f(node.point.x, node.point.y, node.point.z)
                glEnd()
        for node in self.__visited:
            node.Draw((0.7,0.7,1))
        for node in self.__possible:
            node.Draw((0.7,1,1))
        glLineWidth(5)
        glBegin(GL_LINE_STRIP)
        glColor3f(0,1,0)
        for node in self.__solution:
            glVertex3f(node.point.x, node.point.y, node.point.z)
        glEnd()
        self.__startNode.Draw((0,1,0))
        self.__goalNode.Draw((1,0,0))