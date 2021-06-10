import cv2
import numpy as np
import pickle

# Reading the mapping values for stereo image rectification
with open('cam_settings.pkl', 'rb') as f:
    cam_settings = pickle.load(f)
    Left_Stereo_Map_x = cam_settings['left']['mapx']
    Left_Stereo_Map_y = cam_settings['left']['mapy']
    Right_Stereo_Map_x = cam_settings['right']['mapx']
    Right_Stereo_Map_y = cam_settings['right']['mapy']
 
# disparity settings
window_size = 5
min_disp = 0
num_disp = 96 - min_disp
stereo = cv2.StereoSGBM_create()

def nothing(x):
    pass

cv2.namedWindow('disp',cv2.WINDOW_NORMAL)
cv2.resizeWindow('disp',1200,1600)
# Updating the parameters based on the trackbar positions
cv2.createTrackbar('numDisparities','disp',1,17,nothing)
cv2.createTrackbar('blockSize','disp', 5, 50, nothing)
cv2.createTrackbar('uniquenessRatio','disp', 5, 15, nothing)
cv2.createTrackbar('speckleRange','disp', 0, 100, nothing)
cv2.createTrackbar('speckleWindowSize','disp', 3, 25, nothing)
cv2.createTrackbar('disp12MaxDiff','disp', 5, 25, nothing)
cv2.createTrackbar('minDisparity','disp', 0, 25, nothing)
cv2.createTrackbar('windowSize', 'disp', 3, 11, nothing)
cv2.createTrackbar('preFilterCap','disp',0,62,nothing)

# morphology settings
kernel = np.ones((12,12),np.uint8)
 
# load stereo image
image_left= cv2.imread(r".\\temp\\New allign\\left\\test11-59-46-152627.jpg")
image_right= cv2.imread(r".\\temp\\New allign\\right\\test11-59-43-900609.jpg")
#image_left = cv2.cvtColor(image_left,cv2.COLOR_BGR2GRAY)
#image_right = cv2.cvtColor(image_right,cv2.COLOR_BGR2GRAY)

# Applying stereo image rectification on the left image
Left_nice= cv2.remap(image_left,
                    Left_Stereo_Map_x,
                    Left_Stereo_Map_y,
                    cv2.INTER_LANCZOS4,
                    cv2.BORDER_CONSTANT,
                    0)

# Applying stereo image rectification on the right image
Right_nice= cv2.remap(image_right,
                    Right_Stereo_Map_x,
                    Right_Stereo_Map_y,
                    cv2.INTER_LANCZOS4,
                    cv2.BORDER_CONSTANT,
                    0)
#out = Right_nice.copy()
#out[:,:,0] = Right_nice[:,:,0]
#out[:,:,1] = Right_nice[:,:,1]
#out[:,:,2] = Left_nice[:,:,2]
#cv2.imshow("Output image", out)
#cv2.waitKey(0)

#image_left = cv2.imread('image_left/image_left_{}.png'.format(filename))
#image_right = cv2.imread('image_right/image_right_{}.png'.format(filename))

while True:
    # compute disparity
    # Setting the updated parameters before computing disparity map
    numDisparities = cv2.getTrackbarPos('numDisparities','disp')*16
    blockSize = cv2.getTrackbarPos('blockSize','disp')*2
    uniquenessRatio = cv2.getTrackbarPos('uniquenessRatio','disp')
    speckleRange = cv2.getTrackbarPos('speckleRange','disp')
    speckleWindowSize = cv2.getTrackbarPos('speckleWindowSize','disp')*2
    disp12MaxDiff = cv2.getTrackbarPos('disp12MaxDiff','disp')
    minDisparity = cv2.getTrackbarPos('minDisparity','disp')
    windowSize = cv2.getTrackbarPos('windowSize', 'disp')
    preFilterCap = cv2.getTrackbarPos('preFilterCap','disp')

    stereo.setNumDisparities(numDisparities)
    stereo.setBlockSize(blockSize)
    stereo.setUniquenessRatio(uniquenessRatio)
    stereo.setSpeckleRange(speckleRange)
    stereo.setSpeckleWindowSize(speckleWindowSize)
    stereo.setDisp12MaxDiff(disp12MaxDiff)
    stereo.setMinDisparity(minDisparity)
    stereo.setP1(8 * 3 * window_size ** 2)
    stereo.setP2(32 * 3 * window_size ** 2)
    stereo.setPreFilterCap(preFilterCap)

    disparity = stereo.compute(Left_nice, Right_nice).astype(np.float32) / 16.0
    disparity = (disparity-min_disp)/num_disp

    # apply threshold
    #threshold = cv2.threshold(disparity, 0.6, 1.0, cv2.THRESH_BINARY)[1]

    # apply morphological transformation
    #morphology = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)

    # show images
    #cv2.imshow('left eye', image_left)
    #cv2.imshow('right eye', image_right)
    cv2.imshow('disp', disparity)
    #cv2.imshow('threshold', threshold)
    #cv2.imshow('disp', morphology)
    if cv2.waitKey(1) == 27:
        break
