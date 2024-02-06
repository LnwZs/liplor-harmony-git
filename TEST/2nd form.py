import cv2
import dlib
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Load face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Create tkinter window
root = tk.Tk()
root.title('Liplor Harmony')

# Create function to open image
def open_image():
    filepath = filedialog.askopenfilename()
    img = cv2.imread(filepath)
    imgOriginal = img.copy()
    return img, imgOriginal

# Create function to detect faces and apply color to lips
def detect_faces():
    img, imgOriginal = open_image()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = detector(imgGray)

    for face in faces:
        x1,y1 = face.left(),face.top()
        x2,y2 = face.right(),face.bottom()

        # Draw rectangle around face
        cv2.rectangle(imgOriginal,(x1,y1),(x2,y2),(0,255,0),2)

        # Get landmarks
        landmarks = predictor(imgGray,face)
        myPoints =[]
        for n in range(68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            myPoints.append([x,y])
            cv2.circle(imgOriginal,(x,y),5,(50,50,255),cv2.FILLED)
            cv2.putText(imgOriginal,str(n),(x,y-10),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.9,(0,0,255),1)

        myPoints = np.array(myPoints)

        # Create box around lips
        imgLips = createBox(img,myPoints[48:61],8,masked=True,cropped=False)

        # Apply color to lips
        imgColorLips = np.zeros_like(imgLips)
        b = cv2.getTrackbarPos('Blue','BGR')
        g = cv2.getTrackbarPos('Green','BGR')
        r = cv2.getTrackbarPos('Red','BGR')
        imgColorLips[:] = b,g,r
        imgColorLips = cv2.bitwise_and(imgLips,imgColorLips)
        imgColorLips = cv2.GaussianBlur(imgColorLips,(7,7),10)

        # Apply color to lips
        imgColorLips = cv2.addWeighted(imgOriginal,1,imgColorLips,0.4,0)

    # Display image
    imgColorLips = cv2.cvtColor(imgColorLips, cv2.COLOR_BGR2RGB)
    imgColorLips = cv2.resize(imgColorLips, (400, 400))
    photo = tk.PhotoImage(image=imgColorLips)
    label = tk.Label(root, image=photo)
    label.pack()

# Create trackbars for color
cv2.namedWindow('BGR')
cv2.resizeWindow('BGR',640,240)
cv2.createTrackbar('Blue','BGR',0,255,lambda x: None)
cv2.createTrackbar('Green','BGR',0,255,lambda x: None)
cv2.createTrackbar('Red','BGR',0,255,lambda x: None)

# Start tkinter loop
root.mainloop()

# Close trackbar window
cv2.destroyAllWindows()
