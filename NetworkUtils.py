# NetworkUtils.py
import socket
import pygame

def get_local_ip():
    """Return the system's local IP address."""
    try:
        # This dummy connection forces the OS to select the appropriate outbound IP.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_ip_input(screen, prompt="Enter IP to bind to: ", font=None):
    """Display a text input box on the screen and return the entered string."""
    if font is None:
        font = pygame.font.Font(None, 36)
    input_text = ""
    active = True
    clock = pygame.time.Clock()
    
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                    return input_text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        # Clear the screen (or part of it) and draw the prompt.
        screen.fill((0, 0, 0))
        prompt_surface = font.render(prompt + input_text, True, (255, 255, 255))
        screen.blit(prompt_surface, (20, 20))
        pygame.display.flip()
        clock.tick(30)
