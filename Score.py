import os
import json

class Score:
    def __init__(self):
        self.point = 1
        self.autoPoint = 0
        self.score = 0
        self.upgradeCost = 50
        self.level = 1
        self.nextLevelScore = 1000
        self.specialClickBought = False
        self.specialClickLevel = 1
        self.specialClickCost = 20000
        self.investments = [
            {"name": "Fundusz inwestycyjny", "baseCost": 600, "income": 6, "count": 0, "unlockLevel": 2},
            {"name": "Firma", "baseCost": 6000, "income": 60, "count": 0, "unlockLevel": 4},
            {"name": "Korporacja", "baseCost": 12000, "income": 120, "count": 0, "unlockLevel": 8}
        ]
        self.themeName = "Niebieski"
        self.fontSize = 14

    def getScore(self):
        return self.score

    def getPoint(self):
        return self.point

    def getAutoPoint(self):
        return self.autoPoint

    def getLevel(self):
        return self.level

    def getNextLevelScore(self):
        return self.nextLevelScore

    def getProgress(self):
        return self.score

    def getProgressMax(self):
        return self.nextLevelScore

    def getUpgradeCost(self):
        return self.upgradeCost

    def getInvestments(self):
        return self.investments

    def getInvestmentCost(self, index):
        investment = self.investments[index]
        return int(investment["baseCost"] * (1.25 ** investment["count"]))

    def isInvestmentUnlocked(self, index):
        return self.level >= self.investments[index]["unlockLevel"]

    def isSpecialClickUnlocked(self):
        return self.level >= 5

    def isSpecialClickBought(self):
        return self.specialClickBought

    def getSpecialClickCost(self):
        return self.specialClickCost

    def getSpecialClickMultiplier(self):
        return 1 + self.specialClickLevel / 100

    def getThemeName(self):
        return self.themeName

    def setThemeName(self, themeName):
        self.themeName = themeName

    def getFontSize(self):
        return self.fontSize

    def setFontSize(self, fontSize):
        self.fontSize = fontSize

    def addClick(self):
        self.score += self.point

    def addSpecialClick(self):
        self.score = int(self.score * self.getSpecialClickMultiplier())

    def addAuto(self):
        self.score += self.autoPoint

    def addBonus(self, bonus):
        self.score += bonus

    def buyUpgrade(self):
        if self.score >= self.upgradeCost:
            self.score -= self.upgradeCost
            self.point = max(self.point + 1, int(self.point * 1.5))
            self.upgradeCost = int(self.upgradeCost * 1.5)
            return True
        return False

    def buySpecialClick(self):
        if not self.isSpecialClickUnlocked():
            return "locked"
        if self.score >= self.specialClickCost:
            self.score -= self.specialClickCost
            if self.specialClickBought:
                self.specialClickLevel += 1
            else:
                self.specialClickBought = True
            self.specialClickCost = int(self.specialClickCost * 1.6)
            return "bought"
        return "no_money"

    def buyInvestment(self, index):
        if not self.isInvestmentUnlocked(index):
            return "locked"
        cost = self.getInvestmentCost(index)
        investment = self.investments[index]
        if self.score >= cost:
            self.score -= cost
            investment["count"] += 1
            self.autoPoint += investment["income"]
            return "bought"
        return "no_money"

    def setNextLevelScore(self):
        if self.level == 1:
            self.nextLevelScore = 1000
        elif self.level == 2:
            self.nextLevelScore = 5000
        else:
            self.nextLevelScore = 5000 * (2 ** (self.level - 2))

    def checkLevelUp(self):
        leveledUp = False
        totalBonus = 0
        while self.score >= self.nextLevelScore:
            oldLevelScore = self.nextLevelScore
            self.level += 1
            bonus = int(oldLevelScore * 0.1)
            self.score += bonus
            totalBonus += bonus
            self.setNextLevelScore()
            leveledUp = True
        if leveledUp:
            return self.level, totalBonus
        return None, 0

    def saveGame(self):
        data = {
            "score": self.score,
            "point": self.point,
            "autoPoint": self.autoPoint,
            "upgradeCost": self.upgradeCost,
            "level": self.level,
            "nextLevelScore": self.nextLevelScore,
            "specialClickBought": self.specialClickBought,
            "specialClickLevel": self.specialClickLevel,
            "specialClickCost": self.specialClickCost,
            "investments": self.investments,
            "themeName": self.themeName,
            "fontSize": self.fontSize
        }
        with open("save.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def loadGame(self):
        with open("save.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        self.score = data["score"]
        self.point = data["point"]
        self.autoPoint = data["autoPoint"]
        self.upgradeCost = data["upgradeCost"]
        self.level = data["level"]
        self.nextLevelScore = data["nextLevelScore"]
        self.specialClickBought = data.get("specialClickBought", False)
        self.specialClickLevel = data.get("specialClickLevel", 1)
        self.specialClickCost = data.get("specialClickCost", 20000)
        self.investments = data["investments"]
        self.themeName = data.get("themeName", "Niebieski")
        self.fontSize = data.get("fontSize", 14)

    def saveExists(self):
        return os.path.exists("save.json")