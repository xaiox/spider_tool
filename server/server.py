import time
import socket
import server_spider
import threading

class MultiClient(threading.Thread):
    def __init__(self, my_socket):
        super().__init__()
        self.socket = my_socket
        self.spider = server_spider.Spider()

    def run(self):
        while True:
            try:
                recv_data = new_socket.recv(1024).decode('utf-8')

                if not recv_data:
                    break
                elif recv_data == 'q!':
                    break
                if recv_data in bv_list:
                    count = 0
                    while True:
                        if recv_data in bv_list:
                            time.sleep(1)
                            count += 1
                        else:
                            barrage = self.spider.spider_barrage(recv_data)
                            if barrage:
                                self.socket.send('\n'.join(barrage).encode('utf-8'))
                            break
                        if count > 20:
                            print('爬取{}失败！'.format(recv_data))
                            break
                else:
                    bv_list.append(recv_data)
                    print(bv_list)
                    barrage = self.spider.spider_barrage(recv_data)
                    bv_list.remove(recv_data)
                    print(bv_list)
                    if barrage:
                        self.socket.send('\n'.join(barrage).encode('utf-8'))
            except ConnectionResetError as e:
                print(e)

        print('已断开 [{}] 的连接！'.format(client_addr))

    def __del__(self):
        self.socket.close()
        del self.spider


bv_list = []
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
    # 监听socket绑定地址

    listen_socket.bind(('127.0.0.1', 515))
    # 转为被动
    listen_socket.listen(5)

    while True:
        print('正在等待客户端的连接...')
        new_socket, client_addr = listen_socket.accept()
        print('正在连接:', client_addr)

        client = MultiClient(new_socket)
        client.start()

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
#     # 监听socket绑定地址
#
#     listen_socket.bind(('127.0.0.1', 515))
#     # 转为被动
#     listen_socket.listen(5)
#
#     while True:
#         print('正在等待客户端的连接...')
#         new_socket, client_addr = listen_socket.accept()
#         print('正在连接:', client_addr)
#
#         spider = server_spider.Spider()
#         while True:
#             try:
#                 recv_data = new_socket.recv(1024).decode('utf-8')
#
#                 if not recv_data:
#                     break
#                 elif recv_data == 'q!':
#                     break
#
#                 barrage = spider.spider_barrage(recv_data)
#                 if barrage:
#                     new_socket.send('\n'.join(barrage).encode('utf-8'))
#             except ConnectionResetError as e:
#                 print(e)
#
#         new_socket.close()
#         del spider
#         print('已断开 [{}] 的连接！'.format(client_addr))
