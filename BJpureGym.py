#! dont name this file as gym
import random
import gym
import os
from time import ctime, time
from Player import Player
import numpy as np
import matplotlib.pyplot as plt
import logging

if __name__ == '__main__':
    # logging.basicConfig(filename=os.path.join(dir,'log.log'), level=logging.DEBUG)
    logging.basicConfig(filename='log.log', level=logging.DEBUG)

    METHODoptimalTable = 1
    method = METHODoptimalTable
    logName = ctime(time()).replace(" ","_").replace(":","_")
    comment = 'realBlongRunNoD'+f'method{method}'
    logName = comment + logName
    dir = os.path.join('logs',logName)
    os.mkdir(dir)
    # points = {'As': 1, 'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10} #! Ace is just 11 for now
    points = {}

    player = Player(points,dir,method)
    env = gym.make('Blackjack-v1',sab=False,natural=True)

    done = False
    games = 100_000
    money = 100
    bet = 1
    moneyRec = []
    env.np_random.__setstate__(np.random.default_rng(1).__getstate__());print("seed given") #!!!!!!!!!!!!! seeding

    for i in range(games):
        # Start a new game
        state = env.reset()
        # print(f"\nStarting a new game with initial state: {state} {env.dealer[0]} VS {env.player}")
        logging.info(f"\nStarting a new game with initial state: {state} {env.dealer} VS {env.player}")

        done = False
        while not done:

            if len(state) == 2:
                stateDimFix = state[0]
            else: 
                stateDimFix = state

            if stateDimFix[0] == 21 and len(env.player) == 2: #! blackjack
                reward = 1.5
                done = stateDimFix[2]
                logging.info(f">>>>>>>>> black jack {done}")
            else:    
                state4P = [stateDimFix[0], env.player , stateDimFix[1] , stateDimFix[2]]

                action = player.decide(state4P,gym=True)

                if action == 'hit':
                    action = 1
                    state, reward, done, info ,  _ = env.step(action)

                elif action == 'stay':
                    action = 0
                    state, reward, done, info ,  _ = env.step(action)

                elif action == 'double':
                    if len(env.player) > 2:
                        raise NameError("can't double here")
                    action = 1
                    state, reward, done, info ,  _ = env.step(action)
                    if not done: #! if player didn't bust with double 
                        action = 0
                        state, reward, done, info ,  _ = env.step(action)
                    else: #! this actually never happens
                        print("check")
                    reward*=2
                    action = 2 #! just for printing

                # print(f"Taking action {action}")
                logging.info(f"Taking action {action}")
            
                # print(f"New state: {state} {env.dealer[0]} VS {env.player}, reward: {reward}, done: {done}, info: {info}")
                logging.info(f"New state: {state} {env.dealer} VS {env.player}, reward: {reward}, done: {done}, info: {info}")
            
        money += reward*bet
        moneyRec.append(money)    
        logging.info(f"\ngame{i} MOENY:{money}\n")

        if i%5000 == 0: 
            print(f"{round(i/games*100,2)}")
    
    moneyRec = np.array(moneyRec)
    np.save("moneyRecGym.npy",moneyRec)
    plt.plot(moneyRec)
    plt.show()
            