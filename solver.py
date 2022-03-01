import math


WORD_SIZE = 5


def generatePattern(word, answer):
    """
    Generate the resulting pattern from guessing 'word' for 'answer'
    0 - ABSENT
    1 - MISSED
    2 - CORRECT
    """
    # Generate an empty starting pattern
    pattern = [0] * WORD_SIZE

    # Generate array copy of answer for its mutability
    answer_arr = []
    for i in range(WORD_SIZE):
        answer_arr.append(answer[i])

    # First pass - Green
    for i in range(WORD_SIZE):
        if (word[i] == answer[i]):
            pattern[i] = 2
            # Remove match to prevent double-counting in second pass
            answer_arr[i] = None
    
    #Second pass - Yellow
    for i in range(WORD_SIZE):
        if (word[i] in answer_arr and pattern[i] == 0):
            pattern[i] = 1
            # Remove match to prevent double-counting
            answer_arr.remove(word[i])
    return pattern

def patternDistribution(guess, valid_answers):
    """
    Generate all possible answers for each pattern resulting from making a guess
    """
    pattern_distribution = {}
    for answer in valid_answers:
        pattern = generatePattern(guess, answer)
        temp_t = str(pattern)
        if temp_t in pattern_distribution:
            pattern_distribution[temp_t].append(answer)
        else:
            pattern_distribution[temp_t] = [answer]
    return pattern_distribution

def patternNumDistribution(guess, valid_guesses):
    """
    Generate the number of possible answers for all patterns resulting from making a guess
    """
    pattern_distribution = {}
    for answer in valid_guesses:
        pattern = generatePattern(guess, answer)
        temp_t = str(pattern)
        if temp_t in pattern_distribution:
            pattern_distribution[temp_t] += 1
        else:
            pattern_distribution[temp_t] = 1
    return pattern_distribution

def expectedInformation(word, valid_answers):
    """Assuming a uniform distribution(not actually present), return the expected information(in bits) of word"""
    # Calculate the # of matches for each pattern
    match_distribution = patternNumDistribution(word, valid_answers)
    
    # Calculate the information of each pattern
    total_guesses = len(valid_answers) * 1.0

    expected_info = 0.0
    for num_matches in match_distribution.values():
        p = num_matches/total_guesses
        if p == 0:
            i = 0
        elif p == 1:
            i = 1
        else:
            i = -math.log2(p)
        expected_info += p * i
    return expected_info   


if __name__ == "__main__":
    print("solver.py ran directly, intended use as a module.")