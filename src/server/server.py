from src.server import parse_payload, file_manager
import socket, pickle, ssl, os, asyncio, keyboard, json

local_hosting = True

ip = "127.0.0.1" if local_hosting else "0.0.0.0"
port = 8080

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    certfile=os.path.join(file_manager.base_path, "keys/cert.pem"),
    keyfile=os.path.join(file_manager.base_path, "keys/key.pem")
)

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    address = writer.get_extra_info("peername")

    while True:

        data = await reader.read(1024)
        if not data:
            break

        payload = json.loads(data.decode())
        payload["address"] = ":".join([address[0], str(address[1])])
        response: bytes | None = json.dumps(parse_payload.parse_payload(payload)).encode()
        if response:
            writer.write(response)
            await writer.drain()

async def start_server():

    server = await asyncio.start_server(handle_client, ip, port, ssl=context)

    print(f"Starting server: {ip}:{port}")

    async with server:
        await server.serve_forever()

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    #     server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     server.bind((ip, port))
    #     server.listen()
    #     while True:

    #         connection, address = server.accept()
    #         connection = context.wrap_socket(connection, server_side=True)
    #         with connection:
    #             pkg = connection.recv(1024)
    #             if not pkg:
    #                 continue

    #             payload = pickle.loads(pkg)
    #             payload["address"] = ":".join([address[0], str(address[1])])
    #             response: bytes | None = parse_payload.parse_payload(payload)
    #             if response:
    #                 connection.sendall(response)

def main():
    asyncio.run(start_server())

if __name__ == "__main__":
    main()