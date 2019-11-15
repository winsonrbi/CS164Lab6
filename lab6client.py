import socket
import sys

# create dgram udp socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print ('Failed to create socket')
	sys.exit()

host = 'localhost';
port = 8888;

while(1):
	msg = input('Enter Message to Send: ')
	msg = bytes(msg,"UTF-8")
	
	try:
		s.sendto(msg,(host,port))
		d = s.recvfrom(1024)
		reply = d[0]
		addr  = d[1]
		reply = reply.decode("utf-8")
		print ('Server reply: ' + reply)

	except socket.error as msg:
		print ('Error Code: ' + msg)
		sys.exit()
