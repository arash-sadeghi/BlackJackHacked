#! https://www.youtube.com/watch?v=BfAzVNSort0
from math import ceil
h = [6,7,10,8,10,
2,4,8,10,10,5,
4,9,8,7,10,
10,4,4,2,5,10,
2,2,8,10,8,10,7,4,6,
2,11,10,10,11,5,11,3,6,
8,9,6,10,5,9,2,5,
10,7,10,3,10,10,7,
4,4,11,11,6,6,2,6,3,3,
8,8,10,9,10,5,11,
2,3,7,9,3,10,10,5,
5,8,5,10,7,4,4,10,
2,9,9,10,11,11,5,10,10,
6,11,10,7,3,4,4,3,7,
5,7,8,10,10,7,4,6,
11,10,11,11,2,4,11,6,
4,4,4,10,3,5,9,10,
6,9,6,2,10,5,10,
10,7,10,7,
6,4,10,9,8] #! len146 , deck num 3, card% 47 count 7

h.extend([
11,3,10,8,6,6,4,6,11,
5,4,4,10,10,11,10,4,8,4,10,
10,6,10,2,8,3,4,6,11,
10,5,5,10,8]) #! len180 , deck num 4, card% 58 count 18 , true count 9.0

h.extend([
    10,10,7,
    6,10,4,10,3,6,3,9,
    8,10,7,8,9,10,8,
    10,10,9,2,10,0,10,3,2,10
])

def count(hand):
    c = 0
    for i in hand:
        if i>=10:
            c-=1
        elif i<7:
            c+=1
    return c

deckNum = 8
print(f"len {len(h)} , deck num {ceil(len(h)/52)}, card% {ceil(len(h)/(52*deckNum)*100)} count {count(h)} , true count {count(h)/(deckNum-ceil(len(h)/52))}")

for i in range(12):
    print(f"card {i}: {h.count(i)}")

#? at least 5 decks (5 fours), at most 8 decks ()