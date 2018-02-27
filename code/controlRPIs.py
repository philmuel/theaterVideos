# script to control raspberry pis during performance

import socket
import pdb
from time import sleep
import numpy as np

print('---- TV CONTROLLER VERSION 0.01 ----')

<<<<<<< HEAD
raspi_ips = {0:'169.254.207.187',1:'169.254.137.192',
            2:'169.254.135.242',3:'169.254.150.32',4:'169.254.219.217'}
raspi_ids = sorted(raspi_ips.keys())
=======
raspi_ips = {0:'192.168.178.36',1:'192.168.178.23',2:'192.168.178.42',
             1:'192.168.178.39',1:'192.168.178.43'}
>>>>>>> fff8d554a31b710c481542251f10a199dec3f8ec
socks_for_raspis = {}
for raspi_id, raspi_ip in raspi_ips.iteritems():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((raspi_ip,55555))
    socks_for_raspis[raspi_id] = sock
sleep(30)

scenarioList = ['1.4','b','1.6','b','2','b','3']
#scenarioStarts = {'1.4':60*120,'b':0,'1.6':60*130,'b':0,'2':60*140,'b':0,'3':60*50}
scenarioStarts = {'1.4':60*60,'b':0,'1.6':60*70,'b':0,'2':60*80,'b':0,'3':60*95}
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
    if not chosenScenario=='3':
        scenarioStartTime = scenarioStarts[chosenScenario]
        cmd = 'play_'+str(scenarioStartTime)
        print('sending '+cmd)
        for raspi_sock in socks_for_raspis.values():
            raspi_sock.sendall(cmd)
    if chosenScenario=='2':
        done = False
        for raspi_sock in socks_for_raspis.values():
            # switch one raspi at a time to noise
            while True:
                response = raw_input('enter "p" to progress: ')
                if response=='p':
                    cmd = 'play_'+str(scenarioStarts['2']+5*60)
                    raspi_sock.sendall(cmd)
                    break
                elif response=='b':
                    print('going to black screen')
                    done = True
                    break
            if done: break
    if chosenScenario=='3':
        # first switch on single looped videos
        done = False
        for raspi_id in raspi_ids:
            raspi_sock = socks_for_raspis[raspi_id]
            cmd = 'play_'+str(scenarioStarts['3'])
            print('at raspi_id '+str(raspi_id))
            print('sending '+cmd)
            raspi_sock.sendall(cmd)
            if raspi_id==np.max(raspi_ids):
                print('ATTENTION: next one is FAST!!!')
            response = raw_input('enter something to progress, "b" for black screens: ')
            if response=='b':
                print('going to black screen')
                done = True
                break
        if done: continue
        # now add in additional videos:
#        for raspi_id in raspi_ids:
#            print('adding additional videos, raspi_id '+str(raspi_id))
#            raspi_sock = socks_for_raspis[raspi_id]
#            cmd = 'play_'+str(scenarioStarts['3']+10*60)
#            raspi_sock.sendall(cmd)
#            if raspi_id==np.max(raspi_ids):
#                print('ATTENTION: next one is FAST!!!')
#            response = raw_input('enter something to progress, "b" for black screens: ')
#            if response=='b':
#                print('going to black screen')
#                done = True
#                break
#        if done: continue
        print('now setting all to FAST!')
        for raspi_sock in socks_for_raspis.values():
            cmd = 'play_'+str(scenarioStarts['3']+20*60)
            raspi_sock.sendall(cmd)
   



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
