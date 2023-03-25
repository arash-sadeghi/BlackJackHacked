from Player import Player
from Dealer import Dealer

points = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10} #! Ace is just 11 for now
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
        print("[game] handInProgress")
        cardsOnTable = [dealer.dealerHand[0]]
        cardsOnTable.extend(dealer.playerHand)
        decision = player.decide(cardsOnTable)
        result = dealer.takeAction(decision)

    print(f"[game] playerHand {dealer.playerHand}  {sum([ points[_] for _ in dealer.playerHand])} dealerHand {dealer.dealerHand} {sum([ points[_] for _ in dealer.dealerHand])}")
    print(f"[game] {result}")
    player.learn(cardsOnTable , decision , result)
    dealer.endHand()

print("hi")