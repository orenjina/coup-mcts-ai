from random import shuffle, choice, random
# player is asked to perform an action
ACTION = 0
# player is asked whether to react to an action
# both object and block are possible responses
OBJECT = 1
# player is asked whether to object to the block
# prior to this must be a block action
BLOCK = 2
# player is asked to lose an influence
DISCARD = 3
# player is asked to select cards after exchanging using ambassador
EXCHANGE = 4

# 1 v 1 version
class Coup(object):

    def __init__(self, player_count, coins, card_num, copies):
        self.copies = copies
        self.card_num = card_num

        self.players = []
        # Player turn
        self.cur_turn = 0
        # ‘action’, 'object', or 'block' state
        self.cur_state = ACTION
        # current acting player
        self.cur_player = 0
        # last action played
        self.cur_action = None
        # last blocker played, might be 0ed if not relevant
        self.blocker = None
        # mark the target of the current action
        self.target = None

        # debugging log variable
        self.last_choice = None
        # inference variables
        self.obj_res = []

        for i in range(player_count):
            self.players.append(Player(coins, card_num))
            self.obj_res.append((0, 0))

        self.court_deck = [Contessa() for _ in range(copies)] + \
                          [Duke() for _ in range(copies)] + \
                          [Assassin() for _ in range(copies)] + \
                          [Captain() for _ in range(copies)] + \
                          [Ambassador() for _ in range(copies)]

        shuffle(self.court_deck)

        for p in range(player_count):
            for c in range(card_num):
                self.players[p].cards[c] = self.court_deck.pop()

    def __len__(self):
        return sum(1 for p in self.players if p.influence_remaining)

    def filter_out_players(self, list_of_players):
        from random import shuffle
        hits = [p for p in self.players if p not in list_of_players and p.influence_remaining]
        shuffle(hits)
        return hits

    @property
    def winner(self):
        # candidates = [p for p in self.players if p.influence_remaining]
        candidates = [p for p in range(len(self.players)) if \
            len(self.players[p].cardlist()) > 0]
        if len(candidates) == 1:
            return candidates[0]
        else:
            return None

    def available_actions(self):
        if self.cur_state == ACTION:
            base = ['income', 'foreign_aid', 'tax', 'coup', 'steal', \
                'exchange', 'assassinate']
            currency = self.players[self.cur_turn].coins
            if currency > 9:
                return ['coup']
            if currency < 7:
                base.remove('coup')
            if currency < 3:
                base.remove('assassinate')
            return base
        elif self.cur_state == BLOCK:
            return ['pass', 'object']
        elif self.cur_state == DISCARD or self.cur_state == EXCHANGE:
            return self.players[self.cur_player].cardlist()
        else:
            # objecting state
            if self.cur_action == 'foreign_aid':
                return ['pass', 'block']
            elif self.cur_action == 'steal':
                return ['pass', 'blockC', 'blockA', 'object']
            elif self.cur_action == 'tax':
                return ['pass', 'object']
            elif self.cur_action == 'exchange':
                return ['pass', 'object']
            elif self.cur_action == 'assassinate':
                return ['pass', 'block', 'object']
            elif self.cur_action == 'coup':
                # process this maybe
                # shouldn't get here in any version
                print("should not be objecting coup")
                return None
            else:
                # shouldn't be here normally
                print("should not be objecting", self.cur_action)
                return None

    def honest_actions(self):
        cp = self.players[self.cur_player]
        if self.cur_state == ACTION:
            base_set = {'income', 'foreign_aid', 'coup'}
            for c in cp.cards:
                if c.revealed == False:
                    for ac in c.ACTIONS:
                        base_set.add(ac)
            base = list(base_set)
            currency = self.players[self.cur_turn].coins
            if currency > 9:
                return ['coup']
            if currency < 7:
                base.remove('coup')
            if currency < 3 and 'assassinate' in base:
                base.remove('assassinate')
            return base
        elif self.cur_state == BLOCK:
            return ['pass']
        elif self.cur_state == DISCARD:
            return self.players[self.cur_player].cardlist()
        elif self.cur_state == EXCHANGE:
            return self.players[self.cur_player].cardlist()
        else:
            if self.cur_action == 'foreign_aid':
                if cp.contains(Duke()):
                    return ['block']
                else:
                    return ['pass']
            elif self.cur_action == 'steal':
                if cp.contains(Ambassador()):
                    return ['blockA']
                elif cp.contains(Captain()):
                    return ['blockC']
                else:
                    return ['pass']
            elif self.cur_action == 'tax':
                return ['pass']
            elif self.cur_action == 'exchange':
                return ['pass']
            elif self.cur_action == 'assassinate':
                if cp.contains(Contessa()):
                    return ['block']
                elif len(cp.cardlist()) > 1:
                    return ['pass']
                else:
                    return ['object']
            else:
                # shouldn't be here
                return None

    def estimate_actions(self):
        acts = self.honest_actions()
        if 'coup' in acts:
            return ['coup']
        elif 'tax' in acts:
            acts.remove('income')
            acts.remove('foreign_aid')
        return acts

    def prior_actions(self):
        acts = self.available_actions()
        if 'coup' in acts:
            return ['coup']
        if 'tax' in acts:
            acts.remove('income')
            acts.remove('foreign_aid')
        # if 'object' in acts:
        #     acts.remove('object')
        # if 'exchange' in acts:
        #     acts.remove('exchange')
        return acts

    def obj_prior_actions(self):
        acts = self.available_actions()
        if 'coup' in acts:
            return ['coup']
        if 'tax' in acts:
            acts.remove('income')
            acts.remove('foreign_aid')
        # if 'exchange' in acts:
        #     acts.remove('exchange')
        return acts

    def player_turn(self):
        return self.cur_decision[0]

    def perform_action(self, action):
        if self.winner != None:
            print("Game has already ended. The winner is ", self.winner)
        if not action in self.available_actions():
            print("ILLEGAL ACTION: ", action)
            print("can only perform: ", self.available_actions())
            a = 1 / 0
        # inference variable reset
        for i in range(len(self.obj_res)):
            self.obj_res[i] = (0, 0)
        self.last_choice = action # debugging purpose
        if self.cur_state == ACTION:
            self.cur_action = action
            self.target = self.next_player()
        next = self.next_player()
        cur = self.cur_player

        if action == 'income':
            self.realize_action()
            self.cur_action = None
        elif action == 'coup':
            # process coup effect
            Influence.coup(self.players[self.cur_player])
            self.cur_player = next
            self.cur_turn = cur
            self.cur_state = DISCARD
            self.cur_action = None
        elif action == 'foreign_aid' or action == 'steal' or action == 'tax' \
            or action == 'exchange' or action == 'assassinate':
            # only assassinate requires pay even if failed attempt
            if action == 'assassinate':
                Assassin.assassinate(self.players[self.cur_turn])
            self.cur_player = next
            self.cur_turn = cur
            self.cur_state = OBJECT
        elif action == 'object':
            if self.cur_state == BLOCK:
                self.check_object(Coup.influence_translation(self.blocker), cur, next)
            elif self.cur_action == 'steal':
                self.check_object(Captain(), cur, next)
            elif self.cur_action == 'tax':
                self.check_object(Duke(), cur, next)
            elif self.cur_action == 'exchange':
                self.check_object(Ambassador(), cur, next)
            elif self.cur_action == 'assassinate':
                self.check_object(Assassin(), cur, next)
            else:
                print("shouldn't get here")
                # self.log(verbose=False)
            self.blocker = None
            self.cur_action = None
            return
        elif action == 'block':
            if self.cur_action == 'foreign_aid':
                self.blocker = Duke.str()
            elif self.cur_action == 'assassinate':
                self.blocker = Contessa.str()
            else:
                print("wrong command")
                return
            self.cur_state = BLOCK
            self.cur_player = next
        elif action == 'blockA':
            self.cur_state = BLOCK
            self.blocker = Ambassador.str()
            self.cur_player = next
        elif action == 'blockC':
            self.cur_state = BLOCK
            self.blocker = Captain.str()
            self.cur_player = next
        elif action == 'pass':
            if self.cur_action == 'foreign_aid':
                if not self.cur_state == BLOCK:
                    self.realize_action()
                else:
                    self.cur_turn = self.target
                    self.cur_player = self.target
                    self.cur_state = ACTION
            elif self.cur_action == 'steal':
                if not self.cur_state == BLOCK:
                    self.realize_action()
                else:
                    self.cur_turn = self.target
                    self.cur_player = self.target
                    self.cur_state = ACTION
            elif self.cur_action == 'tax':
                self.realize_action()
            elif self.cur_action == 'exchange':
                # irrelevant for now
                self.realize_action()
            elif self.cur_action == 'assassinate':
                # invoke discard influence action
                if not self.cur_state == BLOCK:
                    self.cur_player = self.target
                    self.cur_state = DISCARD
                else:
                    self.cur_turn = self.target
                    self.cur_player = self.target
                    self.cur_state = ACTION
            else:
                print("bad action ", action)
                self.log(verbose=False)
                return
            self.blocker = None
            self.cur_action = None
        elif self.cur_state == DISCARD:
            card = action
            if not card in self.players[self.cur_player].cardlist():
                print("not in list, try again")
                return
            self.players[self.cur_player].lose_influence(Coup.influence_translation(card))
            if self.game_over():
                return
            # rare case of unsuccessfully objecting exchange
            elif len(self.players[1 - self.cur_player].cards) > 2:
                self.cur_state = EXCHANGE
                self.cur_player = 1 - self.cur_player
            elif self.cur_action == 'coup':
                self.cur_turn = self.target
                self.cur_player = self.target
                self.cur_state = ACTION
            else:
                self.cur_turn = self.target
                self.cur_player = self.target
                self.cur_state = ACTION
            self.blocker = None
            self.cur_action = None
        elif self.cur_state == EXCHANGE:
            #discard until 2 or whatever cards left
            card = self.players[self.cur_player].lose_influence(Coup.influence_translation(action), True)
            self.court_deck.append(card)
            if len(self.players[self.cur_player].cards) == self.card_num:
                self.cur_turn = self.target
                self.cur_player = self.target
                self.cur_state = ACTION
            self.blocker = None
            self.cur_action = None
        else:
            # Shouldn't get here in 1 card version
            print("shouldn't get here in 1 card version")
            self.log(verbose=False)
            return

    # perform a direct action in game, if losing card then fill in which
    # card to discard
    def realize_action(self):
        if self.cur_action == 'income':
            Influence.income(self.players[self.cur_turn])
        elif self.cur_action == 'foreign_aid':
            Influence.foreign_aid(self.players[self.cur_turn])
        elif self.cur_action == 'steal':
            Captain.steal(self.players[self.cur_turn], self.players[self.target])
        elif self.cur_action == 'tax':
            Duke.tax(self.players[self.cur_turn])
        elif self.cur_action == 'exchange':
            # add 2 cards then discard until we only have the same cards
            # as starting cards (including revealed cards)
            # print("called")
            self.cur_state = EXCHANGE
            self.cur_player = self.cur_turn
            self.add_card(self.cur_player)
            self.add_card(self.cur_player)
            return
        elif self.cur_action == 'assassinate':
            a = 1 / 0
        else:
            print("shouldn't get here realize_action")
            self.log(verbose=False)
            a = 1 / 0
        self.cur_turn = self.target
        self.cur_player = self.target
        self.cur_state = ACTION
        return

    def check_object(self, influence, cur, next):
        if self.players[next].contains(influence):
            self.card_swap(next, influence)
            # special case of double discard
            if self.cur_state == BLOCK:
                self.cur_player = cur
                self.cur_state = DISCARD
                self.obj_res[cur] = (0, 1)
            else:
                if self.cur_action == "assassinate":
                    self.obj_res[next] = (0, 1)
                    for c in self.players[cur].cards:
                        c.revealed = True
                    return False
                self.cur_player = next
                self.realize_action()
                self.cur_player = cur
                self.cur_state = DISCARD
                self.obj_res[next] = (0, 1)
        else:
            if self.cur_state == BLOCK:
                if self.cur_action == "assassinate":
                    self.obj_res[next] = (1, 1)
                    for c in self.players[next].cards:
                        c.revealed = True
                    return False
                self.cur_player = cur
                self.realize_action()
                self.cur_player = next
                self.cur_state = DISCARD
                self.obj_res[next] = (1, 1)
            else:
                self.cur_player = next
                self.cur_state = DISCARD
                self.obj_res[cur] = (1, 1)

    # happens when objection is handled
    # takes away the confirmed card for a new one
    def card_swap(self, player, card):
        self.court_deck.append(card)
        shuffle(self.court_deck)
        cards = self.players[player].cards
        for i in range(len(cards)):
            if not cards[i].revealed and card.str() == cards[i].str():
                 cards[i] = self.court_deck.pop()
                 break

    def add_card(self, player):
        shuffle(self.court_deck)
        self.players[player].cards.append(self.court_deck.pop())

    def next_player(self):
        return (self.cur_player + 1) % len(self.players)

    @staticmethod
    def influence_translation(card):
        if card == "contessa":
            return Contessa()
        elif card == "captain":
            return Captain()
        elif card == "ambassador":
            return Ambassador()
        elif card == "assassin":
            return Assassin()
        elif card == "duke":
            return Duke()
        else:
            print("ERROR gave influence translation:", card)
            return None

    def info_log(self, player):
        print("==============================")
        print("CURRENT GAME STATUS")
        print("You have", self.players[player].cardlist_log(), "and", self.players\
            [player].coins, " coins.")
        print("Your opponent has", self.players[1 - player].coins, "coins and", \
            "revealed cards", self.players[1 - player].revealedlist())
        print("Current action is ", self.cur_action)
        print("Current state is ", self.cur_state)
        if self.cur_player == player:
            print("Available actions", self.available_actions())
        print("==============================")

    def log(self, verbose=False):
        if verbose:
            print("==============================")
            print("CURRENT GAME STATUS")
            print("Player 1 has ", self.players[0].cardlist(), " and ", self.players\
                [0].coins, " coins.")
            print("Player 2 has ", self.players[1].cardlist(), " and ", self.players\
                [1].coins, " coins.")
            print("Current action is ", self.cur_action)
            print("Current state is ", self.cur_state)
            print("Current turn is Player ", (self.cur_turn + 1))
            print("==============================")
        else:
            print(self.game_state())
            print("act:", self.last_choice)

    def game_state(self):
        ret = []
        ret.append(self.cur_turn)
        ret.append(self.cur_player)
        ret.append(self.cur_state)
        ret.append(self.blocker)
        ret.append(self.target)
        ret.append(self.cur_action)
        ret.append(self.players[0].player_state())
        ret.append(self.players[1].player_state())
        return tuple(ret)

    def information_set(self, player):
        ret = []
        ret.append(self.cur_turn)
        ret.append(self.cur_player)
        ret.append(self.cur_state)
        ret.append(self.blocker)
        ret.append(self.target)
        ret.append(self.cur_action)
        if player == 0:
            ret.append(self.players[0].player_state())
            ret.append(self.players[1].public_info())
        else:
            ret.append(self.players[0].public_info())
            ret.append(self.players[1].player_state())
        return tuple(ret)

    @staticmethod
    def rand_det(player, info_set, copies):
        hid_p = info_set[6 + (1 - player)][1:]
        open_p = info_set[6 + player][1:]

        court_deck = [Contessa() for _ in range(copies)] + \
                     [Duke() for _ in range(copies)] + \
                     [Assassin() for _ in range(copies)] + \
                     [Captain() for _ in range(copies)] + \
                     [Ambassador() for _ in range(copies)]

        shuffle(court_deck)

        num = len(hid_p)
        for item in hid_p:
            if item != None:
                Coup.deck_remove(court_deck, item)
                num -= 1

        for item, _ in open_p:
            Coup.deck_remove(court_deck, item)

        ret = []
        for i in range(num):
            ret.append(court_deck.pop())

        return ret

    @staticmethod
    def deck_remove(deck, card):
        for c in deck:
            if c.str() == card:
                deck.remove(c)
                break

    # assume information set is on player
    # pos is information set
    def determinize(self, pos, player, cards):
        self.cur_turn = pos[0]
        self.cur_player = pos[1]
        self.cur_state = pos[2]
        self.blocker = pos[3]
        self.target = pos[4]
        self.cur_action = pos[5]
        if player == 0:
            self.players[0].set_state(pos[6])
            ap = [pos[7][0]]
            index = 0
            for item in pos[7][1:]:
                if item == None:
                    ap.append((cards[index].str(), 0))
                    index += 1
                else:
                    ap.append((item, 1))
            self.players[1].set_state(ap)
        else:
            ap = [pos[6][0]]
            index = 0
            for item in pos[6][1:]:
                if item == None:
                    ap.append((cards[index].str(), 0))
                    index += 1
                else:
                    ap.append((item, 1))
            self.players[0].set_state(ap)
            self.players[1].set_state(pos[7])

    def set_state(self, pos):
        self.cur_turn = pos[0]
        self.cur_player = pos[1]
        self.cur_state = pos[2]
        self.blocker = pos[3]
        self.target = pos[4]
        self.cur_action = pos[5]
        self.players[0].set_state(pos[6])
        self.players[1].set_state(pos[7])

        if len(self.court_deck) + len(self.players[0].cardlist()) \
            + len(self.players[1].cardlist()) != self.copies * 5:
            court_deck = [Contessa() for _ in range(self.copies)] + \
                         [Duke() for _ in range(self.copies)] + \
                         [Assassin() for _ in range(self.copies)] + \
                         [Captain() for _ in range(self.copies)] + \
                         [Ambassador() for _ in range(self.copies)]

            for item, _ in pos[6][1:]:
                Coup.deck_remove(court_deck, item)

            for item, _ in pos[7][1:]:
                Coup.deck_remove(court_deck, item)

            self.court_deck = court_deck


    def game_over(self):
        return self.winner != None


class Player(object):
    def __init__(self, coins, num_cards):
        self.coins = coins
        self.cards = [None] * num_cards

    # check if this player holds the type of card
    def contains(self, card):
        for c in self.cards:
            if not c.revealed and c.str() == card.str():
                return True
        return False

    # lose an influence card of a given type
    def lose_influence(self, card, ex=False):
        for c in self.cards:
            if c.str() == card.str() and c.revealed == False:
                if not ex:
                    c.revealed = True
                else:
                    self.cards.remove(c)
                return c
        # An error happened, could not find the card to discard
        print("could not lose influence")
        return False

    def revealedlist(self):
        ret = []
        for c in self.cards:
            if c.revealed:
                ret.append(c.str())
        if len(ret) == 0:
            return "None"
        return ret

    # print out every influence in possession not revealed
    def cardlist_log(self):
        ret = []
        for c in self.cards:
            temp = c.str() + "," + str(c.revealed)
            ret.append(temp)
        return ret

    def cardlist(self):
        ret = []
        for c in self.cards:
            if not c.revealed:
                ret.append(c.str())
        return ret

    def player_state(self):
        ret = []
        ret.append(self.coins)
        for c in self.cards:
            ret.append((c.str(), int(c.revealed)))
        return ret

    def public_info(self):
        ret = []
        ret.append(self.coins)
        # separately to maintain order in tuples
        # as to not duplicate some identical information sets
        for c in self.cards:
            if c.revealed:
                ret.append(c.str())

        for c in self.cards:
            if not c.revealed:
                ret.append(None)
        return ret

    def set_state(self, state):
        # set state here
        self.coins = state[0]
        state = state[1:]
        self.cards = []
        for card in state:
            cur_card = Coup.influence_translation(card[0])
            cur_card.revealed = bool(card[1])
            self.cards.append(cur_card)


class Influence(object):
    def __init__(self):
        self.revealed = False

    def __str__(self):
        return str(self.__class__.__name__)

    def reveal(self):
        self.revealed = True

    @staticmethod
    def income(active_player):
        active_player.coins += 1

    @staticmethod
    def foreign_aid(active_player):
        active_player.coins += 2

    @staticmethod
    def coup(active_player):
        if active_player.coins >= 7:
            active_player.coins -= 7
        else:
            raise IllegalAction("insufficient currency to coup")

class Captain(Influence):
    ACTIONS = ['steal']
    BLOCKS = ['steal']

    @staticmethod
    def steal(active_player, player_target):
        if player_target.coins >= 2:
            player_target.coins -= 2
            active_player.coins += 2
        else:
            available_coins = player_target.coins
            player_target.coins -= available_coins
            active_player.coins += available_coins

    @staticmethod
    def str():
        return 'captain'

class Duke(Influence):
    ACTIONS = ['tax']
    BLOCKS = ['foreign_aid']

    @staticmethod
    def tax(active_player):
        active_player.coins += 3

    @staticmethod
    def str():
        return 'duke'

class Assassin(Influence):
    ACTIONS = ['assassinate']
    BLOCKS = []

    @staticmethod
    def assassinate(active_player):
        if active_player.coins >= 3:
            active_player.coins -= 3
        else:
            print("insufficient currency to assassinate")

    @staticmethod
    def str():
        return 'assassin'

class Ambassador(Influence):
    ACTIONS = ['exchange']
    BLOCKS = ['steal']

    @staticmethod
    def str():
        return 'ambassador'

class Contessa(Influence):
    ACTIONS = []
    BLOCKS = ['assassinate']

    @staticmethod
    def str():
        return 'contessa'
