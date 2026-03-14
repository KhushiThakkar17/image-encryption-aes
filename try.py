import tkinter as tk

def move_circle():
    global x, direction
    canvas.move(circle, direction, 0)
    x += direction
    if x > 350 or x < 50:
        direction *= -1
    root.after(50, move_circle)

root = tk.Tk()
root.title("Animation Example")
root.geometry("400x300")

canvas = tk.Canvas(root, bg="white", width=400, height=300)
canvas.pack()

# Draw a circle
x, direction = 50, 5
circle = canvas.create_oval(x-25, 100-25, x+25, 100+25, fill="blue")

# Start animation
move_circle()

root.mainloop()