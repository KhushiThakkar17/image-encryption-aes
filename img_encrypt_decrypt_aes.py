import tkinter as tk
from tkinter import PhotoImage
from tkinter import filedialog, messagebox, simpledialog
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from PIL import Image, ImageTk
import os

# Padding function to ensure the data is a multiple of the AES block size (16 bytes/128 bits)
def pad(data):
    padding_length = 16 - len(data) % 16
    return data + bytes([padding_length]) * padding_length

# Unpadding function used to remove padding after decryption process
def unpad(data):
    return data[:-data[-1]]

# Function to derive AES key from a password using PBKDF2 library
def derive_key(password, salt):
    key = PBKDF2(password, salt, dkLen=32, count=100000)  # AES-256 key (32 bytes/256 bits)
    return key

# Function work -  to encrypt the image
def encrypt_image(image_path, password, output_path):
    img = Image.open(image_path)
    img_bytes = img.tobytes()

    # Padding the image data
    padded_img_bytes = pad(img_bytes)

    # it Generates a random salt and IV(initialization Vector) that is used in AES 
    # IV - its a random or unique value used along enc. key to ensure that same plaintext input will generate different cipher text.
    
    salt = get_random_bytes(16)
    iv = get_random_bytes(16)

    # Derive the key from the password and salt
    
    key = derive_key(password, salt)

    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Encrypting the image data
    encrypted_bytes = cipher.encrypt(padded_img_bytes)

    # Save the salt, IV, and encrypted data
    with open(output_path, 'wb') as encrypted_file:
        encrypted_file.write(salt + iv + encrypted_bytes)

    print(f"Image is encrypted and saved as {output_path}")
    messagebox.showinfo("Encryption", f"Image is encrypted and saved as {output_path}")

# Function to decrypt image

def decrypt_image(encrypted_image_path, password, output_image_path, original_image_size):
    with open(encrypted_image_path, 'rb') as encrypted_file:
        salt = encrypted_file.read(16)  # this to read the salt
        iv = encrypted_file.read(16)  # this to read the IV
        encrypted_bytes = encrypted_file.read()  # Reading the encrypted data

    # Derive the key from the password and salt
    
    key = derive_key(password, salt)

    # Create AES cipher for decryption using the same IV
    
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the image data
    
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes))

    # Create an image from decrypted bytes
    
    img = Image.frombytes('RGB', original_image_size, decrypted_bytes)
    img.save(output_image_path)

    print(f"Image decrypted and saved as {output_image_path}")
    messagebox.showinfo("Decryption", f"Image decrypted and saved as {output_image_path}")

# GUI Functions

def select_image():
    global img_path, original_image_size
    img_path = filedialog.askopenfilename(filetypes=[("Image files", ".png;.jpg;*.jpeg")])
    if img_path:
        img = Image.open(img_path)
        original_image_size = img.size  # Save in original size
        img.thumbnail((200, 200))  # Resizeing for display in the GUI
        img_display = ImageTk.PhotoImage(img)
        img_label.config(image=img_display)
        img_label.image = img_display
        print(f"Selected image: {img_path}")

def encrypt():
    if img_path:
        password = simpledialog.askstring("Password", "Enter a password for encryption:", show='*')
        if password:
            encrypt_image(img_path, password, 'encrypted_image.aes')

def decrypt():
    if os.path.exists('encrypted_image.aes'):
        password = simpledialog.askstring("Password", "Enter the decryption password:", show='*')
        if password:
            decrypt_image('encrypted_image.aes', password, 'decrypted_image.png', original_image_size)
            img = Image.open('decrypted_image.png')
            img.thumbnail((200, 200))
            img_display = ImageTk.PhotoImage(img)
            img_label.config(image=img_display)
            img_label.image = img_display
            print("Decrypted image displayed.")

# GUI Setup

root = tk.Tk()
root.title("Image Encryption & Decryption using AES with Password")

# this function adds the kpgu logo at tkinter's default logo  

icon = PhotoImage(file='kpgu.JPG')
root.iconphoto(False,icon)
img_path = ""
original_image_size = None

frame = tk.Frame(root)
frame.pack(pady=20)

# Button to select image

select_button = tk.Button(frame, text="Select Image", command=select_image)
select_button.grid(row=0, column=0, padx=10)

# Button to encrypt image

encrypt_button = tk.Button(frame, text="Encrypt Image", command=encrypt)
encrypt_button.grid(row=0, column=1, padx=10)

# Button to decrypt image

decrypt_button = tk.Button(frame, text="Decrypt Image", command=decrypt)
decrypt_button.grid(row=0, column=2, padx=10)

# Label to display image

img_label = tk.Label(root)
img_label.pack(pady=20)

root.mainloop()
