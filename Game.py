from Player import Player
from Dealer import Dealer
from termcolor import colored
import logging
from time import ctime , time
import os
import numpy as np
import pickle
import matplotlib.pyplot as plt

METHODmc = 0
METHODoptimalTable = 1
METHODexternalQ = 2
METHODarashCoded = 3

def vizMoney(moneys):
    plt.plot(moneys)

    plt.grid()
    plt.savefig(os.path.join('results','betFalacyWoDoubleStopCondResult3')+''+'.png')
    plt.show()

def print2(inp,color='white',attrs=[]):
    # print(colored(inp,color,attrs=attrs))
    logging.info(inp)

if __name__ == '__main__':
    method = METHODoptimalTable
    logName = ctime(time()).replace(" ","_").replace(":","_")
    comment = 'betFalacy'+f'method{method}'
    logName = comment + logName
    dir = os.path.join('logs',logName)
    os.makedirs(dir, exist_ok=True)
    logging.basicConfig(filename=os.path.join(dir,'log.log'), level=logging.DEBUG)
    points = {'As': 1, 'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10} #! Ace is just 11 for now
    player = Player(points,dir,method)
    dealer = Dealer(points)
    wins = 0
    losses = 0
    pushes = 0
    numberOfGames = 100_000
    # numberOfGames = 600
    money = 10000
    initialMoney = money
    initialBet = 1
    bet = initialBet
    winPercentages = []
    lossPercentages = []
    pushPercentages = []
    MoneyRec = []
    wentBroke = False
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

        BJres = dealer.checkPlayerBJ()
        #! no result is given for player since it was pure luck of player
        if  BJres == "playerWon":
            print2("[game] Player BlackJack",'green')
            wins += 1
            money += bet * 3/2
            bet = initialBet
            dealer.endHand() 
            continue
        elif BJres == "playerLost":
            print2("[game] Dealer BlackJack",'red')
            wins -= 1
            money -= bet 
            bet = bet * 2
            dealer.endHand() 
            continue
        elif BJres == "push":
            print2("[game] BlackJack pushed",'gray')
            dealer.endHand() 
            continue

        SAR = []
        result = 'handInProgress'       
        while result == 'handInProgress':
            print2("[game] handInProgress")
            cardsOnTable = [dealer.dealerHand[0]]
            cardsOnTable.extend(dealer.playerHand)
            print2(f'[game] dealer hand {cardsOnTable[0]} ','cyan',attrs=['bold'])
            print2(f'[game] player hand {[_ for _ in cardsOnTable[1:]]} , sum {sum([points[_] for _ in cardsOnTable[1:]])}','light_green',attrs=['bold'])
            decision = player.decide(cardsOnTable)
            print2(f'[game] decision {decision}')
            if decision == 'double': decision = 'hit' #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            result = dealer.takeAction(decision) 
            SAR.append([cardsOnTable , decision , result])    
        player.record(cardsOnTable , decision , result)
        if method == METHODmc:
            player.learnMC(SAR)
        print2(f"[game] playerHand {dealer.playerHand}  {sum([ points[_] for _ in dealer.playerHand])} dealerHand {dealer.dealerHand} {sum([ points[_] for _ in dealer.dealerHand])}")

        if result == 'playerLost': 
            color = "red"
            losses += 1 
            money -= bet
            bet = bet * 2

        elif result == 'playerLostDouble': 
            color = "red"
            losses += 1 
            money -= 2*bet
            bet = bet * 4
            

        elif result == 'playerWon': 
            color = "green"
            wins += 1
            money += bet
            bet = initialBet


        elif result == 'playerWonDouble': 
            color = "green"
            wins += 1
            money += 2*bet
            bet = initialBet


        elif result == 'push': 
            color = "yellow"
            pushes += 1
        else:
            raise NameError('wrong result')

        dealer.endHand()

        print2(f"[game] {result}",color)
        print2( f"STATS wins {wins} - {round(wins/gameIt*100,2)} |||| losses {losses} - {round(losses/gameIt*100,2)} |||| pushs {pushes} - {round(pushes/gameIt*100,2)} initial Money {initialMoney} money at the end {money} bet {bet}" , 'magenta' , attrs=["bold"])

        if gameIt%500 == 0:
            print( f"STATS game {gameIt} progress {round(gameIt/numberOfGames*100,2)} wins {wins} - {round(wins/gameIt*100,2)} |||| losses {losses} - {round(losses/gameIt*100,2)} |||| pushs {pushes} - {round(pushes/gameIt*100,2)} initial Money {initialMoney} money at the end {money} bet {bet} Broke {wentBroke}")
            if method == METHODexternalQ or method == METHODmc:
                player.vizMC(gameIt) 

        winPercentages.append(round(wins/gameIt*100,2))
        lossPercentages.append(round(losses/gameIt*100,2))
        pushPercentages.append(round(pushes/gameIt*100,2))
        MoneyRec.append(money)

        if money<=0:
            wentBroke = True

    print2(f"Time Passed {time() - startTime} s for {numberOfGames} games")
    print(f"Time Passed {time() - startTime} s for {numberOfGames} games")

    with open(os.path.join(dir,"Results.txt"),"w") as f:
        f.write(f"STATS game {gameIt} progress {round(gameIt/numberOfGames*100,2)} wins {wins} - {round(wins/gameIt*100,2)} |||| losses {losses} - {round(losses/gameIt*100,2)} |||| pushs {pushes} - {round(pushes/gameIt*100,2)} initial Money {initialMoney} money at the end {money} bet {bet} Broke {wentBroke}")
    
    np.save(os.path.join(dir,"Winpers.npy") , np.array(winPercentages))
    np.save(os.path.join(dir,"Losspers.npy") , np.array(lossPercentages))
    np.save(os.path.join(dir,"Pushpers.npy") , np.array(pushPercentages))
    np.save(os.path.join(dir,"MoneyRec.npy") , np.array(MoneyRec))

    with open(os.path.join(dir,"Dealer.pickle"), "wb") as f:
        pickle.dump(dealer, f)
    with open(os.path.join(dir,"Player.pickle"), "wb") as f:
        pickle.dump(player, f)
    player.saveRecords()
    vizMoney(MoneyRec)
    print("files saved! goodbye")
    