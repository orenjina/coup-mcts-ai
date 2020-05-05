from model import *
from cheat_mcts import cheat_mcts_strategy
from det_mcts import det_mcts_strategy
import random
import time

def random_strategy(rule):
    def fxn(pos):
        rule.set_state(pos)
        return random.choice(rule.available_actions())
    return fxn

def random_honest_strategy(rule):
    def fxn(pos):
        rule.set_state(pos)
        return random.choice(rule.honest_actions())
    return fxn

def random_manual_strategy(rule):
    def fxn(pos):
        rule.set_state(pos)
        acts = rule.honest_actions()
        if 'coup' in acts:
            return 'coup'
        elif 'tax' in acts:
            acts.remove('income')
            acts.remove('foreign_aid')
        act = random.choice(acts)
        return act
    return fxn

# number of games, first strat, second strat, and whether they use information
# sets
def test_strategies(games, strat1, strat2, info1, info2, verbose=False):
    wins = 0
    start_time = time.time()
    for g in range(games):
        coup = Coup(2, 2, 2, 3)
        # print("game: ", g)
        if g % 100 == 99:
            print("game: ", g)
        moves = 0
        if verbose:
            coup.log(verbose=False)
        while not coup.game_over():
            # print(coup.available_actions())
            if coup.cur_player == 0:
                if info1:
                    act = strat1(coup.information_set(coup.cur_player))
                else:
                    act = strat1(coup.game_state())
            else:
                if info2:
                    act = strat2(coup.information_set(coup.cur_player))
                else:
                    act = strat2(coup.game_state())
            coup.perform_action(act)
            if verbose:
                print(act)
                coup.log()
            moves += 1

        # print(coup.winner)
        if coup.winner == 0:
            wins += 1

    end_time = time.time()
    # print("took time", end_time - start_time, "seconds")
    print("average game time", (end_time - start_time) / games, "seconds")

    # print("win rate of rand vs cheat is ", wins / games)
    # print("win rate of rand-honest vs rand is ", wins / games)
    print("win rate of the first player", wins / games)

if __name__ == "__main__":
    EXAMPLE_END_STATE = (0, 1, 3, None, 1, 'coup', [7, 'contessa'], [8, 'contessa'])

    coup = Coup(2, 2, 2, 3)

    random_strat = random_strategy(coup)
    random_honest_strat = random_honest_strategy(coup)
    random_manual_strat = random_manual_strategy(coup)

    cheat_mcts_trials = 1000
    cheat_mcts_strat = cheat_mcts_strategy(cheat_mcts_trials, coup, random_manual_strat)

    cheat_mcts_trials2 = 200
    cheat_mcts_strat2 = cheat_mcts_strategy(cheat_mcts_trials2, coup, random_manual_strat)

    det_mcts_trials = 1000
    det_mcts_strat = det_mcts_strategy(det_mcts_trials, coup, random_manual_strat)

    det_mcts_trials2 = 200
    det_mcts_strat2 = det_mcts_strategy(det_mcts_trials2, coup, random_manual_strat)

    det_mcts_trials_big = 10000
    det_mcts_strat_big = det_mcts_strategy(det_mcts_trials_big, coup, random_manual_strat)


    # basic strategy comparisons
    # test_strategies(1000, random_honest_strat, random_manual_strat, False, False)
    # test_strategies(1000, random_manual_strat, random_honest_strat, False, False)
    # test_strategies(1000, random_strat, random_manual_strat, False, False)
    # test_strategies(1000, random_manual_strat, random_strat, False, False)

    # 200 det tests
    # test_strategies(1000, random_strat, det_mcts_strat2, False, True)
    # test_strategies(1000, random_manual_strat, det_mcts_strat2, False, True)
    # test_strategies(1000, det_mcts_strat2, random_strat, True, False)
    # test_strategies(1000, det_mcts_strat2, random_manual_strat, True, False)

    # 2000 det tests
    test_strategies(1000, random_strat, det_mcts_strat, False, True)
    test_strategies(1000, random_manual_strat, det_mcts_strat, False, True)
    test_strategies(1000, det_mcts_strat, random_strat, True, False)
    test_strategies(1000, det_mcts_strat, random_manual_strat, True, False)

    # mixed tests
    # test_strategies(1000, det_mcts_strat2, det_mcts_strat, True, True)
    # test_strategies(1000, det_mcts_strat, det_mcts_strat2, True, True)
    # test_strategies(1000, det_mcts_strat, det_mcts_strat, True, True)
    # test_strategies(1000, det_mcts_strat2, det_mcts_strat2, True, True)

    # test_strategies(400, det_mcts_strat2, cheat_mcts_strat2, True, False)
    # test_strategies(400, det_mcts_strat, cheat_mcts_strat2, True, False)
    # test_strategies(400, cheat_mcts_strat, cheat_mcts_strat2, False, False)

    # test_strategies(200, det_mcts_strat_big, det_mcts_strat, True, False)
