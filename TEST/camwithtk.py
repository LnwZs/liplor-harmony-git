import cv2
import numpy as np
import dlib
from tkinter import *
from PIL import Image, ImageTk

# Set up the webcam
webcam = True
cap = cv2.VideoCapture(0)

# Initialize the face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Set the width and height of the video frame
width, height = 700, 500
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Create a Tkinter window
root = Tk()
root.title("Liplor Harmony")
root.geometry("1500x900")
# Bind the 'Escape' key to quit the application
root.bind('<Escape>', lambda e: root.quit())

# Create a label widget to display the video feed
label_widget = Label(root)
label_widget.grid(row=2, column=4)

label_before = Label(root)
label_before.grid(row=2, column=2)

# Function to create an empty callback
def empty(a):
    pass

# Create trackbars for adjusting color
red_var = IntVar()
green_var = IntVar()
blue_var = IntVar()

red_trackbar = Scale(root, from_=0, to=255, orient=HORIZONTAL, variable=red_var, label="Red")
green_trackbar = Scale(root, from_=0, to=255, orient=HORIZONTAL, variable=green_var, label="Green")
blue_trackbar = Scale(root, from_=0, to=255, orient=HORIZONTAL, variable=blue_var, label="Blue")

red_entry = Entry(root, textvariable=red_var)
green_entry = Entry(root, textvariable=green_var)
blue_entry = Entry(root, textvariable=blue_var)

def update_scale_from_entry(scale, var):
    try:
        value = int(var.get())
        if 0 <= value <= 255:
            scale.set(value)
        else:
            var.set(scale.get())
    except ValueError:
        var.set(scale.get())

red_entry.bind('<Return>', lambda event: update_scale_from_entry(red_trackbar, red_var))
green_entry.bind('<Return>', lambda event: update_scale_from_entry(green_trackbar, green_var))
blue_entry.bind('<Return>', lambda event: update_scale_from_entry(blue_trackbar, blue_var))

red_trackbar.grid(row=2, column=3)
green_trackbar.grid(row=3, column=3)
blue_trackbar.grid(row=4, column=3)

red_entry.grid(row=2, column=4)
green_entry.grid(row=3, column=4)
blue_entry.grid(row=4, column=4)

# Function to process the webcam feed
def update_webcam():
    global imgColorLips
    
    # Capture the latest frame from the webcam
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # Convert to RGBA
        #imgOriginal = frame.copy()
        imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(imgGray)

    if len(faces) > 0:
             for face in faces:
                 landmarks = predictor(imgGray, face)
                 myPoints = []
                 for n in range(68):
                      x = landmarks.part(n).x
                      y = landmarks.part(n).y
                      myPoints.append([x, y])

                 myPoints = np.array(myPoints)

                   # Create lips region
                 imgLips = createBox(frame_rgb, myPoints[48:61], 8, masked=True, cropped=False)

                 # Initialize imgColorLips
                 imgColorLips = np.zeros_like(imgLips)

                 # Access color channels correctly (RGB)
                 r = red_var.get()
                 g = green_var.get()
                 b = blue_var.get()
                 imgColorLips[:, :, 0] = r  # Blue channel
                 imgColorLips[:, :, 1] = g  # Green channel
                 imgColorLips[:, :, 2] = b  # Red channel

                 imgColorLips = cv2.bitwise_and(imgLips, imgColorLips)
                 imgColorLips = cv2.GaussianBlur(imgColorLips, (7, 7), 9)

                 imgColorLips = cv2.addWeighted(frame_rgb, 1, imgColorLips, 0.6, 0)
    else:
            # No face detected, display a message in the middle of the frame in red color
            text = "No face detected"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = (frame_rgb.shape[1] - text_size[0]) // 2
            text_y = (frame_rgb.shape[0] + text_size[1]) // 2
            cv2.putText(frame_rgb, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            imgColorLips = frame_rgb

   # Convert processed image to PhotoImage
    captured_image = Image.fromarray(imgColorLips)
    photo_image = ImageTk.PhotoImage(image=captured_image)
    label_widget.photo_image = photo_image
    label_widget.configure(image=photo_image)

    # Repeat the process
    label_widget.after(10, update_webcam)

# Function to create a boxed region
def createBox(img, points, scale=5, masked=False, cropped=True):
    if masked:
        mask = np.zeros_like(img)
        mask = cv2.fillPoly(mask, [points], (255, 255, 255))
        img = cv2.bitwise_and(img, mask)

    if cropped:
        bbox = cv2.boundingRect(points)
        x, y, w, h = bbox
        imgCrop = img[y:y + h, x:x + w]
        imgCrop = cv2.resize(imgCrop, (0, 0), None, scale, scale)
        return imgCrop
    else:
        return mask


def old_pic():
        # Capture the latest frame from the webcam
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # Convert to RGBA
        #imgOriginal = frame.copy()

    # Convert processed image to PhotoImage
    captured_image2 = Image.fromarray(frame_rgb)
    photo_image2 = ImageTk.PhotoImage(image=captured_image2)
    label_before.photo_image = photo_image2
    label_before.configure(image=photo_image2)

    # Repeat the process
    label_widget.after(10, old_pic)


old_pic()

# Call the function to update the webcam feed
update_webcam()

# Start the Tkinter event loop
root.mainloop()