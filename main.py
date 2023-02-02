import pygame
from pygame.locals import *
from OpenGL.GL import *
from Tools.MapReader import MapReader
from Planners.OccupancyGrid import OccupancyGrid


map = MapReader()
occGrid = OccupancyGrid(map, (0.5, 0.5))


def KeyboardEvent(event):
    global map, occGrid
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            map.NextMap(map.mapID + 1)
            occGrid = OccupancyGrid(map, (0.5, 0.5))
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(map.MinX, map.MaxX, map.MinY, map.MaxY, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if event.key == pygame.K_LEFT:
            map.NextMap(map.mapID - 1)
            occGrid = OccupancyGrid(map, (0.5, 0.5))
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(map.MinX, map.MaxX, map.MinY, map.MaxY, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()
    return map


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800,800), DOUBLEBUF|OPENGL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(map.MinX, map.MaxX, map.MinY, map.MaxY, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            KeyboardEvent(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttonsPressed = pygame.mouse.get_pressed()
                mousePosition = pygame.mouse.get_pos()
                occGrid.DefineStartGoalCell(mousePosition, buttonsPressed, screen.get_size())
        map.Draw()
        occGrid.Draw()
        pygame.display.flip()
        pygame.time.wait(1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)