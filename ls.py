import socket
import sys
import select
from timeit import default_timer as timer

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsListenPort = int(sys.argv[1])
ts1Hostname = sys.argv[2]
ts1ListenPort = int(sys.argv[3])
ts2Hostname = sys.argv[4]
ts2ListenPort = int(sys.argv[5])

s.bind(('', lsListenPort))
s.listen(5)
while True:
    c, addr = s.accept()
    str = c.recv(1024).decode().strip()
    s1 = socket.socket()
    s1.connect((ts1Hostname, ts1ListenPort))
    s2 = socket.socket()
    s2.connect((ts2Hostname, ts2ListenPort))
    s1.send(str.encode())
    s2.send(str.encode())
    rem_time = 5
    received = False
    t1 = timer()
    while True:
        rlist, wlist, xlist = select.select([s1,s2],[],[],rem_time)
        t2 = timer()
        rem_time = rem_time - (t2 - t1)
        t1 = t2
        if(s1 in rlist and len(s1.recv(1, socket.MSG_PEEK)) > 0):
            c.send(s1.recv(1024).decode().encode())
            received = True
            break
        elif(s2 in rlist and len(s2.recv(1, socket.MSG_PEEK)) > 0):
            c.send(s2.recv(1024).decode().encode())
            received = True
            break
        else:
            if(rem_time <= 0):
                break
    if(not received):
        c.send((str + " - Error:HOST NOT FOUND").encode())
    s1.close()
    s2.close()
    c.close()
