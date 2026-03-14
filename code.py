import os
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
from PIL import Image, ImageTk
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import binascii

# Base directory for loading images correctly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------- KEY GENERATION ----------------

def derive_key(password, salt):
    backend = default_backend()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )

    key = kdf.derive(password.encode())
    return key


# ---------------- ENCRYPTION ----------------

def encrypt_image(image_path, password):

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    salt = os.urandom(16)
    print("Encryption Salt:", binascii.hexlify(salt))

    key = derive_key(password, salt)

    iv = os.urandom(16)
    print("Encryption IV:", binascii.hexlify(iv))

    cipher = Cipher(
        algorithms.AES(key),
        modes.CFB(iv),
        backend=default_backend()
    )

    encryptor = cipher.encryptor()

    encrypted_image = encryptor.update(image_data) + encryptor.finalize()

    return salt, iv, encrypted_image


# ---------------- DECRYPTION ----------------

def decrypt_image(encrypted_data, password, salt, iv, save_path):

    key = derive_key(password, salt)

    cipher = Cipher(
        algorithms.AES(key),
        modes.CFB(iv),
        backend=default_backend()
    )

    decryptor = cipher.decryptor()

    try:
        decrypted_image = decryptor.update(encrypted_data) + decryptor.finalize()
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {e}")
        return

    try:
        with open(save_path, "wb") as image_file:
            image_file.write(decrypted_image)

        img = Image.open(save_path)
        img.show()

        messagebox.showinfo("Success", "Image decrypted and saved successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save decrypted image: {e}")


# ---------------- GUI FUNCTIONS ----------------

def select_image():

    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.enc")]
    )

    if file_path:
        image_entry.delete(0, tk.END)
        image_entry.insert(0, file_path)


def encrypt_button_action():

    password = password_entry.get()
    image_path = image_entry.get()

    if not password or not image_path:
        messagebox.showwarning("Input Error", "Please provide password and image.")
        return

    try:

        salt, iv, encrypted_image = encrypt_image(image_path, password)

        save_path = filedialog.asksaveasfilename(
            title="Save Encrypted File",
            defaultextension=".enc",
            filetypes=[("Encrypted Files", "*.enc")]
        )

        if not save_path:
            return

        with open(save_path, "wb") as f:
            f.write(salt + iv + encrypted_image)

        messagebox.showinfo("Success", "Image encrypted successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {e}")


def decrypt_button_action():

    password = password_entry.get()
    image_path = image_entry.get()

    if not password or not image_path:
        messagebox.showwarning("Input Error", "Please provide password and encrypted file.")
        return

    try:

        with open(image_path, "rb") as f:
            file_data = f.read()

        salt = file_data[:16]
        iv = file_data[16:32]
        encrypted_image = file_data[32:]

        save_path = filedialog.asksaveasfilename(
            title="Save Decrypted Image",
            defaultextension=".png",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )

        if not save_path:
            return

        decrypt_image(encrypted_image, password, salt, iv, save_path)

    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {e}")


# ---------------- GUI WINDOW ----------------

root = tk.Tk()

root.title("Image Encryption and Decryption using AES Algorithm")

root.geometry("600x400")

root.minsize(610, 600)


# Background Image

bg_image = tk.PhotoImage(
    file=os.path.join(BASE_DIR, "KD_Background.png")
)

bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)


# Window Icon

icon = PhotoImage(
    file=os.path.join(BASE_DIR, "Project_logo.png")
)

root.iconphoto(False, icon)


# ---------------- FILE INPUT ----------------

tk.Label(
    root,
    text="Select Image File or Encrypted File:",
    bg="light yellow",
    font=("TimesNewRoman", 10, "bold")
).grid(row=0, column=0, padx=10, pady=10)


image_entry = tk.Entry(root, width=40)
image_entry.grid(row=0, column=1, padx=10, pady=10)


# Browse Button

img = Image.open(os.path.join(BASE_DIR, "Browse_button.png"))
resized_img = img.resize((24, 24), Image.LANCZOS)
browse_icon = ImageTk.PhotoImage(resized_img)

browse_button = tk.Button(
    root,
    image=browse_icon,
    text="Browse",
    bg="light blue",
    compound="left",
    command=select_image
)

browse_button.grid(row=0, column=2, padx=10, pady=10)


# ---------------- PASSWORD INPUT ----------------

tk.Label(
    root,
    text="Password:",
    bg="light yellow",
    font=("TimesNewRoman", 10, "bold")
).grid(row=1, column=0, padx=10, pady=10)


password_entry = tk.Entry(root, show="*", width=40)
password_entry.grid(row=1, column=1, padx=10, pady=10)


# ---------------- ENCRYPT BUTTON ----------------

img = Image.open(os.path.join(BASE_DIR, "Encrypt_button.png"))
resized_img = img.resize((24, 24), Image.LANCZOS)
encrypt_icon = ImageTk.PhotoImage(resized_img)

encrypt_button = tk.Button(
    root,
    image=encrypt_icon,
    text="Encrypt",
    bg="tan",
    compound="left",
    command=encrypt_button_action
)

encrypt_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")


# ---------------- DECRYPT BUTTON ----------------

img = Image.open(os.path.join(BASE_DIR, "Decrypt_button.png"))
resized_img = img.resize((24, 24), Image.LANCZOS)
decrypt_icon = ImageTk.PhotoImage(resized_img)

decrypt_button = tk.Button(
    root,
    image=decrypt_icon,
    text="Decrypt",
    bg="tan",
    compound="left",
    command=decrypt_button_action
)

decrypt_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")


# ---------------- RUN GUI ----------------

root.mainloop()