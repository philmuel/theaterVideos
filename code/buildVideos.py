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
    blackFrame = np.zeros((out_height*2,out_width,3),dtype='uint8')
    for i in range(int(secs*fps)):
        out.write(blackFrame)
    return out
   
def addStaticImg(out,imPath,secs=2):
    img = cv2.imread(imPath)
    # resize image to dimensions of video
#    img = np.swapaxes(img,0,1)
    size_multiplier = float(out_width)/img.shape[1]
    new_height = int(img.shape[0]*size_multiplier)
    img = cv2.resize(img,(out_width,new_height))
    lowerPadding = np.zeros((2*out_height-new_height,out_width,3),dtype='uint8')
    img = np.concatenate([img,lowerPadding],axis=0)
    for i in range(int(secs*fps)):
        out.write(img)
    return out



# open out video files and add initial black padding
fourcc = cv2.VideoWriter_fourcc(*'XVID')
videoWriters = {}
for raspi_id in raspi_ids:
    out_path = outDir+'raspi'+str(raspi_id)+'.avi'
    out = cv2.VideoWriter(out_path,
                        fourcc,fps,(out_width,out_height*2))
    out = addBlackPadding(out)
    videoWriters[raspi_id] = out




# --------------------------------------------
# STATIC IMGS FOR SCENE 1
# --------------------------------------------

for raspi_id in raspi_ids:
    # get video writer for raspi_id
    out = videoWriters[raspi_id]
    # first add image forscene 1.4
    imPath = imgInDir+'14_'+str(raspi_id)+'.jpg'
    out = addStaticImg(out,imPath)
    # then for scene 1.6
    imPath = imgInDir+'16_'+str(raspi_id)+'.jpg'
    out = addStaticImg(out,imPath)
    out = addBlackPadding(out)
    videoWriters[raspi_id] = out


# to resize image with opencv:
#resized_image = cv2.resize(image, (100, 50)) 



# finally, close all video out files
for raspi_id in raspi_ids:
    videoWriters[raspi_id].release()
