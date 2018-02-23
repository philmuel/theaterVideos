# script to control raspberry pis during performance

import socket
import pdb
from time import sleep

print('---- TV CONTROLLER VERSION 0.01 ----')

raspi_ips = {0:'192.168.1.18'}
socks_for_raspis = {}
for raspi_id, raspi_ip in raspi_ips.iteritems():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((raspi_ip,55555))
    socks_for_raspis[raspi_id] = sock
sleep(30)

scenarioList = ['1.4','b','1.6','b','2','b','3']
scenarioStarts = {'1.4':60*10,'b':0,'1.6':60*20,'b':0,'2':60*30,'b':0,'3':60*50}
scenarioPointer = 0

while True:
    response = raw_input('enter "n" for next scenario ('+scenarioList[scenarioPointer]\
            +'), or "b" for black screen: ')
    if not response in scenarioList+['n']:
        print('invalid scenario name, try again!')
        continue
    if response=='n':
        chosenScenario = scenarioList[scenarioPointer]
        scenarioPointer += 1
    else:
        chosenScenario = response
    scenarioStartTime = scenarioStarts[chosenScenario]
    cmd = 'play_'+str(scenarioStartTime)
    print('sending '+cmd)
    for raspi_sock in socks_for_raspis.values():
#        sock.sendto(cmd.encode('utf-8'),(raspi_ip,55555))
        raspi_sock.sendall(cmd)
    if chosenScenario=='2':
        response = raw_input('enter "p" to progress: ')
        # TODO: switch one raspi to noise
    
    
    



#print('sending pause_0')
#sock.sendall('pause_0')
#sleep(15)

#sock.sendall('pause_3')
#sleep(5)
#
#cmd = 'play_'+str(60*11)
#print('sending '+cmd)
#sock.sendall(cmd)
#sleep(15)
#
#cmd = 'play_'+str(60*0)
#print('sending '+cmd)
#sock.sendall(cmd)
#sleep(15)
#
#cmd = 'play_'+str(60*21)
#print('sending '+cmd)
#sock.sendall(cmd)
#sleep(15)
#
#cmd = 'play_'+str(60*0)
#print('sending '+cmd)
#sock.sendall(cmd)
#sleep(15)
#
#
#cmd = 'play_'+str(60*30)
#print('sending '+cmd)
#sock.sendall(cmd)
#sleep(15)
#
#
#
#cmd = 'play_'+str(60*36)
#print('sending '+cmd)
#sock.sendall(cmd)
#sleep(15)



sock.sendall('term')
