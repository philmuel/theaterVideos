import cv2
import numpy as np
import glob
import pdb

fps = 30.0
raspi_ids = range(2)

#dataDir = '/Users/philipp/Documents/theater/push_up/tv_project/'

# TODO: add videos for scene 3

dataDir = '/home/pmueller/pushup/'

imgInDir = dataDir+'images_raw/'
videoInDir = dataDir+'videos_raw/'
outDir = dataDir+'videos_out/'

out_width = 656
out_height = 512


def addBlackPadding(out,secs=10*60):
    blackFrame = np.zeros((out_height*2,out_width,3),dtype='uint8')
    for i in range(int(secs*fps)):
        out.write(blackFrame)
    return out
 

def padImage(img,direction,n_pix):
    n_pix1 = int(np.floor(n_pix/2.0))
    n_pix2 = int(np.ceil(n_pix/2.0))
    if direction=='vertical':
        pad_top = np.zeros((n_pix1,out_width,3),dtype='uint8')
        pad_bot = np.zeros((n_pix2,out_width,3),dtype='uint8')
        img = np.concatenate([pad_top,img,pad_bot],axis=0)
    if direction=='horizontal':
        pad_left = np.zeros((out_height,n_pix1,3),dtype='uint8')
        pad_right = np.zeros((out_height,n_pix2,3),dtype='uint8')
        img = np.concatenate([pad_left,img,pad_right],axis=1)
    return img
        


def resizeImage(img):
    imgRatio = float(img.shape[0])/img.shape[1]
    screenRatio = float(out_height)/out_width
    if imgRatio<screenRatio: # image too wide
        size_multiplier = float(out_width)/img.shape[1]
        new_height = int(img.shape[0]*size_multiplier)
        img = cv2.resize(img,(out_width,new_height))
        # pad top and bottom
        img = padImage(img,'vertical',n_pix=out_height-new_height)
    else:
        size_multiplier = float(out_height)/img.shape[0]
        new_width = int(img.shape[1]*size_multiplier)
        img = cv2.resize(img,(new_width,out_height))
        # pad left and right
        img = padImage(img,'horizontal',n_pix=out_width-new_width)
    # padd bottom with size of image to avoid displaying omxplayers messages on the screen
    lowerPadding = np.zeros((out_height,out_width,3),dtype='uint8')
    img = np.concatenate([img,lowerPadding],axis=0)
    return img


def addStaticImg(out,imPath,secs=10*60):
    img = cv2.imread(imPath)
    # resize image to dimensions of video
#    img = np.swapaxes(img,0,1)
    img = resizeImage(img)
    for i in range(int(secs*fps)):
        out.write(img)
    return out



# open out video files and add initial black padding
if cv2.__version__[:3]=='2.4':
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
else:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
videoWriters = {}
for raspi_id in raspi_ids:
    out_path = outDir+'raspi'+str(raspi_id)+'.avi'
    out = cv2.VideoWriter(out_path,
                        fourcc,fps,(out_width,out_height*2))
    out = addBlackPadding(out,1*60) # TODO: change to 120
    videoWriters[raspi_id] = out




## --------------------------------------------
## STATIC IMGS FOR SCENE 1
## --------------------------------------------
#
#for raspi_id in raspi_ids:
#    # get video writer for raspi_id
#    out = videoWriters[raspi_id]
#    # first add image for scene 1.4
#    imPath = imgInDir+'14_'+str(raspi_id)+'.jpg'
#    out = addStaticImg(out,imPath)
#    # then for scene 1.6
#    imPath = imgInDir+'16_'+str(raspi_id)+'.jpg'
#    out = addStaticImg(out,imPath)
##    out = addBlackPadding(out)
#    videoWriters[raspi_id] = out
#
#
#
## --------------------------------------------
## VIDEOS FOR SCENE 2
## --------------------------------------------
#fade_in_time = 3 # seconds of linear fade in
#for raspi_id in raspi_ids:
#    print('writing videos for scene 2, raspi = '+str(raspi_id))
#    out = videoWriters[raspi_id]
##    videoPath = videoInDir+'s2_'+str(raspi_id)+'.mp4'
#    videoPath = videoInDir+'s2_0.mp4'
#    cap = cv2.VideoCapture(videoPath)
#    # light leak video for 5 minutes, starting at different position for every raspi
#    for i in range(int(raspi_id*30*fps)):
#        ret,frame = cap.read()
#    for i in range(int(5*60*fps)):
#        ret,frame = cap.read()
#        if i<fade_in_time*fps:
#            fade_in_multiplier = float(i)/(fade_in_time*fps)
#            frame = (frame*fade_in_multiplier).astype('uint8')
#        frame = resizeImage(frame)
#        out.write(frame)
#    # then noise for 10 minutes
#    for i in range(int(10*60*fps)):
#        frame = np.random.randint(0,255,(120,180,1)).astype('uint8')
#        frame = np.concatenate([frame]*3,axis=2)
#        frame = resizeImage(frame)
#        out.write(frame)


def writeClips_scene3(out,videoPaths,speed):
    videoPath = videoPaths[np.random.randint(len(videoPaths)-1)]
    cap = cv2.VideoCapture(videoPath)
    for i in range(int(10*60*fps)):
        for _ in range(speed):
            ret,frame = cap.read()
        if not ret:
            # have to start with next video
            videoPath = videoPaths[np.random.randint(len(videoPaths)-1)]
            cap = cv2.VideoCapture(videoPath)
            ret,frame = cap.read()
        frame = resizeImage(frame)
        out.write(frame)



# --------------------------------------------
# VIDEOS FOR SCENE 3
# --------------------------------------------
videoPaths = glob.glob(videoInDir+'scene3/*.mp4')
for raspi_id in raspi_ids:
    print('writing videos for scene 3, raspi = '+str(raspi_id))
    out = videoWriters[raspi_id]
    for speed in [1,2,3,4,6]:
        print('speed = '+str(speed))
        writeClips_scene3(out,videoPaths,speed)







# finally, close all video out files
for raspi_id in raspi_ids:
    videoWriters[raspi_id].release()
