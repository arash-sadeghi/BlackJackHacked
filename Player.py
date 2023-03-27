import numpy as np
import random
import os
class Player:
    def __init__(self,points,fileDir):
        self.points = points
        self.softTable = np.zeros((21-2+1, 11-2+1 , 3 , 3)) 
        self.hardTable = np.zeros((21-2+1, 11-2+1 , 3 , 3)) #! sums * dealer card * hit/stay/double * win/loss/push
        self.MCsoftTable = np.zeros((11-2+1, 11-2+1 , 2)) 
        self.MChardTable = np.zeros((21-2+1, 11-2+1 , 2)) #! sums * dealer card * hit/stay

        self.fileDir = fileDir
        self.valueOptimalTables()
        self.e = 0.1 #Epsilon Value for Monte Carlo Algorithm
        self.gamma = 1 #Gamma Value for Monte Carlo Algorithm
        self.alpha=0.02

    def valueOptimalTables(self):
        #! hard table
        self.optimalTableHard = np.zeros((21-2+1, 11-2+1))

        self.optimalTableHard[0:8-2+1 , :] = 1 #! 1 is hit 0 is stay 

        self.optimalTableHard[9-2 , 2-2] = 1
        self.optimalTableHard[9-2 , 3-2:6-2+1] = 2 #! 2 is double
        self.optimalTableHard[9-2 , 6-2+1:] = 1 
        
        self.optimalTableHard[10-2 , 0:9-2+1] = 2
        self.optimalTableHard[10-2 , 9-2+1:] = 1

        self.optimalTableHard[11-2 , :] = 2

        self.optimalTableHard[12-2 , 2-2:3-2+1] = 1
        self.optimalTableHard[12-2 , 3-2+1:6-2+1] = 0
        self.optimalTableHard[12-2 , 6-2+1:] = 1

        self.optimalTableHard[13-2 : 16-2+1  , 0:6-2+1] = 0
        self.optimalTableHard[13-2 : 16-2+1  , 6-2+1:] = 1

        self.optimalTableHard[17-2: , :] = 0

        #! soft table
        self.optimalTableSoft = np.zeros((9-2+1, 11-2+1))
        
        self.optimalTableSoft[2-2 , 2-2:4-2+1] = 1 
        self.optimalTableSoft[2-2 , 4-2+1:6-2+1] = 2 
        self.optimalTableSoft[2-2 , 6-2+1:] = 1

        self.optimalTableSoft[3-2 , 2-2:4-2+1] = 1 
        self.optimalTableSoft[3-2 , 4-2+1:6-2+1] = 2 
        self.optimalTableSoft[3-2 , 6-2+1:] = 1

        self.optimalTableSoft[4-2 , 2-2:3-2+1] = 1 
        self.optimalTableSoft[4-2 , 3-2+1:6-2+1] = 2 
        self.optimalTableSoft[4-2 , 6-2+1:] = 1

        self.optimalTableSoft[5-2 , 2-2:3-2+1] = 1 
        self.optimalTableSoft[5-2 , 3-2+1:6-2+1] = 2 
        self.optimalTableSoft[5-2 , 6-2+1:] = 1

        self.optimalTableSoft[6-2 , 2-2:2-2+1] = 1 
        self.optimalTableSoft[6-2 , 2-2+1:6-2+1] = 2 
        self.optimalTableSoft[6-2 , 6-2+1:] = 1

        self.optimalTableSoft[7-2 , 2-2:6-2+1] = 3 #! 3 double if allowed otherwise stand 
        self.optimalTableSoft[7-2 , 6-2+1:8-2+1] = 0 
        self.optimalTableSoft[7-2 , 8-2+1:] = 1

        self.optimalTableSoft[8-2 , 2-2:5-2+1] = 0
        self.optimalTableSoft[8-2 , 5-2+1:6-2+1] = 3
        self.optimalTableSoft[8-2 , 6-2+1:] = 0

        self.optimalTableSoft[9-2 , :] = 0

        #! split table
        self.optimalTableSplit = np.zeros((11-2+1, 11-2+1))

        self.optimalTableSplit[2-2 , 2-2:3-2+1] = 4 #! split only if DAS is offered
        self.optimalTableSplit[2-2 , 3-2+1:7-2+1] = 5 #! split
        self.optimalTableSplit[2-2 , 7-2+1:] = 6 #! dont split

        self.optimalTableSplit[3-2 , 2-2:3-2+1] = 4 
        self.optimalTableSplit[3-2 , 3-2+1:7-2+1] = 5 
        self.optimalTableSplit[3-2 , 7-2+1:] = 6 

        self.optimalTableSplit[4-2 , 2-2:4-2+1] = 6 
        self.optimalTableSplit[4-2 , 4-2+1:6-2+1] = 4 
        self.optimalTableSplit[4-2 , 6-2+1:] = 6 

        self.optimalTableSplit[5-2 , :] = 6

        self.optimalTableSplit[6-2 , 2-2:2-2+1] = 4
        self.optimalTableSplit[6-2 , 2-2+1:6-2+1] = 5
        self.optimalTableSplit[6-2 , 6-2+1:] = 6

        self.optimalTableSplit[7-2 , 2-2:7-2+1] = 5
        self.optimalTableSplit[7-2 , 7-2+1:] = 6

        self.optimalTableSplit[8-2 , :] = 5 

        self.optimalTableSplit[9-2 , 2-2:6-2+1] = 5
        self.optimalTableSplit[9-2 , 6-2+1:7-2+1] = 6
        self.optimalTableSplit[9-2 , 7-2+1:9-2+1] = 5
        self.optimalTableSplit[9-2 , 9-2+1:] = 6

        self.optimalTableSplit[10-2 , :] = 6 
        
        self.optimalTableSplit[11-2 , :] = 5 
    
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

    def alwaysHit(self):
        return 'hit'

    def alwaysStay(self):
        return 'stay'

    def optimalTable(self,cards):
        dealerCardValue = self.points[cards[0]]
        playerCards = cards[1:]
        playerCardsSum = sum([self.points[_] for _ in playerCards])

        if 'A' in playerCards:
            rowIndex = playerCards[0] if playerCards[1] == 'A' else playerCards[1]
            rowIndex = self.points[rowIndex]
            action = self.optimalTableSoft[rowIndex-2,dealerCardValue-2]
        else:
            action = self.optimalTableHard[playerCardsSum-2,dealerCardValue-2]

        if action == 1:
            return 'hit'
        elif action == 0:
            return 'stay'
        elif action == 2 or action == 3:
            return 'double'
        else:
            raise NameError('[-] invalid action chosen')

    def arashCoded(self,cards):
        dealerCard = cards[0]
        dealerCardValue = self.points[cards[0]]
        playerCards = cards[1:]
        playerCardsSum = sum([self.points[_] for _ in playerCards])

        if playerCardsSum > 21 and 'A' in playerCards: #! for the case of A A
            playerCards[playerCards.index('A')] = 'As'
        playerCardsSum = sum([self.points[_] for _ in playerCards])

        if playerCardsSum >= 17:
            return 'stay'
        elif playerCardsSum<=11:
            return 'hit'
        elif dealerCardValue >= 7:
            return 'hit'
        elif dealerCardValue < 7:
            return 'stay'

    def exploreAllActions(self,cards):
        dealerCard = cards[0]
        dealerCardValue = self.points[cards[0]]
        playerCards = cards[1:]
        playerCardsSum = sum([self.points[_] for _ in playerCards])

        explored = 0
        exploredRec =[]
        for i in range(self.hardTable.shape[2]): #! within actions
            for j in range(self.hardTable.shape[3]): #! within results
                if 'A' in playerCards: #? can be optimized
                    explored += self.softTable[playerCardsSum-2][dealerCardValue-2][i][j]
                else:
                    explored += self.hardTable[playerCardsSum-2][dealerCardValue-2][i][j]
            exploredRec.append(explored)
            explored = 0
        
        actionIndex = exploredRec.index(min(exploredRec))
        
        if actionIndex == 0 :
            return 'hit' 
        elif actionIndex == 1:
            return 'stay' 
        elif actionIndex == 2:
            return 'double'
        else:
            raise NameError('[-][PLAYER] wrong action index')

    def decide(self,cards):
        # return self.interact()
        # return self.arashCoded(cards)
        # return self.randomPlayer()
        # return self.optimalTable(cards)
        # return self.alwaysHit()
        # return self.alwaysStay()
        # return self.exploreAllActions(cards)
        return self.MCtakeAction(cards)


    def record(self,cardsOnTable , decision , result):
        #! record functions different than soft table. because in record you might have more than one card
        #! record is called when there is a result. if you hit and game does not result in anything, its not recorded
        dealerCard = cardsOnTable[0]
        dealerCardValue = self.points[dealerCard]
        playerCards = cardsOnTable[1:]
        playerCardsSum = sum([self.points[_] for _ in playerCards])

        if decision == 'hit':
            actionIndex = 0 
        elif decision == 'stay':
            actionIndex = 1 
        elif decision == 'double':
            actionIndex = 2 

        if 'A' in playerCards:
            if 'playerWon' in result:
                resultIndex = 0 
            elif 'playerLost' in result:
                resultIndex = 1 
            elif result == 'push':
                resultIndex = 2
            else:
                raise NameError("[player] invalid result")
            self.softTable[playerCardsSum-2][dealerCardValue-2][actionIndex][resultIndex] += 1 

        else: 
            if 'playerWon' in result: #! considering double
                resultIndex = 0 
            elif 'playerLost' in result: #! considering double
                resultIndex = 1 
            elif result == 'push':
                resultIndex = 2
            else:
                raise NameError("[player] invalid result")

            self.hardTable[playerCardsSum-2][dealerCardValue-2][actionIndex][resultIndex] += 1 
    
    def saveRecords(self):
        np.save(os.path.join(self.fileDir,"playerhardTable.npy"),self.hardTable)
        np.save(os.path.join(self.fileDir,"playersoftTable.npy"),self.softTable)
        np.save(os.path.join(self.fileDir,"MCplayerhard.npy"),self.MChardTable)
        np.save(os.path.join(self.fileDir,"MCplayersoft.npy"),self.MCsoftTable)

    def learnMC(self,gameTrack):
        allRewards = []
        for i in range(len(gameTrack)):
            if gameTrack[i][2] == "handInProgress": allRewards.append(0)
            elif gameTrack[i][2] == "playerLost": allRewards.append(-1)
            elif gameTrack[i][2] == "playerWon": allRewards.append(1)
        allRewards = np.array(allRewards)

        for i in range(len(gameTrack)):
            state = gameTrack[i][0]
            dealerValue = self.points[state[0]]
            palyerValue = 0
            for j in range(1,len(state)):
                palyerValue += self.points[state[j]]
            action = gameTrack[i][1]

            if action == 'hit':
                action = 0
            elif action == 'stay':
                action = 1
            rewards = allRewards[i:]
            discountRate = [self.gamma**k for k in range(1,len(rewards)+1)] # Create a list with the gamma rate increasing
            updatedReward = rewards*discountRate # Discounting the rewards from t+1 onwards
            Gt = np.sum(updatedReward) # Summing up the discounted rewards to equal the return at time step t
            if 'A' in state[1:]: #! ace in hand of player
                self.MCsoftTable[ palyerValue-11-2 , dealerValue-2 , action] += self.alpha *(Gt - self.MCsoftTable[ palyerValue-11-2 , dealerValue-2 , action])           
            else:
                self.MChardTable[ palyerValue-2 , dealerValue-2 , action] += self.alpha *(Gt - self.MChardTable[ palyerValue-2 , dealerValue-2 , action])           

    def MCtakeAction(self,cards):
        dealerCard = cards[0]
        dealerCardValue = self.points[cards[0]]
        playerCards = cards[1:]
        playerCardsSum = sum([self.points[_] for _ in playerCards])        
        if 'A' in playerCards:
            probHit = self.MCsoftTable[playerCardsSum-11-2 , dealerCardValue-2 , 0]
            probStick = self.MCsoftTable[playerCardsSum-11-2 , dealerCardValue-2 , 1]
        else:
            probHit = self.MChardTable[playerCardsSum-2 , dealerCardValue-2 , 0]
            probStick = self.MChardTable[playerCardsSum-2 , dealerCardValue-2 , 1]


        if probHit>probStick:
            probs = [1-self.e, self.e]
        elif probStick>probHit:
            probs = [self.e, 1-self.e]
        else:
            probs = [0.5, 0.5]
            
        action = np.random.choice(np.arange(2), p=probs)   
        if action == 0:
            return 'hit'
        elif action == 1:
            return 'stay'
        else:
            raise NameError('[-] MC chose invlid action')
