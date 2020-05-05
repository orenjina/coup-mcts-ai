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

    wins = 0
    losses = 0

    ai_strat.obj_rec = (1, 2)
    while True:
        while not coup.game_over():
            coup.info_log(porder)
            if coup.cur_player == porder:
                p_input = input()
                coup.perform_action(p_input)
            else:
                act = ai_strat(coup.information_set(coup.cur_player))
                # act = cheat_mcts_strat(coup.game_state())
                coup.perform_action(act)
                print("opponent performed action", act)

        ai_strat.obj_rec = (ai_strat.obj_rec[0] + coup.obj_res[1][0], \
            ai_strat.obj_rec[1] + coup.obj_res[1][1])
        if coup.winner == porder:
            print("you win")
            wins += 1
        else:
            print("you lose")
            losses += 1
            
        print()
        print("New game: switching player order (Ctrl+c to stop program)")
        print("You have won", wins, "times and lost", losses, "times")
        print()

        porder = 1 - porder
        coup = Coup(2, 2, 2, 3)
