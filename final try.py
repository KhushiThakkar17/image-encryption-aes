import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import binascii

# Function to generate a key using a password and salt
def derive_key(password, salt):
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    key = kdf.derive(password.encode())  # Deriving key from password
    return key

# AES Encryption
def encrypt_image(image_path, password):
    # Read image bytes
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Generate a random salt
    salt = os.urandom(16)
    print(f"Encryption Salt: {binascii.hexlify(salt)}")

    # Derive key from password and salt
    key = derive_key(password, salt)
    iv = os.urandom(16)
    print(f"Encryption IV: {binascii.hexlify(iv)}")

    # AES encryption
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_image = encryptor.update(image_data) + encryptor.finalize()
    print(f"Encrypted image size: {len(encrypted_image)}")

    # Return encrypted image with salt and IV
    return salt, iv, encrypted_image

# AES Decryption
def decrypt_image(encrypted_image, password, salt, iv, save_path):
    key = derive_key(password, salt)
    print(f"Decryption Salt: {binascii.hexlify(salt)}")
    print(f"Decryption IV: {binascii.hexlify(iv)}")

    # AES decryption
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_image = decryptor.update(encrypted_image) + decryptor.finalize()
    print(f"Decrypted image size: {len(decrypted_image)}")

    try:
        # Save the decrypted image
        with open(save_path, "wb") as image_file:
            image_file.write(decrypted_image)

        # Load and verify the image using Pillow
        try:
            img = Image.open(save_path)
            img.verify()  # This checks if the file is a valid image
            messagebox.showinfo("Success", "Image decrypted and saved successfully!")
        except Exception as img_error:
            raise ValueError(f"Image verification failed: {img_error}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save or verify decrypted image: {e}")

# GUI Functions
def select_image():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", ".png;.jpg;.jpeg;.bmp;*.gif")])
    if file_path:
        image_entry.delete(0, tk.END)
        image_entry.insert(0, file_path)

def encrypt_button_action():
    password = password_entry.get()
    image_path = image_entry.get()

    if not password or not image_path:
        messagebox.showwarning("Input Error", "Please provide both password and image.")
        return

    try:
        salt, iv, encrypted_image = encrypt_image(image_path, password)

        # Save the encrypted image
        save_path = filedialog.asksaveasfilename(title="Save Encrypted Image", defaultextension=".enc", filetypes=[("Encrypted Files", "*.enc")])
        with open(save_path, "wb") as encrypted_file:
            encrypted_file.write(salt + iv + encrypted_image)

        messagebox.showinfo("Success", "Image encrypted and saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {e}")

def decrypt_button_action():
    password = password_entry.get()
    image_path = image_entry.get()

    if not password or not image_path:
        messagebox.showwarning("Input Error", "Please provide both password and encrypted image.")
        return

    try:
        with open(image_path, "rb") as encrypted_file:
            file_data = encrypted_file.read()

        salt = file_data[:16]
        iv = file_data[16:32]
        encrypted_image = file_data[32:]
        print(f"Loaded encrypted image size: {len(encrypted_image)}")

        # Save decrypted image
        save_path = filedialog.asksaveasfilename(
            title="Save Decrypted Image", 
            defaultextension=".png",  # Set default extension based on your needs
            filetypes=[("Image Files", ".png;.jpg;.jpeg;.bmp")]
        )

        decrypt_image(encrypted_image, password, salt, iv, save_path)

    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {e}")

# Main window
root = tk.Tk()
root.title("Image Encryption and Decryption using AES Algorithm")
root.geometry("600x400")
root.minsize(550, 300)

# Change window icon (change this to your own icon file path)
icon = PhotoImage(file="kpgu logo final.png")
root.iconphoto(False, icon)

# GUI layout
tk.Label(root, text="Select Image or Encrypted File:", font="TimesNewRoman 10 bold").grid(row=0, column=0, padx=10, pady=10)
image_entry = tk.Entry(root, width=40)
image_entry.grid(row=0, column=1, padx=10, pady=10)

img = Image.open("magnifying glass.png")  # Replace with your image file path
resized_img = img.resize((24, 24), Image.LANCZOS)

browse_icon = ImageTk.PhotoImage(resized_img)
browse_button = tk.Button(root, image=browse_icon, text="Browse", bg="light blue", compound="left", command=select_image)
browse_button.grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Password:", font="TimesNewRoman 10 bold").grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*", width=40)
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Encrypt Button
img = Image.open("encryption logo.png")
resized_img = img.resize((24, 24), Image.LANCZOS)
Encrypt_icon = ImageTk.PhotoImage(resized_img)
Encrypt_button = tk.Button(root, image=Encrypt_icon, text="Encrypt", bg="light grey", compound="left", command=encrypt_button_action)
Encrypt_button.grid(row=2, column=1, padx=10, pady=10, sticky='w')

# Decrypt Button
img = Image.open("decryption logo.png")
resized_img = img.resize((24, 24), Image.LANCZOS)
Decrypt_icon = ImageTk.PhotoImage(resized_img)
Decrypt_button = tk.Button(root, image=Decrypt_icon, text="Decrypt", bg="light green", compound="left", command=decrypt_button_action)
Decrypt_button.grid(row=2, column=1, padx=10, pady=10, sticky='e')

# Run the application
root.mainloop()