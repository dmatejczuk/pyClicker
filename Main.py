from tkinter import *
import Score

def click():
    score.addPoints()
    label.config(text=str(score.getScore()))

root = Tk()
root.title("pyClicker")
root.iconbitmap("icon.ico")

frame = Frame(root)
frame.grid(row=0, column=0)

score = Score.Score()
score.setPoint(1)

label = Label(frame, text="0")
label.grid(row=0, column=0)

button = Button(frame, text="Click Me", command=lambda: click())
button.grid(row=1, column=0)

root.resizable(False, False)
root.mainloop()