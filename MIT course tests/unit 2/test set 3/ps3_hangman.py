# Hangman game
#

# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)

import random
import string

WORDLIST_FILENAME = "words.txt"


def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    # need to check just same letters, easy and shorted with a set difference
    still_missing_letters = set(secretWord) - set(lettersGuessed)
    return False if still_missing_letters else True


def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    '''
    so_far_list = []
    for letter in secretWord:
        char = letter if letter in lettersGuessed else "_ "
        so_far_list.append(char)
    return "".join(so_far_list)


def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    # using set again, rather than a loop
    available_letters_list = sorted(list(set(string.ascii_lowercase) - set(lettersGuessed)))
    return "".join(available_letters_list)



def hangman(secretWord):
    '''
    secretWord: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secretWord contains.

    * Ask the user to supply one guess (i.e. letter) per round.

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computers word.

    * After each round, you should also display to the user the 
      partially guessed word so far, as well as letters that the 
      user has not yet guessed.

    Follows the other limitations detailed in the problem write-up.

    A user is allowed 8 guesses [correct ones do not decrease the number left!]. Make sure to remind the user of how many guesses
    s/he has left after each round. Assume that players will only ever submit one character at a time (A-Z).

    A user loses a guess only when s/he guesses incorrectly.

    If the user guesses the same letter twice, do not take away a guess - instead, print a message letting them know
    they've already guessed that letter and ask them to try again.

    The game should end when the user constructs the full word or runs out of guesses. If the player runs out of guesses (s/he "loses"), reveal the word to the user when the game ends.
    '''
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is {} letters long.".format(len(secretWord)))
    guesses_no, lettersGuessed = 8, []
    while guesses_no > 0:

        print("------------")

        print("You have {} guesses left.".format(guesses_no))
        print("Available letters: {}".format(getAvailableLetters(lettersGuessed)))
        letter = input("Please guess a letter: ")

        if letter in lettersGuessed:
            print("Oops! You've already guessed that letter:", getGuessedWord(secretWord, lettersGuessed))
            continue

        lettersGuessed.append(letter)
        if letter not in secretWord:
            print("Oops! That letter is not in my word:", getGuessedWord(secretWord, lettersGuessed))
            guesses_no -= 1
        else:
            print("Good guess:", getGuessedWord(secretWord, lettersGuessed))

        # check if word has been guessed
        if isWordGuessed(secretWord, lettersGuessed):
            print("------------")
            print("Congratulations, you won!")
            break

    if guesses_no == 0:
        print("------------")
        print("Sorry, you ran out of guesses. The word was {}.".format(secretWord))


if __name__ == "__main__":

    # # test 1
    # print(isWordGuessed("apple", ['a', 'p', 'l', 'e']))  # expected: True
    # print(isWordGuessed("apple", ['a', 'p', 'l', 'd']))  # expected: False

    # # test 2
    # secretWord = 'apple'
    # lettersGuessed = ['e', 'i', 'k', 'p', 'r', 's']
    # print(getGuessedWord(secretWord, lettersGuessed))  # expected: '_ pp_ e'

    # # test 3
    # lettersGuessed = ['e', 'i', 'k', 'p', 'r', 's']
    # print(getAvailableLetters(lettersGuessed))  #  expected: abcdfghjlmnoqtuvwxyz

    # When you've completed your hangman function, uncomment these two lines
    # and run this file to test! (hint: you might want to pick your own
    # secretWord while you're testing)
    # secretWord while you're testing)
    secretWord = 'else'  # chooseWord(wordlist).lower()
    hangman(secretWord)
