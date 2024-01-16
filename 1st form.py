import cv2
import numpy as np
import dlib
import tkinter as tk
from PIL import Image, ImageTk

webcam = True

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Create Tkinter window
root = tk.Tk()
root.title("Liplor Harmony")

# Create Trackbars
blue_var = tk.IntVar()
green_var = tk.IntVar()
red_var = tk.IntVar()

def empty(a):
    pass

# Tkinter GUI Elements
cv_panel = tk.Canvas(root, width=640, height=480)
cv_panel.pack()

tk.Label(root, text="Blue").pack()
blue_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, variable=blue_var)
blue_scale.pack()

tk.Label(root, text="Green").pack()
green_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, variable=green_var)
green_scale.pack()

tk.Label(root, text="Red").pack()
red_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, variable=red_var)
red_scale.pack()

# Initialize color variables
img_color_lips = np.zeros((1, 1, 3), np.uint8)
img_color_lips[:] = 0, 0, 0

# Tkinter Image Panel
img_original = np.zeros((480, 640, 3), np.uint8)
imgtk_original = ImageTk.PhotoImage(Image.fromarray(img_original))
panel = tk.Label(cv_panel, image=imgtk_original)
panel.imgtk = imgtk_original
panel.pack()

def createBox(img, points, scale=5, masked=False, cropped=True):
    if masked:
        mask = np.zeros_like(img)
        mask = cv2.fillPoly(mask, [points], (255, 255, 255))
        img = cv2.bitwise_and(img, mask)

    if cropped:
        bbox = cv2.boundingRect(points)
        x, y, w, h = bbox
        img_crop = img[y:y + h, x:x + w]
        img_crop = cv2.resize(img_crop, (0, 0), None, scale, scale)
        return img_crop
    else:
        return mask

# Move img_lips outside the loop
img_lips = np.zeros((480, 640, 3), np.uint8)

def update_color():
    b = blue_var.get()
    g = green_var.get()
    r = red_var.get()
    img_color_lips[:] = b, g, r
    img_color_lips_result = cv2.bitwise_and(img_lips, img_color_lips)
    img_color_lips_result = cv2.GaussianBlur(img_color_lips_result, (7, 7), 10)
    img_color_lips_result = cv2.addWeighted(img_original, 1, img_color_lips_result, 0.4, 0)
    img_color_lips_result = cv2.cvtColor(img_color_lips_result, cv2.COLOR_BGR2RGB)
    imgtk = ImageTk.PhotoImage(Image.fromarray(img_color_lips_result))
    panel.imgtk = imgtk
    panel.config(image=imgtk)

    root.after(10, update_color)  # Schedule the next update

root.after(10, update_color)  # Initial update

while True:
    # Webcam
    if webcam:
        success, img = cap.read()
    else:
        img = cv2.imread('2.jpg')

    img = cv2.resize(img, (640, 480))
    img_original = img.copy()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(img_gray)

    for face in faces:
        landmarks = predictor(img_gray, face)
        my_points = []
        for n in range(68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            my_points.append([x, y])

        my_points = np.array(my_points)
        img_lips = createBox(img, my_points[48:61], 8, masked=True, cropped=False)

    # Set img_lips to global variable for color update
    img_lips = cv2.cvtColor(img_lips, cv2.COLOR_BGR2RGB)

    # Update the Tkinter window
    root.update_idletasks()
    root.update()

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release the video capture object and close OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Start the Tkinter main loop
root.mainloop()
