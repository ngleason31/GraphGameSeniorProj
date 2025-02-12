import pygame
import time
import turtle
import math
import sys
from pygame.locals import *

pygame.init()   
 
 #Screen Dimensions
infoObject = pygame.display.Info()
screenWidth = infoObject.current_w
screenHeight = infoObject.current_h
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Welcome Screen")

#Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (150, 150, 150)
light_gray = (200, 200, 200)
orange = (255, 165, 0)
blue = (0, 0, 255)

#Font
welcomeFont = pygame.font.Font(None, 60)
graphGameFont = pygame.font.Font(None, 150)
buttonFont = pygame.font.Font(None, 24)

#Buttons
def draw_button(surface, text, rect, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    #Change Color on Hover
    if rect.collidepoint(mouse):
        pygame.draw.rect(surface, active_color, rect)
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(surface, inactive_color, rect)

    #Render and Center Button Text
    textSurf = buttonFont.render(text, True, white)
    textRect = textSurf.get_rect(center=rect.center)
    surface.blit(textSurf, textRect)

    return False


def welcomeScreen():
    clock = pygame.time.Clock()
    running = True

    welcomeY = screenHeight // 4
    buttonWidth = 200
    buttonHeight = 50
    buttonX = screenWidth // 2 - buttonWidth // 2
    button1_Y = welcomeY + 340
    button2_Y = welcomeY + 400
    button3_Y = welcomeY + 460
    button4_Y = welcomeY + 520

    button1_rect = pygame.Rect(buttonX, button1_Y, buttonWidth, buttonHeight)
    button2_rect = pygame.Rect(buttonX, button2_Y, buttonWidth, buttonHeight)
    button3_rect = pygame.Rect(buttonX, button3_Y, buttonWidth, buttonHeight)
    button4_rect = pygame.Rect(buttonX, button4_Y, buttonWidth, buttonHeight)

    base_triangle = [(0, -60), (-70, 60), (70, 60)]
    triangle_center_y = welcomeY + 75
    triangle_center1 = (screenWidth // 2 - 120, triangle_center_y + 60)
    triangle_center2 = (screenWidth // 2 + 120, triangle_center_y + 60)

    angle1 = 0.0
    angle2 = 0.0

    def rotateTriangle(points, angle):
        rotated = []
        for x, y in points:
            newX = x * math.cos(angle) - y * math.sin(angle)
            newY = x * math.sin(angle) + y * math.cos(angle)
            rotated.append((newX, newY))
        return rotated
        


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #Rotate Triangles
        angle1 += 0.007
        angle2 -= 0.007
            

        #Clear Screen
        screen.fill(gray)

        #Welcome Banner
        welcomeTo = "_________ WELCOME TO _________"
        graphGame =  "GRAPH GAME"
        welcome_text = welcomeFont.render(welcomeTo, True, white)
        welcome_text1 = graphGameFont.render(graphGame, True, white)
        welcome_react = welcome_text.get_rect(center=(screenWidth // 2, welcomeY - 100))
        welcome_react1 = welcome_text1.get_rect(center=(screenWidth // 2, welcomeY - 20))
        screen.blit(welcome_text, welcome_react)
        screen.blit(welcome_text1, welcome_react1)

        #Press to Start
        start_text = welcomeFont.render("Press to Start:", True, white)
        start_react = start_text.get_rect(center=(screenWidth // 2, welcomeY + 300))
        screen.blit(start_text, start_react)

        #Draw Triangle 1
        triangle1 = rotateTriangle(base_triangle, angle1)
        triangle1_points = [(triangle_center1[0] + x, triangle_center1[1] + y) for x, y in triangle1]
        pygame.draw.polygon(screen, orange, triangle1_points)

        #Draw Triangle 2
        triangle2 = rotateTriangle(base_triangle, angle2)
        triangle2_points = [(triangle_center2[0] + x, triangle_center2[1] + y) for x, y in triangle2]
        pygame.draw.polygon(screen, blue, triangle2_points)

        #Draw Buttons
        if draw_button(screen, "Player 1", button1_rect, gray, black):
            print("Player 1 button clicked!")
            running = False

        if draw_button(screen, "Player 2", button2_rect, gray, black):
            print("Player 2 button clicked!")
            running = False

        if draw_button(screen, "Settings", button3_rect, gray, black):
            print("Settings button clicked!")
            running = False

        if draw_button(screen, "Credits", button4_rect, gray, black):  
            print("Credits button clicked!")
            running = False

        #Update Display
        pygame.display.flip()
        clock.tick(60)

welcomeScreen()
