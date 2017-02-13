import re
import socket
import time

port = 8888

users = {}

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = s.getsockname()[0]
s.bind((host, port))
s.setblocking(0)
print("Server is running...")

while True:
    try:
        data, addr = s.recvfrom(1024)
        decoded_data = data.decode()
        parsed_data = re.split(':+', decoded_data)
        print(parsed_data)
        #parsed_data[0] = name of source
        #parsed_data[1] = name of recipient
        #parsed_data[2] = message

        print(addr)

        print(users)
        #print(users[parsed_data[1]])  

        if(parsed_data[0] not  in users.keys()):
            users[parsed_data[0]] = addr

        if(users[parsed_data[0]] != addr):
            users[parsed_data[0]] = addr

        s.sendto(data, users[parsed_data[1]])

        #if("!q" == parsed_data[2]):
        #    quitting = True
                
        #print(time.ctime(time.time()) + str(addr) + ':  :' + str(data))

                
        #if("/users" == parsed_data[2]):
        #    s.sendto(users.keys(), users[parsed_data[0]])

    except:
        pass 

s.close()
