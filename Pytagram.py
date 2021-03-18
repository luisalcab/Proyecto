import cv2
import imutils

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

#Imagen a incrustar en el video
image=cv2.imread("CubrebocasTec.png", cv2.IMREAD_UNCHANGED)

faceClassIf = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
while True:
    ret, frame = cap.read()
    if ret == False: break 

    faces = faceClassIf.detectMultiScale(frame,1.2,5)

    for (x,y,w,h) in faces :
        #cv2.rectangle(frame,(x,y),(x+w, y+h ), (0,255,0),2)

        resized_image = imutils.resize(image, width= w)
        filas_image = resized_image.shape[0]
        col_image = w

        dif = 0

        porcion_alto = filas_image // 1
 
        if y - filas_image + porcion_alto >= 0:
            n_frame = frame[y - filas_image + porcion_alto: y + porcion_alto, x: x + w]
        else:
            dif = abs(y - filas_image + porcion_alto)
            n_frame = frame[0: y + porcion_alto, x: x + w]

        mask = resized_image[:, :, 3]
        mask_inv = cv2.bitwise_not(mask)

        bg_black = cv2.bitwise_and(resized_image, resized_image, mask=mask)
        bg_black = bg_black[dif:, :, 0:3]
        bg_frame = cv2.bitwise_and(n_frame, n_frame, mask = mask_inv[dif:, :])

        #Sumar imagenes
        result = cv2.add(bg_black, bg_frame)
        if y - filas_image + porcion_alto >= 0:
            frame[y - filas_image + porcion_alto: y + porcion_alto, x: x + w] = result
        else:
            frame[0: y + porcion_alto, x: x + w] = result
    



    cv2.imshow('Camera', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
