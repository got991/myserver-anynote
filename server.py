# import socket
# import multiprocessing
# 
# print("Hello from Anynote alpha 0.0.100 server")
# 
# # This is Anynote alpha 0.0.100.
# # Try to connect n clients using socket
# # and recv messages from clients and write them to a dictionary.
# # When recved one message, send 'done dtn={the data number},cid={connection id}'.
# # https://anynote.api.magiccube.site:23216
# 
# # Anynote
# # 自主研发 · 守正创新
# 
# # 写死在代码里的最大连接数量
# maxConnections = 1000
# 
# AllSocket = []
# 
#     
# 
# def Anynote_Connection(thisSocketId):
#     j = 1
#     cid = 0
#     while True:
#         recv_data, cli_addr = AllSocket[thisSocketId].recvfrom(1024)
#         recv_encoded_data = recv_data.decode('utf-8')
#         if recv_data:
#             match recv_encoded_data:
#                 case 'cid':
#                     while recv_cid_data:
#                         recv_cid_data, cli_cid_addr = AllSocket[ThisSocketId].recvform(1024)
#                 # case f'done dtn={j} cid={}'
#                 
#                 
# class Processes():
#     def __init__(self):
#         for i in range(maxConnections):
#             AllSocket.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
#             AllSocket[i].bind(('127.0.0.1', 23216))
#         for i in range(maxConnections):
#             setattr(self, 'process'+str(i+1), multiprocessing.Process(target=Anynote_Connection, args=(i)))
import socket
import multiprocessing
import asyncio

print("Hello from Anynote alpha 0.0.100 server")

maxConnections = 1000

class Processes:
    def __init__(self):
        self.max_connections = maxConnections
        self.all_sockets = []

    async def create_socket(self, index):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 23216))
        self.all_sockets.append(sock)

    async def note_connection(self, sock, index):
        while True:
            try:
                recv_data, cli_addr = sock.recvfrom(1024)
                recv_data = recv_data.decode('utf-8')

                if recv_data == 'cid':
                    while True:
                        recv_cid_data, cli_cid_addr = sock.recvform(1024)
                        # 处理recv_cid_data（例如，存储到字典中）

                elif recv_data.startswith('done dtn='):
                    # 处理完成消息（例如，从字典中删除相关条目）
                    pass

            except Exception as e:
                print(f"Error in socket {index}: {e}")
                break

            finally:
                sock.close()

    async def start(self):
        for i in range(self.max_connections):
            await self.create_socket(i)
            setattr(self, f'process{i+1}', multiprocessing.Process(target=self.note_connection, args=(self.all_sockets[i], i)))

if __name__ == "__main__":
    server = Processes()
    asyncio.run(server.start())
