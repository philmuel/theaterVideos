import cv2
import numpy as np
import pdb

fps = 30.0
raspi_ids = range(2)

#dataDir = '/Users/philipp/Documents/theater/push_up/tv_project/'
dataDir = '/home/pmueller/pushup/'

imgInDir = dataDir+'images_raw/'
videoInDir = dataDir+'videos_raw/'
outDir = dataDir+'videos_out/'

out_width = 720
out_height = 480


def addBlackPadding(out,secs=2):
    blackFrame = np.zeros((out_height*2,out_width,3),dtype='uint8')
    for i in range(int(secs*fps)):
        out.write(blackFrame)
    return out
  

def resizeImage(img):
    size_multiplier = float(out_width)/img.shape[1]
    new_height = int(img.shape[0]*size_multiplier)
    img = cv2.resize(img,(out_width,new_height))
    lowerPadding = np.zeros((2*out_height-new_height,out_width,3),dtype='uint8')
    img = np.concatenate([img,lowerPadding],axis=0)
    return img


def addStaticImg(out,imPath,secs=2):
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
    out = addBlackPadding(out)
    videoWriters[raspi_id] = out




# --------------------------------------------
# STATIC IMGS FOR SCENE 1
# --------------------------------------------

for raspi_id in raspi_ids:
    # get video writer for raspi_id
    out = videoWriters[raspi_id]
    # first add image for scene 1.4
    imPath = imgInDir+'14_'+str(raspi_id)+'.jpg'
    out = addStaticImg(out,imPath)
    # then for scene 1.6
    imPath = imgInDir+'16_'+str(raspi_id)+'.jpg'
    out = addStaticImg(out,imPath)
    out = addBlackPadding(out)
    videoWriters[raspi_id] = out



# --------------------------------------------
# VIDEOS FOR SCENE 2
# --------------------------------------------
fade_in_time = 3 # seconds of linear fade in
for raspi_id in raspi_ids:
    print('writing videos for scene 2, raspi = '+str(raspi_id))
    out = videoWriters[raspi_id]
    videoPath = videoInDir+'s2_'+str(raspi_id)+'.mp4'
    # first, keep repeating light leak video for 5 minutes (fading in and out if video too short)
    cap = cv2.VideoCapture(videoPath)
    for i in range(int(5*60*fps)):
        ret,frame = cap.read()
        if i<fade_in_time*fps:
            fade_in_multiplier = float(i)/(fade_in_time*fps)
            frame = (frame*fade_in_multiplier).astype('uint8')
        frame = resizeImage(frame)
        out.write(frame)
    # then noise for 10 minutes
    for i in range(int(10*60*fps)):
        frame = np.random.randint(0,255,(120,180,1)).astype('uint8')
        frame = np.concatenate([frame]*3,axis=2)
        frame = resizeImage(frame)
        out.write(frame)



# --------------------------------------------
# VIDEOS FOR SCENE 3
# --------------------------------------------





# finally, close all video out files
for raspi_id in raspi_ids:
    videoWriters[raspi_id].release()
