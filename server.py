import socket
import multiprocessing
import asyncio

print("Hello from Anynote alpha 0.0.100 server")

# Anynote
# 自主研发 · 守正创新

maxConnections = 1000


class Processes:
    def __init__(self):
        self.max_connections = maxConnections
        self.all_sockets = []
        self.clients = {}

    async def create_socket(self, index):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 23216 + index))
        self.all_sockets.append(sock)

    async def note_connection(self, sock, index):
        while True:
            try:
                recv_data, cli_addr = sock.recvfrom(1024)
                recv_data = recv_data.decode("utf-8")

                command, data = recv_data.split(" ", 1)

                if command == "init":
                    print(f"Connection from {cli_addr}")
                    client_id = data.strip()
                    self.clients[client_id] = cli_addr
                    sock.sendto("ok cid=".encode("utf-8"), cli_addr)
                elif command == "done":
                    # TODO: handle_done
                    pass

            except Exception as e:
                print(f"Error in socket {index}: {e}")
                break

            finally:
                sock.close()

    async def start(self):
        await asyncio.gather(
            *[self.create_socket(i) for i in range(self.max_connections)]
        )
        for i in range(self.max_connections):
            setattr(
                self,
                f"process{i+1}",
                multiprocessing.Process(
                    target=self.note_connection, args=(self.all_sockets[i], i)
                ),
            )


if __name__ == "__main__":
    server = Processes()
    asyncio.run(server.start())
