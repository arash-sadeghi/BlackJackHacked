#! 1 is hit 0 is stay
HIT = 1
STAY = 0
DOUBLE = 2
DOUBLE2 = 3

HITstr = 'hit'
STAYstr = 'stay'
DOUBLEstr = 'double'

WIN = "playerWon"
LOSS = 'playerLost'
PUSH = "push"

METHODmc = 0
METHODoptimalTable = 1
METHODexternalQ = 2
METHODarashCoded = 3
METHODcountCard = 4

deckNum = 2
deckPenetration = 0.9

points = {'As': 1, 'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10} #! Ace is just 11 for now
