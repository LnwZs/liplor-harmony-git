import cv2
import dlib
import numpy as np
from tkinter import *
from PIL import Image,ImageTk

# Create tkinter window
#root = Tk()
#root.title('Liplor Harmony')

webcam = True

cap = cv2.VideoCapture(0)


# Load face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

#def show_values():
 #   #print (b.get(), g.get(), r.get())
 #   pass

root = Tk()
root.geometry('1500x900+400+100')
root.title('Liplor Harmony')

#load pic
pic1=ImageTk.PhotoImage(file='pic1.png')
pic2=ImageTk.PhotoImage(file='pic2.png')
pic3=ImageTk.PhotoImage(file='pic3.png')
pic4=ImageTk.PhotoImage(file='pic4.png')
pic5=ImageTk.PhotoImage(file='pic5.png')
pic6=ImageTk.PhotoImage(file='pic6.png')
pic7=ImageTk.PhotoImage(file='pic7.png')
pic8=ImageTk.PhotoImage(file='pic8.png')

b = Scale(root,label='BLUE', from_=0, to=255,tickinterval=10, orient=HORIZONTAL).grid(column=5,row=10)
g = Scale(root,label='GREEN', from_=0, to=255,tickinterval=10, orient=HORIZONTAL).grid(column=5,row=20)
r = Scale(root,label='RED', from_=0, to=255,tickinterval=10, orient=HORIZONTAL).grid(column=5,row=30)

Button1 = Button(root, image=pic1, text="pic1").grid(column=6,row=40)
Button2 = Button(root, image=pic2, text="pic2").grid(column=7,row=40)
Button3 = Button(root, image=pic3, text="pic3").grid(column=8,row=40)
Button4 = Button(root, image=pic4, text="pic4").grid(column=9,row=40)
Button5 = Button(root, image=pic5, text="pic5").grid(column=6,row=50)
Button6 = Button(root, image=pic6, text="pic6").grid(column=7,row=50)
Button7 = Button(root, image=pic7, text="pic7").grid(column=8,row=50)
Button8 = Button(root, image=pic8, text="pic8").grid(column=9,row=50)

# Start tkinter loop
root.mainloop()

# Close trackbar window
#cv2.destroyAllWindows()
