#!/usr/bin/env python3

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import logging
logging.basicConfig(level=logging.INFO)
import socket
import pdb


noCommMode = False

if not noCommMode:
    HOST = ''
    PORT = 55555
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST,PORT))
    sock.listen(1)
    conn,addr = sock.accept()


vidPath = "raspi.avi"
player_log = logging.getLogger("Player 1")

player = OMXPlayer(vidPath, 
                dbus_name='org.mpris.MediaPlayer2.omxplayer1')
player.playEvent += lambda _: player_log.info("Play")
player.pauseEvent += lambda _: player_log.info("Pause")
player.stopEvent += lambda _: player_log.info("Stop")

player.set_aspect_mode('stretch')
player.set_video_pos(0, 0, 700, int(512*2.14))
sleep(10)
#player.pause()
#player.set_position(0)
#player.play()
#sleep(10)
#player.pause()



if noCommMode:
    #player.play()
    #sleep(1)
    #player.pause()
    #player.pause()
#    sleep(10)
    player.set_position(120*60)
#    player.play()
#    sleep(1)
#    player.pause()
    sleep(20)
    player.set_position(130*60)
#    player.play()
    sleep(20)
    player.set_position(140*60)
    sleep(20)
    player.stop()

else:
    while True:
        data = conn.recv(1024)
        print('received: '+str(data))
        if data=='term':
            break
        if '_' in data:
            cmd = data.split('_')[0]
            arg = float(data.split('_')[1])
            if cmd=='pause':
                player.set_position(arg)
                player.play()
                sleep(10)
                player.pause()
            elif cmd=='play':
                player.set_position(arg)
#                player.play()

    


conn.close()
player.quit()

#sleep(2.5)

#player.set_position(5)
#player.pause()


#player.play()

#sleep(5)

