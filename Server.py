import socket
import pygame
from NetworkUtils import send_msg
from Game import runGame
import GlobalSettings

def server(screen, player1, player2, host_ip):
    '''
    Handles the server side with a loading screen and console logs.
    '''

    PORT = 5555
    client = None

    # — bind & listen —
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host_ip, PORT))
        server_socket.listen(1)
        server_socket.setblocking(False)    # non‑blocking accept()
    except Exception as e:
        print(f"[ERROR] Failed to bind/listen on {host_ip}:{PORT} - {e}")
        return

    # — console logs —
    print(f"[SERVER] Hosting on {host_ip} on port {PORT}...")
    print(f"[SERVER] Listening for Player 2...")

    # — prepare loading‑screen UI —
    font = pygame.font.Font(None, 36)
    cancel_btn = pygame.Rect(
        screen.get_width()//2 - 60,
        screen.get_height()//2 + 40,
        120, 40
    )
    waiting = True

    # — loading‑screen loop —
    while waiting:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                server_socket.close()
                pygame.quit()
                return
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if cancel_btn.collidepoint(ev.pos):
                    server_socket.close()
                    return

        # try to accept
        try:
            conn, addr = server_socket.accept()
        except BlockingIOError:
            conn = None

        if conn:
            print(f"[SERVER] Player 2 connected from {addr}")
            client = conn
            waiting = False
            break

        # draw loading screen
        if GlobalSettings.dark_background:
            bg_color = GlobalSettings.dark_mode_bg
            detail_color = GlobalSettings.dark_mode_details
        else:
            bg_color = GlobalSettings.light_mode_bg
            detail_color = GlobalSettings.light_mode_details
            
        screen.fill(bg_color)
        txt = font.render("Waiting for Player 2 to connect…", True, detail_color)
        screen.blit(txt, (screen.get_width()//2 - txt.get_width()//2,
                          screen.get_height()//2 - 60))

        ip_txt = font.render(f"IP: {host_ip}", True, detail_color)
        screen.blit(ip_txt, (screen.get_width()//2 - ip_txt.get_width()//2,
                             screen.get_height()//2 - 20))

        pygame.draw.rect(screen, (200,0,0), cancel_btn)
        pos = pygame.mouse.get_pos()
        cancel_color = GlobalSettings.black if cancel_btn.collidepoint(pos) else GlobalSettings.gray
        pygame.draw.rect(screen, cancel_color, cancel_btn)

        lbl = font.render("Cancel", True, GlobalSettings.white)
        screen.blit(lbl, lbl.get_rect(center=cancel_btn.center))

        pygame.display.flip()
        pygame.time.delay(100)

    # — on connect, run the game —
    def broadcast_game_state(game_state):
        try:
            send_msg(client, game_state)
        except Exception as e:
            print(f"[ERROR] Failed to broadcast: {e}")

    runGame(
        screen=screen,
        player1=player1,
        player2=player2,
        server_mode=True,
        broadcast=broadcast_game_state,
        server=client
    )

    client.close()
    server_socket.close()
    print("[SERVER] Server socket closed.")
