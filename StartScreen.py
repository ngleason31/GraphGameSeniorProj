import pygame
import time
import turtle
from pygame.locals import *

pygame.init()   
 
 #Screen Dimensions
screenWidth = 800
screenHeight = 800
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Welcome Screen")

#Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (150, 150, 150)
light_gray = (200, 200, 200)

#Font
font = pygame.font.Font(None, 36)

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
    textSurf = font.render(text, True, white)
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
    button1_Y = welcomeY + 240
    button2_Y = welcomeY + 300

    button1_rect = pygame.Rect(buttonX, button1_Y, buttonWidth, buttonHeight)
    button2_rect = pygame.Rect(buttonX, button2_Y, buttonWidth, buttonHeight)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RETURN:
            #         running = False
        #Clear Screen
        screen.fill(black)

        #Welcome Banner
        welcome_text = font.render("Welcome to Graph Game!", True, white)
        welcome_react = welcome_text.get_rect(center=(screenWidth // 2, welcomeY))
        screen.blit(welcome_text, welcome_react)
        start_text = font.render("Press to Start:", True, white)
        start_react = start_text.get_rect(center=(screenWidth // 2, welcomeY + 200))
        screen.blit(start_text, start_react)

        #Draw Buttons
        if draw_button(screen, "Player 1", button1_rect, gray, black):
            print("Player 1 button clicked!")
            running = False

        if draw_button(screen, "Player 2", button2_rect, gray, black):
            print("Player 2 button clicked!")
            running = False

        pygame.display.flip()
        clock.tick(60)

welcomeScreen()