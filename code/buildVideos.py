import cv2
import numpy as np
import pdb

fps = 30.0
raspi_ids = range(2)


imgInDir = '/Users/philipp/Documents/theater/push_up/tv_project/images_raw/'
videoInDir = '/Users/philipp/Documents/theater/push_up/tv_project/videos_raw/'
outDir = '/Users/philipp/Documents/theater/push_up/tv_project/videos_out/'

out_width = 720
out_height = 480


def addBlackPadding(out,secs=2):
    blackFrame = np.zeros((out_width,out_height,3))
    for i in range(secs*fps):
        out.write(blackFrame)
    


# open out video files and add initial black padding
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_videoFiles = {}
for raspi_id in raspi_ids:
    curr_outPath = outDir+'raspi'+str(raspi_id)+'.avi'
    out = cv2.VideoWriter(out_path,
                        fourcc,fps,(out_width,out_height*2))
    addBlackPadding(out)
    out_videoFiles[raspi_id] = out




# --------------------------------------------
# STATIC IMGS FOR SCENE 1
# --------------------------------------------

for raspi_id in raspi_ids:
   

# resize imagfe with opencv:
#resized_image = cv2.resize(image, (100, 50)) 



# finally, close all video out files
for raspi_id in raspi_ids:
    out_videoFiles[raspi_id].release()
