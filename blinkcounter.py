import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np

cap = cv2.VideoCapture('Video.mp4')
detector= FaceMeshDetector(maxFaces=1)

while True:
    #Since this shuts down very quickly checks the frames in video is equal to the frames we are currently in then reset the position of the frame
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):   
        cap.set(cv2.CAP_PROP_POS_FRAMES,0) #the video keeps playing

    detector.findFaceMesh


    success, img = cap.read() 
    img= cv2.resize(img,(640,360) )  #Slow down the video player
    cv2.imshow("Image", img) #Show our image
    cv2.waitKey(1)  #1ms run