from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import random
import Score

backgroundColor = "#EDEDED"
panelColor = "#BDBDBD"
textColor = "black"
fontSize = 14
themes = {
    "Blue": ("#3D82ED", "#19376D"),
    "Gray": ("#808080", "#404040"),
    "White": ("#EDEDED", "#BDBDBD"),
    "Green": ("#2E6F40", "#1A2421")
}
currentBonusValue = 20
bonusVisible = False
bonusShowAfterId = None
bonusHideAfterId = None
settingsWindow = None
screenWidth = 1120
screenHeight = 700
worldDecorations = []

def money(value):
    return str(int(value)) + " $"

def changeTheme(choice):
    global backgroundColor
    global panelColor
    global textColor

    score.setThemeName(choice)
    backgroundColor, panelColor = themes[choice]

    if choice == "White":
        textColor = "black"
    else:
        textColor = "white"

    root.configure(bg=backgroundColor)
    mainFrame.configure(bg=backgroundColor)
    leftFrame.configure(bg=backgroundColor)
    rightFrame.configure(bg=panelColor)
    worldCanvas.configure(bg=backgroundColor)
    button.configure(bg=backgroundColor, activebackground=backgroundColor)
    bonusButton.configure(bg=backgroundColor, activebackground=backgroundColor)

    labels = [moneyTitleLabel, label, pointLabel, autoLabel, levelLabel, nextLevelLabel, shopTitle, investmentTitle]
    for widget in labels:
        widget.configure(bg=backgroundColor if widget in [moneyTitleLabel, label, pointLabel, autoLabel, levelLabel, nextLevelLabel] else panelColor)

    moneyTitleLabel.configure(fg=textColor)
    label.configure(fg=textColor)
    pointLabel.configure(fg=textColor)
    autoLabel.configure(fg=textColor)
    levelLabel.configure(fg=textColor)
    nextLevelLabel.configure(fg=textColor)
    shopTitle.configure(fg=textColor)
    investmentTitle.configure(fg=textColor)

    for investmentLabel in investmentLabels:
        investmentLabel.configure(bg=panelColor, fg=textColor)

    for investmentButton in investmentButtons:
        investmentButton.configure(bg=panelColor, activebackground=panelColor)

def openSettingsWindow():
    global settingsWindow
    if settingsWindow is not None and settingsWindow.winfo_exists():
        settingsWindow.focus()
        settingsWindow.lift()
        return
    settingsWindow = Toplevel(root)
    settingsWindow.title("Ustawienia")
    settingsWindow.iconbitmap("icon.ico")
    settingsWindow.geometry("300x300")
    settingsWindow.resizable(False, False)
    settingsWindow.configure(bg=panelColor)

    settingsWindow.transient(root)
    settingsWindow.focus_force()

    title = Label(settingsWindow, text="USTAWIENIA", font=("Arial", 16, "bold"), bg=panelColor, fg=textColor)
    title.pack(pady=12)

    themeLabel = Label(settingsWindow, text="Motyw kolorystyczny", font=("Arial", 11, "bold"), bg=panelColor, fg=textColor)
    themeLabel.pack(pady=5)

    Button(settingsWindow, text="Blue", command=lambda: changeTheme("Blue"), width=18).pack(pady=2)
    Button(settingsWindow, text="Gray", command=lambda: changeTheme("Gray"), width=18).pack(pady=2)
    Button(settingsWindow, text="White", command=lambda: changeTheme("White"), width=18).pack(pady=2)
    Button(settingsWindow, text="Green", command=lambda: changeTheme("Green"), width=18).pack(pady=2)

    fontLabel = Label(settingsWindow, text="Rozmiar czcionki", font=("Arial", 11, "bold"), bg=panelColor, fg=textColor)
    fontLabel.pack(pady=(10, 4))

    fontFrame = Frame(settingsWindow, bg=panelColor)
    fontFrame.pack()

    Button(fontFrame, text="A+", command=increaseFont, width=8).grid(row=0, column=0, padx=4)
    Button(fontFrame, text="A-", command=decreaseFont, width=8).grid(row=0, column=1, padx=4)

    def onSettingsClose():
        global settingsWindow

        if settingsWindow is not None:
            settingsWindow.destroy()

        settingsWindow = None

    settingsWindow.protocol("WM_DELETE_WINDOW", onSettingsClose)

def increaseFont():
    global fontSize
    fontSize += 2
    score.setFontSize(fontSize)
    updateFonts()

def decreaseFont():
    global fontSize
    if fontSize > 8:
        fontSize -= 2
    score.setFontSize(fontSize)
    updateFonts()

def updateFonts():
    label.config(font=("Arial", fontSize + 14, "bold"))

    pointLabel.config(font=("Arial", fontSize))
    autoLabel.config(font=("Arial", fontSize))
    levelLabel.config(font=("Arial", fontSize))
    nextLevelLabel.config(font=("Arial", fontSize - 2))

    moneyTitleLabel.config(font=("Arial", fontSize, "bold"))

    shopTitle.config(font=("Arial", fontSize + 6, "bold"))
    investmentTitle.config(font=("Arial", fontSize + 2, "bold"))

    skillButton.config(font=("Arial", fontSize - 1, "bold"))
    specialUpgradeButton.config(font=("Arial", fontSize - 1, "bold"))
    settingsButton.config(font=("Arial", fontSize - 1, "bold"))

    specialButton.config(font=("Arial", fontSize - 1, "bold"))

    for investmentLabel in investmentLabels:
        investmentLabel.config(font=("Arial", fontSize - 2))
    for investmentButton in investmentButtons:
        investmentButton.config(width=cartImage.width(), height=cartImage.height())

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
    updateLabels()
    checkLevelUp()
    updateLabels()

def specialClick():
    score.addSpecialClick()
    updateLabels()
    checkLevelUp()
    updateLabels()

def autoPoints():
    if score.getAutoPoint() > 0:
        score.addAuto()
        updateLabels()
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
        investmentName = score.getInvestments()[index]["name"]
        if investmentName == "Firma" or investmentName == "Korporacja":
            createWorldDecoration(investmentName)
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
        levelWindow = Toplevel(root)
        levelWindow.title("Awans!")
        levelWindow.iconbitmap("icon.ico")
        levelWindow.geometry("280x310")
        levelWindow.resizable(False, False)
        levelWindow.configure(bg=backgroundColor)

        levelWindow.transient(root)
        levelWindow.grab_set()
        levelWindow.focus_force()

        medalCanvas = Canvas(levelWindow, width=180, height=180, bg=backgroundColor, highlightthickness=0)
        medalCanvas.pack(pady=(15, 5))

        medalCanvas.create_image(90, 90, image=medalImage)
        medalCanvas.create_text(90, 90, text=str(level), font=("Arial", 24, "bold"), fill="white")

        infoLabel = Label(levelWindow, text="Gratulacje!\nOsiągnięto poziom " + str(level) + "\nBonus: +" + money(bonus), font=("Arial", 12, "bold"), bg=backgroundColor, fg=textColor, justify="center")
        infoLabel.pack(pady=8)

        Button(levelWindow, text="Zamknij", command=levelWindow.destroy, width=12).pack(pady=(0, 12))

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
    bonusButton.config(text=money(currentBonusValue))
    bonusButton.place(x=x, y=y)
    bonusVisible = True
    bonusShowAfterId = None
    bonusHideAfterId = root.after(3000, hideBonus)

def createWorldDecoration(investmentName):
    if investmentName == "Firma":
        image = companyImage
    elif investmentName == "Korporacja":
        image = corporationImage
    else:
        return

    bottomY = 30
    spacing = 90
    startX = 30
    x = startX + (len(worldDecorations) * spacing)
    if x > screenWidth - 120:
        x = random.randint(30, screenWidth - 120)
    decoration = worldCanvas.create_image(x, bottomY, image=image, anchor="nw")
    worldDecorations.append(decoration)

def loadWorldDecorations():
    investments = score.getInvestments()
    for investment in investments:
        if investment["name"] == "Firma" or investment["name"] == "Korporacja":
            for i in range(investment["count"]):
                createWorldDecoration(investment["name"])

root = Tk()
root.title("pyClicker")
root.iconbitmap("icon.ico")
root.configure(bg=backgroundColor)
root.geometry(f"{screenWidth}x{screenHeight}")
root.protocol("WM_DELETE_WINDOW", onClosing)
root.resizable(False, False)

score = Score.Score()
startGame()

worldCanvas = Canvas(root, width=1120, height=120, bg=backgroundColor, bd=0, highlightthickness=0)
worldCanvas.place(x=0, y=580)

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

companyImage = PhotoImage(file="./company.png")
companyImage = companyImage.subsample(5, 5)

corporationImage = PhotoImage(file="./corporation.png")
corporationImage = corporationImage.subsample(5, 5)

medalImage = PhotoImage(file="./medal.png")
medalImage = medalImage.subsample(3, 3)

for i in range(len(score.getInvestments())):
    investmentButton = Button(rightFrame, image=cartImage, command=lambda i=i: buyInvestment(i), bd=0, relief="flat", highlightthickness=0, bg=panelColor, activebackground=panelColor, width=cartImage.width(), height=cartImage.height())
    investmentButton.grid(row=4 + i, column=0, padx=6, pady=8)
    investmentButton.image = cartImage
    investmentLabel = Label(rightFrame, text="", bg=panelColor, fg="white", font=("Arial", 10), justify="left", width=42, anchor="w")
    investmentLabel.grid(row=4 + i, column=1, padx=6, pady=8)
    investmentButtons.append(investmentButton)
    investmentLabels.append(investmentLabel)

settingsButton = Button(rightFrame, text="Ustawienia", command=openSettingsWindow, width=28, font=("Arial", 11, "bold"))
settingsButton.grid(row=7, column=0, columnspan=2, pady=(18, 0))

bonusImage = PhotoImage(file="./dollar.png")
bonusImage = bonusImage.subsample(3, 3)
bonusButton = Button(root, image=bonusImage, text="20 $", compound="center", command=bonusClick, font=("Arial", 10, "bold"), fg="white", bd=0, relief="flat", highlightthickness=0, padx=0, pady=0, bg=backgroundColor, activebackground=backgroundColor)

fontSize = score.getFontSize()
updateFonts()
changeTheme(score.getThemeName())

updateLabels()
loadWorldDecorations()
autoPoints()
scheduleNextBonus()

root.mainloop()