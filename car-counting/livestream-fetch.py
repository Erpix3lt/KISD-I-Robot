import cv2

cap = cv2.VideoCapture('http://87.193.219.148/record/current.jpg?rand=755223')

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break