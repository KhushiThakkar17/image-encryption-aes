# Image Encryption and Decryption using AES

This project implements a GUI-based image encryption and decryption tool using Python.  
It allows users to securely encrypt image files using a password and decrypt them back using the same password.

## Technologies Used
- Python
- Tkinter (GUI)
- Cryptography Library
- AES Encryption

## Features
- Encrypt images using password-based AES encryption
- Decrypt encrypted images with the correct password
- Simple graphical user interface
- Secure key generation using PBKDF2

## How to Run

Install dependencies:

pip install cryptography
pip install pillow

Run the program:

python img_encrypt_decrypt_aes.py

## Workflow

1. Launch the program
2. Click **Browse** and select an image
3. Enter a password
4. Click **Encrypt** and save the encrypted file
5. Select encrypted file and click **Decrypt**
6. Enter correct password to restore image

## Author
Khushi Thakkar