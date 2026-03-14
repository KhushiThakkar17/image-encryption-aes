from cryptography.fernet import Fernet
# to generate the secret key to encrypt the file
secret_key = Fernet.generate_key()
# print(secret_key)
#for ENCRYPTION PROCESS
fernet = Fernet(secret_key)


with open('secret_key.key',"wb") as filekey :
    filekey.write(secret_key)
    
with open('secret_key.key',"rb") as filekey :
    secret_key = filekey.read()
    
with open('computer.jpeg',"rb") as file :
    real_file = file.read()
    
#for encryption..
    
encrypted = fernet.encrypt(real_file)

with open('encrypted computer.jpeg',"wb") as file :
    file.write(encrypted)
    
fernet = Fernet(secret_key)

with open('encrypted computer.jpeg',"rb") as file :
    encrypted_file = file.read()

#for decryption 

decrypted = fernet.decrypt(encrypted_file)

with open('decrypted computer.jpeg',"wb") as file :
    file.write(decrypted)