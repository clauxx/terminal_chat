import re
import socket
import time

class Server:
    def __init__(self, port=8888): 
        self.port = port 
        self.users = {}
        self.socket = None

    def init_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host = self.socket.getsockname()[0]
        self.socket.bind((host, self.port))
        self.socket.setblocking(0)
        print("Socket initialized on port %s" % self.port)

    def close_socket(self):
        self.socket.close()

    def receive(self):
        return self.socket.recvfrom(1024)

    def parse(self, data):
        return re.split(':+', data.decode())

    def set_db(self, parsed, addr):
        #parsed_data[0] = name of source
        #parsed_data[1] = name of recipient
        #parsed_data[2] = message
        msg_source = parsed[0]
        if(msg_source not  in self.users.keys()):
            self.users[msg_source] = addr

        if(self.users[msg_source] != addr):
            self.users[msg_source] = addr

    def display(self, parsed, addr): 
        print(parsed)
        print(addr)
        print('***')
        print(self.users)
        print('***')

    def check_quit(self):
        return "!q" == parsed[2]

    def send(self, parsed, data):
        self.socket.sendto(data, self.users[parsed[1]])

    def start(self):
        stop = False
        while not stop:
            try:    
                data, addr = self.receive()
                parsed = self.parse(data)
                self.set_db(parsed, addr)
                self.display(parsed, addr)
                self.send(parsed, data)
                stop = check_quit(parsed)
            except:
                pass
        self.close_socket()

myServ = Server(8888)
myServ.init_socket()
myServ.start()
