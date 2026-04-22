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

    def getUpgradeCost(self):
        return self.upgradeCost

    def buyUpgrade(self):
        if self.score >= self.upgradeCost:
            self.score -= self.upgradeCost
            self.point += 2
            self.upgradeCost = int(self.upgradeCost * 1.5)
            return True
        return False

    def getAutoUpgradeCost(self):
        return self.autoUpgradeCost

    def buyAutoUpgrade(self):
        if self.score >= self.autoUpgradeCost:
            self.score -= self.autoUpgradeCost
            self.autoPoint += 1
            self.autoUpgradeCost = int(self.autoUpgradeCost * 1.5)
            return True
        return False

    def addBonus(self, bonus):
        self.score += bonus