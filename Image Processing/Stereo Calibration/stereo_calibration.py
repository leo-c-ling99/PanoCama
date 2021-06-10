import cv2
import numpy as np
import os
import glob
import pickle

# Defining the dimensions of checkerboard
CHECKERBOARD = (6, 9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

img_ptsL = []
img_ptsR = []
obj_pts = []

# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

# Extracting path of individual image stored in a given directory
imagesL = glob.glob(r'.\\temp\\New allign\\left\\*.jpg')
imagesR = glob.glob(r'.\\temp\New allign\\right\\*.jpg')
for fnameLeft, fnameRight in zip(imagesL, imagesR):
    imgL = cv2.imread(fnameLeft)
    imgL_gray = cv2.cvtColor(imgL,cv2.COLOR_BGR2GRAY)
    imgR = cv2.imread(fnameRight)
    imgR_gray = cv2.cvtColor(imgR,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    #outputL = imgL_gray.copy()
    #outputR = imgR_gray.copy()

    retR, cornersR =  cv2.findChessboardCorners(imgR_gray,CHECKERBOARD,cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    retL, cornersL = cv2.findChessboardCorners(imgL_gray,CHECKERBOARD,cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

    if retR and retL:
        obj_pts.append(objp)
        corners2R = cv2.cornerSubPix(imgR_gray,cornersR,(11,11),(-1,-1),criteria)
        corners2L = cv2.cornerSubPix(imgL_gray,cornersL,(11,11),(-1,-1),criteria)
        #cv2.drawChessboardCorners(imgR,CHECKERBOARD,cornersR,retR)
        #cv2.drawChessboardCorners(imgL,CHECKERBOARD,cornersL,retL)
        #cv2.imshow('cornersR',imgR)
        #cv2.imshow('cornersL',imgL)
        #cv2.waitKey(0)

        img_ptsL.append(cornersL)
        img_ptsR.append(cornersR)

# Calibrating left camera
retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(obj_pts,img_ptsL,imgL_gray.shape[::-1],None,None)
hL,wL= imgL_gray.shape[:2]
new_mtxL, roiL= cv2.getOptimalNewCameraMatrix(mtxL,distL,(wL,hL),1,(wL,hL))
# Method 1 to undistort the imageL
dst = cv2.undistort(imgL, mtxL, distL, None, new_mtxL)

# Method 2 to undistort the image
mapx,mapy=cv2.initUndistortRectifyMap(mtxL,distL,None,new_mtxL,(wL,hL),5)

dst = cv2.remap(imgL,mapx,mapy,cv2.INTER_LINEAR)

# Displaying the undistorted image
cv2.imshow("undistorted image left",dst)


# Calibrating right camera
retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(obj_pts,img_ptsR,imgR_gray.shape[::-1],None,None)
hR,wR= imgR_gray.shape[:2]
new_mtxR, roiR= cv2.getOptimalNewCameraMatrix(mtxR,distR,(wR,hR),1,(wR,hR))
# Method 1 to undistort the imageL
dst = cv2.undistort(imgR, mtxR, distR, None, new_mtxR)

# Method 2 to undistort the image
mapx,mapy=cv2.initUndistortRectifyMap(mtxR,distR,None,new_mtxR,(wR,hR),5)

dst = cv2.remap(imgR,mapx,mapy,cv2.INTER_LINEAR)

# Displaying the undistorted image
cv2.imshow("undistorted image right",dst)
cv2.waitKey(0)


flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC
flags |= cv2.CALIB_FIX_ASPECT_RATIO
flags |= cv2.CALIB_FIX_FOCAL_LENGTH
# Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
# Hence intrinsic parameters are the same 

#riteria_stereo= (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
criteria_stereo= (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0)

# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retS, new_mtxL, distL, new_mtxR, distR, Rot, Trns, Emat, Fmat = cv2.stereoCalibrate(obj_pts, img_ptsL, img_ptsR, new_mtxL, distL, new_mtxR, distR, imgL_gray.shape[::-1], criteria=criteria_stereo, flags=flags)

rectify_scale= 1
rect_l, rect_r, proj_mat_l, proj_mat_r, Q, roiL, roiR= cv2.stereoRectify(new_mtxL, distL, new_mtxR, distR, imgL_gray.shape[::-1], Rot, Trns, alpha=1)

Left_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxL, distL, rect_l, proj_mat_l,
                                             imgL_gray.shape[::-1], cv2.CV_16SC2)
Right_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxR, distR, rect_r, proj_mat_r,
                                              imgR_gray.shape[::-1], cv2.CV_16SC2)

# Save the variables within the pickle file
#with open('cam_settings.pkl', 'wb') as f:
#    pickle.dump({'left':{'mapx': Left_Stereo_Map[0],
#                         'mapy': Left_Stereo_Map[1]}, 
#                'right':{'mapx': Right_Stereo_Map[0],
#                         'mapy': Right_Stereo_Map[1]}}, f)

cv2.imshow("Left image before rectification", imgL)
cv2.imshow("Right image before rectification", imgR)

Left_nice= cv2.remap(imgL,Left_Stereo_Map[0],Left_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
Right_nice= cv2.remap(imgR,Right_Stereo_Map[0],Right_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

cv2.imshow("Left image after rectification", Left_nice)
cv2.imshow("Right image after rectification", Right_nice)
cv2.waitKey(0)

out = Right_nice.copy()
out[:,:,0] = Right_nice[:,:,0]
out[:,:,1] = Right_nice[:,:,1]
out[:,:,2] = Left_nice[:,:,2]

cv2.imshow("Output image", out)
cv2.waitKey(0)