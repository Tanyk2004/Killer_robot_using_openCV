import cv2
import RPi.GPIO as GPIO
from time import sleep
import serial

faceCentreX = 0
faceCentreY = 0
direction = 2
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup( 7 ,GPIO.OUT) #right backward
GPIO.setup( 8 ,GPIO.OUT) #right forward
GPIO.setup( 11 ,GPIO.OUT)# left backward
GPIO.setup( 12 ,GPIO.OUT)#left forward
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.output(13, GPIO.HIGH)
rightBackward = GPIO.PWM(7, 100)
rightForward = GPIO.PWM(8, 100)
leftForward = GPIO.PWM(11, 100)
leftBackward = GPIO.PWM(12, 100)
w1 = 0
h1 = 0
rightBackward.start(0)
rightForward.start(0)
leftForward.start(0)
leftBackward.start(0)

def forwardFast():
    rightForward.ChangeDutyCycle(100)
    leftForward.ChangeDutyCycle(100)
    leftBackward.ChangeDutyCycle(0)
    rightBackward.ChangeDutyCycle(0)
def forward():
    rightForward.ChangeDutyCycle(50)
    leftForward.ChangeDutyCycle(50)
    leftBackward.ChangeDutyCycle(0)
    rightBackward.ChangeDutyCycle(0)
def backward():
    rightForward.ChangeDutyCycle(0)
    leftForward.ChangeDutyCycle(0)
    rightBackward.ChangeDutyCycle(50)
    leftBackward.ChangeDutyCycle(50)
def left():
    rightForward.ChangeDutyCycle(30)
    rightBackward.ChangeDutyCycle(0)
    leftForward.ChangeDutyCycle(0)
    leftBackward.ChangeDutyCycle(30)
def right():
    rightForward.ChangeDutyCycle(0)
    rightBackward.ChangeDutyCycle(30)
    leftForward.ChangeDutyCycle(30)
    leftBackward.ChangeDutyCycle(0)
def stop():
    rightForward.ChangeDutyCycle(0)
    rightBackward.ChangeDutyCycle(0)
    leftForward.ChangeDutyCycle(0)
    leftBackward.ChangeDutyCycle(0)
cap = cv2.VideoCapture(0)
GPIO.output(15, GPIO.HIGH)
GPIO.output(16, GPIO.LOW)
face_cascade = cv2.CascadeClassifier('/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_default.xml')
width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
screenCentre = (width/2)+1;

referencePoint1 = 320 * (3/10)
referencePoint2 = 320 * (7/10)

while(True):
      
    _, img = cap.read()
    img = cv2.resize(img, (320, 320))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3,5)
    if( len(faces) == 0):
        stop()
        print(" faces not found")
        GPIO.output(15, GPIO.LOW)
        GPIO.output(16, GPIO.HIGH)
        print("The width and the height of the face when not recognizing it:" ,w1 ,h1)
        if(w1 >= 150 and h1 >= 150):
            forwardFast()
            GPIO.output(15, GPIO.HIGH)
            GPIO.output(16, GPIO.HIGH)
            print("going forward")
            sleep(5)
            print("now not going forward")
            w1 = 0
            h1 = 0
        
    else :
        print("recognising faces")
        GPIO.output(15, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        
    for(x,y,w,h) in faces:
        faceCentreX = x + (w  / 2)
        print("the width and the height of the face:" , w , h)
        
       # print("The coordinates of the face are: " , x, y)
        #print("Face Centre :" , (faceCentreX))
        if( faceCentreX  <= referencePoint1):
            print("Going left")
            left()
        elif(faceCentreX >= referencePoint2):
            print("Going right")
            right()
        else:
            print("Going forward")
            forward()
        if( w >= 140 and h >= 140):
            w1 = w
            h1 = h
            GPIO.output(15, GPIO.HIGH)
            GPIO.output(16, GPIO.HIGH)
        #img = cv2.rectangle(img, (x,y) , (x+w , y+h), (255, 0,0) ,2)
    #cv2.imshow('img', img)
    
    
    
    if(cv2.waitKey(1) & 0xFF == ord('f')):
       cv2.destroyAllWindows()
       break

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
