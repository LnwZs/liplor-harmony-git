import cv2
import dlib
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
# Set up the webcam
webcam = True
cap = cv2.VideoCapture(0)

# Initialize the face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")



# Set the width and height of the video frame
width, height = 200, 200
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


# Create a Tkinter window
root = Tk()
root.title("Liplor Harmony")
root.geometry("1500x1000")
root.configure(bg="#fff7f3")
# Bind the 'Escape' key to quit the application
root.bind('<Escape>', lambda e: root.quit())

rectangle_label = tk.Frame(root, width=395, height=245, bg="#d9aaaa", relief="solid", bd=0)
rectangle_label.grid(row=2,column=2,columnspan=2,sticky= "w")

rectangle_label2 = tk.Frame(root, width=395, height=245, bg="#edc9bf", relief="solid", bd=0)
rectangle_label2.grid(row=2,column=4,columnspan=2, sticky= "w")

before=ImageTk.PhotoImage(file='before.png')
after=ImageTk.PhotoImage(file='after.png')
manylip=ImageTk.PhotoImage(file='tryitout.png')


pic1=ImageTk.PhotoImage(file='IMG_5017.png')
pic2=ImageTk.PhotoImage(file='IMG_50192.png')
pic3=ImageTk.PhotoImage(file='IMG_5022.png')
pic4=ImageTk.PhotoImage(file='IMG_5028.png')
pic5=ImageTk.PhotoImage(file='IMG_5029.png')
pic6=ImageTk.PhotoImage(file='IMG_5030.png')
pic7=ImageTk.PhotoImage(file='IMG_5031.png')
pic8=ImageTk.PhotoImage(file='IMG_50362.png')
pic9=ImageTk.PhotoImage(file='IMG_5027.png')
pic10=ImageTk.PhotoImage(file='IMG_50212.png')

manylipl = tk.Label(root, image=manylip)
manylipl.grid(row=2,column=1,sticky= "w")



# Create a Text widget
text_box = tk.Text(root, height=1, width=80, bg="#b04747", fg="white", bd=0, relief="solid", font=("Times New Roman", 24))
text_box.grid(row=3, column=1, columnspan=5 )

# Add some initial text to the text box
text_box.insert(tk.END, "LIPLOR HARMONY")

# Center the text within the text box
text_box.tag_configure("center", justify='center')
text_box.tag_add("center", "1.0", "end")

# Disable editing
text_box.configure(state='disabled')

before1 = tk.Label(root, image=before, height=245, bg="#d9aaaa", relief="solid", bd=0)
before1.grid(row=2,column=3,padx=20)

after1 = tk.Label(root, image=after, height=245, bg="#edc9bf", relief="solid", bd=0)
after1.grid(row=2,column=5, padx=20)

# Create a label widget to display the video feed
label_widget = Label(root, width=250, height=190)
label_widget.grid(row=2, column=4,columnspan=2, sticky="w",pady=5)

label_before = Label(root, width=250, height=190)
label_before.grid(row=2, column=2,columnspan=2, sticky="w", pady=5)

# Function to create an empty callback
def empty(a):
    pass

# Create trackbars for adjusting color
red_var = IntVar()
green_var = IntVar()
blue_var = IntVar()

#red_trackbar = Scale(root, from_=0, to=255, orient=HORIZONTAL, variable=red_var, label="Red")
#green_trackbar = Scale(root, from_=0, to=255, orient=HORIZONTAL, variable=green_var, label="Green")
#blue_trackbar = Scale(root, from_=0, to=255, orient=HORIZONTAL, variable=blue_var, label="Blue")

#red_entry = Entry(root, textvariable=red_var)
#green_entry = Entry(root, textvariable=green_var)
#blue_entry = Entry(root, textvariable=blue_var)

def update_scale_from_entry(scale, var):
    try:
        value = int(var.get())
        if 0 <= value <= 255:
            scale.set(value)
        else:
            var.set(scale.get())
    except ValueError:
        var.set(scale.get())

#red_entry.bind('<Return>', lambda event: update_scale_from_entry(red_trackbar, red_var))
#green_entry.bind('<Return>', lambda event: update_scale_from_entry(green_trackbar, green_var))
#blue_entry.bind('<Return>', lambda event: update_scale_from_entry(blue_trackbar, blue_var))

#red_trackbar.grid(row=2, column=2)
#green_trackbar.grid(row=3, column=2)
#blue_trackbar.grid(row=4, column=2)

#red_entry.grid(row=2, column=3)
#green_entry.grid(row=3, column=3)
#blue_entry.grid(row=4, column=3)

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
                imgColorLips[:, :, 3] = 255

                imgColorLips = cv2.bitwise_and(imgLips, imgColorLips)
                imgColorLips = cv2.GaussianBlur(imgColorLips, (7, 7), 9)

                #imgColorLips = cv2.addWeighted(frame_rgb, 1, imgColorLips, 0.4, 0)
                #print(frame_rgb.shape)


                nolips = cv2.bitwise_xor(frame_rgb,img2)

                nolips = cv2.GaussianBlur(nolips, (7,7),9)

                prefinal = cv2.addWeighted(nolips,0.8,frame_rgb,0.8,0)
                final = cv2.addWeighted(prefinal,0.9,imgColorLips,0.5,0)

        else:
            # No face detected, display a message in the middle of the frame in red color
            text = "No face detected"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = (frame_rgb.shape[1] - text_size[0]) // 2
            text_y = (frame_rgb.shape[0] + text_size[1]) // 2
            cv2.putText(frame_rgb, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            final = frame_rgb

        # Convert processed image to PhotoImage
        captured_image = Image.fromarray(final)
        photo_image = ImageTk.PhotoImage(image=captured_image)
        label_widget.photo_image = photo_image
        label_widget.configure(image=photo_image)

        #cv2.imshow('Liplor Harmony ',final)

    # Repeat the process
    label_widget.after(10, update_webcam)

# Function to create a boxed region
def createBox(img, points, scale=5, masked=False, cropped=True):
    global img2
    if masked:
        mask = np.zeros_like(img)
        mask = cv2.fillPoly(mask, [points], (255, 255, 255))
        img2 = cv2.bitwise_and(img, mask)

    if cropped:
        bbox = cv2.boundingRect(points)
        x, y, w, h = bbox
        imgCrop = img[y:y + h, x:x + w]
        imgCrop = cv2.resize(imgCrop, (0, 0), None, scale, scale)
        return imgCrop
    else:
        return mask

# Function to change RGB values based on button clicks
def change_rgb(r, g, b):
    red_var.set(r)
    green_var.set(g)
    blue_var.set(b)

# Create buttons with corresponding RGB values
Button(root, image=pic3, text="Pic3", command=lambda: change_rgb(202, 84, 85), bg='#ffe5eb').grid(row=7, column=1, pady=7)
vertical_text = "1\n2\n0\nP\nU\nN\nC\nH\nY"
label1 = tk.Label(root, text=vertical_text, font=("Arial", 12), justify="left", bg="white",bd=1,relief="raised",highlightbackground="black",height=9)
label1.grid(row=7, column=1, padx=(190, 0))

Button(root, image=pic2, text="Pic2", command=lambda: change_rgb(161, 69, 70), bg='#d48686').grid(row=7, column=2)#
vertical_text = "3\n5\nC\nH\nE\nE\nK\nY"
label2 = tk.Label(root, text=vertical_text, font=("Arial", 12), justify="left", bg="white",bd=1,relief="raised",highlightbackground="black",height=9)
label2.grid(row=7, column=2, padx=(190, 0))

Button(root, image=pic7, text="Pic7", command=lambda: change_rgb(197, 66, 100), bg='#b04747').grid(row=7, column=3)
vertical_text = "2\n0\nC\nO\nY"
label3 = tk.Label(root, text=vertical_text, font=("Arial", 12), justify="left", bg="white",bd=1,relief="raised",highlightbackground="black",height=9)
label3.grid(row=7, column=3, padx=(190, 0))

Button(root, image=pic9, text="Pic9", command=lambda: change_rgb(167, 55, 77), bg='#d48686').grid(row=7, column=4)
vertical_text = "8\n0\nE\nC\nE\nT\nR\nI\nC"
label4 = tk.Label(root, text=vertical_text, font=("Arial", 12), justify="left", bg="white",bd=1,relief="raised",highlightbackground="black",height=9)
label4.grid(row=7, column=4, padx=(190, 0))

Button(root, image=pic10, text="Pic10", command=lambda: change_rgb(167, 18, 32), bg='#ffe5eb').grid(row=7, column=5)#
vertical_text = "1\n0\nL\nI\nP\nP\nY"
label5 = tk.Label(root, text=vertical_text, font=("Arial", 12), justify="left", bg="white",bd=1,relief="raised",highlightbackground="black",height=9)
label5.grid(row=7, column=5, padx=(190, 0))


Button(root, image=pic4, text="Pic4", command=lambda: change_rgb(213, 36, 57), bg='#ffb39d').grid(row=8, column=1)
vertical_text = "5\n3\nU\nN\nP\nR\nE\nD\nC"
label5 = tk.Label(root, text=vertical_text, font=("Arial", 12), justify="left", bg="white",bd=1,relief="raised",highlightbackground="black",height=9)
label5.grid(row=8, column=1, padx=(190, 0))

Button(root, image=pic1, text="Pic1", command=lambda: change_rgb(207, 57, 53), bg='#ef9981').grid(row=8, column=2)
vertical_text = "3\n7\nD\nA\nR\nL\nI\nN\nG"
label5 = tk.Label(root, text=vertical_text, font=("Arial", 12), justify="left", bg="white",bd=1,relief="raised",highlightbackground="black",height=9)
label5.grid(row=8, column=2, padx=(190, 0))

Button(root, image=pic8, text="Pic8", command=lambda: change_rgb(184, 68, 47), bg='#c5664b').grid(row=8, column=3)#
vertical_text = "6\n1\nR\nI\nS\nK\nY"
label5 = tk.Label(root, text=vertical_text, font=("Arial", 12), justify="left", bg="white",bd=1,relief="raised",highlightbackground="black",height=9)
label5.grid(row=8, column=3, padx=(190, 0))

Button(root, image=pic6, text="Pic6", command=lambda: change_rgb(179, 57, 43), bg='#ef9981').grid(row=8, column=4)
vertical_text = "1\n2\n5\nK\nE\nE\nN"
label5 = tk.Label(root, text=vertical_text, font=("Arial", 12), justify="left", bg="white",bd=1,relief="raised",highlightbackground="black",height=9)
label5.grid(row=8, column=4, padx=(190, 0))

Button(root, image=pic5, text="Pic5", command=lambda: change_rgb(159, 57, 43), bg='#ffb39d').grid(row=8, column=5)
vertical_text = "1\n3\n0\nE\nX\nT\nR\nA"
label5 = tk.Label(root, text=vertical_text, font=("Arial", 12), justify="left", bg="white",bd=1,relief="raised",highlightbackground="black",height=9)
label5.grid(row=8, column=5, padx=(190, 0))







def old_pic():
        # Capture the latest frame from the webcam
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # Convert to RGBA
        #imgOriginal = frame.copy()

    # Convert processed image to PhotoImage
    frame_rgb = cv2.GaussianBlur(frame_rgb, (3, 3), 9)
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