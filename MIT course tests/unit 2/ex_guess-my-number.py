"""
You (the user) thinks of an integer between 0 (inclusive) and 100 (not inclusive).

The computer makes guesses, and you give it input - is its guess too high or too low? Using bisection search,
the computer will guess the user's secret number!

** Your program should use bisection search. So think carefully what that means.
What will the first guess always be? How should you calculate subsequent guesses?

** Your initial endpoints should be 0 and 100.
Do not optimize your subsequent endpoints by making them be the halfway point plus or minus 1.
Rather, just make them be the halfway point.

* Be sure to handle the case when the user's input is not one of h, l, or c.

Test case 1. Secret guess = 42
    Please think of a number between 0 and 100!
    Is your secret number 50?
    Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. h
    Is your secret number 25?
    Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. l
    Is your secret number 37?
    Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. l
    Is your secret number 43?
    Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. h
    Is your secret number 40?
    Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. l
    Is your secret number 41?
    Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. l
    Is your secret number 42?
    Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. c
    Game over. Your secret number was: 42

"""
MSG = "Enter 'h' to indicate the guess is too high. " \
      "Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. "
low, up, ans = 0, 100, "bah"

print("Please think of a number between 0 and 100!")

while ans != 'c':
    num = (low+up) // 2
    print("Is your secret number {}?".format(num))

    ans = input(MSG)
    if ans not in ('h', 'l', 'c'):
        print("Sorry, I did not understand your input.")
    else:
        if ans == 'l':
            low = num
        else:
            up = num

print("Game over. Your secret number was: {}:".format(num))
