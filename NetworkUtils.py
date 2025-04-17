# NetworkUtils.py
import socket
import pygame
import pickle, struct

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

def send_msg(sock, msg_obj):
    raw = pickle.dumps(msg_obj)
    header = struct.pack('!I', len(raw))   # 4‑byte unsigned int, network byte order
    sock.sendall(header + raw)
    
def recv_all(sock, n):
    """Receive exactly n bytes from sock, or return None on EOF/error."""
    data = bytearray()
    remaining = n
    while remaining > 0:
        # ask for at most 4 KiB at a time
        to_read = min(4096, remaining)
        try:
            chunk = sock.recv(to_read)
        except socket.error as e:
            print(f"[NetworkUtils] recv error: {e}")
            return None
        if not chunk:
            # peer closed connection before sending everything
            return None
        data.extend(chunk)
        remaining -= len(chunk)
    return bytes(data)

def recv_msg(sock):
    # 1) read 4‑byte length
    hdr = recv_all(sock, 4)
    if hdr is None:
        return None
    msg_len = struct.unpack('!I', hdr)[0]

    # 2) read the full payload
    raw = recv_all(sock, msg_len)
    if raw is None:
        return None

    # 3) unpickle
    return pickle.loads(raw)