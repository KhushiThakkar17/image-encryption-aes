from tkinter import *

root = Tk()

root.geometry("500x400")
root.minsize(300,300)

root.title("CAPSTONE PROJECT")
label = Label(text="Image Encryption and Decryption", bg="blue",fg="black",padx=5,pady=5 , font="timesroman 12 bold", borderwidth=5, relief=SUNKEN)
label.pack(side=TOP,fill=X)
button = Button(root,bg="green",fg="white",text="Add File",font="timesroman 10 bold", relief=SUNKEN)
button.pack(side=BOTTOM,)
root.mainloop()