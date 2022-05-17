#!/usr/bin/python
# -*- coding: UTF-8 -*-
#####################################
# NAME: Justin Kim
# COURSE: ICS3U
# FILE: kim_justin_ISU.py
# PROJECT: ISU
# DATE SUBMITTED: 2016-08-05
#####################################
import pygame
import math
import pygame_menu

from math import sqrt

def vertex2edge(vertices):
    v2e = []
    for i in range(len(vertices)):
        point1 = vertices[i]
        point2 = vertices[(i + 1) % len(vertices)]

        v2e.append((point2[0] - point1[0], point2[1] - point1[1]))

    return v2e

def project(vertices, axis):
    dotProducts = []
    for vertex in vertices:
        dotProducts.append(vertex[0] * axis[0] + vertex[1] * axis[1])

    return [min(dotProducts), max(dotProducts)]

def contains(x, pointRange):
    p1 = pointRange[0]
    p2 = pointRange[1]
    if p2 < p1:
        p1 = pointRange[1]
        p2 = pointRange[0]

    if x >= p1:
        if x <= p2:
            return True
    
    return False


def getOverlap(a, b):
    if contains(a[0], b):
        return True
    if contains(a[1], b):
        return True
    if contains(b[0], a):
        return True
    if contains(b[1], a):
        return True
    return False


def SATCollision(vertexSet1, vertexSet2):
    '''This is the driver function for detecting collision between 2 polygons using SAT'''

    edges = vertex2edge(vertexSet1) + vertex2edge(vertexSet2)

    axes = []
    for edge in edges:
        orthed = (edge[1], 0-edge[0])
        norm = sqrt(orthed[0] ** 2 + orthed[1] ** 2)
        axes.append((orthed[0] / norm, orthed[1] / norm))

    for i in range(len(axes)):
        if not getOverlap(project(vertexSet1, axes[i]), project(vertexSet2, axes[i])):
            return False
    
    return True

pygame.init()

global WIN_DIM
WIN_DIM = (800,600)


gameDisplay = pygame.display.set_mode(WIN_DIM)
pygame.display.set_caption('Collision Demo')
clock = pygame.time.Clock()


class Square(object):
    def __init__(self, coordx, coordy):
        self.dist = 5
        self.xmove = self.dist
        self.ymove = self.dist

        self.cenx = 50
        self.ceny = 50
        
        self.rect = pygame.rect.Rect((coordx-self.cenx, coordy-self.ceny, 100, 100))

        self.my_color = (255, 255, 255)

        # print(self.rect.__dir__())
        # print(self.rect.centerx)
        # print(self.rect.centery)
        
    ## Returns the drawable
    def get_object(self):
        return self.rect

    def inject_color(self, color):
        self.my_color = color

    def move(self):
        if self.rect.centerx+self.cenx == 800:
            self.xmove = -self.dist
        if self.rect.centerx-self.cenx == 0:
            self.xmove = self.dist
        
        if self.rect.centery+self.ceny == 600:
            self.ymove = -self.dist
        if self.rect.centery-self.ceny == 0:
            self.ymove = self.dist
        
        # self.ceny = self.ymove
        # self.cenx = self.xmove

        # print(self.ceny, self.cenx, self.rect.centery)

        self.rect.move_ip(self.xmove, self.ymove)

    def draw(self, surface):
        pygame.draw.rect(gameDisplay, self.my_color, self.rect, 1)

class Circle(object):
    def __init__(self, coordx, coordy, rad):
        self.dist = 5
        self.xmove = self.dist
        self.ymove = self.dist

        self.cenx = 50
        self.ceny = 50
        
        self.center = (coordx, coordy)
        self.radius = rad

        self.my_color = (255, 255, 255)

        # print(self.rect.__dir__())
        # print(self.rect.centerx)
        # print(self.rect.centery)
        
    ## Returns the center
    def get_center(self):
        return self.center

    ## Returns the center
    def get_radius(self):
        return self.radius

    def inject_color(self, color):
        self.my_color = color

    def move(self):
        if self.center[0]+self.cenx == WIN_DIM[0]:
            self.xmove = -self.dist
        if self.center[0]-self.cenx == 0:
            self.xmove = self.dist
        
        if self.center[1]+self.ceny == WIN_DIM[1]:
            self.ymove = -self.dist
        if self.center[1]-self.ceny == 0:
            self.ymove = self.dist
        
        # self.ceny = self.ymove
        # self.cenx = self.xmove

        # print(self.center)

        self.center = (self.center[0]+self.xmove, self.center[1]+self.ymove)

        # self.center[0] += self.xmove
        # self.center[1] += self.ymove

        # self.rect.move_ip(self.xmove, self.ymove)

    def draw(self, surface):
        # pygame.draw.rect(gameDisplay, self.my_color, self.rect, 1)

        pygame.draw.circle(gameDisplay, self.my_color, self.center, self.radius, 1)

class Polygon(object):
    def __init__(self, coordx, coordy, rad):
        self.dist = 5
        self.xmove = self.dist
        self.ymove = self.dist

        self.cenx = 50
        self.ceny = 50
        
        self.center = (coordx, coordy)
        self.radius = rad

        self.my_color = (255, 255, 255)

        self.poly = [(200, 200), (220, 160), (300, 120), (280, 220)]

        temp = []
        for i in self.poly:
            temp.append((i[0]+coordx, i[1]+coordy))

        self.poly = temp
        # print(self.poly)

        # print(self.rect.__dir__())
        # print(self.rect.centerx)
        # print(self.rect.centery)
        
    ## Returns the center
    def get_poly(self):
        # for i in self.poly:
        #     print("poly", i)
        return self.poly

    def inject_color(self, color):
        self.my_color = color

    def move(self):
        if self.poly[0][0]+50+self.cenx == WIN_DIM[0]:
            self.xmove = -self.dist
        if self.poly[0][0]+50-self.cenx == 0:
            self.xmove = self.dist
        
        if self.poly[0][1]-30+self.ceny == WIN_DIM[1]:
            self.ymove = -self.dist
        if self.poly[0][1]-30-self.ceny == 0:
            self.ymove = self.dist
        
        temp = []
        for i in self.poly:
            temp.append((i[0]+self.xmove, i[1]+self.ymove))

        self.poly = temp

        # self.ceny = self.ymove
        # self.cenx = self.xmove

        # print(self.center)

        # self.center = (self.center[0]+self.xmove, self.center[1]+self.ymove)

        # self.center[0] += self.xmove
        # self.center[1] += self.ymove

        # self.rect.move_ip(self.xmove, self.ymove)

    def draw(self, surface):
        # pygame.draw.rect(gameDisplay, self.my_color, self.rect, 1)

        # pygame.draw.circle(gameDisplay, self.my_color, self.center, self.radius, 1)

        pygame.draw.polygon(gameDisplay, self.my_color, self.poly, 1)


def isSquareCollision(sq1, sq2):
    '''This is the driver function for detecting collision between 2 squares'''
    
    if (abs(sq1.centerx - sq2.centerx) < sq2.width and abs(sq1.centery - sq2.centery) < sq2.width):
        return True
    return False

def isCircleCollision(ci1, ci2, rad):
    '''This is the driver function for detecting collision between 2 circles'''

    distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(ci1, ci2)]))

    if distance <= rad*2:
        return True

    # print(ci1, ci2)

    return False



# These 2 variables are used to either stop loops or start menus
crashed = False
pause = False

# Here I initialize the game objects
squares = [Square(50, 100), Square(175, 190)]
circles = [Circle(50, 100, 50), Circle(175, 190, 50)]
polygons = [Polygon(50, 100, 50), Polygon(175, 150, 50)]


# Color definitions for re-usability
RED_COLOR = (255, 0, 0)
WHITE_COLOR = (255, 255, 255)


STATE = 2 # the state variablee manages what part of the demo to test

def main_game():
    '''This is the function that controls the main gameplay'''


    global menu
    global crashed

    menu.disable()
    menu.reset(1)

    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
                crashed = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # This where we initiate the pause sequence
                    menu.enable()
                    return
                elif event.key == 113:
                    # This is an emergency exit key (q)
                    pygame.quit()
                    exit()
            # print(event)

        gameDisplay.fill((0, 0, 0))

        # All the 3 states in the flesh

        if STATE == 0:
            if isSquareCollision(squares[0].get_object(), squares[1].get_object()):
                squares[0].inject_color(RED_COLOR)
                squares[1].inject_color(RED_COLOR)
            else:
                squares[0].inject_color(WHITE_COLOR)
                squares[1].inject_color(WHITE_COLOR)

            for i in squares:
                i.draw(gameDisplay)
                i.move()
        elif STATE == 1:
            if isCircleCollision(circles[0].get_center(), circles[1].get_center(), 50):
                circles[0].inject_color(RED_COLOR)
                circles[1].inject_color(RED_COLOR)
            else:
                circles[0].inject_color(WHITE_COLOR)
                circles[1].inject_color(WHITE_COLOR)

            for i in circles:
                i.draw(gameDisplay)
                i.move()
        elif STATE == 2:
            if SATCollision(polygons[0].get_poly(), polygons[1].get_poly()):
                polygons[0].inject_color(RED_COLOR)
                polygons[1].inject_color(RED_COLOR)
            else:
                polygons[0].inject_color(WHITE_COLOR)
                polygons[1].inject_color(WHITE_COLOR)

            for i in polygons:
                i.draw(gameDisplay)
                i.move()
                # print(i.get_poly())
            # pygame.quit()
            # exit()
                # i.move()

        # square.draw(gameDisplay)
        # square.move()

        pygame.display.update()
        
        clock.tick(60)

def set_circle():
    global STATE
    global menu

    menu.disable()
    STATE = 1

    main_game()

def set_square():
    global STATE
    global menu

    menu.disable()
    STATE = 0
    main_game()

def set_sat():
    global STATE
    global menu

    menu.disable()

    STATE = 2
    main_game()

# This is where we configure the menu 
main_theme = pygame_menu.themes.THEME_DEFAULT.copy()
main_theme.menubar_close_button = False  # Disable close button

menu = pygame_menu.Menu(WIN_DIM[1], WIN_DIM[0], 'Demo Menu',
                       theme=main_theme,
                       onclose=pygame_menu.events.DISABLE_CLOSE)


menu.add_button('Square', set_square)
menu.add_button('Circle', set_circle)
menu.add_button('SAT', set_sat)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(gameDisplay, fps_limit=60.0)

# main_game()

FPS = 60.0

# -------------------------------------------------------------------------
# Main loop
# -------------------------------------------------------------------------
while True:

    # Tick
    clock.tick(FPS)

    # Paint background
    main_background()

    # Application events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    # Main menu
    menu.mainloop(surface, fps_limit=FPS)

    # Flip surface
    pygame.display.flip()

