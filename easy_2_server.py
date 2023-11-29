import socket
import socketserver
import time

connect_member = []


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global connect_member
        # 有用户连接服务器，保存用户信息
        print('客户端连接:', self.client_address)
        connect_member.append([self.client_address, self.request])
        self.request.sendall(bytes(f"欢迎用户{str(self.client_address)}连接,目前在线{len(connect_member)}人", 'utf-8'))
        try:
            while True:
                data = self.request.recv(1024)
                if not data:
                    break
                # 返回的信息
                res = f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] 客户端 [{str(self.client_address)}]" \
                      f" : [data:{data.decode('utf-8')}]"
                print(res)
                self.request.sendall(bytes(res, 'utf-8'))
                # 向当前在线的所有的用户发送消息
                for i in connect_member:
                    if i[0] != self.client_address:
                        i[1].sendall(bytes(res, 'utf-8'))
        finally:
            # 客户端失去链接,删去用户的信息
            delete_member_index = 0
            for i, d in enumerate(connect_member):
                if d == self.client_address:
                    delete_member_index = i
            del connect_member[delete_member_index]
            print('客户端离线:', self.client_address)
            self.request.close()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    hostname = socket.gethostname()  # 获取本机计算机名称
    ip = socket.gethostbyname(hostname)  # 获取本机ip
    port = 9999
    server = ThreadedTCPServer(("0.0.0.0", port), MyTCPHandler)
    print('Server loop running in ip:', str(ip) + ":" + str(port))
    server.serve_forever()
