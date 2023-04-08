import numpy as np
import random
import os
from PIL import Image
from Constants import *

class Player:
    def __init__(self , fileDir , method , betUnit , hardUrl="" , softUrl="" , totalDecks = None):
        self.points = points
        self.softTable = np.zeros((21-2+1, 11-2+1 , 3 , 3)) 
        self.hardTable = np.zeros((21-2+1, 11-2+1 , 3 , 3)) #! sums * dealer card * stay/hit/double * win/loss/push
        self.method = method
        self.fileDir = fileDir
        self.betUnit = betUnit
        if self.method == METHODmc:
            self.MCsoftTable = np.zeros((11-2+1, 11-2+1 , 2)) 
            self.MChardTable = np.zeros((21-2+1, 11-2+1 , 2)) #! sums * dealer card * stay/hit
            # self.e = 0.1 #Epsilon Value for Monte Carlo Algorithm
            self.e = 0.01 #Epsilon Value for Monte Carlo Algorithm
            self.gamma = 1 #Gamma Value for Monte Carlo Algorithm
            self.alpha=0.01

        if self.method == METHODoptimalTable or self.method == METHODcountCard:
            self.valueOptimalTables()
        if self.method == METHODexternalQ:
            self.MCuplaod(hardUrl,softUrl) 
        if self.method == METHODcountCard:
            self.runningCount = 0
            self.trueCount = 0
            self.totalDecks = totalDecks

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
        self.optimalTableSoft = np.zeros((10-2+1, 11-2+1))
        
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
        self.optimalTableSoft[10-2 , :] = 0 #! including sum 21


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
            return HITstr
        elif key == 's':
            return STAYstr

    def randomPlayer(self):
        if random.random()>0.5:
            return HITstr
        else:
            return STAYstr

    def optimalTable(self,cards):
        dealerCardValue = self.points[cards[0]]
        playerCards = cards[1:]
        playerCardsSum = sum([self.points[_] for _ in playerCards])

        if 'A' in playerCards:
            if playerCards[0] == 'A' and playerCards[1] == 'A': #! special case
                rowIndex = 2 #! treat double ace as A and 2.     
            else:
                rowIndex = playerCardsSum - 11 
            action = self.optimalTableSoft[rowIndex-2,dealerCardValue-2]
        else:
            action = self.optimalTableHard[playerCardsSum-2,dealerCardValue-2]

        if action == HIT:
            return HITstr
        elif action == STAY:
            return STAYstr
        elif action == DOUBLE or action == DOUBLE2:
            if len(playerCards) >2: #! this is not first action. you cannot double
                return HITstr
            else:
                return DOUBLEstr
        else:
            raise NameError('[-] invalid action chosen')

    def arashCoded(self,cards):
        dealerCardValue = self.points[cards[0]]
        playerCards = cards[1:]
        playerCardsSum = sum([self.points[_] for _ in playerCards])

        if playerCardsSum > 21 and 'A' in playerCards: #! for the case of A A
            playerCards[playerCards.index('A')] = 'As'
        playerCardsSum = sum([self.points[_] for _ in playerCards])

        if playerCardsSum >= 17:
            return STAYstr
        elif playerCardsSum<=11:
            return HITstr
        elif dealerCardValue >= 7:
            return HITstr
        elif dealerCardValue < 7:
            return STAYstr

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
        
        if actionIndex == HIT :
            return HITstr 
        elif actionIndex == STAY:
            return STAYstr 
        elif actionIndex == DOUBLE:
            if len(playerCards) >2: #! this is not first action. you cannot double
                return HITstr
            else:
                return DOUBLEstr
        else:
            raise NameError('[-][PLAYER] wrong action index')

    def decide(self,cards):
        if self.method == METHODmc:
            return self.MCtakeAction(cards)
        elif self.method == METHODoptimalTable or self.method == METHODcountCard:
            return self.optimalTable(cards)
        elif self.method == METHODexternalQ:
            return self.MCtakeActionPreUploaded(cards)
        elif self.method == METHODarashCoded:
            return self.arashCoded(cards)
        else:
            raise NameError('Invalid decision method')
        # return self.interact()
        # return self.randomPlayer()
        # return self.alwaysHit()
        # return self.alwaysStay()
        # return self.exploreAllActions(cards)

    def record(self,cardsOnTable , decision , result):
        #! record functions different than soft table. because in record you might have more than one card
        #! record is called when there is a result. if you hit and game does not result in anything, its not recorded
        dealerCard = cardsOnTable[0]
        dealerCardValue = self.points[dealerCard]
        playerCards = cardsOnTable[1:]
        playerCardsSum = sum([self.points[_] for _ in playerCards])

        if decision == HITstr:
            actionIndex = HIT 
        elif decision == STAYstr:
            actionIndex = STAY
        elif decision == DOUBLEstr:
            actionIndex = DOUBLE

        if 'A' in playerCards:
            if WIN in result: #! in includes doubles as well
                resultIndex = 0 
            elif LOSS in result: #! in includes doubles as well
                resultIndex = 1 
            elif result == PUSH:
                resultIndex = 2
            else:
                raise NameError("[player] invalid result")
            self.softTable[playerCardsSum-2][dealerCardValue-2][actionIndex][resultIndex] += 1 

        else: 
            if WIN in result: #! considering double
                resultIndex = 0 
            elif LOSS in result: #! considering double
                resultIndex = 1 
            elif result == PUSH:
                resultIndex = 2
            else:
                raise NameError("[player] invalid result")

            self.hardTable[playerCardsSum-2][dealerCardValue-2][actionIndex][resultIndex] += 1 
    
    def saveRecords(self):
        np.save(os.path.join(self.fileDir,"playerhardTable.npy"),self.hardTable)
        np.save(os.path.join(self.fileDir,"playersoftTable.npy"),self.softTable)
        if self.method == METHODmc:
            np.save(os.path.join(self.fileDir,"MCplayerhard.npy"),self.MChardTable)
            np.save(os.path.join(self.fileDir,"MCplayersoft.npy"),self.MCsoftTable)

    def learnMC(self,gameTrack):
        allRewards = []
        for i in range(len(gameTrack)):
            if gameTrack[i][2] == "handInProgress": allRewards.append(0)
            elif gameTrack[i][2] == LOSS: allRewards.append(-1)
            elif gameTrack[i][2] == WIN: allRewards.append(1)
        allRewards = np.array(allRewards)

        for i in range(len(gameTrack)):
            state = gameTrack[i][0]
            dealerValue = self.points[state[0]]
            palyerValue = 0
            for j in range(1,len(state)):
                palyerValue += self.points[state[j]]
            action = gameTrack[i][1]

            if action == HITstr:
                action = HIT
            elif action == STAYstr:
                action = STAY
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
            probHit = self.MCsoftTable[playerCardsSum-11-2 , dealerCardValue-2 , HIT]
            probStick = self.MCsoftTable[playerCardsSum-11-2 , dealerCardValue-2 , STAY]
        else:
            probHit = self.MChardTable[playerCardsSum-2 , dealerCardValue-2 , HIT]
            probStick = self.MChardTable[playerCardsSum-2 , dealerCardValue-2 , STAY]


        if probHit>probStick:
            probs = [self.e, 1-self.e] #!!!!!!!!!!!!!!!!
        elif probStick>probHit:
            probs = [1-self.e, self.e]
        else:
            probs = [0.5, 0.5]
            
        action = np.random.choice(np.arange(2), p=probs)   
        if action == HIT:
            return HITstr
        elif action == STAY:
            return STAYstr
        else:
            raise NameError('[-] MC chose invlid action')
    
    def MCtakeActionPreUploaded(self,cards):
        dealerCard = cards[0]
        dealerCardValue = self.points[cards[0]]
        playerCards = cards[1:]
        playerCardsSum = sum([self.points[_] for _ in playerCards])        
        if 'A' in playerCards:
            probHit = self.MCsoftTableOnline[playerCardsSum-11-2 , dealerCardValue-2 , 1]
            probStick = self.MCsoftTableOnline[playerCardsSum-11-2 , dealerCardValue-2 , 0]
        else:
            probHit = self.MChardTableOnline[playerCardsSum-2 , dealerCardValue-2 , 1]
            probStick = self.MChardTableOnline[playerCardsSum-2 , dealerCardValue-2 , 0]


        if probHit>probStick:
            probs = [self.e, 1-self.e]
        elif probStick>probHit:
            probs = [1-self.e, self.e]
        else:
            probs = [0.5, 0.5]
            
        action = np.random.choice(np.arange(2), p=probs)   
        if action == HIT:
            return HITstr
        elif action == STAY:
            return STAYstr
        else:
            raise NameError('[-] MC chose invlid action')

    def countCards(self , cardsDealt , numAllDealt):
        for i in cardsDealt:
            if self.points[i]>=2 and self.points[i]<=6:
                self.runningCount += 1
            elif self.points[i]>= 10 or self.points[i] == 1: #! == 1 is for the case of soft ace
                self.runningCount -= 1

        remainingDeck = self.totalDecks - numAllDealt//52         
        self.trueCount = self.runningCount // remainingDeck 
        betWeight = self.trueCount - 1 if self.trueCount >= 3 else 1
        bet = self.betUnit * betWeight
        return bet

    def resetCounting(self):
        self.trueCount = 0
        self.runningCount = 0

    def MCuplaod(self,hardUrl,softUrl):
        self.MChardTableOnline = np.load(hardUrl)
        self.MCsoftTableOnline = np.load(softUrl)

    def vizMC(self,it): #! for MC online

        input_array = np.copy(self.MChardTable) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # input_array = np.copy(self.MChardTableOnline)

        # Define the colors for the table cells
        blue = (0, 0, 255) 
        red = (255, 0, 0)#! hit

        # Create the output image as a 2D array of pixels
        image_array = np.zeros((input_array.shape[0], input_array.shape[1], 3), dtype=np.uint8)

        # Set the colors of the pixels based on the input array
        for i in range(input_array.shape[0]):
            for j in range(input_array.shape[1]):
                if input_array[i, j ,0] > input_array[i, j ,1]:
                    image_array[i, j] = blue
                else:
                    image_array[i, j] = red

        # Create a PIL Image object from the pixel array
        image = Image.fromarray(image_array)
        image = image.resize((image_array.shape[1]*200,image_array.shape[0]*200))
        # Save the image to a file
        # file_name = os.path.splitext(os.path.basename(url))[0]
        file_name = os.path.join(self.fileDir,f"MyMChardTable{it}.png")

        image.save(file_name)