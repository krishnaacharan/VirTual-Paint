import cv2
import requests
import numpy as np

mycolors=[[24,55,53,100,255,255],[5,107,0,19,255,255],[133,56,0,159,155,255]]

mycolorvalues=[[255,0,255],[51,153,255],[0,255,0]]


#cv2.namedWindow("Trackbars")
#cv2.resizeWindow("Trackbars",300,400)
#cv2.createTrackbar("h_min","Trackbars",0,179,empty)
#cv2.createTrackbar("h_max","Trackbars",0,179,empty)
#cv2.createTrackbar("s_min","Trackbars",0,255,empty)
#cv2.createTrackbar("s_max","Trackbars",0,255,empty)
#cv2.createTrackbar("v_min","Trackbars",0,255,empty)
#cv2.createTrackbar("v_max","Trackbars",0,255,empty)
myPoints=[]
def drawCanvas(myPoints,mycolorvalues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 30, mycolorvalues[point[2]], cv2.FILLED)

def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>800:
            cv2.drawContours(imgResult,cnt,-1,(255,255,0),3)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.01*peri,True)
            x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y

def findColor(render,mycolors,mycolorvalues):
    count=0
    imgHsv2=cv2.cvtColor(render,cv2.COLOR_BGR2HSV)
    newPoints=[]
    #h_min=cv2.getTrackbarPos("h_min","Trackbars")
    #h_max = cv2.getTrackbarPos("h_max", "Trackbars")
    #s_min = cv2.getTrackbarPos("s_min", "Trackbars")
    #s_max = cv2.getTrackbarPos("s_max", "Trackbars")
    #v_min = cv2.getTrackbarPos("v_min", "Trackbars")
    #v_max = cv2.getTrackbarPos("v_max", "Trackbars")
    for color in mycolors:
        lower = np.array([mycolors[0:4]])
        upper = np.array([mycolors[4:7]])
        mask = cv2.inRange(imgHsv2, (24,55,53), (100,255,255))
        imgRes = cv2.bitwise_and(render,render,mask=mask)
        x,y=getContours(mask)
        cv2.circle(imgResult, (x, y), 10, mycolorvalues[count], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
    return newPoints

while True:
    #For people with no webcam Download IP Webcam on phone and type ip address
    image = requests.get("http://26.21.68.127:8080/shot.jpg")
    video = np.array(bytearray(image.content), dtype=np.uint8)
    render = cv2.imdecode(video, 1)
    #for people with Webcam
    """VID =cv2.VideoCapture(0)
    val,render=VID.read()"""
    imgResult=render.copy()
    newPoints=findColor(render,mycolors,mycolorvalues)
    if len(newPoints)!=0:
        for new in newPoints:
            myPoints.append(new)
    drawCanvas(myPoints,mycolorvalues)
    cv2.imshow("res", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


   # cv2.imshow("1",imgHsv)
    #cv2.imshow("2",imgHsv2)
# cv2.imshow("3",mask)
