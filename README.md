# coup-mcts-ai
AI for the board game Coup the Resistance for the 2 players version.

## Coup
Coup is a social deduction game where each player start with 2 cards in secret and perform various actions to eliminate opponents. Rules can be referred to [here](https://upload.snakesandlattes.com/rules/c/CoupTheResistance.pdf)

## Theory
This project uses determinization to build an AI capable to analyzing imperfect information games. More specifics on using different ways to solve the game can be seen [here](https://docs.google.com/presentation/d/1rUaidpyjCGRGxmy9uBgs_LZeMD-8qRFn9M6eg1J2ZEM/edit?usp=sharing). More specifics on using the general techniques can be seen [here](http://orangehelicopter.com/academic/papers/cig11.pdf).

## Implementation
The implementation of the game can be seen in model.py. The game can be set to a state and the state will change for the actions fed into it. Specifics on some of the decisions can be summarized [here](https://docs.google.com/presentation/d/1najC_uoUNzfxWfBcDjeZJau3AWtqVKU3AH9G29WEpHU/edit?usp=sharing).

## model.py
The game mode is described in here.

## det_mcts.py
The determinized MCTS AI is here.

## det_obj_mcts.py
The determinized MCTS AI with inference abilities is here

## cheat_mcts.py
The MCTS AI ran given all the information is seen here.

## compare.py
Compare moves made by different agents here.

## runner.py
Many different agents are initialized here. Then the agents (described below) are played against each other for the data seen in results.MD.

random_strat = random_strategy(coup)
Take a random legal move every turn.

random_honest_strat = random_honest_strategy(coup)
Take a random legal move that is consistent with cards held every turn.

random_manual_strat = random_manual_strategy(coup)
Take a slightly better than random legal move that is consistent with cards held every turn.

random_noobject_strat = random_noobject_strategy(coup)
Take a random legal move that does not include object every turn.

random_inf_strat = random_inf_strategy(coup)
Take a random legal move that weighs objection using past references every turn.

random_manual_inf_strat = random_manual_inf_strategy(coup)
Take a slightly better than random legal move that is consistent with cards held every turn. Also weights objection using past references every turn.

cheat_mcts_strat = cheat_mcts_strategy(cheat_mcts_trials, coup, random_manual_strat)
Take a trained move given the number of trials and the perfect game state. Uses the last variable as the simulation method.

det_mcts_strat = det_mcts_strategy(det_mcts_trials, coup, random_manual_strat)
Take a trained move given the number of trials and the current information set. Uses the last variable as the simulation method.

det_obj_mcts_strat = det_obj_mcts_strategy(det_obj_mcts_trials, coup, random_manual_strat)
Take a trained move given the number of trials and the current information set. Also take into account the record of the agent we currently play against. Uses the last variable as the simulation method.


## manual.py
Running this file using "python3 manual.py" gives the user a game cycle where the user takes control of both sides of the game. Prints given gives information about the entire current game state.

## play.py
Running this file using "python3 manual.py" gives the user a game cycle where the user takes control of one of the players in the game. The other side of the game will be played by a 5000 trials determinized Monte Carlo Tree Search with some inference abilities. Prints given will update the user of the player information the user plays as.

## results.MD
This file contains the experimental results of different agents made in the runner.py file.

## Conclusion
The determinization technique works for Coup in the 2 player version and gives us significant better than random results. To be used well against individual people, perhaps more specific parameters need to be tuned manually. This repository is also on github [here](https://github.com/orenjina/coup-mcts-ai)
