# Coup AI results

We revised the game to be easier to compute to see the results given. We call
this the mostly deterministic variation of Coup. In this version, we do not have
any randomness in the game. To achieve this, we edited out the rule that players
shuffle back their card in circumstances and that players can draw ambassador.

(Ran using pypy3)
## MDV Coup results:
### random results

### 200 iterations determinized against random strategies:
test_strategies(100, random_strat, det_mcts_strat2, False, True)
test_strategies(100, random_manual_strat, det_mcts_strat2, False, True)
test_strategies(100, random_noobject_strat, det_mcts_strat2, False, True)
test_strategies(100, det_mcts_strat2, random_strat, True, False)
test_strategies(100, det_mcts_strat2, random_manual_strat, True, False)
test_strategies(100, det_mcts_strat2, random_noobject_strat, True, False)

game:  99
average game time 0.5109931802749634 seconds
win rate of the first player 0.18
game:  99
average game time 0.4450853705406189 seconds
win rate of the first player 0.77
game:  99
average game time 0.3281665587425232 seconds
win rate of the first player 0.24
game:  99
average game time 0.3497893691062927 seconds
win rate of the first player 0.91
game:  99
average game time 0.48463144063949587 seconds
win rate of the first player 0.29
game:  99
average game time 0.21860154151916503 seconds
win rate of the first player 0.83

#### with inference
test_strategies(100, random_strat, det_obj_mcts_strat2, False, True)
test_strategies(100, random_manual_strat, det_obj_mcts_strat2, False, True)
test_strategies(100, random_noobject_strat, det_obj_mcts_strat2, False, True)
test_strategies(100, det_obj_mcts_strat2, random_strat, True, False)
test_strategies(100, det_obj_mcts_strat2, random_manual_strat, True, False)
test_strategies(100, det_obj_mcts_strat2, random_noobject_strat, True, False)

game:  99
average game time 0.4640966987609863 seconds
inference result for p1 is (82, 129)
win rate of the first player 0.17
game:  99
average game time 0.8355445289611816 seconds
inference result for p1 is (1, 27)
win rate of the first player 0.35
game:  99
average game time 0.21798995971679688 seconds
inference result for p1 is (141, 152)
win rate of the first player 0.18
game:  99
average game time 0.45675885915756226 seconds
inference result for p0 is (21, 103)
win rate of the first player 0.89
game:  99
average game time 0.8072255301475525 seconds
inference result for p0 is (1, 21)
win rate of the first player 0.7
game:  99
average game time 0.3042540812492371 seconds
inference result for p0 is (122, 141)
win rate of the first player 0.79


### 1000 iterations determinized against random strategies:

#### with inference
test_strategies(100, random_strat, det_obj_mcts_strat, False, True)
test_strategies(100, random_manual_strat, det_obj_mcts_strat, False, True)
test_strategies(100, random_noobject_strat, det_obj_mcts_strat, False, True)
test_strategies(100, det_obj_mcts_strat, random_strat, True, False)
test_strategies(100, det_obj_mcts_strat, random_manual_strat, True, False)
test_strategies(100, det_obj_mcts_strat, random_noobject_strat, True, False)

game:  99
average game time 1.5203406381607056 seconds
inference result for p1 is (75, 143)
win rate of the first player 0.16
game:  99
average game time 3.68903666973114 seconds
inference result for p1 is (1, 16)
win rate of the first player 0.42
game:  99
average game time 0.6337531089782715 seconds
inference result for p1 is (112, 130)
win rate of the first player 0.3
game:  99
average game time 1.1937953901290894 seconds
inference result for p0 is (21, 125)
win rate of the first player 0.94
game:  99
average game time 2.83753634929657 seconds
inference result for p0 is (1, 26)
win rate of the first player 0.58
game:  99
average game time 0.8481584095954895 seconds
inference result for p0 is (113, 131)
win rate of the first player 0.77


### Determinized against each other
test_alt_strategies(100, det_obj_mcts_strat2, det_mcts_strat2, True, True)
test_alt_strategies(100, det_obj_mcts_strat, det_mcts_strat, True, True)
test_alt_strategies(100, det_obj_mcts_strat, det_obj_mcts_strat2, True, True)
test_alt_strategies(100, det_obj_mcts_strat_big, det_obj_mcts_strat2, True, True)

game:  99
average game time 1.1684460306167603 seconds
inference result for p0 is (23, 122)
win rate of the first player 0.73
game:  99
average game time 3.2210009407997133 seconds
inference result for p0 is (18, 119)
win rate of the first player 0.75
game:  99
average game time 4.637382378578186 seconds
inference result for p0 is (6, 53)
inference result for p1 is (6, 56)
win rate of the first player 0.48
game:  99
average game time 13.902421200275421 seconds
inference result for p0 is (17, 92)
inference result for p1 is (18, 77)
win rate of the first player 0.63

### Determinized against cheating


## Domain specific learnings
Given the option of ambassador, the tree like going exchange all the time,
because likely one of the many variances of exchange will happen to be good
by chance.

The base version of MCTS has no memory, this means that it does not learn anything
from how the opponent played.
