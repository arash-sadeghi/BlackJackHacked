import numpy as np

inpH = "/home/arash/Workdir/BJ/BlackJackHacked/logs/ExploringSun_Mar_26_22_21_02_2023/playerhardTable.npy"
hars = np.load(inpH)

inpS = "/home/arash/Workdir/BJ/BlackJackHacked/logs/ExploringSun_Mar_26_22_21_02_2023/playersoftTable.npy"
soft = np.load(inpS)


print("hi")

'''
inpH = "/home/arash/Workdir/BJ/BlackJackHacked/logs/ExploringSun_Mar_26_22_21_02_2023/playerhardTable.npy"
inpS = "/home/arash/Workdir/BJ/BlackJackHacked/logs/ExploringSun_Mar_26_22_21_02_2023/playersoftTable.npy"

np.all(array[0:10]==0) --> true

first non zero starts at row 11

this is maybe because no sum below 13 is possible to end in result. 

array[19][0]
array([[ 0., 89.,  0.],
       [76., 13.,  0.], ---> how can you stay at 21 and loose? at worst you push
       [ 0., 89.,  0.]])

 array[19][9]
array([[ 0., 93.,  0.],
       [61., 31.,  0.],
       [ 0., 92.,  0.]])

array[11][0] --> 12 against 2
array([[  0., 119.,   0.],
       [ 45.,  74.,   0.],
       [ 39.,  72.,   7.]])
array[11][9]
array([[  0., 118.,   0.],
       [ 17., 101.,   0.],
       [ 25.,  88.,   5.]])
ofcourse hitting never wins. stay and double only switch the hand. hitting never wins it only busts. that why it has all the losses. double row represents hitting here because after you double you also stay. 

SOFT:

soft only has non zero elements at its last row. it corresponds to blackjack I think or A 4 7 ish

'''