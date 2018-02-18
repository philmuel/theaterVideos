#!/usr/bin/env python3

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import logging
logging.basicConfig(level=logging.INFO)
import socket


HOST = ''
PORT = 55555
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
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
player.set_video_pos(0, 0, 2000, 1800)
player.pause()

while True:
    data = conn.recv(1024)
    pdb.set_trace()



conn.close()
player.quit()

sleep(2.5)

player.set_position(5)
#player.pause()


#player.play()

sleep(5)

