from Trie import Trie
from string import ascii_lowercase
from collections import defaultdict

def getInput(question:str) -> bool:
    print(question)
    ans = input()
    return ans.casefold()

class SpellingBee:
    def __init__(self, trie: Trie):
        self.trie = trie._scrabbleWordsInstance

    def play(self):
        alphabet = getInput("Type all the letters on todays spelling bee, starting with the middle letter.\nExample: captive (where c is the middle letter)")
        if len(set(alphabet)) != 7:
            print("Uh oh. That was not seven unique letters. Please try again")
            return True

        self.trie.alphabet = alphabet
        print(f"Here's a list of all the words I found containing {alphabet[1:]} with {alphabet[0]} as the middle letter:")
        [print(i) for i in sorted(self.trie.wildcardMatches(self.trie.root, "", f"*{alphabet[0]}*"))]

        return getInput("Would you like to play again? (y/n)") == "y"

class Wordle:
    def __init__(self, trie: Trie):
        self.trie = trie._scrabbleWordsInstance

    def processGuess(self):
        query = ''
        invalidPositions = defaultdict(list)
        for i, (f, g) in enumerate(zip(self.feedback, self.guess)):
            query += g if f == 'g' else '?'
            if f == 'n':
                self.trie.alphabet.discard(g)
            if f == 'y':
                invalidPositions[g].append(i)

        return query, invalidPositions, set(invalidPositions.keys())

    def getGuess(self) -> None:
        guessInstance = "first" if not self.guess else "next"
        self.guess = getInput(f"Type your {guessInstance} guess")
        if len(self.guess) != 5:
            print("Uh oh. That was not five letters. Please try again")
            self.guess = ""

    def getFeedback(self) -> None:
        print("For each letter guessed type y for yellow, n for 'not included', and g for green -- not separated by spaces. For example:")
        self.feedback = getInput(f"'ygnnn' if '{self.guess[0]}' is in the wrong position, '{self.guess[1]}' is in the right position, and '{self.guess[2:5]}' are not in the wordle")

        if len(self.feedback) != 5:
            print("Uh oh. That was not five letters. Please try again")
            self.feedback = ""

        if not set(self.feedback) <= {'n', 'y', 'g'}:
            print("Uh oh. Please only use letters 'n', 'y', and 'g'")
            self.feedback = ""

    def play(self):
        self.trie.alphabet = set(ascii_lowercase)
        self.guess = ""
        self.feedback = ""
        NUM_GUESSES = 5
        for _ in range(NUM_GUESSES):
            self.getGuess()
            if not self.guess:
                return True

            self.getFeedback()
            if not self.feedback:
                return True

            query, invalidPositions, unusedLetters = self.processGuess()
            print(f"Here's a list of all the words I found that may be the wordle:")
            [print(i) for i in sorted(self.trie.wildcardMatches(self.trie.root, "", query, invalidPositions, unusedLetters))]

""" User Interface Logic """
def runMainProgram() -> bool:

    if getInput("Fancy a game of Spelling Bee? (y/n)") == "y":
        while SpellingBee(Trie()).play():
            continue
    if getInput("How about a game of Wordle? (y/n)") == "y":
        while Wordle(Trie(forWordle = True)).play():
            continue
    if getInput("Want to query the dictionary? (y/n)") == "y":
        alphabet = getInput("Type letters you'd like to make words out of, not separated by a space")

    return getInput("Do you want to do this again? (y/n)") == "y"

if __name__ == '__main__':
    while runMainProgram():
        continue
    print("Peace!")
