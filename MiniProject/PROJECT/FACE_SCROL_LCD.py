import cv2
import numpy as np
import face_recognition
import requests

data_to_send={}


from RPLCD import i2c
# Import sleep library
from time import sleep
# constants to initialise the LCD
lcdmode = 'i2c'
cols = 16
rows = 2
charmap = 'A00'
i2c_expander = 'PCF8574'

# Generally 27 is the address;Find yours using: i2cdetect -y 1 
address = 0x27 
port = 1 # 0 on an older Raspberry Pi
# Initialise the LCD
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
                  cols=cols, rows=rows)

# Write a string on first line and move to next line
lcd.backlight_enabled = True 

from RPLCD import *
from time import sleep
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27)
#lcd.cursor_pos = (0, 5)
#lcd.write_string('Wlcomme to')
#lcd.cursor_pos = (1, 3)
#lcd.write_string('Circuit Digest')
#sleep(2)
framebuffer = [
        '',
        '',
        ]
def write_to_lcd(lcd, framebuffer, num_cols):
        """Write the framebuffer out to the specified LCD."""
        lcd.home()
        for row in framebuffer:
            lcd.write_string(row.ljust(num_cols)[:num_cols])
            lcd.write_string('\r\n')
def long_text(text):
        if len(text)<16:
            lcd.write_string(text)            
        for i in range(len(text) - 16 + 1):
            framebuffer[1] = text[i:i+16]
            write_to_lcd(lcd, framebuffer, 16)
            sleep(0.2)


import os
from datetime import datetime
import time
# from PIL import ImageGrab
from apds9960.const import *
import board
from adafruit_apds9960.apds9960 import APDS9960

i2c = board.I2C()

apds = APDS9960(i2c)
apds.gesture_gain:0
apds.enable_proximity = True
apds.enable_gesture = True
global cap
cap = cv2.VideoCapture(0)
global dtstring
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)
 
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 
def markAttendance(name):
    global dtString
    global datestr
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            datestr=now.strftime('%Y-%m-%d')
            f.writelines(f'n{name},{dtString}')
    #cap.release()
 
#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr
 
encodeListKnown = findEncodings(images)
print('Encoding Complete')
print(time.time())
 
def apdsdetect():
    print("expecting gesture\n \n\n")
    lcd.write_string('Expecting gesture')
    while True:
        #print("expecting gesture\n \n\n")
        #lcd.write_string('Expecting gesture')
        gesture = apds.gesture()

        if ((gesture == 0x03) or (gesture == 0x04)) :
            print(gesture)
            lcd.clear()
            starttime=time.time()
            global cap
            while (time.time()-starttime<8):
                global cap
                success, img = cap.read()
    #img = captureScreen()
                imgS = cv2.resize(img,(0,0),None,0.25,0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
 
                facesCurFrame = face_recognition.face_locations(imgS)
                encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
 
                for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
                    #print(faceDis)
                    matchIndex = np.argmin(faceDis)
 
                    if matches[matchIndex]:
                        name = classNames[matchIndex].upper()
                #print(name)
                        y1,x2,y2,x1 = faceLoc
                        y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                        cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                        cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                        markAttendance(name)
                        global dtString
                        global datestr
                        print(dtString,name," Present")
                        
                        strnamepre=str(dtString+" "+datestr+" "+name+" is present")
                        #lcd.write_string(strnamepre)
                        data_to_send["Time"]=str(dtString)
                        #datestr=datetime.date.today()
                        data_to_send["Date"]=str(datestr)
                        data_to_send["Roll number"]=str(name[:7])
                        data_to_send["Name"]=str(name[8:])
                        #data_to_send["Subject"]=str('Ml')
                        data_to_send["Attendance"]=str('P')
                        print(data_to_send)
                        r=requests.post("https://hook.eu1.make.com/g9kjc2g965zrruqf7e15oz65rkpjuoiz",json=data_to_send)
                        print(r.status_code)
                        op=1
                        cap.release()
                        cv2.destroyAllWindows()
                        sleep(3)
                        lcd.clear()
                        cap = cv2.VideoCapture(0)
                    
                        while op:
                            #lcd.clear()
                            #a ="1904109 SATHISH is present"
                            #long_text('This is a Scrolling text')
                            long_text(strnamepre)
                        #     lcd.cursor_pos = (3, 19)
                        #     lcd.write_string(U_L_Ch)
                        #     sleep(.6)
                            lcd.cursor_pos = (1, 4)
                            lcd.clear()
                            lcd.write_string('\x04')
                            lcd.cursor_pos = (2, 5)
                            lcd.clear()
                            lcd.write_string('\x05')
                            lcd.cursor_pos = (3, 4)
                            lcd.clear()
                            lcd.write_string('\x06')
                            lcd.cursor_pos = (3, 5)
                            lcd.clear()
                            lcd.write_string('\x07')
                            lcd.clear()
                            op=op-1
#                         lcd.write_string(strnamepre)
                        #lcd.clear()
                            
                        apdsdetect()
                    #cv2.waitKey(3)
            
                    #break
                    
 
                cv2.imshow('Webcam',img)
                cv2.waitKey(1)
            cap.release()
            cv2.destroyAllWindows()
            cap = cv2.VideoCapture(0)
            apdsdetect()
                
                
apdsdetect()



            


    
