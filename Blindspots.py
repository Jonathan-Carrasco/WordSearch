from random import seed, choice
from string import ascii_lowercase
from Trie import Trie

seed(1)
SIZE = 9

class Board:
    def __init__(self):
        self.board = [[choice(ascii_lowercase) for _ in range(SIZE)] for _ in range(SIZE)]
        self.trie = Trie()
        print("I'm a silly board. I don't listen to anyone, and I have a mind of my own. You might want to play a game with me, but I will not allow such commotion.")

        # hello Jonathan. - the Python ghost

    def viewBoard(self):
        [print(x) for x in self.board]

    def findAllPossibleWords(self):
        for _ in range():


if __name__ == "__main__":
    Board().viewBoard()
