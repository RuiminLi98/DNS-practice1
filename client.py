import socket
import sys

lsHostName = sys.argv[1]
lsListenPort = int(sys.argv[2])
file = open('PROJ2-HNS.txt')
file2 = open('RESOLVED.txt','w')

while 1:
	lines = file.readlines()
	if not lines:
		break
	for line in lines:
		s = socket.socket()
		s.connect((lsHostName, lsListenPort))
		s.send(line.encode())
		str = s.recv(1024).decode()
		str = str.strip()
		file2.write(str)
		file2.write('\n')
		s.close()
