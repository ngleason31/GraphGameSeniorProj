import socket
import pygame
import pickle, struct
import GlobalSettings

def get_local_ip():
    """Return the system's local IP address."""
    try:
        # This dummy connection forces the OS to select the appropriate outbound IP.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        # Returns basic IP if the above fails.
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_ip_input(screen, prompt="Enter IP to bind to: ", font=None):
    """Display a text input box on the screen and return the entered string."""
    if font is None:
        # Sets the font to default.
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

        # Sets the background color and asks for the IP.
        if GlobalSettings.dark_background:
            screen.fill(GlobalSettings.dark_mode_bg)
        else:
            screen.fill(GlobalSettings.light_mode_bg)
        prompt_surface = font.render(prompt + input_text, True, (255, 255, 255))
        screen.blit(prompt_surface, (20, 20))
        
        pygame.display.flip()
        clock.tick(30)

def send_msg(sock, msg_obj):
    '''Sends a message with a 4-byte header.'''
    raw = pickle.dumps(msg_obj, protocol=pickle.HIGHEST_PROTOCOL)
    header = struct.pack('!I', len(raw))   # 4‑byte unsigned int, network byte order
    sock.sendall(header + raw)
    
def recv_all(sock, n):
    '''Receive exactly n bytes from sock, or return None on EOF/error.'''
    
    data = bytearray()
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise EOFError(f"Expected {n} bytes, got only {len(data)} before EOF")
        data.extend(chunk)
    return bytes(data)

def recv_msg(sock):
    '''
    Receive a message with a 4-byte header, and unpickle it.
    '''
    hdr = b''
    raw = b''
    
    try:
        # Reads the 4-byte header.
        hdr = recv_all(sock, 4)
        msg_len = struct.unpack('!I', hdr)[0]
        # Reads the payload.
        raw = recv_all(sock, msg_len)
        # Sanity Check
        if len(raw) != msg_len:
            print(f"[recv_msg] Warning: expected {msg_len} payload bytes, got {len(raw)}")
        # Unpickle.
        return pickle.loads(raw)

    except Exception as e:
        # Dump the first few bytes of the raw data for debugging.
        snippet = raw[:10] if 'raw' in locals() else hdr
        print(f"[recv_msg] failed to load pickle, first bytes: {snippet!r}, error: {e}")
        return None