import random

class Dealer:
    def __init__(self,deck=8):
        self.deck = deck
        self.cards = self.createCard() 
        self.points = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10} #! Ace is just 11 for now
        self.shuffleCards()
        self.yellowPos = len(self.cards) // 2 #! approximate
        self.dealtCards = []
        self.playerHand = []
        self.dealerHand = []
    
    def createCard(self):
        oneDeck = [str(_) for _ in range(2,11)] #! 2 to 10
        oneDeck.extend(['J','Q','K','A']) #! shapes
        oneDeck *= 4 #! dimond club spade heart
        oneDeck *= self.deck #! deck
        return oneDeck

    def shuffleCards(self):
        random.shuffle(self.cards)

    def deal(self):
        chosenCards = self.cards[0:4] #! select four cards
        self.cards = self.cards[4:] #! delete those cards from availble cards
        self.dealtCards.extend(chosenCards) #! add chosen cards to dealt cards
        self.playerHand.extend(chosenCards[0:2])
        self.dealerHand.extend(chosenCards[2:4])
        return [self.dealerHand[0] , self.playerHand[0] , self.playerHand[1]] #! this return is mainly for player 
    
    def checkPlayerBJ(self):
        if self.points[self.playerHand[0]] + self.points[self.playerHand[1]] == 21:
            return 1 #! player blackjack
        else: 
            return 0 #! player not blackjack

    def takeAction(self,action):
        if action == 'hit':
            self.hit()
            playerHandSum = sum([self.points[_] for _ in self.playerHand])
            if playerHandSum > 21:
                return 'playerBust' #! palyer busted
            else:
                return 'handInProgress' #! hand is still going
        
        elif action == 'stay':
            return self.play() #! return result of dealer play
        else:
            raise NameError("[-] invalid decision")



    def hit(self):
        newCard= self.cards.pop(0) #! select new card
        self.dealtCards.extend(newCard) #! add new card to dealt card
        self.playerHand.extend(newCard) #! put new card in playerHand
    
    
    def play(self): #! 0 push 1 player win -1 player lost
        playerSum = sum([self.points[_] for _ in self.playerHand])
        dealerSum = sum([self.points[_] for _ in self.dealerHand])

        while dealerSum < 17: #! dealer needs to play
            newCard= self.cards.pop(0) #! select new card
            self.dealtCards.extend(newCard) #! add new card to dealt card
            self.dealerHand.extend(newCard) #! put new card in dealerHand
            dealerSum = sum([self.points[_] for _ in self.dealerHand])

        if dealerSum == 21: #! smart : if 21 is on first two cards, then its surely blackjack
            return -1 #! dealer blackjack
        
        elif dealerSum >= 17: 
            if dealerSum > playerSum:
                return 'playerLost' #! player lost
            elif dealerSum < playerSum:
                return 'playerWon' #! player won
            elif dealerSum == playerSum:
                return 'push' #! push

    def endHand(self):
        self.playerHand = []
        self.dealerHand = []


        
