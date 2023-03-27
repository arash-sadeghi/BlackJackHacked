from Player import Player
from Dealer import Dealer
from termcolor import colored
import logging
from time import ctime , time
import os
import numpy as np
import pickle

def print2(inp,color='white',attrs=[]):
    # print(colored(inp,color,attrs=attrs))
    logging.info(inp)

if __name__ == '__main__':
    logName = ctime(time()).replace(" ","_").replace(":","_")
    comment = 'OptimalTableMoneyCheck'
    logName = comment + logName
    dir = os.path.join('logs',logName)
    os.mkdir(dir)
    # logName = os.path.join(dir,logName)
    # logging.basicConfig(filename=logName+'.log', level=logging.DEBUG)
    logging.basicConfig(filename=os.path.join(dir,'log.log'), level=logging.DEBUG)

    points = {'As': 1, 'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10} #! Ace is just 11 for now
    hardUrl = "/home/arash/Workdir/BJ/BlackjackAI/hard18000.npy"
    softUrl = "/home/arash/Workdir/BJ/BlackjackAI/soft18000.npy"
    player = Player(points,dir,hardUrl,softUrl)
    dealer = Dealer(points)
    wins = 0
    losses = 0
    pushes = 0
    numberOfGames = 180000
    money = 100000
    initialMoney = money
    bet = 10
    winPercentages = []
    lossPercentages = []
    pushPercentages = []
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
            money += bet * 3/2
            dealer.endHand() #! no result is given for player since it was pure luck of player
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
            result = dealer.takeAction(decision) 
            SAR.append([cardsOnTable , decision , result])    
        player.record(cardsOnTable , decision , result)
        player.learnMC(SAR) 
        print2(f"[game] playerHand {dealer.playerHand}  {sum([ points[_] for _ in dealer.playerHand])} dealerHand {dealer.dealerHand} {sum([ points[_] for _ in dealer.dealerHand])}")

        dealer.endHand()

        if result == 'playerLost': 
            color = "red"
            losses += 1 
            money -= bet

        if result == 'playerLostDouble': 
            color = "red"
            losses += 1 
            money -= 2*bet


        if result == 'playerWon': 
            color = "green"
            wins += 1
            money += bet

        if result == 'playerWonDouble': 
            color = "green"
            wins += 1
            money += 2*bet

        if result == 'push': 
            color = "yellow"
            pushes += 1

        print2(f"[game] {result}",color)
        print2( f"STATS wins {wins} - {round(wins/gameIt*100,2)} |||| losses {losses} - {round(losses/gameIt*100,2)} |||| pushs {pushes} - {round(pushes/gameIt*100,2)} initial Money {initialMoney} money at the end {money} bet {bet}" , 'magenta' , attrs=["bold"])

        if gameIt%500 == 0:
            print( f"STATS game {gameIt} progress {round(gameIt/numberOfGames*100,2)} wins {wins} - {round(wins/gameIt*100,2)} |||| losses {losses} - {round(losses/gameIt*100,2)} |||| pushs {pushes} - {round(pushes/gameIt*100,2)} initial Money {initialMoney} money at the end {money} bet {bet}")

            player.vizMC(gameIt)

        winPercentages.append(round(wins/gameIt*100,2))
        lossPercentages.append(round(losses/gameIt*100,2))
        pushPercentages.append(round(pushes/gameIt*100,2))

        if money<=0:
            print2("WENT BROKE")

    print2(f"Time Passed {time() - startTime} s for {numberOfGames} games")
    print(f"Time Passed {time() - startTime} s for {numberOfGames} games")

    with open(os.path.join(dir,"Results.txt"),"w") as f:
        f.write(f"STATS game {gameIt} progress {round(gameIt/numberOfGames*100,2)} wins {wins} - {round(wins/gameIt*100,2)} |||| losses {losses} - {round(losses/gameIt*100,2)} |||| pushs {pushes} - {round(pushes/gameIt*100,2)} initial Money {initialMoney} money at the end {money} bet {bet}")
    
    np.save(os.path.join(dir,"Winpers.npy") , np.array(winPercentages))
    np.save(os.path.join(dir,"Losspers.npy") , np.array(lossPercentages))
    np.save(os.path.join(dir,"Pushpers.npy") , np.array(pushPercentages))
    with open(os.path.join(dir,"Dealer.pickle"), "wb") as f:
        pickle.dump(dealer, f)
    with open(os.path.join(dir,"Player.pickle"), "wb") as f:
        pickle.dump(player, f)
    player.saveRecords()
    print("files saved! goodbye")
