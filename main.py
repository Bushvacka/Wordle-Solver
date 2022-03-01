import solver
import os
#Program Constants
PATH_GUESSES = "Resources/allowed_guesses.txt"
PATH_ANSWERS = "Resources/possible_answers.txt"
DEBUG = True
BAR_LENGTH = 40
# Game Constants
MAX_TRIES = 6
WORD_SIZE = 5
MISSED = "🟨"
ABSENT = "⬛"
CORRECT = "🟩"
SOLVED = [2] * WORD_SIZE

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
    """Convert a pattern to text"""
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

def displayBar(partial, total):
    """Print a percent completion bar to the terminal"""
    percent = (partial / total) * 100
    filled = int((BAR_LENGTH * partial) / total)
    bar = "[" + "=" * filled + "-" * (BAR_LENGTH - filled) + "]"
    print("{0} {1:0.1f}% {2}/{3}".format(bar, percent, partial, total))

def bestFirstGuess(valid_guesses, valid_answers):
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

    
def simulateGames(valid_guesses, valid_answers, first_guess = None):
    """
    Return the distribution of the # of tries it takes the algorithim to solve n games.
    valid_guesses: List of allowed guesses. 
    valid_answers: List of answers to all possible Wordle games.
    first_guess: First word to guess for all games. If None, calculates best first guess.
    """
    # If the first guess is not provided, calculate the optimal first guess.
    if (first_guess == None):
        first_guess = bestFirstGuess(valid_guesses, valid_answers)

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



def main():
    # Load necessary files
    valid_guesses = loadGuesses()
    valid_answers = loadAnswers()

    # Simulate all games with an initial guess of "raise"
    simulateGames(valid_guesses, valid_answers, "raise")

    input("Press any key to exit")



if __name__ == "__main__":
    main()