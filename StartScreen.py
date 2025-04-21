import pygame
import math
import sys
import GlobalSettings
from pygame.locals import *

pygame.init()

# Hardcoded colors.
white = (255, 255, 255)
black = (0, 0, 0)
gray = (150, 150, 150)
light_gray = (200, 200, 200)
orange = (255, 165, 0)
blue = (0, 0, 255)

# Fonts.
welcomeFont = pygame.font.Font(None, 60)
graphGameFont = pygame.font.Font(None, 150)
buttonFont = pygame.font.Font(None, 24)

def draw_button(surface, text, rect, inactive_color, active_color):
    '''
    Helper function to draw a button with text.
    '''
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Change Color on Hover.
    if rect.collidepoint(mouse):
        pygame.draw.rect(surface, active_color, rect)
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(surface, inactive_color, rect)

    # Render and Center Button Text.
    textSurf = buttonFont.render(text, True, white)
    textRect = textSurf.get_rect(center=rect.center)
    surface.blit(textSurf, textRect)

    return False


def welcomeScreen(screen, screenWidth, screenHeight):
    '''
    Displays the welcome screen with options for the user to select.
    '''

    clock = pygame.time.Clock()
    running = True

    # Initialize helpful variables.
    welcomeY = screenHeight // 4
    buttonWidth = 200
    buttonHeight = 40
    buttonX = screenWidth // 2 - buttonWidth // 2
    button1_Y = welcomeY + 330
    button2_Y = welcomeY + 380
    button3_Y = welcomeY + 430
    button4_Y = welcomeY + 480
    button5_Y = welcomeY + 530


    # Initialize the buttons.
    button1_rect = pygame.Rect(buttonX, button1_Y, buttonWidth, buttonHeight)
    button2_rect = pygame.Rect(buttonX, button2_Y, buttonWidth, buttonHeight)
    button3_rect = pygame.Rect(buttonX, button3_Y, buttonWidth, buttonHeight)
    button4_rect = pygame.Rect(buttonX, button4_Y, buttonWidth, buttonHeight)
    button5_rect = pygame.Rect(buttonX, button5_Y, buttonWidth, buttonHeight)

    # Initialize the triangles.
    base_triangle = [(0, -60), (-70, 60), (70, 60)]
    triangle_center_y = welcomeY + 75
    triangle_center1 = (screenWidth // 2 - 120, triangle_center_y + 60)
    triangle_center2 = (screenWidth // 2 + 120, triangle_center_y + 60)

    angle1 = 0.0
    angle2 = 0.0

    def rotateTriangle(points, angle):
        '''
        Helper function to rotate the triangle points around their center.
        '''
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

        # Rotates Triangles.
        angle1 += 0.007
        angle2 -= 0.007
            

        # Clears Screen.
        if GlobalSettings.dark_background:
            bg_color = GlobalSettings.dark_mode_bg
            detail_color = GlobalSettings.dark_mode_details
        else:
            bg_color = GlobalSettings.light_mode_bg
            detail_color = GlobalSettings.light_mode_details
        screen.fill(bg_color)

        # Welcome Banner.
        welcomeTo = "_________ WELCOME TO _________"
        graphGame =  "GRAPH GAME"
        welcome_text = welcomeFont.render(welcomeTo, True, detail_color)
        welcome_text1 = graphGameFont.render(graphGame, True, detail_color)
        welcome_react = welcome_text.get_rect(center=(screenWidth // 2, welcomeY - 100))
        welcome_react1 = welcome_text1.get_rect(center=(screenWidth // 2, welcomeY - 20))
        screen.blit(welcome_text, welcome_react)
        screen.blit(welcome_text1, welcome_react1)

        # Press to Start button.
        start_text = welcomeFont.render("Press to Start:", True, detail_color)
        start_react = start_text.get_rect(center=(screenWidth // 2, welcomeY + 300))
        screen.blit(start_text, start_react)

        # Draw Triangle 1.
        triangle1 = rotateTriangle(base_triangle, angle1)
        triangle1_points = [(triangle_center1[0] + x, triangle_center1[1] + y) for x, y in triangle1]
        pygame.draw.polygon(screen, orange, triangle1_points, width=6)

        # Draw Triangle 2.
        triangle2 = rotateTriangle(base_triangle, angle2)
        triangle2_points = [(triangle_center2[0] + x, triangle_center2[1] + y) for x, y in triangle2]
        pygame.draw.polygon(screen, blue, triangle2_points, width=6)

        # Draw Buttons.
        if draw_button(screen, "Single Player", button1_rect, gray, black):
            selectedOption = "single player"
            running = False

        if draw_button(screen, "Multiplayer", button2_rect, gray, black):
            selectedOption = "multiplayer"
            running = False
            
        if draw_button(screen, "Computer", button3_rect, gray, black):
            selectedOption = "computer"
            running = False

        if draw_button(screen, "Settings", button4_rect, gray, black):
            selectedOption = "settings"
            running = False

        if draw_button(screen, "Credits", button5_rect, gray, black):  
            selectedOption = "credits"
            running = False

        # Update Display.
        pygame.display.flip()
        clock.tick(60)

    return selectedOption

