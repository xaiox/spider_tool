import os
import time
import socket
from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

class Client:
    def __init__(self):
        self.status = []
        self.data = []
        self.bv = None
        self.ui = QUiLoader().load(qfile_stats)
        self.ui.connect_.clicked.connect(self.connect)
        self.ui.crawl_.clicked.connect(self.crawl)
        self.ui.close_.clicked.connect(self.close)
        self.ui.down.clicked.connect(self.download)

    def connect(self):
        if self.status:
            self.tip('已经连接了服务器！')
        else:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 515))
            self.status.append(client_socket)
            self.status.append(time.time())
            self.tip('成功连接服务器!')

    def close(self):
        if self.status:
            self.status[0].close()
            self.status.pop()
            self.status.pop()
            self.tip('成功断开服务器!')
        else:
            self.tip('未连接服务器！')

    def crawl(self):
        if self.status:
            url = self.ui.url_edit.text()
            self.tip('正在处理中...')
            start = time.time()
            try:
                if url[:2] == 'BV':
                    self.bv = url[:12]
                else:
                    idx = url.find('BV')
                    if idx != -1:
                        # print(idx)
                        self.bv = url[idx:idx + 12]
                    else:
                        raise KeyError
                self.tip('已解析:'+self.bv)
            except KeyError:
                self.tip('请输入正确的链接！')
                return
            self.status[0].send(self.bv.encode('utf-8'))
            data = self.status[0].recv((1024 ** 2) * 10).decode('utf-8')
            self.data = []
            for i in data.split('\n'):
                self.tip(i)
                self.data.append(i+'\n')
            self.tip('\n花费时间:'+str(time.time()-start) + 's')
        else:
            self.tip('还没有连接服务器!')

    def download(self):
        if self.data and self.bv:
            with open(self.bv+'.txt', 'w', encoding='utf-8') as f:
                f.writelines(self.data)
            path = os.getcwd()
            self.tip('已成功导出数据至:'+path[:len(path)-6]+self.bv+'.txt')
            self.data.clear()
            self.bv = None
        else:
            self.tip('没有数据或数据已导出！')

    def tip(self, s):
        self.ui.text.append(s)
        self.ui.text.ensureCursorVisible()
        QApplication.processEvents()

    def __del__(self):
        if self.status:
            self.status[0].close()
            self.status.pop()
            self.status.pop()


if __name__ == '__main__':
    app = QApplication([])
    qfile_stats = QFile('test.ui')
    qfile_stats.open(QFile.ReadOnly)
    qfile_stats.close()
    test = Client()
    test.ui.show()
    app.exec_()