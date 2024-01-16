import cv2
import tkinter as tk
from PIL import Image, ImageTk

class WebcamApp:
    def __init__(self, window, window_title="Webcam Feed"):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0  # Use 0 for the default camera
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window)
        self.canvas.pack()

        self.btn_snapshot = tk.Button(window, text="Snapshot", width=10, command=self.snapshot)
        self.btn_snapshot.pack(padx=20, pady=10)

        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.resize(frame, (640, 480))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(10, self.update)

    def snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("snapshot.png", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

app = WebcamApp(tk.Tk(), "Webcam Feed")
