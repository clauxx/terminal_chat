import re
import socket
import threading
import time

class Client:
    def __init__(self, port=0):
        self.thread_shutdown = False
        self.thread_lock = None
        self.port = port
        self.socket = None
        self.server = ('10.222.2.37',8888)
        self.rT = None
        self.name = input("Your name: ")
        self.target = input("Other user's name: ")
        self.message = ""

    #threading
    def lock_thread(self):
        self.thread_lock = threading.Lock()

    def acquire_thread(self):
        self.thread_lock.acquire()
    
    def release_thread(self):
        self.thread_lock.release()

    def init_thread(self):
        self.rT = threading.Thread(target=self.receive_msg, args=("RecvThread", self.socket))
        self.rT.start()

    #receiving the data
    def receive_msg(self, name, sock):
        while not self.thread_shutdown:
            try:    
                self.acquire_thread()
                while True: 
                    self.receive_data()
                    self.parse_data()
                    self.display_data()
            except:
                pass
            finally:
                self.release_thread()

    def receive_data(self):
        self.data, self.addr = self.socket.recvfrom(1024)

    def parse_data(self):
        re.split(':+', self.data.decode())

    def display_data(self):
        print("\n" + "(" + time.ctime(time.time()) + ")" + "{" + self.parsed[0] + "}" + "> " + self.parsed[2])
        
    #sockets
    def init_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host = self.socket.getsockname()[0]
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, self.port))
        self.socket.setblocking(0)

    def close_socket(self):
        self.socket.close()

    def send_mess(self):
        fin_mess = self.name + "::" + self.target + "::" +  self.message
        self.socket.sendto(fin_mess.encode(), self.server)

    #main function
    def start(self):
        self.lock_thread()
        self.init_thread()
        while self.message != '!q':
            self.message = input("(" + time.ctime(time.time()) + ")" + "[" +  self.name + "]" + "> ")
            if self.message != "":
                self.send_mess()
            self.acquire_thread()
            self.release_thread()
        self.thread_shutdown = True
        self.rT.join()
        self.close_socket()

myClient = Client()
myClient.init_socket()
myClient.start()
