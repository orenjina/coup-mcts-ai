from random import shuffle, choice
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

        for i in range(player_count):
            self.players.append(Player(coins, card_num))

        self.court_deck = [Contessa() for _ in range(copies)] + \
                          [Duke() for _ in range(copies)] + \
                          [Assassin() for _ in range(copies)] + \
                          [Captain() for _ in range(copies)]
                        # [Ambassador() for _ in range(copies)]

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
                'assassinate']
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
        elif self.cur_state == DISCARD:
            return self.players[self.cur_player].cardlist()
        else:
            # objecting state
            if self.cur_action == 'foreign_aid':
                return ['pass', 'block']
            elif self.cur_action == 'steal':
                return ['pass', 'blockC', 'object'] # no ambassador in game
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
            base = ['income', 'foreign_aid', 'coup']
            for c in cp.cards:
                base += c.ACTIONS
            currency = self.players[self.cur_turn].coins
            if currency > 9:
                return ['coup']
            if currency < 7:
                base.remove('coup')
            if currency < 3 and 'assassinate' in base:
                base = [x for x in base if x != 'assassinate']
            return base
        elif self.cur_state == BLOCK:
            return ['pass']
        elif self.cur_state == DISCARD:
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
                    return ['object']
                elif len(cp.cardlist()) > 1:
                    return ['pass']
                else:
                    return ['object']
            elif self.cur_action == 'coup':
                # process this maybe
                # shouldn't get here in 1 card version
                return None
            else:
                # shouldn't be here normally
                return None

    def player_turn(self):
        return self.cur_decision[0]

    def perform_action(self, action):
        if self.winner != None:
            print("Game has already ended. The winner is ", self.winner)
        if not action in self.available_actions():
            print("ILLEGAL ACTION: ", action)
            a = 1 / 0
            return None
        self.last_choice = action # debugging purpose
        if self.cur_state == ACTION:
            self.cur_action = action
            self.target = self.next_player()
        next = self.next_player()
        cur = self.cur_player

        if action == 'income':
            self.realize_action()
        elif action == 'coup':
            # process coup effect
            Influence.coup(self.players[self.cur_player])
            self.cur_player = next
            self.cur_turn = cur
            self.cur_state = DISCARD
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
                self.log(verbose=False)
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
                    self.realize_action()
                else:
                    self.cur_turn = self.target
                    self.cur_player = self.target
                    self.cur_state = ACTION
            else:
                print("bad action ", action)
                self.log(verbose=False)
                return
        elif self.cur_state == DISCARD:
            self.realize_action(card=action)
        else:
            # Shouldn't get here in 1 card version
            print("shouldn't get here in 1 card version")
            self.log(verbose=False)
            return

    # perform a direct action in game, if losing card then fill in which
    # card to discard
    def realize_action(self, card=None):
        if card != None:
            if not card in self.players[self.cur_player].cardlist():
                print("not in list, try again")
                return
            self.players[self.cur_player].lose_influence(Coup.influence_translation(card))
            if self.game_over():
                return
            elif self.cur_action == 'coup':
                self.cur_turn = self.target
                self.cur_player = self.target
                self.cur_state = ACTION
                return
            elif self.cur_player != self.cur_turn:
                # irrelevant in 1 card version
                # self.cur_turn = self.target
                # self.cur_player = self.target
                # self.cur_state = ACTION
                self.realize_action()
                return
            else:
                self.cur_turn = self.target
                self.cur_player = self.target
                self.cur_state = ACTION
                return
        elif self.cur_action == 'income':
            Influence.income(self.players[self.cur_turn])
        elif self.cur_action == 'foreign_aid':
            Influence.foreign_aid(self.players[self.cur_turn])
        elif self.cur_action == 'steal':
            Captain.steal(self.players[self.cur_turn], self.players[self.target])
        elif self.cur_action == 'tax':
            Duke.tax(self.players[self.cur_turn])
        elif self.cur_action == 'exchange':
            Ambassador.exchange(self.players[self.cur_turn], \
                self.players[self.court_deck])
        elif self.cur_action == 'assassinate':
            self.cur_player = self.target
            self.cur_state = DISCARD
            return
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
            self.cur_player = cur
        else:
            self.cur_player = next
        self.cur_state = DISCARD

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

    def log(self, verbose=False):
        if verbose:
            print("==============================")
            print("CURRENT STATUS OF THE COUP GAME")
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
                     [Captain() for _ in range(copies)]

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
    def lose_influence(self, card):
        for c in self.cards:
            if c.str() == card.str() and c.revealed == False:
                c.revealed = True
                return True
        # An error happened, could not find the card to discard
        print("could not lose influence")
        return False

    # print out every influence in possession not revealed
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
    def exchange(active_player, court_deck):
        from random import randint

        available_influence = []
        available_influence.append(court_deck.pop())
        available_influence.append(court_deck.pop())

        if not active_player.left.revealed:
            available_influence.append(active_player.left)
        if not active_player.right.revealed:
            available_influence.append(active_player.right)

        if not active_player.left.revealed:
            active_player.left = available_influence.pop(randint(0, len(available_influence)-1))
        if not active_player.right.revealed:
            active_player.right = available_influence.pop(randint(0, len(available_influence)-1))

        court_deck.extend(available_influence)

    @staticmethod
    def str():
        return 'ambassador'

class Contessa(Influence):
    ACTIONS = []
    BLOCKS = ['assassinate']

    @staticmethod
    def str():
        return 'contessa'
