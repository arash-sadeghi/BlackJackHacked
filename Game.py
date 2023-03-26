from Player import Player
from Dealer import Dealer
from termcolor import colored
import logging
from time import ctime , time
import os
def print2(inp,color='white',attrs=[]):
    print(colored(inp,color,attrs=attrs))
    logging.info(inp)

if __name__ == '__main__':
    logName = ctime(time()).replace(" ","_").replace(":","_")
    dir = 'logs'
    logName = os.path.join(dir,logName)
    logging.basicConfig(filename=logName+'.log', level=logging.DEBUG)

    points = {'As': 1, 'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10} #! Ace is just 11 for now
    player = Player(points,logName)
    dealer = Dealer(points)
    wins = 0
    losses = 0
    pushes = 0
    numberOfGames = 10000
    startTime = time()
    for gameIt in range(1,numberOfGames+1): #! just to avoid game number 0

        if dealer.shoeChange:
            print2("\n"+"<>"*20+"\n")
            print2(f"changing shoe after dealing {len(dealer.dealtCards)}")
            print2("\n"+"<>"*20+"\n")
            dealer = Dealer(points)
            
        print2("\n"+"-"*20+f" game {gameIt} "+"-"*20+"\n")
        cardsOnTable = dealer.deal()
        print2(f'[game] dealer hand {cardsOnTable[0]} ','cyan',attrs=['bold'])
        print2(f'[game] player hand {[_ for _ in cardsOnTable[1:]]} , sum {sum([points[_] for _ in cardsOnTable[1:]])}','light_green',attrs=['bold'])

        if dealer.checkPlayerBJ() == 1:
            print2("[game] Player BlackJack",'green')
            wins += 1
            dealer.endHand() #! no result is given for player since it was pure luck of player
            continue

        decision = player.decide(cardsOnTable)
        print2(f'[game] decision {decision}')
        
        
        
        result = dealer.takeAction(decision)
        while result == 'handInProgress':
            print2("[game] handInProgress")
            cardsOnTable = [dealer.dealerHand[0]]
            cardsOnTable.extend(dealer.playerHand)
            print2(f'[game] dealer hand {cardsOnTable[0]} ','cyan',attrs=['bold'])
            print2(f'[game] player hand {[_ for _ in cardsOnTable[1:]]} , sum {sum([points[_] for _ in cardsOnTable[1:]])}','light_green',attrs=['bold'])
            decision = player.decide(cardsOnTable)
            result = dealer.takeAction(decision)

        player.record(cardsOnTable , decision , result)

        print2(f"[game] playerHand {dealer.playerHand}  {sum([ points[_] for _ in dealer.playerHand])} dealerHand {dealer.dealerHand} {sum([ points[_] for _ in dealer.dealerHand])}")

        dealer.endHand()

        if result == 'playerLost': 
            color = "red"
            losses += 1 
        if result == 'playerWon': 
            color = "green"
            wins += 1
        if result == 'push': 
            color = "yellow"
            pushes += 1

        print2(f"[game] {result}",color)
        print2( f"STATS wins {wins} - {round(wins/gameIt*100,2)} |||| losses {losses} - {round(losses/gameIt*100,2)} |||| pushs {pushes} - {round(pushes/gameIt*100,2)}" , 'magenta' , attrs=["bold"])


    print2(f"Time Passed {time() - startTime} s for {numberOfGames} games")