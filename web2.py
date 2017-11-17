# coding:utf-8
from socket import *
import re
import sys


class WsgiSever(object):
    def __init__(self, port):
        # 指定文件的路径
        self.document = './html'
        # 创建套接字
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        addr = ("", port)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind(addr)
        self.server_socket.listen(128)

    def handle(self):
        """循环接受客户端"""
        while True:
            # 变为监听套接字
            self.new_socket, new_addr = self.server_socket.accept()

            # 接受一个新的套接字
            date = self.new_socket.recv(1024)
            # print('date', date)
            if not date:
                break
            # 把数据切割成行
            request_lines = date.splitlines()
            print(request_lines)
            if request_lines:
                temp = request_lines[0]

                ret = re.match(r'[^/]*([^ ]+)', temp)
                if ret:
                    try:
                        file_name = ret.group(1)
                        print('------', file_name)
                    except:
                        return
                    else:
                        self.deal_with(file_name)

    def deal_with(self, file_name):
        """处理文件内容"""
        if file_name == '/':
            file_name = 'index.html'
        else:
            file_name = self.document + file_name
            print(file_name)

        try:
            # 以2进制的方式打开
            f = open(file_name, 'rb')

        except:
            # 不能打开文件，发送404错误
            response_header = 'HTTP/1.1 404 not found \r\n'
            response_header += 'Content-Type:text/html; charset=utf-8\r\n'
            response_header += '\r\n'
            response_body = 'not found file' + u'请输入正确的url'
            response = response_header + response_body
            self.new_socket.send(response.encode('utf-8'))
        else:
            # 打开文件
            content = f.read()
            response_header = 'HTTP/1.1 200 ok\r\n'
            response_header += '\r\n'
            response_body = content
            self.new_socket.send(response_header.encode('utf-8'))
            self.new_socket.send(response_body)
            f.close()
        finally:
            self.new_socket.close()


def main():
    if len(sys.argv) == 2:
        port = sys.argv[1]
        if port.isdigit():
            port = int(port)
    else:
        print('python web2.py 8000')
        return

    wsgi_server = WsgiSever(port)
    wsgi_server.handle()

if __name__ == '__main__':
    main()
