import numpy as np
import re
from io import StringIO

def num_has_adjacent_num(engine: np.array, engine_side: int, i: int, min_j: int, max_j: int) -> bool:

    gears_coordinates = None
    i_minus_1 = i if i - 1 < 0 else i - 1
    i_plus_2 = i + 1 if i + 2 > engine_side else i + 2
    j_minus_1 = min_j if min_j - 1 < 0 else min_j - 1
    j_plus_1 = max_j + 1 if max_j + 2 > engine_side else max_j + 2

    for i_prima in range(i_minus_1, i_plus_2):
        for j_prima in range(j_minus_1, j_plus_1):
            position = engine[i_prima][j_prima]
            if not (position == '.' or position.isnumeric()) : 
                if position == '*':
                    gears_coordinates = (i_prima, j_prima)
                return True, gears_coordinates
    return False, gears_coordinates


def sum_engine_schematic(engine: np.array):
    f = open('/tmp/wrong.txt', mode='w') 
    engine_side = engine.shape[0]
    in_digit = False
    digits = ''
    engine_schematic_sum = 0
    for i in range(engine_side):
        for j in range(engine_side):
            if not in_digit and engine[i][j].isnumeric():
                in_digit = True
                min_j = j
                digits += engine[i][j]
            elif in_digit and engine[i][j].isnumeric():
                digits += engine[i][j]

            if in_digit and (not engine[i][j].isnumeric() or j == engine_side -1):
                max_j = j - 1
                in_digit = False
                digits_int = int(digits)
                is_adjacent, gear_coordinates = num_has_adjacent_num(engine, engine_side, i, min_j, max_j)
                if is_adjacent:
                    engine_schematic_sum += digits_int
                    print(digits, file=f)
                digits = ''
    f.close()
    return engine_schematic_sum



############### TEST CASES ################        

engine_text = StringIO(
'''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..''')

engine = np.loadtxt(engine_text, dtype='str', comments='|')

def test_sum_engine_schematic():
    assert 4361 == sum_engine_schematic(engine)

def test_top_left_is_number():
    is_adjacent, gear_coordinates = num_has_adjacent_num(engine, 10, 0, 0, 2)
    assert is_adjacent
    assert gear_coordinates == (1,3)

def test_top_right_is_not_number():
    is_adjacent, gear_coordinates = num_has_adjacent_num(engine, 10, 0, 5, 7)
    assert not is_adjacent
    assert gear_coordinates is None

def test_middle_right_is_not_number():
    is_adjacent, gear_coordinates = num_has_adjacent_num(engine, 10, 5, 7, 8)
    assert not is_adjacent
    assert gear_coordinates is None

def test_middle_right_is_number_plus_gear():
    is_adjacent, gear_coordinates = num_has_adjacent_num(engine, 10, 2, 2, 4)
    assert is_adjacent
    assert gear_coordinates == (1, 3)

def test_sum_engine_example():
    engine_example_text = StringIO(
'''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..''')
    engine_example = np.loadtxt(engine_example_text, dtype='str', comments='|')
    assert 4361 == sum_engine_schematic(engine_example)

def test_sum_engine_star1():
    with open('./day3/input') as advent_problem_input:
        engine_star1 = np.loadtxt(advent_problem_input, dtype='str', comments='|')
        assert 551094 == sum_engine_schematic(engine_star1)
        
def test_num_has_adjacent_num_case1():
    case_text = StringIO('''.....
./764
.....
.....
.....''')
    engine_case = np.loadtxt(case_text, dtype='str', comments='|')
    #assert not num_has_adjacent_num(engine_case, 19, 1, 3, 6)
    assert 764 == sum_engine_schematic(engine_case)
