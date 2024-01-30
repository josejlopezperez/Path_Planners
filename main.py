import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from Planners.OccupancyGrid import OG
from Planners.ProbabilisticRoadMap import PRM
from Planners.VisibilityGraph import VG
from Tools.MapReader import MapReader
from Tools.Points import Point3D

map = MapReader()
pathPlannerType = 'OG'

def CheckEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        KeyboardEvents(event)
        MouseEvents(event)

def KeyboardEvents(event):
    global map
    global pathPlanner
    global pathPlannerType
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
            map = MapReader(map.mapID + 1) if event.key == pygame.K_RIGHT else MapReader(map.mapID - 1)
            if pathPlannerType == 'OG':
                pathPlanner = OG(map, (0.5, 0.5))
            elif pathPlannerType == 'PRM':
                pathPlanner = PRM(map)
            elif pathPlannerType == 'VG':
                pathPlanner = VG(map)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(map.OrthoPoints[0].x, map.OrthoPoints[1].x, map.OrthoPoints[0].y, map.OrthoPoints[1].y, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if event.key == pygame.K_1 or event.key == pygame.K_KP1:
            pathPlannerType = 'OG'
            pathPlanner = OG(map, (0.5, 0.5))
        if event.key == pygame.K_2 or event.key == pygame.K_KP2:
            pathPlannerType = 'PRM'
            pathPlanner = PRM(map)
        if event.key == pygame.K_3 or event.key == pygame.K_KP3:
            pathPlannerType = 'VG'
            pathPlanner = VG(map)
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()

def MouseEvents(event):
    global pathPlanner
    if event.type == pygame.MOUSEBUTTONDOWN:
        buttonsPressed = pygame.mouse.get_pressed()
        mousePosition = pygame.mouse.get_pos()
        screenSize = pygame.display.get_window_size()
        minPoint ,maxPoint = map.OrthoPoints
        glPoint = Point3D(minPoint.x + ((maxPoint.x - minPoint.x)/screenSize[0])*mousePosition[0], 
                        minPoint.y + ((maxPoint.y - minPoint.y)/screenSize[1])*(screenSize[1] - mousePosition[1]), 
                        0.0)
        pathPlanner.DefineStartGoal(glPoint, buttonsPressed)

if __name__ == '__main__':
    global pathPlanner
    pathPlannerType = sys.argv[1] if (len(sys.argv) > 1) else pathPlannerType
    pygame.init()
    pygame.display.set_mode((800,800), DOUBLEBUF|OPENGL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(map.OrthoPoints[0].x, map.OrthoPoints[1].x, map.OrthoPoints[0].y, map.OrthoPoints[1].y, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    if pathPlannerType == 'OG':
        pathPlanner = OG(map, (0.5, 0.5))
    elif pathPlannerType == 'PRM':
        pathPlanner = PRM(map)
    elif pathPlannerType == 'VG':
        pathPlanner = VG(map)
    while True:
        CheckEvents()
        map.DrawBorder()
        pathPlanner.Draw()
        map.DrawObstacles()
        pygame.display.flip()
        pygame.time.wait(1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)