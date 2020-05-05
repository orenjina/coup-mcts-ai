# Coup AI results

We revised the game to be easier to compute to see the results given. We call
this the mostly deterministic variation of Coup. In this version, we do not have
any randomness in the game. To achieve this, we edited out the rule that players
shuffle back their card in circumstances and that players can draw ambassador.

(Ran using pypy3)
## MDV Coup results:
### random results

### 200 iterations determinized against random strategies:
test_strategies(1000, random_strat, det_mcts_strat2, False, True)
average game time 0.10331902480125427 seconds
win rate of the first player 0.431

test_strategies(1000, random_manual_strat, det_mcts_strat2, False, True)
average game time 0.11008567404747009 seconds
win rate of the first player 0.543

test_strategies(1000, det_mcts_strat2, random_strat, True, False)
average game time 0.07180580711364747 seconds
win rate of the first player 0.579

test_strategies(1000, det_mcts_strat2, random_manual_strat, True, False)
average game time 0.0726590759754181 seconds
win rate of the first player 0.601

### 1000 iterations determinized against random strategies:
test_strategies(1000, random_strat, det_mcts_strat, False, True)
average game time 0.4039181959629059 seconds
win rate of the first player 0.424

test_strategies(1000, random_manual_strat, det_mcts_strat, False, True)
average game time 0.43879233694076536 seconds
win rate of the first player 0.5

test_strategies(1000, det_mcts_strat, random_strat, True, False)
average game time 0.31835660815238953 seconds
win rate of the first player 0.582

test_strategies(1000, det_mcts_strat, random_manual_strat, True, False)
average game time 0.34851068711280825 seconds
win rate of the first player 0.571


### 1000 iterations determinized against random strategies:
average game time 9.41776641702652 seconds
win rate of the first player 0.449

### Determinized against each other
test_strategies(300, det_mcts_strat2, det_mcts_strat, True, True)

test_strategies(300, det_mcts_strat, det_mcts_strat2, True, True)

test_strategies(300, det_mcts_strat, det_mcts_strat, True, True)

test_strategies(300, det_mcts_strat2, det_mcts_strat2, True, True)

### Determinized against cheating
test_strategies(400, det_mcts_strat2, cheat_mcts_strat2, True, False)

test_strategies(400, det_mcts_strat, cheat_mcts_strat2, True, False)
test_strategies(400, cheat_mcts_strat, cheat_mcts_strat2, False, False)

test_strategies(200, det_mcts_strat_big, det_mcts_strat, True, False)
