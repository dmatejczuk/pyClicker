from tkinter import *
from tkinter import messagebox
import random
import Score

backgroundColor = "#3D82ED"
currentBonusValue = 20
bonusVisible = False
bonusShowAfterId = None
bonusHideAfterId = None

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

def getRandomBonusValue():
    return random.choices([20, 50, 100, 200, 500], weights=[50, 25, 15, 8, 2])[0]

def scheduleNextBonus():
    global bonusShowAfterId

    if bonusShowAfterId is not None:
        root.after_cancel(bonusShowAfterId)

    nextTime = random.randint(8000, 18000)
    bonusShowAfterId = root.after(nextTime, showBonus)

def bonusClick():
    global currentBonusValue
    global bonusVisible
    global bonusHideAfterId
    score.addBonus(currentBonusValue)
    updateLabels()
    bonusButton.place_forget()
    bonusVisible = False
    if bonusHideAfterId is not None:
        root.after_cancel(str(bonusHideAfterId))
        bonusHideAfterId = None
    scheduleNextBonus()

def hideBonus():
    global bonusVisible
    global bonusHideAfterId
    if bonusVisible:
        bonusButton.place_forget()
        bonusVisible = False
    bonusHideAfterId = None
    scheduleNextBonus()

def showBonus():
    global currentBonusValue
    global bonusVisible
    global bonusShowAfterId
    global bonusHideAfterId
    if bonusVisible:
        return
    currentBonusValue = getRandomBonusValue()
    x = random.randint(20, 420)
    y = random.randint(20, 500)
    bonusButton.config(text="+" + str(currentBonusValue))
    bonusButton.place(x=x, y=y)
    bonusVisible = True
    bonusShowAfterId = None
    bonusHideAfterId = root.after(3000, hideBonus)

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
button = Button(frame, image=mainButtonImage, command=click, borderwidth=0, highlightthickness=0, bg=backgroundColor, activebackground=backgroundColor)
button.grid(row=3, column=0, columnspan=2, pady=20)

upgradeButton = Button(frame, text="Ulepsz klik", command=buyUpgrade, width=20, font=("Arial", 12))
upgradeButton.grid(row=4, column=0, padx=10, pady=8)

upgradeLabel = Label(frame, text="50 Pkt", bg=backgroundColor, font=("Arial", 12), fg="white")
upgradeLabel.grid(row=4, column=1, padx=10, pady=8)

autoUpgradeButton = Button(frame, text="Ulepsz auto", command=buyAutoUpgrade, width=20, font=("Arial", 12))
autoUpgradeButton.grid(row=5, column=0, padx=10, pady=8)

autoUpgradeLabel = Label(frame, text="100 Pkt", bg=backgroundColor, font=("Arial", 12), fg="white")
autoUpgradeLabel.grid(row=5, column=1, padx=10, pady=8)

bonusButton = Button(root, text="+20", command=bonusClick, bg="gold", fg="black", font=("Arial", 12, "bold"))

autoPoints()
scheduleNextBonus()

root.resizable(False, False)
root.mainloop()