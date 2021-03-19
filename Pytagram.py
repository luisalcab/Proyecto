#Importa la libreria para el funcionamiento optimo del programa
import cv2
#Importa la libreria que ayuda a redimensionar la imagen a incrustar en el video
import imutils

#Abre la camara para la captura de video 
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

#Imagen a incrustar en el video
image=cv2.imread("CubrebocasTec.png", cv2.IMREAD_UNCHANGED)

#Codigo que identifica las caras captadas por la camara
faceClassIf = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#Ciclo que mantiene la ventana emergente del video hasta que se pulse la tecla ESC
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

        #Ajusta la imagen a incrustar en el video en la zona de las caras o cara detectadas por la camara
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

        #Suma las imagenes
        result = cv2.add(bg_black, bg_frame)
        if y - filas_image + porcion_alto >= 0:
            frame[y - filas_image + porcion_alto: y + porcion_alto, x: x + w] = result
        else:
            frame[0: y + porcion_alto, x: x + w] = result
    


    #Activa la ventana emergente del video
    cv2.imshow('Camera', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

#Cierra la ventana emergente
cap.release()
cv2.destroyAllWindows()
