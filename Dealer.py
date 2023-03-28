import random
class Dealer:
    def __init__(self,points,deck=8):
        self.deck = deck
        self.cards = self.createCard() 
        self.points = points
        # random.seed(100) #! DEBUG
        self.shuffleCards()
        self.yellowPos = len(self.cards) // 2 #! approximate
        self.dealtCards = []
        self.playerHand = []
        self.dealerHand = []
        self.shoeChange = False
        
    
    
    def createCard(self):
        oneDeck = [str(_) for _ in range(2,11)] #! 2 to 10
        oneDeck.extend(['J','Q','K','A']) #! shapes
        oneDeck *= 4 #! dimond club spade heart
        oneDeck *= self.deck #! deck
        return oneDeck

    def shuffleCards(self):
        random.shuffle(self.cards)

    def giveCards(self,num):
        chosenCards = self.cards[0:num] #! select four cards
        self.cards = self.cards[num:] #! delete those cards from availble cards
        self.dealtCards.extend(chosenCards) #! add chosen cards to dealt cards
        if len(self.cards) <= self.yellowPos:
            self.shoeChange = True
        return chosenCards

    def deal(self):
        chosenCards = self.giveCards(4)
        self.playerHand.extend(chosenCards[0:2])
        if self.playerHand[0] == 'A' and self.playerHand[1] == 'A': #! handling A A case
            self.playerHand[1] = 'As'

        self.dealerHand.extend(chosenCards[2:4])
        if self.dealerHand[0] == 'A' and self.dealerHand[1] == 'A':
            self.dealerHand[1] = 'As'

        return [self.dealerHand[0] , self.playerHand[0] , self.playerHand[1]] #! this return is mainly for player 
    
    def checkPlayerBJ(self):
        if self.points[self.playerHand[0]] + self.points[self.playerHand[1]] == 21:
            return 1 #! player blackjack
        else: 
            return 0 #! player not blackjack

    def checkBust(self,hand):
        HandSum = sum([self.points[_] for _ in hand])
        if 'A' in hand:
            if HandSum > 21 and HandSum-10 <= 21:
                return 0 #! soft hand and not busted and A is 1 after this
            elif HandSum > 21 and HandSum-10 > 21:
                return 1 #! soft hand and busted
            elif HandSum <= 21:
                return -1 #! soft hand and not busted

        elif HandSum > 21: 
            return 1 #! busted
        else:
            return -1 #! not busted


    def takeAction(self,action): #! 'playerLost' 'handInProgress' 'playerWon' 'push'
        if action == 'hit':
            self.hit()
            bustRes = self.checkBust(self.playerHand)
            if bustRes == 1:
                return 'playerLost' #! palyer busted
            elif bustRes == -1:
                return 'handInProgress' #! hand is still going
            elif bustRes == 0: #! ace is 1 after this
                self.playerHand[ self.playerHand.index('A') ] = 'As' #! Ace is by default considered 11. this solves the fact that player should take the maximum from players hand in soft hands
                return 'handInProgress' #! hand is still going

        
        elif action == 'stay':
            return self.play() #! return result of dealer play

        elif action == 'double':
            if len(self.playerHand)>2:
                raise NameError('[-] invalid double')

            self.hit()
            bustRes = self.checkBust(self.playerHand)
            if bustRes == 1:
                return 'playerLostDouble' #! palyer busted
            elif bustRes == 0: #! ace is 1 after this. bustRes is zero only if there is a ace in hand
                self.playerHand[ self.playerHand.index('A') ] = 'As' #! Ace is by default considered 11. this solves the fact that player should take the maximum from players hand in soft hands
            
            dealerRes = self.play() #! return result of dealer play
            if dealerRes == "playerWon":
                return "playerWonDouble"
            elif dealerRes == "playerLost":            
                return "playerLostDouble"
            elif dealerRes == "push":            
                return "push"

        else:
            raise NameError("[-] invalid decision")



    def hit(self):
        newCard= self.giveCards(1)[0] #! select new card
        self.playerHand.append(newCard) #! put new card in playerHand
    
    
    def play(self): #! 0 push 1 player win -1 player lost
        playerSum = sum([self.points[_] for _ in self.playerHand])
        dealerSum = sum([self.points[_] for _ in self.dealerHand])

        while dealerSum < 17: #! dealer needs to play
            newCard= self.giveCards(1)[0] #! select new card
            if 'A' in self.dealerHand:
                if newCard == 'A': #! 2 aces would definitly bust dealer, so it should count soft
                    newCard = 'As'
                elif dealerSum + self.points[newCard]> 21: #! new card is busting the hand, ace should become 1
                    self.dealerHand[self.dealerHand.index('A')] = 'As'
            self.dealerHand.append(newCard) #! put new card in dealerHand
            dealerSum = sum([self.points[_] for _ in self.dealerHand])

        if dealerSum > 21:
            return 'playerWon' #! dealer busted

        elif dealerSum == 21: #! smart : if 21 is on first two cards, then its surely blackjack
            return 'playerLost' #! dealer blackjack
        
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


        
