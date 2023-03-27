# TODO
- [x] implement soft A

- [ ] implement split and double

# Experiments to do:
- [ ] **Brute force:**  explore the whole sum/dealer card table. visit each state at least 10 times. table is 20(sums)*10(dealer cards)*3(actions) = 600. Visit each state 10 times--> 600 * 10 = 6000. explorable

- [ ] implement montecarlo and see if it really increases number of wins

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

- optimal Table with double : STATS game 100000 progress 100.0 wins 44721 - 44.72 |||| losses 47658 - 47.66 |||| pushs 7621 - 7.62 initial Money 100000 money at the end 113430.0 bet 10 --> despite the low percentage, we made money with double
STATS game 100000 progress 100.0 wins 44443 - 44.44 |||| losses 47970 - 47.97 |||| pushs 7587 - 7.59 initial Money 100000 money at the end 106875.0 bet 10