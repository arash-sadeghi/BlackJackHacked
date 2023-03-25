from Player import Player
from Dealer import Dealer

player = Player()
dealer = Dealer()
numberOfGames = 100
for _ in range(numberOfGames):
    cardsOnTable = dealer.deal()
    if dealer.checkPlayerBJ():
        dealer.endHand() #! no result is given for player since it was pure luck of player
    decision = player.decide(cardsOnTable)
    result = dealer.takeAction(decision)
    while result == 'handInProgress':
        cardsOnTable = dealer.dealerHand[0]
        cardsOnTable.extend(dealer.playerHand)
        decision = player.decide(cardsOnTable)
        result = dealer.takeAction(decision)

    player.learn(cardsOnTable , decision , result)
    dealer.endHand()

print("hi")