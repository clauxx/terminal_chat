import socket
import threading
import time

tLock = threading.Lock()
shutdown = False

def receiving(name, sock):
    while not shutdown:
        try:    
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print(data.decode())
        except:
            pass
        finally:    
            tLock.release()

host = 'localhost'
port = 0

server = ('localhost', 8888)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receiving, args=("RecvThread", s))
rT.start()

name = input("Name: ")
message = input(name + "> ")
while message != "!q":
    if message != "":
        fin_mess = name + ": " + message
        s.sendto(fin_mess.encode(), server)
    tLock.acquire()
    tLock.release()
    message = input(name + "> ")
    time.sleep(0.2)

shutdown = True
rT.join()
s.close()
