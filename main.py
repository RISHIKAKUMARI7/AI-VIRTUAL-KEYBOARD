import cv2
# from gbsoft import HandDetector
import localhanddetectormodule as HandDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)


detector = HandDetector.HandDetector(detectionCon=0.8)
keys = [["1","2","3","4","5","6","7","8","9","0"],
["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""

keyboard = Controller()
def draw(img, buttonList):

     for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (0,0,0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
     return  img


class Button():
    def __init__(self,pos, text, size=[85,85]):
        self.pos = pos
        self.size = size
        self.text = text



buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


while cap.isOpened():
    ret, img = cap.read()
    img = cv2.resize(img,(1280,720))
    img = detector.findHands(img)
    lmlist,bboxinfo = detector.findPosition(img)
    img = draw(img, buttonList)
    if lmlist:
         for button in buttonList:
             x, y = button.pos
             w, h = button.size

             if x < lmlist[8][0]< x+w and y < lmlist[8][1] < y + h:
                 cv2.rectangle(img, button.pos, (x + w, y + h), (0,255,0), cv2.FILLED)
                 cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                 l,_,_ = detector.findDistance(8, 4, img,draw=False)
                 if l<30:
                     keyboard.press(button.text)
                     cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                     cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                     finalText += button.text
                     sleep(0.15)


    cv2.rectangle(img,(50, 550), (700, 450), (0,0,0), cv2.FILLED)
    cv2.putText(img, finalText, (60, 530), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


