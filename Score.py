import os

class Score:
    def __init__(self):
        self.point = 1
        self.autoPoint = 0
        self.score = 0
        self.upgradeCost = 50
        self.autoUpgradeCost = 100
        self.level = 1
        self.nextLevelScore = 1000

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
            self.point *= 2
            self.upgradeCost = int(self.upgradeCost * 1.5)
            return True
        return False

    def buyAutoUpgrade(self):
        if self.score >= self.autoUpgradeCost:
            self.score -= self.autoUpgradeCost
            if self.autoPoint == 0:
                self.autoPoint = 1
            else:
                self.autoPoint *= 2
            self.autoUpgradeCost = int(self.autoUpgradeCost * 1.5)
            return True
        return False

    def checkLevelUp(self):
        leveledUp = False
        totalBonus = 0
        while self.score >= self.nextLevelScore:
            oldLevel = self.level
            self.level += 1
            if self.nextLevelScore == 1000:
                self.nextLevelScore = 5000
            else:
                self.nextLevelScore = int(self.nextLevelScore * 2.5)
            bonus = oldLevel * 100
            self.score += bonus
            totalBonus += bonus
            leveledUp = True
        if leveledUp:
            return self.level, totalBonus
        return None, 0

    def saveGame(self):
        file = open("save.txt", "w")
        file.write(str(self.score) + "\n")
        file.write(str(self.point) + "\n")
        file.write(str(self.autoPoint) + "\n")
        file.write(str(self.upgradeCost) + "\n")
        file.write(str(self.autoUpgradeCost) + "\n")
        file.write(str(self.level) + "\n")
        file.write(str(self.nextLevelScore) + "\n")
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

        if len(lines) > 5:
            self.level = int(lines[5].strip())
            self.nextLevelScore = int(lines[6].strip())

    def saveExists(self):
        return os.path.exists("save.txt")