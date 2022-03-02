from turtle import color

from numpy import rec
import solver
import os
#Program Constants
PATH_GUESSES = "Resources/allowed_guesses.txt"
PATH_ANSWERS = "Resources/possible_answers.txt"
DEBUG = True
BAR_LENGTH = 50
# Game Constants
MAX_TRIES = 6
WORD_SIZE = 5
MISSED = "🟨"
ABSENT = "⬛"
CORRECT = "🟩"
SOLVED = [2] * WORD_SIZE
GREY = "\u001b[30;1m"
YELLOW = "\u001b[33m"
GREEN = "\u001b[32m"
COLOR_END = "\u001b[0m"

def loadGuesses():
    guesses = []
    with open(PATH_GUESSES, "r") as f:
        for line in f.readlines():
            guesses.append(line.strip())
    return guesses

def loadAnswers():
    answers = []
    with open(PATH_ANSWERS, "r") as f:
        for line in f.readlines():
            answers.append(line.strip())
    return answers

def patternToString(pattern):
    """Convert a pattern to text
    0 - Not in word
    1 - In word but misplaced
    2 - Same position
    """
    txt = ""
    for element in pattern:
        if (element == 0):
            txt += ABSENT
        elif (element == 1):
            txt += MISSED
        else:
            txt += CORRECT
    txt += "\n"
    return txt

def coloredGuess(guess, pattern):
    """Return a string containg each character in guess color-coded to match the pattern"""
    colored = ""

    for i in range(WORD_SIZE):
        # Add the color-coded letter
        if (pattern[i] == 2):
            colored += GREEN + guess[i]
        elif (pattern[i] == 1):
            colored += YELLOW + guess[i]
        else:
            colored += GREY + guess[i]
        # Add a spacer
        if (i < WORD_SIZE - 1):
            colored += " "
    colored += COLOR_END + "\n"

    return colored

def displayBar(partial, total):
    """Print a percent completion bar to the terminal"""
    percent = (partial / total) * 100
    filled = int((BAR_LENGTH * partial) / total)
    bar = "[" + "=" * filled + "-" * (BAR_LENGTH - filled) + "]"
    print("{0} {1:0.1f}% {2}/{3}".format(bar, percent, partial, total))

def analyzeHistogram(data):
    """Print the defining characteristics of a histogram to the terminal"""
    # Determine the mean of the histogram
    total = 0
    frequency = 0

    for i in range(len(data)):
        total += data[i]
        frequency += data[i] * (i+1)

    mean = frequency / total

    print("Algorithim finished with an average score of {0:0.3f}.".format(mean))
    # Display the histogram in the terminal
    for i in range(len(data)):
        displayBar(data[i], total)

def bestFirstGuess(valid_answers):
    """Returns the word with the highest expected information for the first guess"""
    best_guess = None
    best_info = 0
    for i, guess in enumerate(valid_answers):
        info = solver.expectedInformation(guess, valid_answers)
        # Replace the best guess if our expected information is higher
        if (info > best_info):
            best_guess = guess
            best_info = info
        if DEBUG:
            os.system("cls")
            print("Guess: {0} Best Guess: {1} E[I]: {2:0.2f}".format(guess, best_guess, best_info))
            displayBar(i + 1, len(valid_answers))
    return best_guess
    
def simulateGames(valid_answers, first_guess = None):
    """
    Return the distribution of the # of tries it takes the algorithim to solve n games.
    valid_guesses: List of allowed guesses. 
    valid_answers: List of answers to all possible Wordle games.
    first_guess: First word to guess for all games. If None, calculates best first guess.
    """
    # If the first guess is not provided, calculate the optimal first guess.
    if (first_guess == None):
        first_guess = bestFirstGuess(valid_answers)

    scores = [0] * (MAX_TRIES + 1)
    for i, answer in enumerate(valid_answers):
        # Initialize answer specific values
        remaining_answers = valid_answers
        score = 0
        pattern = [0] * WORD_SIZE

        # Make first guess
        guesses = [first_guess]
        pattern = solver.generatePattern(first_guess, answer)
        patterns = patternToString(pattern)

        # Update the list of valid guesses based on the pattern
        remaining_answers = solver.patternDistribution(first_guess, remaining_answers)[str(pattern)]

        # If our guess was not the solution, calculate a new guess
        while (score < MAX_TRIES and pattern != SOLVED):
            # Find the guess with the highest expected information
            best_guess = None
            best_info = 0
            for guess in remaining_answers:
                info = solver.expectedInformation(guess, remaining_answers)

                # Replace the best guess if our expected information is higher
                if (info > best_info):
                    best_guess = guess
                    best_info = info
            
            # Make the guess and find the resulting pattern
            guesses.append(best_guess)
            pattern = solver.generatePattern(best_guess, answer)
            patterns += patternToString(pattern)
            score += 1

            # Update the list of valid guesses based on the pattern
            remaining_answers = solver.patternDistribution(best_guess, remaining_answers)[str(pattern)]

            if DEBUG:
                os.system("cls")
                print("Score: ", score)
                print("Answer:", answer)
                print("Guesses:", guesses)
                print(patterns)
                print("Distribution:", scores)
                displayBar(i + 1, len(valid_answers))
        scores[score] += 1

    return scores

def input2pattern(prompt):
    """
    Obtain and convert user input into a pattern
    Ex: '00121' -> [0, 0, 1, 2, 1]
    """
    
    user_pattern = input(prompt)
    while (len(user_pattern) != WORD_SIZE):
        print("Invalid input.")
        user_pattern = input(prompt)
    
    pattern = [int(char) for char in user_pattern]

    return pattern


def solveGame(valid_guesses, valid_answers, first_guess = None):
    """Reccomend guesses to the user based off of inputted patterns"""
    # Game-specific variables
    colored_guesses = ""
    tries = 1

    # Recommend a guess
    if (first_guess == None):
        rec_guess = bestFirstGuess(valid_answers)
    else:
        rec_guess = first_guess
    
    info = solver.expectedInformation(rec_guess, valid_answers)
    print("Reccomended guess: {0} E[I]: {1:0.2f}".format(rec_guess, info))

    # Obtain the actual guess and pattern
    guess = input("Guess made: ")
    pattern = input2pattern("Pattern recieved: ")

    colored_guesses += coloredGuess(guess.upper(), pattern)

    # Update the list of valid guesses based on the pattern
    remaining_answers = solver.patternDistribution(guess, valid_answers)[str(pattern)]

    while (tries < MAX_TRIES and pattern != SOLVED):
    # Find the guess with the highest expected information
            rec_guesses = [None] * 5
            rec_info = [0] * 5
            for guess in remaining_answers:
                info = solver.expectedInformation(guess, remaining_answers)
                for i in range(len(rec_info)):
                    # If this is a better guess, insert and shift over the other guesses
                    if info > rec_info[i]:
                        rec_guesses.insert(i, guess)
                        del rec_guesses[-1]

                        rec_info.insert(i, info)
                        del rec_info[-1]

                        # Avoid multiple insertions of the same guess
                        break

            os.system("cls")
            # Print all guesses so far
            print(colored_guesses)

            
            print("Reccomended guesses: ")
            for i in range(len(rec_guesses)):
                if rec_guesses[i]:
                    print("{0} E[I]: {1:0.2f}".format(rec_guesses[i], rec_info[i]))

            # Obtain the actual guess and pattern
            guess = input("Guess made: ").lower()
            pattern = input2pattern("Pattern recieved: ")

            colored_guesses += coloredGuess(guess.upper(), pattern)
            tries += 1

            # Update the list of valid guesses based on the pattern
            if (guess in remaining_answers):
                remaining_answers = solver.patternDistribution(guess, remaining_answers)[str(pattern)]
            else:
                temp_answers = solver.patternDistribution(guess, valid_guesses)[str(pattern)]

                # Cull remaining answers not in temp_answers
                for answer in remaining_answers:
                    if answer not in temp_answers:
                        remaining_answers.remove(answer)

    if (pattern == SOLVED):
        os.system("cls")
        print(colored_guesses)
        print("Game solved in {0} tries, the word was {1}!".format(tries, guess))
    else:
        os.system("cls")
        print(colored_guesses)
        print("Ran out of tries.")
        

def main():
    # Load necessary files
    valid_guesses = loadGuesses()
    valid_answers = loadAnswers()

    
    # Simulate all games with an initial guess of "raise"
    #scores = simulateGames(valid_answers, "raise")
    #os.system("cls")
    # Analyze the resulting score distribution
    #analyzeHistogram(scores)

    solveGame(valid_guesses, valid_answers, "raise")



if __name__ == "__main__":
    main()