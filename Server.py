import socket
import threading
import pickle
from Game import runGame

def server(screen, player1, player2):
    HOST = '0.0.0.0'
    PORT = 5555

    clients = []
    inputs = [None, None]

    def client_handler(conn, player_id):
        while True:
            try:
                data = conn.recv(8192)
                if not data:
                    break
                inputs[player_id] = pickle.loads(data)
            except Exception as e:
                print(f"[ERROR] Player {player_id+1} disconnected: {e}")
                break
        conn.close()

    def broadcast_game_state(game_state):
        try:
            data = pickle.dumps(game_state.to_dict())
            for client in clients:
                client.sendall(data)
        except Exception as e:
            print(f"[ERROR] Failed to broadcast: {e}")


    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print("[SERVER] Waiting for clients to connect...")

    for i in range(2):
        conn, addr = server.accept()
        print(f"[SERVER] Player {i+1} connected from {addr}")
        clients.append(conn)
        threading.Thread(target=client_handler, args=(conn, i)).start()

    runGame(
        screen=screen,
        player1=player1,
        player2=player2,
        server_mode=True,
        broadcast=broadcast_game_state,
        server=server
    )

    server.close()