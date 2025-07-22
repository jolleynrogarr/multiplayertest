#multiplayer test by jolley rogarr
# 21 july 2025
import socket, threading, json

players = {}

def handle_client(conn):
    username = None
    try:
        #takes the first datas before loop, may this cause to multiple nicknames issue. Idk
        first_data = conn.recv(4096).decode()
        info = json.loads(first_data)
        username = info["username"]
        players[username] = (info["x"], info["y"])
        print(f"[JOINED] {username} joined the game.")

        while True:
            data = conn.recv(4096).decode()
            info = json.loads(data)
            players[username] = (info["x"], info["y"])

            #send info to client back
            payload = []
            for name, pos in players.items():
                payload.append({"username": name, "x": pos[0], "y": pos[1]})
            conn.send(json.dumps(payload).encode())

    except:
        pass
    finally:
        if username and username in players:
            del players[username]
            print(f"[LEFT] {username} left the game.")
        conn.close()

#server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen()
    print("SERVER STARTED, Waiting for clients...")

    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

start_server()
