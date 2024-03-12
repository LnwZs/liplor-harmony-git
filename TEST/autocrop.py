import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

class AutoCropApp:
    def __init__(self, root):
        # Initialize the Tkinter window
        self.root = root
        self.root.title("Auto Crop Tool")  # Set the title of the window

        # Create a label widget
        self.label = tk.Label(root, text="Auto Crop Tool")
        self.label.pack()  # Pack the label into the window

        # Create a button for selecting an image
        self.select_button = tk.Button(root, text="Select Image", command=self.select_image)
        self.select_button.pack()  # Pack the button into the window

        # Create a canvas for displaying images
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()  # Pack the canvas into the window

    def select_image(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename()
        if file_path:  # If a file is selected
            self.crop_image(file_path)  # Perform cropping on the selected image

    def crop_image(self, file_path):
        # Open the image file using OpenCV
        image = cv2.imread(file_path)
        
        # Perform automatic cropping
        cropped_image = self.auto_crop(image)
        
        # Display the cropped image
        self.display_image(cropped_image)

    def display_image(self, image):
        # Convert the OpenCV image format to RGB format
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Convert the image to a format that Tkinter can handle
        img = ImageTk.PhotoImage(image=Image.fromarray(image_rgb))
        
        # Delete any previous image displayed on the canvas
        self.canvas.delete("all")
        
        # Keep a reference to the image to avoid garbage collection
        self.canvas.image = img
        
        # Display the image on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)

    def auto_crop(self, image):
        # Get the dimensions of the image
        height, width, _ = image.shape

        # Calculate the dimensions for the center crop
        crop_size = min(height, width) // 4  # You can adjust this value for your desired crop size
        center_x = width // 2
        center_y = height // 2
        half_crop_size = crop_size // 2

        # Calculate the bounding box for the center crop
        x1 = max(0, center_x - half_crop_size)
        y1 = max(0, center_y - half_crop_size)
        x2 = min(width, center_x + half_crop_size)
        y2 = min(height, center_y + half_crop_size)

        # Perform the center crop
        cropped_image = image[y1:y2, x1:x2]

        # Resize the cropped image to a very small size
        resized_image = cv2.resize(cropped_image, (16, 16))  # Adjust the size as needed

        return resized_image

if __name__ == "__main__":
    # Create a Tkinter window
    root = tk.Tk()
    
    # Create an instance of the AutoCropApp class
    app = AutoCropApp(root)
    
    # Start the Tkinter event loop
    root.mainloop()
