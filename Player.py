import numpy as np
import random
class Player:
    def __init__(self,points,logName):
        self.points = points
        self.softTable = np.zeros((21-2+1, 11-2+1 , 2 , 3)) #! sums * dealer card * hit/stay * win/loss/push
        self.hardTable = np.zeros((21-2+1, 11-2+1 , 2 , 3)) 
        self.fileName = logName

    def interact(self):
        key = input('[player] decide >>> ')
        if key == 'h':
            return 'hit'
        elif key == 's':
            return 'stay'

    def randomPlayer(self):
        if random.random()>0.5:
            return 'hit'
        else:
            return 'stay'



    def arashCoded(self,cards):
        dealerCard = cards[0]
        dealerCardValue = self.points[cards[0]]
        playerCards = cards[1:]
        playerCardsSum = sum([self.points[_] for _ in playerCards])

        if playerCardsSum >= 17:
            return 'stay'
        elif playerCardsSum<=11:
            return 'hit'
        elif dealerCardValue >= 7:
            return 'hit'
        elif dealerCardValue < 7:
            return 'stay'




    def decide(self,cards):
        # return self.interact()
        # return self.arashCoded(cards)
        return self.randomPlayer()

    def record(self,cardsOnTable , decision , result):
        dealerCard = cardsOnTable[0]
        dealerCardValue = self.points[dealerCard]
        playerCards = cardsOnTable[1:]
        playerCardsSum = sum([self.points[_] for _ in playerCards])
        if playerCardsSum > 21 and 'A' in playerCards:
            playerCards[playerCards.index('A')] = 'As'
            playerCardsSum -= 10
        if 'A' in playerCards:
            actionIndex = 0 if decision == 'hit' else 1
            if result == 'playerWon':
                resultIndex = 0 
            elif result == 'playerLost':
                resultIndex = 1 
            elif result == 'push':
                resultIndex = 2
            else:
                raise NameError("[player] invalid result")

            self.softTable[playerCardsSum-2][dealerCardValue-2][actionIndex][resultIndex] += 1 

        else: 
            actionIndex = 0 if decision == 'hit' else 1
            if result == 'playerWon':
                resultIndex = 0 
            elif result == 'playerLost':
                resultIndex = 1 
            elif result == 'push':
                resultIndex = 2
            else:
                raise NameError("[player] invalid result")

            self.hardTable[playerCardsSum-2][dealerCardValue-2][actionIndex][resultIndex] += 1 
    
    def saveRecords(self):
        np.save("logs/playerhardTable"+self.fileName+".npy",self.hardTable)
        np.save("logs/playersoftTable"+self.fileName+".npy",self.softTable)

