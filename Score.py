class Score:
    def __init__(self):
        self.point = 1
        self.score = 0

    def setScore(self, score):
        self.score = score

    def getScore(self):
        return self.score

    def setPoint(self, point):
        self.point = point

    def getPoint(self):
        return self.point

    def addPoints(self):
        self.score += self.point