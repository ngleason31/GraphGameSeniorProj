import socket
import threading
import pickle
from Game import runGame

def server(screen, player1, player2, host_ip):
    #HOST = '0.0.0.0'
    PORT = 5555
    clients = []
    inputs = [None, None]

    def client_handler(conn, player_id):
        while True:
            try:
                data = conn.recv(8192)
                if not data:
                    print(f"[SERVER] No data received from Player {player_id+1}. Disconnecting...")
                    break
                inputs[player_id] = pickle.loads(data)
            except Exception as e:
                print(f"[ERROR] Player {player_id+1} disconnected: {e}")
                break
        conn.close()
        print(f"[SERVER] Connection with Player {player_id+1} closed.")

    def broadcast_game_state(game_state):
        try:
            state_data = pickle.dumps(game_state)
            for client in clients:
                client.sendall(state_data)
        except Exception as e:
            print(f"[ERROR] Failed to broadcast: {e}")


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host_ip, PORT))
    except Exception as e:
        print(f"[ERROR] Failed to bind to {host_ip}:{PORT} - {e}")
        return
    #server.bind((host_ip, PORT))
    server_socket.listen(1)
    print("[SERVER] Waiting for clients to connect...")
    try:
        conn, addr = server_socket.accept()
        print(f"[SERVER] Player 2 connected from {addr}")
        clients.append(conn)
        threading.Thread(target=client_handler, args=(conn, 0)).start()
    except Exception as e:
        print(f"[ERROR] Error accepting connection for Player 2: {e}")


    runGame(
        screen=screen,
        player1=player1,
        player2=player2,
        server_mode=True,
        broadcast=broadcast_game_state,
        server=conn
    )

    server_socket.close()
    print("[SERVER] Server socket closed.")
