

class Player:
    def __init__(self,points):
        self.points = points
    def decide(self,cards):
        playerSum = sum([self.points[_] for _ in cards[1:]])
        key = input('[player] decide >>> ')
        if key == 'h':
            return 'hit'
        elif key == 's':
            return 'stay'

        pass
    def learn(self,*args):
        pass