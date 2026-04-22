from tkinter import *
from tkinter import messagebox
import Score

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

root = Tk()
root.title("pyClicker")
root.iconbitmap("icon.ico")

frame = Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10)

score = Score.Score()

label = Label(frame, text="Punkty: 0", font=("Arial", 14))
label.grid(row=0, column=0, columnspan=2, pady=5)

pointLabel = Label(frame, text="Klik: +1", font=("Arial", 12))
pointLabel.grid(row=1, column=0, columnspan=2)

autoLabel = Label(frame, text="Auto Pkt: +0", font=("Arial", 12))
autoLabel.grid(row=2, column=0, columnspan=2)

button = Button(frame, text="Click Me", command=click, width=20, height=2)
button.grid(row=3, column=0, columnspan=2, pady=10)

upgradeButton = Button(frame, text="Ulepsz klik", command=buyUpgrade, width=20)
upgradeButton.grid(row=4, column=0)

upgradeLabel = Label(frame, text="50 Pkt")
upgradeLabel.grid(row=4, column=1)

autoUpgradeButton = Button(frame, text="Ulepsz auto", command=buyAutoUpgrade, width=20)
autoUpgradeButton.grid(row=5, column=0)

autoUpgradeLabel = Label(frame, text="100 Pkt")
autoUpgradeLabel.grid(row=5, column=1)

autoPoints()

root.resizable(False, False)
root.mainloop()