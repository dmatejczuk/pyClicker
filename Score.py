import os

class Score:
    def __init__(self):
        self.point = 1
        self.autoPoint = 0
        self.score = 0
        self.upgradeCost = 50
        self.autoUpgradeCost = 100

    def getScore(self):
        return self.score

    def getPoint(self):
        return self.point

    def getAutoPoint(self):
        return self.autoPoint

    def addClick(self):
        self.score += self.point

    def addAuto(self):
        self.score += self.autoPoint

    def addBonus(self, bonus):
        self.score += bonus

    def getUpgradeCost(self):
        return self.upgradeCost

    def getAutoUpgradeCost(self):
        return self.autoUpgradeCost

    def buyUpgrade(self):
        if self.score >= self.upgradeCost:
            self.score -= self.upgradeCost
            self.point += 2
            self.upgradeCost = int(self.upgradeCost * 1.5)
            return True
        return False

    def buyAutoUpgrade(self):
        if self.score >= self.autoUpgradeCost:
            self.score -= self.autoUpgradeCost
            self.autoPoint += 1
            self.autoUpgradeCost = int(self.autoUpgradeCost * 1.5)
            return True
        return False

    def saveGame(self):
        file = open("save.txt", "w")
        file.write(str(self.score) + "\n")
        file.write(str(self.point) + "\n")
        file.write(str(self.autoPoint) + "\n")
        file.write(str(self.upgradeCost) + "\n")
        file.write(str(self.autoUpgradeCost) + "\n")
        file.close()

    def loadGame(self):
        file = open("save.txt", "r")
        lines = file.readlines()
        file.close()

        self.score = int(lines[0].strip())
        self.point = int(lines[1].strip())
        self.autoPoint = int(lines[2].strip())
        self.upgradeCost = int(lines[3].strip())
        self.autoUpgradeCost = int(lines[4].strip())

    def saveExists(self):
        return os.path.exists("save.txt")