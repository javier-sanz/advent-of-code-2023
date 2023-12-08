from functools import reduce 

def race_combination(time_pressing_button: int, time: int):
    return (time - time_pressing_button) * time_pressing_button

def race_winning_options(time:int, record_distance:int):
    combinations = map(lambda x: race_combination(x, time), range(1, time))
    return list(filter(lambda x: x > record_distance, combinations))

def race_records_options(races: list):
    return reduce(lambda a, b: a * b, map(lambda x: len(race_winning_options(x[0], x[1])), races))

############### TEST CASES ################        

def test_race_combination_case1():
    assert 10 == race_combination(2, 7)

def test_race_combination_case2():
    assert 12 == race_combination(3, 7)

def test_race_winning_options_case1():
    assert [10, 12, 12, 10] == race_winning_options(7, 9)

def test_race_records_options_example():
    assert 288 == race_records_options([(7, 9), (15, 40), (30, 200)])

def test_race_records_options_example():
    assert 288 == race_records_options([(7, 9), (15, 40), (30, 200)])

def test_race_records_options_star1():
    assert 316800 == race_records_options([(61, 430), (67, 1036), (75, 1307), (71, 1150)])

def test_start2():
    # see https://www.wolframalpha.com/input?i=%28+61677571-y%29+*y%3C430103613071150 
    import math 
    assert 45647654 == int(round(1/2*(61677571 + math.sqrt(2083708312175441)) - 1/2*(61677571 - math.sqrt(2083708312175441))))
