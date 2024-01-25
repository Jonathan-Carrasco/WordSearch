from string import ascii_lowercase
from typing import List

class TrieNode:
    def __init__(self):
        self.isWord = False
        self.children = defaultdict(TrieNode)

class Trie(object):
    _wordleWordsInstance = None
    _scrabbleWordsInstance = None

    """
    Lazy initializes two Tries:
        • Trie with words of length 5 if solving the Wordle
        • Trie with scrabble words if solving the Spelling Bee or querying the Trie
    """
    def __new__(cls, forWordle = False):
        if forWordle:
            if cls._wordleWordsInstance is None:
                cls._wordleWordsInstance = super(Trie, cls).__new__(cls)
            return cls._wordleWordsInstance

        if cls._scrabbleWordsInstance is None:
            cls._scrabbleWordsInstance = super(Trie, cls).__new__(cls)
        return cls._scrabbleWordsInstance

    def __init__(self, **kwargs):
        self.root = TrieNode()
        self.alphabet = ascii_lowercase
        self.filename = "WordleWords.txt" if kwargs.get('forWordle', False) else "ScrabbleWords.txt"

        with open(self.filename, 'r') as f:
            [self.addWord(line.strip()) for line in f]

    def addWord(self, word: str) -> None:
        node = self.root
        for c in word:
            node = trie.children[c]
        node.isWord = True

    def isWord(self, word: str) -> bool:
        trie = self.root
        for c in word:
            if c not in trie.children:
                return False
            trie = trie.children[c]

        return trie.isWord

    def getAllWords(self, node: TrieNode = None, prefix: str = "", wordsFound: List[str] = []) -> List[str]:
        node = self.root if not node else node

        if node.isWord:
            wordsFound.append(prefix)

        [self.getAllWords(node.children[c], prefix+c, wordsFound) for c in self.alphabet if c in node.children]

        return wordsFound

    # Optimize by adding to set? Also do i need the set? Maybe all the words that are added are unique
    def wildcardMatches(self, remaining: str, node: TrieNode = None, prefix: str = "", matches: List[str] = [], invalidPositions = None, unusedLetters = None) -> List[str]:
        node = self.root if not node else node

        print(f"query = {remaining} prefix = {prefix} \n matches = {matches}")

        if node.isWord and all(c == '*' for c in remaining) and not unusedLetters:
            matches.append(prefix)

        if not remaining:
            return matches

        if remaining[0] == '*':
            for c in self.alphabet:
                if c in node.children:
                    self.wildcardMatches(remaining[1:], node.children[c], prefix+c, matches)  # Use char and process '*'
                    self.wildcardMatches(remaining, node.children[c], prefix+c, matches)      # Use char but don't process '*'
            self.wildcardMatches(remaining[1:], node, prefix, matches)                    # Skip '*'

        elif remaining[0] == '?':
            for c in self.alphabet:
                if c in node.children and len(prefix) not in invalidPositions.get(c,[]):
                    remainingLetters = unusedLetters - {c} if unusedLetters else None
                    self.wildcardMatches(remaining[1:], node.children[c], prefix+c, matches, invalidPositions, remainingLetters)

        elif remaining[0] in node.children:
            self.wildcardMatches(remaining[1:], node.children[remaining[0]], prefix+remaining[0], matches, invalidPositions, unusedLetters)

        print(f"query = {remaining} prefix = {prefix} \nmatches = {matches}\nreturning")
        return matches

    """ Test Methods """
    def AllWordsAreReadTest(self) -> bool:
        allWords = set(self.getAllWords())

        with open(self.filename, 'r') as f:
            [allWords.remove(line.strip()) for line in f]

        return not allWords

    def WildcardResultsAreUnique(self) -> bool:
        trie.alphabet = "chbamoe"
        results = self.wildcardMatches("*c*")
        print(len(set(results)))
        print(len(results))
        print(results)
        return len(set(results)) == len(results)


if __name__ == "__main__":
    trie = Trie(forWordle = True)
    # print(trie.AllWordsAreReadTest())
    # print(trie.WildcardResultsAreUnique())
