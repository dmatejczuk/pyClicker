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

def money(value):
    return str(int(value)) + " $"

def updateLabels():
    label.config(text=money(score.getScore()))
    pointLabel.config(text="Umiejętności: +" + money(score.getPoint()))
    autoLabel.config(text="Inwestycje: +" + money(score.getAutoPoint()) + "/s")
    levelLabel.config(text="Poziom: " + str(score.getLevel()))
    nextLevelLabel.config(text="Następny poziom: " + money(score.getNextLevelScore()))
    skillButton.config(text="Rozwijaj umiejętności\nKoszt: " + money(score.getUpgradeCost()))
    progressBar["maximum"] = max(1, score.getProgressMax())
    progressBar["value"] = min(score.getProgress(), score.getProgressMax())

    if score.isSpecialClickBought():
        specialButton.grid(row=8, column=0, columnspan=2, pady=(0, 10))
        specialButton.config(text="Innowacyjność\nx" + str(round(score.getSpecialClickMultiplier(), 2)))
    else:
        specialButton.grid_forget()

    if not score.isSpecialClickUnlocked():
        specialUpgradeButton.config(state="disabled", text="Innowacyjność\nOd poziomu 5")
    elif score.isSpecialClickBought():
        specialUpgradeButton.config(state="normal", text="Ulepsz Innowacyjność\nKoszt: " + money(score.getSpecialClickCost()))
    else:
        specialUpgradeButton.config(state="normal", text="Kup Innowacyjność\nKoszt: " + money(score.getSpecialClickCost()))

    updateInvestmentLabels()

def updateInvestmentLabels():
    for i in range(len(investmentLabels)):
        investment = score.getInvestments()[i]
        cost = score.getInvestmentCost(i)
        if score.isInvestmentUnlocked(i):
            investmentLabels[i].config(text=investment["name"] + "\nCena: " + money(cost) + " | +" + money(investment["income"]) + "/s | x" + str(investment["count"]))
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
        messagebox.showerror("Błąd", "Nie masz pieniędzy!")

def buySpecialClick():
    result = score.buySpecialClick()
    if result == "bought":
        updateLabels()
    elif result == "locked":
        messagebox.showerror("Błąd", "Innowacyjność jest dostępna od poziomu 5!")
    else:
        messagebox.showerror("Błąd", "Nie masz wystarczająco pieniędzy!")

def buyInvestment(index):
    result = score.buyInvestment(index)
    if result == "bought":
        updateLabels()
    elif result == "locked":
        messagebox.showerror("Błąd", "Ta inwestycja nie jest jeszcze odblokowana!")
    else:
        messagebox.showerror("Błąd", "Nie masz wystarczająco pieniędzy!")

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
        messagebox.showinfo("Awans!", "Awansowałeś na poziom " + str(level) + "!\nBonus: +" + money(bonus))

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
    bonusButton.config(text="+" + money(currentBonusValue))
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

moneyTitleLabel = Label(leftFrame, text="PIENIĄDZE", font=("Arial", 14, "bold"), bg=backgroundColor, fg="white")
moneyTitleLabel.grid(row=0, column=0, columnspan=2, pady=(10, 0))

label = Label(leftFrame, text="0 $", font=("Arial", 28, "bold"), bg=backgroundColor, fg="white")
label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

pointLabel = Label(leftFrame, text="Umiejętności: +1 $", font=("Arial", 14), bg=backgroundColor, fg="white")
pointLabel.grid(row=2, column=0, columnspan=2, pady=3)

autoLabel = Label(leftFrame, text="Inwestycje: +0 $/s", font=("Arial", 14), bg=backgroundColor, fg="white")
autoLabel.grid(row=3, column=0, columnspan=2, pady=3)

levelLabel = Label(leftFrame, text="Poziom: 1", font=("Arial", 14), bg=backgroundColor, fg="white")
levelLabel.grid(row=4, column=0, columnspan=2, pady=3)

nextLevelLabel = Label(leftFrame, text="Następny poziom: 1000 $", font=("Arial", 12), bg=backgroundColor, fg="white")
nextLevelLabel.grid(row=5, column=0, columnspan=2, pady=3)

progressBar = ttk.Progressbar(leftFrame, length=300)
progressBar.grid(row=6, column=0, columnspan=2, pady=10)

mainButtonImage = PhotoImage(file="./mainButton.png")
button = Button(leftFrame, image=mainButtonImage, command=click, borderwidth=0, highlightthickness=0, bg=backgroundColor, activebackground=backgroundColor)
button.grid(row=7, column=0, columnspan=2, pady=20)

specialButton = Button(leftFrame, text="Innowacyjność", command=specialClick, width=18, height=2, font=("Arial", 11, "bold"))

shopTitle = Label(rightFrame, text="ROZWÓJ", font=("Arial", 20, "bold"), bg=panelColor, fg="white")
shopTitle.grid(row=0, column=0, columnspan=2, pady=(0, 15))

skillButton = Button(rightFrame, text="Rozwijaj umiejętności\nKoszt: 50 $", command=buyUpgrade, width=28, height=2, font=("Arial", 11, "bold"))
skillButton.grid(row=1, column=0, columnspan=2, padx=6, pady=(0, 18))

specialUpgradeButton = Button(rightFrame, text="Innowacyjność\nOd poziomu 5", command=buySpecialClick, width=28, height=2, font=("Arial", 11, "bold"), state=DISABLED)
specialUpgradeButton.grid(row=2, column=0, columnspan=2, padx=6, pady=(0, 18))

investmentTitle = Label(rightFrame, text="INWESTYCJE", font=("Arial", 16, "bold"), bg=panelColor, fg="white")
investmentTitle.grid(row=3, column=0, columnspan=2, pady=(0, 10))

investmentButtons = []
investmentLabels = []

cartImage = PhotoImage(file="./cart.png")
cartImage = cartImage.subsample(4, 4)

for i in range(len(score.getInvestments())):
    investmentButton = Button(rightFrame, image=cartImage, command=lambda i=i: buyInvestment(i), bd=0, relief="flat", highlightthickness=0, bg=panelColor, activebackground=panelColor, width=cartImage.width(), height=cartImage.height())
    investmentButton.grid(row=4 + i, column=0, padx=6, pady=8)
    investmentButton.image = cartImage
    investmentLabel = Label(rightFrame, text="", bg=panelColor, fg="white", font=("Arial", 10), justify="left", width=42, anchor="w")
    investmentLabel.grid(row=4 + i, column=1, padx=6, pady=8)
    investmentButtons.append(investmentButton)
    investmentLabels.append(investmentLabel)

bonusImage = PhotoImage(file="./dollar.png")
bonusImage = bonusImage.subsample(3, 3)
bonusButton = Button(root, image=bonusImage, text="+20 $", compound="center", command=bonusClick, font=("Arial", 10, "bold"), fg="white", bd=0, relief="flat", highlightthickness=0, padx=0, pady=0, bg=backgroundColor, activebackground=backgroundColor)

updateLabels()
autoPoints()
scheduleNextBonus()

root.mainloop()