import socket
import server_spider

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
    # 监听socket绑定地址

    listen_socket.bind(('10.0.12.13', 515))
    # 转为被动
    listen_socket.listen(5)

    while True:
        print('正在等待客户端的连接...')
        new_socket, client_addr = listen_socket.accept()
        print('正在连接:', client_addr)

        spider = server_spider.Spider()
        while True:
            try:
                recv_data = new_socket.recv(1024).decode('utf-8')

                if not recv_data:
                    break
                elif recv_data == 'q!':
                    break

                barrage = spider.spider_barrage(recv_data)
                if barrage:
                    new_socket.send('\n'.join(barrage).encode('utf-8'))
            except ConnectionResetError as e:
                print(e)

        new_socket.close()
        del spider
        print('已断开 [{}] 的连接！'.format(client_addr))
