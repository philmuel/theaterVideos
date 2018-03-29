# theaterVideos
This is code I quickly wrote for a theater project in which a bunch of TVs on stage played videos.
In front of each TV there is a raspberry pi and they in turn are controlled via LAN.

buildVideos.py generates the videos to be played using open cv.
playVideo.py is the program running on each of the raspberry pis waiting for incoming messages to jump to a certain point in the video.
controlRPIs.py is the program running on an additional computer in the network from which the presentation can be controlled via keyboard inputs.
