# Coup AI results

We revised the game to be easier to compute to see the results given. We call
this the mostly deterministic variation of Coup. In this version, we do not have
any randomness in the game. To achieve this, we edited out the rule that players
shuffle back their card in circumstances and that players can draw ambassador.

(Ran using pypy3)
## MDV Coup results:
### random results
test_strategies(1000, random_honest_strat, random_manual_strat, False, False)
average game time 0.0025778088569641112 seconds
win rate of the first player 0.411

test_strategies(1000, random_manual_strat, random_honest_strat, False, False)
average game time 0.0014804930686950683 seconds
win rate of the first player 0.66

test_strategies(1000, random_strat, random_manual_strat, False, False)
average game time 0.0009615099430084228 seconds
win rate of the first player 0.306

test_strategies(1000, random_manual_strat, random_strat, False, False)
average game time 0.0006715619564056397 seconds
win rate of the first player 0.736

### 200 iterations determinized against random strategies:
test_strategies(1000, random_strat, det_mcts_strat2, False, True)
average game time 0.11667178392410278 seconds
win rate of the first player 0.36666666666666664

test_strategies(1000, random_manual_strat, det_mcts_strat2, False, True)
average game time 0.09579986310005188 seconds
win rate of the first player 0.552

test_strategies(1000, det_mcts_strat2, random_strat, True, False)
average game time 0.08054962801933288 seconds
win rate of the first player 0.604

test_strategies(1000, det_mcts_strat2, random_manual_strat, True, False)
average game time 0.08630214285850525 seconds
win rate of the first player 0.567

### 1000 iterations determinized against random strategies:
test_strategies(300, random_strat, det_mcts_strat, False, True)
average game time 0.42974292707443235 seconds
win rate of the first player 0.431

test_strategies(300, random_manual_strat, det_mcts_strat, False, True)
average game time 0.42681921792030336 seconds
win rate of the first player 0.538

test_strategies(300, det_mcts_strat, random_strat, True, False)
average game time 0.32938678002357485 seconds
win rate of the first player 0.606

test_strategies(300, det_mcts_strat, random_manual_strat, True, False)
average game time 0.36232214093208315 seconds
win rate of the first player 0.599


### Determinized against each other
test_strategies(300, det_mcts_strat2, det_mcts_strat, True, True)
average game time 0.8214671890735626 seconds
win rate of the first player 0.505

test_strategies(300, det_mcts_strat, det_mcts_strat2, True, True)
average game time 0.8001180851459503 seconds
win rate of the first player 0.49

### Determinized against cheating
test_strategies(400, det_mcts_strat2, cheat_mcts_strat2, True, False)
average game time 0.2854998099803925 seconds
win rate of the first player 0.0275
