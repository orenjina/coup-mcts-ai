from model import *
from cheat_mcts import cheat_mcts_strategy
from det_mcts import det_mcts_strategy
from runner import *
import random
import time



def main():
    coup = Coup(2, 2, 2, 3)
    random_manual_strat = random_manual_strategy(coup)

    det_mcts_trials = 1000
    det_mcts_strat = det_mcts_strategy(det_mcts_trials, coup, random_manual_strat)

    det_mcts_trials2 = 200
    det_mcts_strat2 = det_mcts_strategy(det_mcts_trials2, coup, random_manual_strat)

    neo_coup = Coup(2, 2, 2, 3)
    while not neo_coup.game_over():
        neo_coup.log()
        a = det_mcts_strat2(neo_coup.information_set(neo_coup.cur_player))
        b = det_mcts_strat(neo_coup.information_set(neo_coup.cur_player))
        print(a)
        print(b)
        neo_coup.perform_action(b)


main()
