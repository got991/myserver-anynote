import socket
import multiprocessing
import asyncio

print("Hello from Anynote alpha 0.0.100 server")

# # Anynote
# # 自主研发 · 守正创新

maxConnections = 1000


class Processes:
    def __init__(self):
        self.max_connections = maxConnections
        self.all_sockets = []

    async def create_socket(self, index):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 23216))
        self.all_sockets.append(sock)

    async def note_connection(self, sock, index):
        while True:
            try:
                recv_data, cli_addr = sock.recvfrom(1024)
                recv_data = recv_data.decode("utf-8")

                if recv_data == "cid":
                    while True:
                        recv_cid_data, cli_cid_addr = sock.recvform(1024)
                        # 处理recv_cid_data（例如，存储到字典中）

                elif recv_data.startswith("done dtn="):
                    pass

            except Exception as e:
                print(f"Error in socket {index}: {e}")
                break

            finally:
                sock.close()

    async def start(self):
        for i in range(self.max_connections):
            await self.create_socket(i)
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
