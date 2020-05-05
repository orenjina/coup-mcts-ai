from model import *
from cheat_mcts import cheat_mcts_strategy
from det_mcts import det_mcts_strategy
from det_obj_mcts import det_obj_mcts_strategy
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

def random_noobject_strategy(rule):
    def fxn(pos):
        rule.set_state(pos)
        return random.choice(rule.prior_actions())
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
    # inference reset
    if hasattr(strat1, 'obj_rec'):
        strat1.obj_rec = (1, 2)
    if hasattr(strat2, 'obj_rec'):
        strat2.obj_rec = (1, 2)

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
            if hasattr(strat1, 'obj_rec'):
                strat1.obj_rec = (strat1.obj_rec[0] + coup.obj_res[0][0], \
                    strat1.obj_rec[1] + coup.obj_res[0][1])
            if hasattr(strat2, 'obj_rec'):
                # print(coup.obj_res)
                strat2.obj_rec = (strat2.obj_rec[0] + coup.obj_res[1][0], \
                    strat2.obj_rec[1] + coup.obj_res[1][1])
                # print(strat2.obj_rec)
            if verbose:
                print(act)
                coup.log()
            moves += 1
        if coup.winner == 0:
            wins += 1

    end_time = time.time()
    print("average game time", (end_time - start_time) / games, "seconds")
    if hasattr(strat1, 'obj_rec'):
        print("inference result for p0 is", strat1.obj_rec)
    if hasattr(strat2, 'obj_rec'):
        print("inference result for p1 is", strat2.obj_rec)
    print("win rate of the first player", wins / games)

# same as above, but alternating starting player
def test_alt_strategies(games, strat1, strat2, info1, info2, verbose=False):
    wins = 0
    start_time = time.time()
    # inference reset
    if hasattr(strat1, 'obj_rec'):
        strat1.obj_rec = (1, 2)
    if hasattr(strat2, 'obj_rec'):
        strat2.obj_rec = (1, 2)

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
            if coup.cur_player == g % 2:
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
            if hasattr(strat1, 'obj_rec'):
                strat1.obj_rec = (strat1.obj_rec[0] + coup.obj_res[0][0], \
                    strat1.obj_rec[1] + coup.obj_res[0][1])
            if hasattr(strat2, 'obj_rec'):
                # print(coup.obj_res)
                strat2.obj_rec = (strat2.obj_rec[0] + coup.obj_res[1][0], \
                    strat2.obj_rec[1] + coup.obj_res[1][1])
                # print(strat2.obj_rec)
            if verbose:
                print(act)
                coup.log()
            moves += 1

        if coup.winner == g % 2:
            wins += 1

    end_time = time.time()
    print("average game time", (end_time - start_time) / games, "seconds")

    if hasattr(strat1, 'obj_rec'):
        print("inference result for p0 is", strat1.obj_rec)
    if hasattr(strat2, 'obj_rec'):
        print("inference result for p1 is", strat2.obj_rec)
    print("win rate of the first player", wins / games)

if __name__ == "__main__":
    EXAMPLE_END_STATE = (0, 1, 3, None, 1, 'coup', [7, 'contessa'], [8, 'contessa'])
    STATE = (0, 0, 0, 'duke', 0, 'income', [4, ('duke', 0), ('contessa', 0)], [1, ('assassin', 1), ('assassin', 0)])

    coup = Coup(2, 2, 2, 3)

    random_strat = random_strategy(coup)
    random_honest_strat = random_honest_strategy(coup)
    random_manual_strat = random_manual_strategy(coup)
    random_noobject_strat = random_noobject_strategy(coup)

    cheat_mcts_trials = 1000
    cheat_mcts_strat = cheat_mcts_strategy(cheat_mcts_trials, coup, random_manual_strat)

    cheat_mcts_trials2 = 200
    cheat_mcts_strat2 = cheat_mcts_strategy(cheat_mcts_trials2, coup, random_manual_strat)

    det_mcts_trials = 1000
    det_mcts_strat = det_mcts_strategy(det_mcts_trials, coup, random_manual_strat)

    det_mcts_trials2 = 200
    det_mcts_strat2 = det_mcts_strategy(det_mcts_trials2, coup, random_manual_strat)

    det_obj_mcts_trials = 1000
    det_obj_mcts_strat = det_obj_mcts_strategy(det_obj_mcts_trials, coup, random_manual_strat)

    det_obj_mcts_trials2 = 200
    det_obj_mcts_strat2 = det_obj_mcts_strategy(det_obj_mcts_trials2, coup, random_manual_strat)

    det_mcts_trials_big = 5000
    det_mcts_strat_big = det_mcts_strategy(det_mcts_trials_big, coup, random_manual_strat)

    det_obj_mcts_trials_big = 5000
    det_obj_mcts_strat_big = det_obj_mcts_strategy(det_obj_mcts_trials_big, coup, random_manual_strat)


    # basic strategy comparisons
    # test_strategies(1000, random_strat, random_manual_strat, False, False) # 0.204
    # test_strategies(1000, random_manual_strat, random_strat, False, False) # 0.852
    # test_strategies(1000, random_manual_strat, random_noobject_strat, False, False) # 0.458
    # test_strategies(1000, random_noobject_strat, random_manual_strat, False, False) # 0.574
    # test_strategies(1000, random_strat, random_noobject_strat, False, False) # 0.722
    # test_strategies(1000, random_noobject_strat, random_strat, False, False) # 0.345

    # 200 det tests
    # test_strategies(100, random_strat, det_mcts_strat2, False, True)
    # test_strategies(100, random_manual_strat, det_mcts_strat2, False, True)
    # test_strategies(100, random_noobject_strat, det_mcts_strat2, False, True)
    # test_strategies(100, det_mcts_strat2, random_strat, True, False)
    # test_strategies(100, det_mcts_strat2, random_manual_strat, True, False)
    # test_strategies(100, det_mcts_strat2, random_noobject_strat, True, False)

    # 200 det tests
    test_alt_strategies(1000, random_strat, det_obj_mcts_strat2, False, True)
    test_alt_strategies(1000, random_manual_strat, det_obj_mcts_strat2, False, True)
    test_alt_strategies(1000, random_noobject_strat, det_obj_mcts_strat2, False, True)

    # test_alt_strategies(100, det_obj_mcts_strat2, random_manual_strat, True, False)

    # 1000 det tests
    # test_strategies(100, random_strat, det_mcts_strat, False, True)
    # test_strategies(100, random_manual_strat, det_mcts_strat, False, True)
    # test_strategies(100, random_noobject_strat, det_mcts_strat, False, True)
    # test_strategies(100, det_mcts_strat, random_strat, True, False)
    # test_strategies(100, det_mcts_strat, random_manual_strat, True, False)
    # test_strategies(100, det_mcts_strat, random_noobject_strat, True, False)

    # 1000 det tests
    test_alt_strategies(1000, random_strat, det_obj_mcts_strat, False, True)
    test_alt_strategies(1000, random_manual_strat, det_obj_mcts_strat, False, True)
    test_alt_strategies(1000, random_noobject_strat, det_obj_mcts_strat, False, True)

    # 10000 det tests
    # test_strategies(400, random_strat, det_mcts_strat_big, False, True)
    # test_strategies(400, random_manual_strat, det_mcts_strat_big, False, True)
    # test_strategies(400, det_mcts_strat_big, random_strat, True, False)
    # test_strategies(40, det_mcts_strat_big, random_manual_strat, True, False, True)

    # mixed tests
    # test_alt_strategies(100, det_obj_mcts_strat2, det_mcts_strat2, True, True)
    # test_alt_strategies(100, det_obj_mcts_strat, det_mcts_strat, True, True)
    # test_alt_strategies(100, det_obj_mcts_strat, det_obj_mcts_strat2, True, True)
    # test_alt_strategies(100, det_obj_mcts_strat_big, det_obj_mcts_strat2, True, True)

    # test_strategies(100, det_mcts_strat2, det_mcts_strat, True, True)
    # test_strategies(100, det_mcts_strat, det_mcts_strat2, True, True)
    # test_strategies(1000, det_mcts_strat, det_mcts_strat, True, True)
    # test_strategies(1000, det_mcts_strat2, det_mcts_strat2, True, True)

    # test_strategies(400, det_mcts_strat_big, random_manual_strat, True, False)
    # test_strategies(400, det_mcts_strat_big, random_manual_strat, True, False)
    # test_strategies(400, det_mcts_strat_big, random_manual_strat, True, False)
    #
    # test_strategies(400, random_manual_strat, det_mcts_strat_big, False, True)
    # test_strategies(400, random_manual_strat, det_mcts_strat_big, False, True)
    # test_strategies(400, random_manual_strat, det_mcts_strat_big, False, True)



    # test_strategies(400, random_manual_strat, cheat_mcts_strat2, False, False)
    # test_strategies(400, det_mcts_strat, cheat_mcts_strat2, True, False)
    # test_strategies(400, cheat_mcts_strat, cheat_mcts_strat2, False, False)

    # test_strategies(200, det_mcts_strat_big, det_mcts_strat, True, False)
