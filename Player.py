

class Player:
    def __init__(self):
        self.points = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10} #! Ace is just 11 for now
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