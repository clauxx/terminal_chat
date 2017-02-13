import re
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
                data_decoded = data.decode()
                parsed = re.split(":+", data_decoded)
                print("\n" + "(" + time.ctime(time.time()) + ")" + "{" + parsed[0] + "}" + "> " + parsed[2])
        except:
            pass
        finally:    
            tLock.release()

port = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = s.getsockname()[0]
server = ('192.168.178.113', 8888)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receiving, args=("RecvThread", s))
rT.start()

name = input("Your name: ")
target = input("Other user's name: ")
message = ""
while message != "!q":
    message = input("(" + time.ctime(time.time()) + ")" + "[" +  name + "]" + "> ")
    if message != "":
        fin_mess = name + "::" + target + "::" +  message
        s.sendto(fin_mess.encode(), server)
    tLock.acquire()
    tLock.release()

shutdown = True
rT.join()
s.close()
