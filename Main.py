from tkinter import *
from tkinter import messagebox
import random
import Score

backgroundColor = "#3D82ED"

def updateLabels():
    label.config(text="Punkty: " + str(score.getScore()))
    pointLabel.config(text="Klik: +" + str(score.getPoint()))
    autoLabel.config(text="Auto: +" + str(score.getAutoPoint()))
    upgradeLabel.config(text=str(score.getUpgradeCost()) + " Pkt")
    autoUpgradeLabel.config(text=str(score.getAutoUpgradeCost()) + " Pkt")

def click():
    score.addClick()
    updateLabels()

def autoPoints():
    if score.getAutoPoint() > 0:
        score.addAuto()
        updateLabels()

    root.after(1000, autoPoints)

def buyUpgrade():
    if score.buyUpgrade():
        updateLabels()
    else:
        messagebox.showerror("Błąd", "Nie masz punktów!")

def buyAutoUpgrade():
    if score.buyAutoUpgrade():
        updateLabels()
    else:
        messagebox.showerror("Błąd", "Nie masz punktów!")

def bonusClick():
    score.addBonus(500)
    updateLabels()
    bonusButton.place_forget()

def hideBonus():
    bonusButton.place_forget()

def showBonus():
    x = random.randint(20, 420)
    y = random.randint(20, 500)

    bonusButton.place(x=x, y=y)
    root.after(3000, hideBonus)
    root.after(60000, showBonus)

root = Tk()
root.title("pyClicker")
root.iconbitmap("icon.ico")
root.configure(bg=backgroundColor)
root.geometry("600x700")

score = Score.Score()

frame = Frame(root, bg=backgroundColor)
frame.place(relx=0.5, rely=0.5, anchor="center")

label = Label(frame, text="Punkty: 0", font=("Arial", 20, "bold"), bg=backgroundColor, fg="white")
label.grid(row=0, column=0, columnspan=2, pady=(10, 10))

pointLabel = Label(frame, text="Klik: +1", font=("Arial", 14), bg=backgroundColor, fg="white")
pointLabel.grid(row=1, column=0, columnspan=2, pady=3)

autoLabel = Label(frame, text="Auto: +0", font=("Arial", 14), bg=backgroundColor, fg="white")
autoLabel.grid(row=2, column=0, columnspan=2, pady=3)

mainButtonImage = PhotoImage(file="mainButton.png")
button = Button(
    frame,
    image=mainButtonImage,
    command=click,
    borderwidth=0,
    highlightthickness=0,
    bg=backgroundColor,
    activebackground=backgroundColor
)
button.grid(row=3, column=0, columnspan=2, pady=20)

upgradeButton = Button(frame, text="Ulepsz klik", command=buyUpgrade, width=20, font=("Arial", 12))
upgradeButton.grid(row=4, column=0, padx=10, pady=8)

upgradeLabel = Label(frame, text="50 Pkt", bg=backgroundColor, font=("Arial", 12), fg="white")
upgradeLabel.grid(row=4, column=1, padx=10, pady=8)

autoUpgradeButton = Button(frame, text="Ulepsz auto", command=buyAutoUpgrade, width=20, font=("Arial", 12))
autoUpgradeButton.grid(row=5, column=0, padx=10, pady=8)

autoUpgradeLabel = Label(frame, text="100 Pkt", bg=backgroundColor, font=("Arial", 12), fg="white")
autoUpgradeLabel.grid(row=5, column=1, padx=10, pady=8)

bonusButton = Button(root, text="+500", command=bonusClick, bg="gold", fg="black", font=("Arial", 12, "bold"))

autoPoints()
root.after(60000, showBonus)

root.resizable(False, False)
root.mainloop()