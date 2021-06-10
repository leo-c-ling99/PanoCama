# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2
import matplotlib.pyplot as plt

# grab the paths to the input images and initialize our images list
print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images(
    ".\\temp\\stitch_test")))
images = []
# loop over the image paths, load each one, and add them to our
# images to stich list
for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    images.append(image)

def warpTwoImages(img1, img2, H):
    '''warp img2 to img1 with homograph H'''
    h1,w1 = img1.shape[:2]
    h2,w2 = img2.shape[:2]
    pts1 = np.float32([[0,0],[0,h1],[w1,h1],[w1,0]]).reshape(-1,1,2)
    pts2 = np.float32([[0,0],[0,h2],[w2,h2],[w2,0]]).reshape(-1,1,2)
    pts2_ = cv2.perspectiveTransform(pts2, H)
    pts = np.concatenate((pts1, pts2_), axis=0)
    [xmin, ymin] = np.int32(pts.min(axis=0).ravel() - 0.5)
    [xmax, ymax] = np.int32(pts.max(axis=0).ravel() + 0.5)
    t = [-xmin,-ymin]
    Ht = np.array([[1,0,t[0]],[0,1,t[1]],[0,0,1]]) # translate

    result = cv2.warpPerspective(img2, Ht.dot(H), (xmax-xmin, ymax-ymin))
    result[t[1]:h1+t[1],t[0]:w1+t[0]] = img1
    return result


img_ = images[6]
img1 = cv2.cvtColor(img_,cv2.COLOR_BGR2GRAY)

img = images[7]
img2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

sift = cv2.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2) 

#print matches
# Apply ratio test
good = []
for m in matches:
     if m[0].distance < 0.5*m[1].distance:         
     	good.append(m)
matches = np.asarray(good)

if len(matches[:,0]) >= 4:
	dst_pts = np.float32([kp1[m.queryIdx].pt for m in matches[:,0]]).reshape(-1,1,2)
	src_pts = np.float32([kp2[m.trainIdx].pt for m in matches[:,0]]).reshape(-1,1,2)
	M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

result = warpTwoImages(img_, img, M)
plt.imshow(result)
plt.show()
cv2.imwrite('panorama2.jpg', result)
