import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import mediapipe as mp

# cap = cv2.VideoCapture('Video.mp4')
cap = cv2.VideoCapture(0)
detector= FaceMeshDetector(maxFaces=1)

#Create livplot
plotY=LivePlot(640,360,[20,50], invert= False)

idList=[22,23,24,26,110,157,159,158,160,161,130,243]  #based on these points we're going to find 
ratioList= []

blinkCounter=0
counter=0
color=(255,0,255)

while True:
    #Since this shuts down very quickly checks the frames in video is equal to the frames we are currently in then reset the position of the frame
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):   
        cap.set(cv2.CAP_PROP_POS_FRAMES,0) #the video keeps playing

    success, img = cap.read()
    img,faces= detector.findFaceMesh(img,draw=False)

    if faces: #we plot the points
        face=faces[0] #one face
        for id in idList:
            cv2.circle(img,face[id],5,color,cv2.FILLED)

        leftUp= face[159]
        leftDown= face[23]
        leftLeft= face[130]
        leftRight= face [243]
        lengthVer,_= detector.findDistance(leftUp,leftDown)
        lengthHor,_=detector.findDistance(leftLeft,leftRight)

        cv2.line(img,leftUp,leftDown,(0,200,0),3)
        cv2.line(img,leftLeft,leftRight,(0,200,0),3)

        ratio= int((lengthVer/lengthHor)*100)
        ratioList.append(ratio)

        if len(ratioList)> 3:
            ratioList.pop(0)

        ratioAvg= sum(ratioList)/len(ratioList)


        if ratioAvg< 35 and counter==0:
            blinkCounter += 1
            counter = 1
            color= (0,200,0)

        if counter !=0:
            counter+=1
            if counter> 10:
                counter=0
                color=(255,0,255)


        cvzone.putTextRect(img, f'Blink Count: {blinkCounter}',(50,100), colorR=color)

    
        imgPlot= plotY.update(ratioAvg, color)
        # cv2.imshow("ImagePlot", imgPlot)
        img= cv2.resize(img,(640,360) )  #resize the image

        imgStack= cvzone.stackImages([img,imgPlot],2,1)

    else:
        img= cv2.resize(img,(640,460) )  #resize the image
        imgStack= cvzone.stackImages([img,img],1,1)

     
    
    cv2.imshow("Image", imgStack) #Show our image
    cv2.waitKey(25)  #1ms run