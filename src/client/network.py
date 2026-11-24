from src.client.events import events
from src.client import config, file_manager
import socket, time, json, pygame, pickle, ssl

debug = True

local_hosting = True

IP = "127.0.0.1" if local_hosting else "192.168.122.255"
PORT = 8080
timeout_s = 10          # How long to wait for a response at the first connect.
alive_timeout_s = 3     # How long to wait for a response when playing

context = ssl.create_default_context(cafile=file_manager.resource_path("keys/cert.pem"))

def try_connect(ip=IP, port=PORT):
    for _ in range(timeout_s):
        if debug:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET:
                with context.wrap_socket(SOCKET, server_hostname=IP) as client:
                    client.connect((ip, port))
        else:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET:
                    with context.wrap_socket(SOCKET, server_hostname=IP) as client:
                        client.connect((ip, port))
            except OSError:
                time.sleep(1)
                continue
        print("Connected!")
        break
    else:
        print("Couldn't connect to server!")

def send(payload: dict, ip=IP, port=PORT):
    for _ in range(config.FPS *alive_timeout_s):
        if debug:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET:
                with context.wrap_socket(SOCKET, server_hostname=IP) as client:
                    client.connect((ip, port))
                    client.sendall(pickle.dumps(payload))
                    data = client.recv(1024)
        else:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET:
                    with context.wrap_socket(SOCKET, server_hostname=IP) as client:
                        client.connect((ip, port))
                        client.sendall(pickle.dumps(payload))
                        data = client.recv(1024)
            except OSError:
                time.sleep(config.PING_DELAY/config.FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        events.quit_game()
                continue
        break
    else:
        print("Disconnected from server!")
        return None
    if data:
        return pickle.loads(data)
    return None