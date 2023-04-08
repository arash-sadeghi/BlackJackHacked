from Player import Player
from Dealer import Dealer
from termcolor import colored
import logging
from time import ctime , time
import os
import numpy as np
import pickle
import matplotlib.pyplot as plt
from Constants import *
def vizMoney(moneys):
    plt.plot(moneys)

    plt.grid()
    plt.savefig(os.path.join(dir,'MyDealerWithBJcheck')+''+'.png')
    plt.show()

def print2(inp,color='white',attrs=[]):
    # print(colored(inp,color,attrs=attrs))
    # logging.info(inp) #! no logging - increase running time from 2.7s to 23 s !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    pass

if __name__ == '__main__':
    method = METHODcountCard
    logName = ctime(time()).replace(" ","_").replace(":","_")
    comment = 'aggresiveCount'+f'method{method}'
    logName = comment + logName
    dir = os.path.join('logs',logName)
    os.makedirs(dir, exist_ok=True)
    logging.basicConfig(filename=os.path.join(dir,'log.log'), level=logging.DEBUG)
    money = 100
    bet = 1
    initialMoney = money
    dealer = Dealer(deckNum , deckPenetration)
    player = Player(dir , method , bet , totalDecks=dealer.deckNum)
    wins = 0
    losses = 0
    pushes = 0
    numberOfGames = 100_000
    winPercentages = []
    lossPercentages = []
    pushPercentages = []
    MoneyRec = []
    wentBroke = False
    startTime = time()
    cardsOnTable = []
    for gameIt in range(1,numberOfGames+1): #! just to avoid game number 0
        print2("\n"+"-"*20+f" game {gameIt} "+"-"*20+"\n")
        if dealer.shoeChange:
            print2("\n"+"<>"*20+"\n"+f"changing shoe after dealing {len(dealer.dealtCards)}")
            dealer = Dealer(deckNum , deckPenetration)
            if method == METHODcountCard:
                player.resetCounting()
            
        if method == METHODcountCard and gameIt>1:
            bet = player.countCards(dealer.dealerHand+dealer.playerHand , len(dealer.dealtCards))
            print2(f'[game] bet {bet} running count {player.runningCount} true count {player.trueCount} cards dealt {round((deckNum*52-len(dealer.cards)) / (deckNum*52) , 2)*100} %')
            # if player.trueCount >= 5 and round((deckNum*52-len(dealer.cards)) / (deckNum*52) , 2)*100 >= 88:
            #     print(len(dealer.cards) , round((deckNum*52-len(dealer.cards)) / (deckNum*52) , 2)*100 )
            #     print(" lemme see")
            #     # l = np.array([points[_] for _ in dealer.cards]) ; np.count_nonzero(l<=6);

        dealer.endHand() 

        cardsOnTable = dealer.deal()
        print2(f'[game] dealer {cardsOnTable[0]} player {[_ for _ in cardsOnTable[1:]]} , sum {sum([points[_] for _ in cardsOnTable[1:]])}','light_green',attrs=['bold'])
        BJres = dealer.checkPlayerBJ()
        if  BJres == WIN:
            print2("[game] Player BlackJack",'green')
            wins += 1
            money += bet * 3/2
            continue
        elif BJres == LOSS:
            print2("[game] Dealer BlackJack",'red')
            wins -= 1
            money -= bet 
            continue
        elif BJres == PUSH:
            print2("[game] BlackJack pushed",'gray')
            continue

        SAR = []
        result = 'handInProgress'       
        while result == 'handInProgress':
            cardsOnTable = [dealer.dealerHand[0]]
            cardsOnTable.extend(dealer.playerHand)

            print2(f'[game] dealer {cardsOnTable[0]} player {[_ for _ in cardsOnTable[1:]]} , sum {sum([points[_] for _ in cardsOnTable[1:]])}','light_green',attrs=['bold'])

            decision = player.decide(cardsOnTable)
            
            print2(f'[game] decision {decision}')

            result = dealer.takeAction(decision) 
            SAR.append([cardsOnTable , decision , result])    
        player.record(cardsOnTable , decision , result)
        if method == METHODmc:
            player.learnMC(SAR)
        print2(f"[game] playerHand {dealer.playerHand}  {sum([ points[_] for _ in dealer.playerHand])} dealerHand {dealer.dealerHand} {sum([ points[_] for _ in dealer.dealerHand])}")

        if result == LOSS: 
            color = "red"
            losses += 1 
            money -= bet

        elif result == 'playerLostDouble': 
            color = "red"
            losses += 1 
            money -= 2*bet


        elif result == WIN: 
            color = "green"
            wins += 1
            money += bet

        elif result == 'playerWonDouble': 
            color = "green"
            wins += 1
            money += 2*bet

        elif result == PUSH: 
            color = "yellow"
            pushes += 1
        else:
            raise NameError('wrong result')

        print2(f"[game] {result}",color)
        print2( f"STATS wins {wins} - {round(wins/gameIt*100,2)} |||| losses {losses} - {round(losses/gameIt*100,2)} |||| pushs {pushes} - {round(pushes/gameIt*100,2)} initial Money {initialMoney} money at the end {money} bet {bet}" , 'magenta' , attrs=["bold"])

        if gameIt%1000 == 0 and False:  #! no printing !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
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
    