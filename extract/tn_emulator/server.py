import numpy as np
import socket
import image
import cv2

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('192.168.1.3', 8888))
serversocket.listen(5) # become a server socket, maximum 5 connections

#def get_tile_location(img, lowbounds, highbounds, tilex, tiley, pixelx, pixely):

tilex = 40
tiley = 40
pixelx = 1280
pixely = 720
RED_LOWER = np.array([17, 15, 100])
RED_UPPER = np.array([50, 56, 200])

while True:
		data = ''
		connection, address = serversocket.accept()
		while 1:
			packet = connection.recv(1024)
			data += packet
			if not packet: break
		if len(data) > 0:
			f = open('___trash___.jpg', 'w+')
			print('before f.write(data)')
			f.write(data)
			print('before imread')
			print(len(data))
			#img = cv2.imread('___trash___.jpg')
			img = cv2.imread('___trash___.jpg')
			print("image.data: " + str(len(img.data)))
			x, y = image.get_tile_location(img, RED_LOWER, RED_UPPER, tilex, tiley, pixelx, pixely)
			y = tiley - 1 - y #because y is inverted
			
			clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			clientsocket.connect(('192.168.1.2', 9999))
			print x, y
			clientsocket.send('%d,%d'%(x, y))
			clientsocket.close()

