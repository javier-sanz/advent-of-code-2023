import numpy as np

from io import StringIO
from functools import reduce 

def scoring_func_power2(played_won_numbers: set):
    return int(2 ** (len(played_won_numbers) - 1))

def score_scratchcards(line: str, scoring_func):
    card_numbers = line.split(':')[1].split('|')
    winning_numbers = set(filter(lambda x: x != '', card_numbers[0].split(" ")))
    played_numbers = set(filter(lambda x: x != '', card_numbers[1].split(" ")))
    # Intersection 
    played_won_numbers = winning_numbers & played_numbers
    return scoring_func(played_won_numbers)

def scratchcards_total_score(cards: list):
    individual_scores = map(lambda x: score_scratchcards(x, scoring_func_power2), cards)
    return reduce(lambda a, b: a + b, individual_scores)

def problem_solution_start_1() -> int:
    lines = []
    with open('./day4/input') as advent_problem_input:
        lines = advent_problem_input.read().split('\n')
    return scratchcards_total_score(lines)

def scoring_func_len(played_won_numbers: set):
    return len(played_won_numbers)

def scratchcards_copies(cards: list):
    individual_scores = map(lambda x: score_scratchcards(x, scoring_func_len), cards)
    return np.array(list(individual_scores))

def total_score_single_copies(cards_copies: np.array) -> int:
    total_copies = np.ones(cards_copies.shape, dtype='int')
    n_cards = cards_copies.shape[0]
    for i in range(n_cards):
        for j in range(1, cards_copies[i] + 1):
            index_to_add = i + j
            if index_to_add < n_cards:
                total_copies[index_to_add] += total_copies[i]
    return total_copies.sum()

def problem_solution_start_2() -> int:
    lines = []
    with open('./day4/input') as advent_problem_input:
        lines = advent_problem_input.read().split('\n')
    return total_score_single_copies(scratchcards_copies(lines))

############### TEST CASES ################        

def test_score_scratchcards_case_1():
    assert 8 == score_scratchcards('Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53', scoring_func_power2)

def test_score_scratchcards_case_2():
    assert 2 == score_scratchcards('Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1', scoring_func_power2)

def test_score_scratchcards_case_3():
    assert 1 == score_scratchcards('Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83', scoring_func_power2)

def test_score_scratchcards_case_4():
    assert 0 == score_scratchcards('Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36', scoring_func_power2)

def test_score_scratchcards_total_score_example():
    test_cards = StringIO(
'''Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11''')
    cards = []
    cards = test_cards.read().split('\n')
    assert 13 == scratchcards_total_score(cards)

def test_score_scratchcards_star1():
    assert 21105 == problem_solution_start_1()

def test_score_scratchcards_copies():
    test_cards = StringIO(
'''Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11''')
    cards = []
    cards = test_cards.read().split('\n')
    assert [4, 2, 2, 1, 0, 0] == scratchcards_copies(cards).tolist()

def test_total_score_single_copies():
    assert 30 == total_score_single_copies(np.asarray([4, 2, 2, 1, 0, 0]))

def test_total_score_single_copies_out_of_range():
    assert 30 == total_score_single_copies(np.asarray([4, 2, 2, 1, 0, 1]))

def test_total_score_single_copies_out_of_range2():
    assert 32 == total_score_single_copies(np.asarray([4, 2, 2, 1, 0, 1, 0]))

def test_score_scratchcards_star2():
    assert 5329815 == problem_solution_start_2()