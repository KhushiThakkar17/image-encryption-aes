import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Pillow for image processing

# Create main window
root = tk.Tk()
root.title("Button with Resized Search Icon")

# Open the image with Pillow and resize it
img = Image.open("magnifying glass.png")  # Replace with your image file path
resized_img = img.resize((24, 24), Image.LANCZOS)  # Resize to 24x24 pixels

# Convert the resized image to PhotoImage
search_icon = ImageTk.PhotoImage(resized_img)

# Create a button with the resized search icon
search_button = tk.Button(root, image=search_icon, text="Search", compound="left")
search_button.grid(row=0, column=0, padx=10, pady=10)

# Run the application
root.mainloop()