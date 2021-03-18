import cv2
import imutils

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

#Imagen a incrustar en el video
image=cv2.imread("pixlr-bg-result.png", cv2.IMREAD_UNCHANGED)
print("image.shape = ", image.shape)
cv2.imshow("image", image[:,:,3])

faceClassIf = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
while True:
    ret, frame = cap.read()
    if ret == False: break 

    faces = faceClassIf.detectMultiScale(frame,1.2,5)

    for (x,y,w,h) in faces :
        cv2.rectangle(frame,(x,y),(x+w, y+h ), (0,255,0),2)
    cv2.imshow('Camera', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
