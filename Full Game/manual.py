from model import *

if __name__ == "__main__":
    coup = Coup(2, 2, 2, 3)

    while not coup.game_over():
        coup.log(verbose=False)
        print(coup.available_actions())
        p_input = input()
        coup.perform_action(p_input)

    coup.log(verbose=False)

    print("winner is", coup.winner)
