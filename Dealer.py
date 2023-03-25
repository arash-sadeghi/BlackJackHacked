import random

class Dealer:
    def __init__(self,deck=8):
        self.deck = deck
        cardsStr = self.createCard() #? cards with shape
        self.cards = self.createValues(cardsStr) #? only value of cards
        self.shuffleCards()
        self.yellowPos = len(self.cards) // 2 #? approximate
        self.dealtCards = []
        self.turn = 'dealer' #? ['dealer','palyer']
        self.playerHand = []
        self.dealerHand = []
        self.playerSoft == 0 #?
    
    def deal(self):
        chosenCards = self.cards[0:4] #? select four cards
        self.cards = self.cards[4:] #? delete those cards from availble cards
        self.dealtCards.extend(chosenCards) #? add chosen cards to dealt cards
        self.turn = 'palyer'
        self.playerHand.extend(chosenCards[0:2])
        self.playerSoft == 1 #?

        self.dealerHand.extend(chosenCards[2:4])
    
    def createCard(self):
        oneDeck = [str(_) for _ in range(2,11)] #? 2 to 10
        oneDeck.extend(['J','Q','K','A']) #? shapes
        oneDeck *= 4 #? dimond club spade heart
        oneDeck *= self.deck #? deck
        return oneDeck

    def createValues(self,cards):
        values = []
        for i in cards:
            if i == 'A':
                values.append(11)
            elif i == 'J' or i == 'Q' or i == 'K':
                values.append(10)
            else:
                values.append(int(i))
        return values
    
    def shuffleCards(self):
        random.shuffle(self.cards)

    def hit(self):
        newCard = self.cards[0] #? select new card
        self.cards = self.cards[1:] #? delete selected card from availble cards
        self.dealtCards.extend(newCard) #? add new card to dealt card
        if self.turn == 'player':
            self.playerHand.extend(newCard) #? put new card in playerHand
        elif self.turn == 'dealer':
            self.dealerHand.extend(newCard) #? put new card in playerHand
    
    def playerStand(self):
        self.turn = 'dealer'
    
    def resetHand(self):
        self.playerHand = []
        self.dealerHand = []

    def checkTable(self): #? 0 hand is in progredd 1 player wim -1 player lose 2 push
        if sum(self.playerHand) > 21 and self.turn == 'palyer': #? palyer busted
            self.resetHand()
            self.turn = 'dealer'
            returnValue = -1

        elif self.turn == 'palyer': #? hand is in progress
            returnValue = 0

        elif sum(self.dealerHand) >= 17 : #? its dealers turn and his sum is above= 17
            if sum(self.dealerHand) > 21 : #? dealer bust
                returnValue = 1
            elif sum(self.dealerHand) > sum(self.playerHand) : #? dealer win
                self.resetHand()
                returnValue = -1
            elif sum(self.dealerHand) < sum(self.playerHand) : #? palyer win
                self.resetHand()
                returnValue = 1
            else: #? push
                self.resetHand()
                returnValue = 2
            self.resetHand()
            self.turn = 'dealer'

        else: #? dealer should continue
            returnValue = 0

        return returnValue

class Player:
    pass

player = Player()
dealer = Dealer()
table = dealer.deal()
decision = player.decide([dealer.dealerHand[0] , sum(dealer.playerHand) ,  ])
if decision == 'hit':
    dealer.hit()
elif decision == 'stand':
    dealer.stand()
status = dealer.checkTable()

print(table)
        
