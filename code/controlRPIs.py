# script to control raspberry pis during performance

import socket
import pdb
from time import sleep


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect(('192.168.1.71',55555))
sleep(30)



#print('sending pause_0')
#sock.sendall('pause_0')
#sleep(15)

#sock.sendall('pause_3')
#sleep(5)

cmd = 'play_'+str(60*10)
print('sending '+cmd)
sock.sendall(cmd)
sleep(15)


cmd = 'play_'+str(60*20)
print('sending '+cmd)
sock.sendall(cmd)
sleep(15)

sock.sendall('term')
