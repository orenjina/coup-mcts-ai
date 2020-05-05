import random
import math
from model import *

POS = 0
ANC = 1
SUC = 2
SCO = 3
PLA = 4
MOV = 5

CP = 1

# n for number of iterations
def det_mcts_strategy(n, rule, sim):
    def fxn(pos):
        value, move = det_mcts(pos, rule, n, sim)
        return move
    return fxn

# do the simulation in a loop given number of iterations
# pass in an information set
def det_mcts(pos, rule, n, sim):
    # print(pos)
    # tree array structure
    # key: series of moves
    # value: position, ancestor, successors, wins, times traversed, last action
    # ancestor and predecessor then are series of moves.
    tree = []
    tree.append([pos, None, [], 0, 1, None])
    t_size = 1
    # possible nodes to be expanded
    # moves = [pos]
    me = pos[CP] # cur player

    # number of iterations
    it = 1
    no_explore = 0
    # loop until number of iterations are hit
    while (it < n + 1):
        det = Coup.rand_det(me, pos, rule.copies)
        rule.determinize(pos, me, det)
        # Now we have determinized
        det = rule.game_state()

        # find the best node to expand using the formula
        # expand and find the children of the node
        cur_state, cur = nextExpand(tree, it, me, rule, det, sim)
        # special case of extra expansion
        if cur == None:
            it += cur_state
            continue
        rule.set_state(cur_state)
        # if the current node is already the end, we don't need to expand
        if rule.game_over():
            it += 1
            res = simulation(cur_state, me, rule, sim)
            backProp(tree, cur, res)
            no_explore += 1
            if no_explore > n / 10:
                break
            continue

        moves = rule.prior_actions()
        # otherwise evaluate all moves and update the tree
        for move in moves:
            rule.set_state(cur_state)
            rule.perform_action(move)
            cur_info = rule.information_set(me)
            new_pos = rule.game_state()

            res = simulation(new_pos, me, rule, sim)
            tree[cur][SUC].append(t_size)
            tree.append([cur_info, cur, [], res, 1, move])
            # back propagate up the tree
            backProp(tree, t_size, res)
            t_size += 1
        it += len(moves)
    # take the children with the best result
    det = Coup.rand_det(me, pos, rule.copies)
    rule.determinize(pos, me, det)
    move_votes = {}
    for m in rule.available_actions():
        move_votes[m] = (0, 0)
    # print("stuck:", stuck)
    # assume at least 1 element in the successor
    # print(tree[0][SUC])
    for child in tree[0][SUC]:
        info = tree[child]
        res = info[SCO] / info[PLA]
        # print(info[MOV], ",", res)
        move_votes[info[MOV]] = (info[SCO] + move_votes[info[MOV]][0], \
            info[PLA] + move_votes[info[MOV]][1])

    max = -1
    ret = None
    for m, (s, p) in move_votes.items():
        if p == 0:
            continue
        res = s / p
        # print(m, ",", res)
        if (res >= max):
            max = res
            ret = m
    return max, ret

# find the next node we should expand by traversing down the tree
# and applying the formula
def nextExpand(tree, total, me, rule, det, sim):
    k = math.sqrt(2 * math.log(total))
    cur = 0
    cur_state = det
    rule.set_state(cur_state)
    while not rule.game_over() and len(tree[cur][SUC]) > 0:
        children = tree[cur][SUC]
        cur_sets = []
        for i in range(len(children)):
            cur_sets.append(tree[children[i]][POS])
        # coverage check
        moves = rule.prior_actions()
        # otherwise evaluate all moves and update the tree
        return_flag = 0
        for move in moves:
            rule.set_state(cur_state)
            rule.perform_action(move)
            cur_info = rule.information_set(me)
            if not cur_info in cur_sets:
                new_pos = rule.game_state()
                res = simulation(new_pos, me, rule, sim)
                tree[cur][SUC].append(len(tree))
                tree.append([cur_info, cur, [], res, 1, move])
                # back propagate up the tree
                backProp(tree, len(tree) - 1, res)
                return_flag += 1
        if return_flag > 0:
            return return_flag, None

        # print("regular descent with", children)
        # print("has information set", rule.information_set(me))
        # regular MCTS descent
        max = -1000
        res = None
        for child in children:
            info = tree[child]
            rule.set_state(cur_state)
            if info[MOV] in rule.available_actions():
                rule.perform_action(info[MOV])
            else:
                continue
            if rule.information_set(me) != info[POS]:
                # print("not a good information set")
                continue
            # print("a good information set exists")
            # get the search value
            val = k * math.sqrt(1 / info[PLA])
            if (tree[cur][POS][CP] == me):
                val += info[SCO] / info[PLA]
            else:
                val -= info[SCO] / info[PLA]
            if (val > max):
                max = val
                res = child
        if max == -1000:
            return cur_state, cur
        cur = res
        rule.set_state(cur_state)
        rule.perform_action(tree[cur][MOV])
        cur_state = rule.game_state()
    return cur_state, cur

# propagate findings back up the tree
def backProp(tree, move, res):
    cur = move
    while (tree[cur][ANC]):
        cur = tree[cur][ANC]
        tree[cur][PLA] += 1
        tree[cur][SCO] += res

# Given position, simulate results by picking reasonable steps, return result
def simulation(pos, me, rule, sim):
    rule.set_state(pos)
    while not rule.game_over():
        pos = rule.game_state()
        act = sim(pos)
        rule.perform_action(act)
    return int(rule.winner == me)
