import socket
import time

host = 'localhost'
port = 8888

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

quitting = False
print('Server running...')

while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        if("!q" in str(data)):
            quitting = True
        if(addr not in clients):
            clients.append(addr)

        print(time.ctime(time.time()) + str(addr) + ':  :' + str(data))
        for client in clients: 
            if(client != addr): 
                s.sendto(data, client)
                print(data, client)
                
                if("/users" in str(data)):
                   s.sendto(clients, client)

    except:
        pass

s.close()
