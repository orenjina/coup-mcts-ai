# Coup AI results
(Ran using pypy3)
### random results
test_alt_strategies(1000, random_manual_strat, random_honest_strat, False, False)
test_alt_strategies(1000, random_manual_strat, random_strat, False, False)
test_alt_strategies(1000, random_manual_strat, random_noobject_strat, False, False)
test_alt_strategies(1000, random_manual_strat, random_inf_strat, False, False)
test_alt_strategies(1000, random_noobject_strat, random_inf_strat, False, False)
test_alt_strategies(1000, random_strat, random_inf_strat, False, False)
test_alt_strategies(1000, random_manual_inf_strat, random_manual_strat, False, False)

average game time 0.0034807159900665284 seconds
win rate of the first player 0.643
average game time 0.0017936379909515381 seconds
win rate of the first player 0.896
average game time 0.0015256550312042236 seconds
win rate of the first player 0.852
average game time 0.001555536985397339 seconds
inference result for p1 is (60, 393)
win rate of the first player 0.798
average game time 0.0006072819232940674 seconds
inference result for p1 is (874, 1135)
win rate of the first player 0.426
average game time 0.0007651100158691406 seconds
inference result for p1 is (831, 1133)
win rate of the first player 0.443
average game time 0.001328758955001831 seconds
inference result for p0 is (1, 88)
win rate of the first player 0.5


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


test_alt_strategies(1000, random_strat, det_obj_mcts_strat2, False, True)
test_alt_strategies(1000, random_manual_strat, det_obj_mcts_strat2, False, True)
test_alt_strategies(1000, random_noobject_strat, det_obj_mcts_strat2, False, True)

average game time 0.32407860398292543 seconds
inference result for p1 is (646, 1063)
win rate of the first player 0.143
average game time 0.8829392759799958 seconds
inference result for p1 is (13, 191)
win rate of the first player 0.336
average game time 0.16022918295860292 seconds
inference result for p1 is (766, 1128)
win rate of the first player 0.163


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


test_alt_strategies(1000, random_strat, det_obj_mcts_strat, False, True)
test_alt_strategies(1000, random_manual_strat, det_obj_mcts_strat, False, True)
test_alt_strategies(1000, random_noobject_strat, det_obj_mcts_strat, False, True)

average game time 1.2253550119400025 seconds
inference result for p1 is (644, 1038)
win rate of the first player 0.126
average game time 3.5617982671260835 seconds
inference result for p1 is (6, 99)
win rate of the first player 0.351
average game time 0.7026303250789643 seconds
inference result for p1 is (720, 1108)
win rate of the first player 0.141

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


test_alt_strategies(1000, det_obj_mcts_strat2, det_mcts_strat2, True, True)
average game time 0.5037996690273285 seconds
inference result for p0 is (230, 1082)
win rate of the first player 0.656

test_alt_strategies(800, det_obj_mcts_strat, det_mcts_strat, True, True)
average game time 1.7104276412725448 seconds
inference result for p0 is (140, 881)
win rate of the first player 0.81

test_alt_strategies(1000, det_obj_mcts_strat, det_obj_mcts_strat2, True, True)
average game time 3.0833091270923614 seconds
inference result for p0 is (60, 541)
inference result for p1 is (63, 486)
win rate of the first player 0.484

test_alt_strategies(400, det_obj_mcts_strat_big, det_obj_mcts_strat2, True, True)
average game time 13.11105286002159 seconds
inference result for p0 is (41, 265)
inference result for p1 is (47, 252)
win rate of the first player 0.5125

test_alt_strategies(400, det_obj_mcts_strat_big, det_obj_mcts_strat, True, True)
average game time 18.341653695106505 seconds
inference result for p0 is (16, 141)
inference result for p1 is (13, 143)
win rate of the first player 0.525

### Determinized against cheating
test_alt_strategies(400, det_obj_mcts_strat, cheat_mcts_strat2, True, False)
average game time 2.1784502172470095 seconds
inference result for p0 is (119, 366)
win rate of the first player 0.0725

## Domain specific learnings
The base version of MCTS has no memory, this means that it does not learn anything
from how the opponent played. The obj version of the tree learns from experience
how often the opponent lies
