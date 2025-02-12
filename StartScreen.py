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
font = pygame.font.Font(None, 36)

def welcomeScreen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
        screen.fill(black)
        text = font.render("Welcome to Graph Game!", True, white)
        text_rect = text.get_rect(center=(screenWidth/2, screenHeight/2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(1)


welcomeScreen()