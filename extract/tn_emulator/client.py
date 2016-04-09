import socket

for i in range(0, 1):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('192.168.1.2', 9999))
        clientsocket.send('40,40')
        clientsocket.close()
