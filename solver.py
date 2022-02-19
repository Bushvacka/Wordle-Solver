from distutils.log import info
import math
from re import I


WORD_SIZE = 5


def generatePattern(word, answer):
    """
    Generate the resulting pattern from guessing 'word' for 'answer'
    0 - ABSENT
    1 - MISSED
    2 - CORRECT
    """
    pattern = [0] * WORD_SIZE
    for i in range(WORD_SIZE):
        if (word[i] == answer[i]):
            pattern[i] = 2
        elif (word[i] in answer):
            pattern[i] = 1
        else:
            pattern[i] = 0
    return pattern

def uMatchDistribution(guess, valid_guesses):
    """
    Generate the possible answers for all patterns resulting from making a guess
    """
    match_distribution = {}
    for answer in valid_guesses:
        pattern = generatePattern(guess, answer)
        temp_t = str(pattern)
        if temp_t in match_distribution:
            match_distribution[temp_t].append(answer)
        else:
            match_distribution[temp_t] = [answer]
    return match_distribution

def uMatchNumDistribution(guess, valid_guesses):
    """
    Generate the number of possible answers for all patterns resulting from making a guess
    """
    match_distribution = {}
    for answer in valid_guesses:
        pattern = generatePattern(guess, answer)
        temp_t = str(pattern)
        if temp_t in match_distribution:
            match_distribution[temp_t] += 1
        else:
            match_distribution[temp_t] = 1
    return match_distribution

def uExpectedInformation(word, valid_guesses):
    """Assuming a uniform distribution(not actually present), return the expected information(in bits) of word"""
    # Calculate the # of matches for each pattern
    match_distribution = uMatchNumDistribution(word, valid_guesses)
    
    # Calculate the information of each pattern, return the average
    total_guesses = len(valid_guesses) * 1.0

    expected_info = 0.0
    for num_matches in match_distribution.values():
        p = num_matches/total_guesses
        i = math.log2(1/p)
        expected_info += p * i
    return expected_info

def uExpectedInformationDistribution(valid_guesses):
    info_distribution = {}
    for guess in valid_guesses:
        info_distribution[guess] = uExpectedInformation(guess, valid_guesses)
    return info_distribution
    


if __name__ == "__main__":
    print("solver.py ran directly, intended use as a module.")