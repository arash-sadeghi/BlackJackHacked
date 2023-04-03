# situation
- fixed some fatal errors and incorporated gym. everything works reliably. but for the future I need t make sure of sanity of code before I run experiments. this will save me a lot of time. all this debug nonsense was because of if statements aces and all those stuff. code slower save time for later and avouid wrong rushed resuls. However for now we know how blackjack works monte carlo and all other stuff related to it. now count cards, estimate win and loss, and implement spliting.
# TODO
- [ ] implement high/low card counting.
    - [ ] try different deck penetration and compare win rate.
- [x] implement bet fallacy.
    - IN betFalacy branch.
    - except few occasion where you go far below negative, your money grows. In reality i made few bucks but for safety you need big bankroll and small bets. I lost 80$ eventually.
- [x] implement soft A
- [ ] implement split
- [x] implement double
- [ ] implement card counting with your own method and analyze how much its effecting over 600 hands
- [ ] check win loss streak theory and adapt your bet accordingly. estimate next hands win/loss.
- [ ] deal from low value deck and high value deck and see which one is favorable to palyer?


# Experiments to do:
- [x] **Brute force:**  explore the whole sum/dealer card table. visit each state at least 10 times. table is 20(sums)*10(dealer cards)*3(actions) = 600. Visit each state 10 times--> 600 * 10 = 6000. explorable --> cant say about hit. Monte carlo is doing the same thing.

- [x] implement montecarlo and see if it really increases number of wins --> no. online solution was fake

- [ ] count series of wins and losses. see if you can predict wins and losses before hand. instead of trying to win, try to know when you will loose.
    - [ ] count consecutive losses and wins through out the hand. and say foreaxmple its this much % chance to lose x hands consecutively. Adjust your bet accordingly

# Results:

- Optimal Table With Double:
    - STATS game 1000000 progress 100.0 wins 428765 - 42.88 |||| losses 489511 - 48.95 |||| pushs 81724 - 8.17 initial Money 100 money at the end -22050.0 bet 1 Broke True 
- bet fallacy:
    - STATS game 100000 progress 100.0 wins 38711 - 38.71 |||| losses 43446 - 43.45 |||| pushs 8600 - 8.6 initial Money 10000 money at the end 71538.5 bet 1 Broke True
# Facts

- The probability of a win in a typical shoe blackjack game is 43.3%, a push is 8.7%, and a loss is 48.0% 
