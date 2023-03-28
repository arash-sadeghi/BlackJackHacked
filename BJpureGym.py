#! dont name this file as gym
import random
import gym

env = gym.make('Blackjack-v1')

done = False
while not done:
    # Start a new game
    state = env.reset()
    print(f"\nStarting a new game with initial state: {state}")

    # Play until game is over
    done = False
    while not done:
        # Draw a card
        action = env.action_space.sample()
        print(f"Taking action {action}")
        state, reward, done, info ,  _ = env.step(action)
        print(f"New state: {state}, reward: {reward}, done: {done}, info: {info}")