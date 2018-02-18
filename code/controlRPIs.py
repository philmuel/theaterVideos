# script to control raspberry pis during performance

import socket
import pdb
from time import sleep


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect(('139.19.64.86',55555))


sock.sendall('pause_0')
sleep(2)

sock.sendall('pause_3')
sleep(5)

sock.sendall('play_5')


sock.sendall('term')
