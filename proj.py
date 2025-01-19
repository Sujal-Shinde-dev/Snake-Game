import cvzone
import cv2
import numpy as np
import math
import random
from cvzone.HandTrackingModule import HandDetector


capture=cv2.VideoCapture(0)
capture.set(3,1280)
capture.set(4,720)

detect=HandDetector(detectionCon=0.8,maxHands=1)

class snake:
    def __init__(self,foodPath):
        self.point = []  
        self.length = []  
        self.currentLength = 0  
        self.TotalAllowedLength = 150  
        self.headPrevious = 0, 0
        
        self.foodimg=cv2.imread(foodPath,cv2.IMREAD_UNCHANGED)
        self.foodHeight,self.foodWidth,_=self.foodimg.shape
        self.foodLocation=0,0
        self.FoodLocationRandom()
        self.score=0
        self.gameOver=False
        
    def FoodLocationRandom(self):
        self.foodLocation=random.randint(100,1000),random.randint(100,600)
        
    def update(self,mainImg,headCurrent):
        if self.gameOver:
            cvzone.putTextRect(mainImg,"GameOver",[250,350],scale=8,thickness=4,colorT=(255,255,255),colorR=(0,0,255),offset=20)
            cvzone.putTextRect(mainImg,f"Your Score:{self.score}",[250,500],scale=8,thickness=5,colorT=(255,255,255),colorR=(0,0,255),offset=20)
        else:
             previousX,previousY=self.headPrevious
             currentX,currentY=headCurrent
             
             self.point.append([currentX,currentY])
             distance=math.hypot(currentX-previousX,currentY-previousY)
             self.length.append(distance)
             self.currentLength+=distance
             self.headPrevious=currentX,currentY
             
             if self.currentLength>self.TotalAllowedLength:
                 for i,length in enumerate(self.length):
                     self.currentLength -=length
                     self.length.pop(i)
                     self.point.pop(i)
                     
                     if self.currentLength<self.TotalAllowedLength:
                         break
                     
             randomX,randomY=self.foodLocation
             if(
                 randomX-self.foodWidth//2<currentX<randomX+self.foodWidth//2
                 and randomY-self.foodHeight//2 < currentY <randomY+self.foodHeight//2):
                 self.FoodLocationRandom()
                 self.TotalAllowedLength +=50
                 self.score+=1
                 print(self.score)
                 
             if self.point:
                 for i,point in enumerate(self.point):
                     if i!=0:
                         cv2.line(mainImg,self.point[i-1],self.point[i],(0,0,255),20)
                 cv2.circle(img,self.point[-1],20,(200,0,200),cv2.FILLED)
                 
             point=np.array(self.point[:-2],np.int32)
             point=point.reshape((-1,1,2))
             cv2.polylines(mainImg,[point],False,(0,200,0),3)
             minDist=cv2.pointPolygonTest(point,(currentX,currentY),True)
             
             if -1 <=minDist<=1:
                 print("hit")
                 self.gameOver = True
                 self.point = []
                 self.length = []
                 self.currentLength = 0
                 self.TotalAllowedLength = 150
                 self.headPrevious = 0, 0
                 self.FoodLocationRandom() 
            
             randomX,randomY=self.foodLocation
             mainImg=cvzone.overlayPNG(mainImg,self.foodimg,
                                    (randomX-self.foodWidth//2,randomY-self.foodHeight//2))
             
             cvzone.putTextRect(mainImg,f"Your Score :{self.score}",[50,80],scale=3,thickness=3,offset=10)
        return mainImg
game=snake("Donut.png")
restart_game=False

while True:
    success,img=capture.read()
    img=cv2.flip(img,1)
    hand,img=detect.findHands(img,flipType=False)
    
    if hand:
        landmarkList=hand[0]['lmList']
        pointIndex=landmarkList[8][0:2]
        img=game.update(img,pointIndex)
    
    cv2.imshow("Image",img)
    key=cv2.waitKey(1)
    if key == ord('r'):
        game.gameOver = False
        game.score = 0  
        restart_game = True

    if restart_game:
        game = snake("Donut.png") 
        restart_game = False

    if key == ord('q'):
        break
    
                 