# TODO
- [x] implement soft A
- [ ] implement split
- [x] implement double

# Experiments to do:
- [x] **Brute force:**  explore the whole sum/dealer card table. visit each state at least 10 times. table is 20(sums)*10(dealer cards)*3(actions) = 600. Visit each state 10 times--> 600 * 10 = 6000. explorable --> cant say about hit. Monte carlo is doing the same thing.

- [x] implement montecarlo and see if it really increases number of wins --> no. online solution was fake

- [ ] count series of wins and losses. see if you can predict wins and losses before hand. instead of trying to win, try to know when you will loose.
    - [ ] count consecutive losses and wins through out the hand. and say foreaxmple its this much % chance to lose x hands consecutively. Adjust your bet accordingly

# Results:

- my strategy codded : STATS game 1000000 progress 100.0 wins 449830 - 44.98 |||| losses 472730 - 47.27 |||| pushs 77440 - 7.74

- random player : STATS game 100000 progress 100.0 wins 32009 - 32.01 |||| losses 64559 - 64.56 |||| pushs 3432 - 3.43

- manual play: INFO:root:STATS wins 55 - 55.0 |||| losses 39 - 39.0 |||| pushs 6 - 6.0 (100 games)

- optimal table : STATS game 100000 progress 100.0 wins 44496 - 44.5 |||| losses 47887 - 47.89 |||| pushs 7617 - 7.62 initial Money 100000 money at the end 89385.0 bet 10

- always hit: STATS game 100000 progress 100.0 wins 4765 - 4.76 |||| losses 95235 - 95.23 |||| pushs 0 - 0.0 initial Money 100000 money at the end -780875.0 bet 10
STATS game 100000 progress 100.0 wins 4774 - 4.77 |||| losses 95226 - 95.23 |||| pushs 0 - 0.0 initial Money 100000 money at the end -780650.0 bet 10

- always stay: STATS game 100000 progress 100.0 wins 41590 - 41.59 |||| losses 53976 - 53.98 |||| pushs 4434 - 4.43 initial Money 100000 money at the end 165.0 bet 10

- optimal Table with double (faulty double): STATS game 100000 progress 100.0 wins 44721 - 44.72 |||| losses 47658 - 47.66 |||| pushs 7621 - 7.62 initial Money 100000 money at the end 113430.0 bet 10 --> despite the low percentage, we made money with double
STATS game 100000 progress 100.0 wins 44443 - 44.44 |||| losses 47970 - 47.97 |||| pushs 7587 - 7.59 initial Money 100000 money at the end 106875.0 bet 10
STATS game 180000 progress 100.0 wins 79409 - 44.12 |||| losses 86991 - 48.33 |||| pushs 13600 - 7.56 initial Money 100000 money at the end 101435.0 bet 10



- MyMC :  STATS game 600000 progress 100.0 wins 252588 - 42.1 |||| losses 309954 - 51.66 |||| pushs 37458 - 6.24 initial Money 100000 money at the end -331815.0 bet 10
STATS game 180000 progress 100.0 wins 78875 - 43.82 |||| losses 88386 - 49.1 |||| pushs 12739 - 7.08 initial Money 100000 money at the end 47310.0 bet 10

- online MC : STATS game 16500 progress 9.17 wins 6831 - 41.4 |||| losses 8802 - 53.35 |||| pushs 867 - 5.25 initial Money 100000 money at the end 84180.0 bet 10


- optimal Table fixed double:
STATS game 180000 progress 100.0 wins 79919 - 44.4 |||| losses 85930 - 47.74 |||| pushs 14151 - 7.86 initial Money 100000 money at the end 116435.0 bet 10

# Facts

- The probability of a win in a typical shoe blackjack game is 43.3%, a push is 8.7%, and a loss is 48.0% 

- if your bet is small compared to your initial money, your money will grow over time. However if your bet is small (1$ bet for initial money of 100$) you will get broke few times

- if you bet 0.001$ for 100$, over 180000 hands, you will reach to 102$ dollar without busting. lets say each hand takes 20 seconds to play. 180000 will take ~ 17 hours to play. in 17 hours you will make 2$. Minimum wage is 10$/h. for this. you want 17h*/10$ = 170$ earning. this requires initial money of 170/2\*100 = 8500. So if you risk 8500$ with bet of 8500/100\*0.001 = 0.085 and you play 17h, you will make minimum wage, 170$ earning total.

- No double makes you broke. so money comes with double. I tried many times without double it always goes down.

- your money grows over time but over reasonable time, the growth is slow