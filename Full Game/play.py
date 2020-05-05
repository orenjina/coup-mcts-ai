from model import *
from runner import *

if __name__ == "__main__":
    coup = Coup(2, 2, 2, 3)

    TRY_STATE = (1, 0, 1, None, 0, 'exchange', [4, ('duke', 0), ('contessa', 1)], [6, ('captain', 1), ('ambassador', 0)])


    random_manual_strat = random_manual_strategy(coup)

    det_mcts_trials = 5000
    ai_strat = det_obj_mcts_strategy(det_mcts_trials, coup, random_manual_strat)

    cheat_mcts_trials = 1000
    ai_cheat_strat = cheat_mcts_strategy(cheat_mcts_trials, coup, random_manual_strat)

    coup = Coup(2, 2, 2, 3)
    # coup.set_state(TRY_STATE)
    while True:
        select = input("do you want to go first? (yes or no)")
        while True:
            if select == "yes":
                porder = 0
                break
            elif select == "no":
                porder = 1
                break
            else:
                select = input("yes or no I said")
        while not coup.game_over():
            coup.info_log(porder)
            if coup.cur_player == porder:
                p_input = input()
                coup.perform_action(p_input)
            else:
                act = ai_strat(coup.information_set(coup.cur_player))
                # act = cheat_mcts_strat(coup.game_state())
                coup.perform_action(act)
                print("action picked is ", act)

        if coup.winner == porder:
            print("you win")
        else:
            print("you lose")
