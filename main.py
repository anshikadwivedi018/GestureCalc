# import cv2
# from cvzone.HandTrackingModule import HandDetector

# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4,720)

# detector = HandDetector(detectionCon = 0.8)

# while True:
#     success, img = cap.read()
#     img = detector.findHands(img)
#     lmList, bboxInfo = detector.findPosition(img)
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)


import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width of the webcam
cap.set(4, 720)   # Set height of the webcam

# Initialize hand detector
detector = HandDetector(detectionCon=0.8)
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]

def drawALL(img, buttonList):
    for button in buttonList:
        x,y=button.pos
        w,h=button.size
        cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(img,button.text,(x + 20 , y + 60),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255), 4)
    return img

class Button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos = pos
        self.size = size
        self.text = text
    # def draw(self,img):
        
        
buttonList = []
for i in range(len(keys)):
    for j,key in enumerate(keys[i]):
        buttonList.append(Button([j*100+50, 100*i+50],key))


while True:
    # Read a frame from the webcam
    success, img = cap.read()
    
    if not success:
        print("Error: Could not read frame from the webcam.")
        break  # Exit the loop if frame is not captured

    # Detect hands
    hands, img = detector.findHands(img)  # Returns the hand(s) and the annotated image

    # Check if any hands were detected
    
    if hands:
        # Get the landmark list of the first hand
        hand1 = hands[0]
        lmList = hand1["lmList"]  # List of 21 Landmark points
        bbox = hand1["bbox"]      # Bounding box info x, y, w, h
        # myButton = Button([100,100],"Q")
        img = drawALL(img, buttonList)
        if lmList:
            for button in buttonList:
                x,y = button.pos
                w,h = button.size
                if x < lmList[8][0] < x+w:
                    cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                    cv2.putText(img,button.text,(x + 20 , y + 60),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255), 4)

    
    cv2.imshow("Image", img)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
