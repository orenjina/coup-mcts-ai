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
def cheat_mcts_strategy(n, rule, sim):
    def fxn(pos):
        value, move = mcts(pos, rule, n, sim)
        return move
    return fxn

# do the simulation in a loop given number of iterations
# update the dictionary
def mcts(pos, rule, n, sim):
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

        # find the best node to expand using the formula
        # expand and find the children of the node
        cur = nextExpand(tree, it, me, rule)
        # if the current node is already the end, we don't need to expand
        cur_pos = tree[cur][POS]

        # rule.log()
        # print(rule.game_state())

        rule.set_state(cur_pos)

        if rule.game_over():
            it += 1
            res = simulation(cur_pos, me, rule, sim)
            backProp(tree, cur, res)
            no_explore += 1
            if no_explore > n / 10:
                break
            continue

        rule.set_state(cur_pos)
        moves = rule.available_actions()
        # rule.log()
        # print(rule.game_state())

        # otherwise evaluate all moves and update the tree
        for move in moves:
            rule.set_state(cur_pos)
            rule.perform_action(move)
            new_pos = rule.game_state()

            res = simulation(new_pos, me, rule, sim)
            tree[cur][SUC].append(t_size)
            tree.append([new_pos, cur, [], res, 1, move])
            # back propagate up the tree
            backProp(tree, t_size, res)
            t_size += 1
        it += len(moves)
    # take the children with the best result
    max = -1
    ret = None
    moves = rule.available_actions()
    # print("stuck:", stuck)
    # assume at least 1 element in the successor
    # print(tree[0][SUC])
    for child in tree[0][SUC]:
        res = tree[child][SCO] / tree[child][PLA]
        if (res >= max):
            max = res
            ret = tree[child][MOV]
    return max, ret

# find the next node we should expand by traversing down the tree
# and applying the formula
def nextExpand(tree, total, me, rule):
    k = math.sqrt(2 * math.log(total))
    cur = 0
    rule.set_state(tree[cur][POS])
    while not rule.game_over() and len(tree[cur][SUC]) > 0:
        children = tree[cur][SUC]
        max = -1000
        res = None
        for child in children:
            info = tree[child]
            # print(tree[cur][POS]._seeds)
            val = k * math.sqrt(1 / info[PLA])
            if (tree[cur][POS][CP] == me):
                val += info[SCO] / info[PLA]
            else:
                val -= info[SCO] / info[PLA]
            if (val > max):
                max = val
                res = child
        cur = res
        rule.set_state(tree[cur][POS])
    return cur

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
