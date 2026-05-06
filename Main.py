from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import random
import Score

backgroundColor = "#3D82ED"
panelColor = "#19376D"
currentBonusValue = 20
bonusVisible = False
bonusShowAfterId = None
bonusHideAfterId = None

def updateLabels():
    label.config(text="Punkty: " + str(score.getScore()))
    pointLabel.config(text="Umiejętności: +" + str(score.getPoint()))
    autoLabel.config(text="Inwestycje: +" + str(score.getAutoPoint()) + "/s")
    levelLabel.config(text="Poziom: " + str(score.getLevel()))
    nextLevelLabel.config(text="Następny poziom: " + str(score.getNextLevelScore()) + " pkt")
    skillButton.config(text="Rozwijaj umiejętności\nKoszt: " + str(score.getUpgradeCost()) + " Pkt")
    progressBar["maximum"] = max(1, score.getProgressMax())
    progressBar["value"] = min(score.getProgress(), score.getProgressMax())

    if score.isSpecialClickBought():
        specialButton.grid(row=7, column=0, columnspan=2, pady=(0, 10))
        specialButton.config(text="Innowacyjność\nx" + str(round(score.getSpecialClickMultiplier(), 2)))
    else:
        specialButton.grid_forget()

    if not score.isSpecialClickUnlocked():
        specialUpgradeButton.config(state="disabled", text="Innowacyjność\nOd poziomu 5")
    elif score.isSpecialClickBought():
        specialUpgradeButton.config(state="normal", text="Ulepsz Innowacyjność\nKoszt: " + str(score.getSpecialClickCost()) + " pkt")
    else:
        specialUpgradeButton.config(state="normal", text="Kup Innowacyjność\nKoszt: " + str(score.getSpecialClickCost()) + " pkt")

    updateInvestmentLabels()

def updateInvestmentLabels():
    for i in range(len(investmentLabels)):
        investment = score.getInvestments()[i]
        cost = score.getInvestmentCost(i)
        if score.isInvestmentUnlocked(i):
            investmentLabels[i].config(text=investment["name"] + "\nCena: " + str(cost) + " pkt | +" + str(investment["income"]) + "/s | x" + str(investment["count"]))
            investmentButtons[i].config(state=NORMAL)
        else:
            investmentLabels[i].config(text=investment["name"] + "\nOd poziomu " + str(investment["unlockLevel"]))
            investmentButtons[i].config(state=DISABLED)

def click():
    score.addClick()
    checkLevelUp()
    updateLabels()

def specialClick():
    score.addSpecialClick()
    checkLevelUp()
    updateLabels()

def autoPoints():
    if score.getAutoPoint() > 0:
        score.addAuto()
        checkLevelUp()
        updateLabels()

    root.after(1000, autoPoints)

def buyUpgrade():
    if score.buyUpgrade():
        updateLabels()
    else:
        messagebox.showerror("Błąd", "Nie masz punktów!")

def buySpecialClick():
    result = score.buySpecialClick()
    if result == "bought":
        updateLabels()
    elif result == "locked":
        messagebox.showerror("Błąd", "Innowacyjność jest dostępny od poziomu 5!")
    else:
        messagebox.showerror("Błąd", "Nie masz wystarczająco punktów!")

def buyInvestment(index):
    result = score.buyInvestment(index)
    if result == "bought":
        updateLabels()
    elif result == "locked":
        messagebox.showerror("Błąd", "Ta inwestycja nie jest jeszcze odblokowana!")
    else:
        messagebox.showerror("Błąd", "Nie masz wystarczająco punktów!")

def saveGame():
    score.saveGame()
    messagebox.showinfo("Zapis", "Gra została zapisana.")

def startGame():
    if score.saveExists():
        answer = messagebox.askyesno("Zapis gry", "Znaleziono zapis gry.\nCzy chcesz wczytać grę?")
        if answer:
            score.loadGame()

def onClosing():
    saveAnswer = messagebox.askyesno("Zapis", "Czy chcesz zapisać grę?")

    if saveAnswer:
        score.saveGame()
        exitAnswer = messagebox.askyesno("Wyjście", "Gra została zapisana.\nCzy chcesz wyjść z gry?")
        if exitAnswer:
            root.destroy()
    else:
        exitAnswer = messagebox.askyesno("Wyjście", "Czy chcesz wyjść z gry?")
        if exitAnswer:
            root.destroy()

def checkLevelUp():
    level, bonus = score.checkLevelUp()
    if level is not None:
        messagebox.showinfo("Awans!", "Awansowałeś na poziom " + str(level) + "!\nBonus: +" + str(bonus) + " pkt")

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
    checkLevelUp()
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
    x = random.randint(20, 1020)
    y = random.randint(20, 620)
    bonusButton.config(text="+" + str(currentBonusValue))
    bonusButton.place(x=x, y=y)
    bonusVisible = True
    bonusShowAfterId = None
    bonusHideAfterId = root.after(3000, hideBonus)

root = Tk()
root.title("pyClicker")
root.iconbitmap("icon.ico")
root.configure(bg=backgroundColor)
root.geometry("1120x700")
root.protocol("WM_DELETE_WINDOW", onClosing)
root.resizable(False, False)

score = Score.Score()
startGame()

mainFrame = Frame(root, bg=backgroundColor)
mainFrame.place(relx=0.5, rely=0.5, anchor="center")

leftFrame = Frame(mainFrame, bg=backgroundColor)
leftFrame.grid(row=0, column=0, padx=30, pady=20)

rightFrame = Frame(mainFrame, bg=panelColor, padx=18, pady=18)
rightFrame.grid(row=0, column=1, padx=30, pady=20)

label = Label(leftFrame, text="Punkty: 0", font=("Arial", 28, "bold"), bg=backgroundColor, fg="white")
label.grid(row=0, column=0, columnspan=2, pady=(10, 10))

pointLabel = Label(leftFrame, text="Umiejętności: +1", font=("Arial", 14), bg=backgroundColor, fg="white")
pointLabel.grid(row=1, column=0, columnspan=2, pady=3)

autoLabel = Label(leftFrame, text="Inwestycje: +0/s", font=("Arial", 14), bg=backgroundColor, fg="white")
autoLabel.grid(row=2, column=0, columnspan=2, pady=3)

levelLabel = Label(leftFrame, text="Poziom: 1", font=("Arial", 14), bg=backgroundColor, fg="white")
levelLabel.grid(row=3, column=0, columnspan=2, pady=3)

nextLevelLabel = Label(leftFrame, text="Następny poziom: 1000 pkt", font=("Arial", 12), bg=backgroundColor, fg="white")
nextLevelLabel.grid(row=4, column=0, columnspan=2, pady=3)

progressBar = ttk.Progressbar(leftFrame, length=300)
progressBar.grid(row=5, column=0, columnspan=2, pady=10)

mainButtonImage = PhotoImage(file="mainButton.png")
button = Button(leftFrame, image=mainButtonImage, command=click, borderwidth=0, highlightthickness=0, bg=backgroundColor, activebackground=backgroundColor)
button.grid(row=6, column=0, columnspan=2, pady=20)

specialButton = Button(leftFrame, text="Innowacyjność", command=specialClick, width=18, height=2, font=("Arial", 11, "bold"))

shopTitle = Label(rightFrame, text="ROZWÓJ", font=("Arial", 20, "bold"), bg=panelColor, fg="white")
shopTitle.grid(row=0, column=0, columnspan=2, pady=(0, 15))

skillButton = Button(rightFrame, text="Rozwijaj umiejętności\nKoszt: 50 pkt", command=buyUpgrade, width=28, height=2, font=("Arial", 11, "bold"))
skillButton.grid(row=1, column=0, columnspan=2, padx=6, pady=(0, 18))

specialUpgradeButton = Button(rightFrame, text="Innowacyjność\nOd poziomu 5", command=buySpecialClick, width=28, height=2, font=("Arial", 11, "bold"), state=DISABLED)
specialUpgradeButton.grid(row=2, column=0, columnspan=2, padx=6, pady=(0, 18))

investmentTitle = Label(rightFrame, text="INWESTYCJE", font=("Arial", 16, "bold"), bg=panelColor, fg="white")
investmentTitle.grid(row=3, column=0, columnspan=2, pady=(0, 10))

investmentButtons = []
investmentLabels = []

for i in range(len(score.getInvestments())):
    investmentButton = Button(rightFrame, text="Kup", command=lambda i=i: buyInvestment(i), width=8, font=("Arial", 10))
    investmentButton.grid(row=4 + i, column=0, padx=6, pady=8)
    investmentLabel = Label(rightFrame, text="", bg=panelColor, fg="white", font=("Arial", 10), justify="left", width=42, anchor="w")
    investmentLabel.grid(row=4 + i, column=1, padx=6, pady=8)
    investmentButtons.append(investmentButton)
    investmentLabels.append(investmentLabel)

bonusButton = Button(root, text="+20", command=bonusClick, bg="gold", fg="black", font=("Arial", 12, "bold"))

updateLabels()
autoPoints()
scheduleNextBonus()

root.mainloop()