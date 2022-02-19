import solver

PATH_GUESSES = "Resources/allowed_guesses.txt"
PATH_ANSWERS = "Resources/possible_answers.txt"
MAX_TRIES = 6
WORD_SIZE = 5
ABSENT = "⬛"
MISSED = "🟨"
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

def simulateGames(valid_guesses, valid_answers):
    """
    Return the distribution of the # of tries it takes the algorithim to solve n games.
    valid_guesses: List of allowed guesses. 
    valid_answers: List of answers to all possible Wordle games.
    n: Number of games to simulate. Runs through all possible games by default.
    """
    scores = [0] * MAX_TRIES
    for answer in valid_answers:
        # Answer specific
        guesses = valid_guesses
        tries = 0
        pattern = [0] * WORD_SIZE
        while (tries < MAX_TRIES and pattern != SOLVED):
            # 
            info_distribution = solver.uExpectedInformationDistribution(guesses)
            guess = max(info_distribution, key=info_distribution.get)
            pattern = solver.generatePattern(guess, answer)
            if (pattern == SOLVED):
                scores[tries] += 1
            guesses = solver.uMatchDistribution(guess, guesses)[str(pattern)]
            tries += 1



def main():
    # Load files
    valid_guesses = loadGuesses()
    valid_answers = loadAnswers()
    simulateGames(valid_guesses, valid_answers)



if __name__ == "__main__":

    main()