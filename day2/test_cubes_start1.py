
import re
from functools import reduce 

cubes_pattern = re.compile(' ([0-9]+) (blue|green|red)')

def parse_cubes(cubes) -> (int, str):
    cubes_values = cubes_pattern.search(cubes)
    return (int(cubes_values.group(1)), cubes_values.group(2))

def is_valid_cube(value: int, color: str) -> bool:
    if color == 'blue':
        return value <= 14
    elif color == 'green':
        return value <= 13
    elif color == 'red':
        return value <= 12

def is_possible_round(play: str) -> bool:
    cubes_to_parse = play.split(',')
    cubes_parsed = map(lambda c: parse_cubes(c), cubes_to_parse)
    cubes_validity = map(lambda x: is_valid_cube(x[0], x[1]), cubes_parsed)
    return bool(reduce(lambda a, b: a and b, cubes_validity))

def is_possible_game(game: str) -> bool:
    game_rounds = game.split(';')
    rounds_validities = map(lambda r: is_possible_round(r), game_rounds)
    return bool(reduce(lambda a, b: a and b, rounds_validities))

def parse_game(game: str) -> int:
    game_data = game.split(':')
    if is_possible_game(game_data[1]):
        return int(game_data[0].split(' ')[1])
    else:
        return 0

def problem_solution_start_1() -> int:
    solution = 0
    with open('./day2/input') as advent_problem_input:
        for game in advent_problem_input:
            solution += parse_game(game)
    return solution

def get_max_color_values(game: str) -> dict:
    cubes_values = cubes_pattern.findall(game)
    max_values = {}
    for v, color in cubes_values:
        if color in max_values:
            max_values[color] = max(max_values[color], int(v))
        else:
            max_values[color] = int(v)
    return max_values

def get_game_power(colors_max: dict) -> int:
    result = 1
    for color in colors_max:
        result *= colors_max[color]
    return result

def problem_solution_start_2() -> int:
    solution = 0
    with open('./day2/input') as advent_problem_input:
        for game in advent_problem_input:
            solution += get_game_power(get_max_color_values(game))
    return solution

############### TEST CASES ################        

def test_get_max_color_values():
    max_values = get_max_color_values('Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red')
    assert max_values['red'] == 20
    assert max_values['green'] == 13
    assert max_values['blue'] == 6

def test_game_power():
    max_colors = {
        'blue' : 6,
        'red'  : 20,
        'green': 13
    }
    assert 1560 == get_game_power(max_colors)

def test_parse_cubes1():
    n_cubes, color = parse_cubes(' 3 blue')
    assert n_cubes == 3
    assert color == 'blue'

def test_parse_cubes2():
    n_cubes, color = parse_cubes(' 12 red')
    assert n_cubes == 12    
    assert color == 'red'

def test_parse_cubes3():
    n_cubes, color = parse_cubes(' 17 green')
    assert n_cubes == 17
    assert color == 'green'

def test_parse_play_invalid():
    assert not is_possible_round(' 1 red, 16 green, 2 blue')

def test_parse_play_valid():
    assert is_possible_round(' 1 red, 3 green, 2 blue')
    
def test_valid_cube_red():
    assert is_valid_cube(12, 'red')

def test_invalid_red():
    assert not is_valid_cube(13, 'red')

def test_valid_green():
    assert is_valid_cube(13, 'green')

def test_invalid_green():
    assert not is_valid_cube(14, 'green')

def test_valid_blue():
    assert is_valid_cube(14, 'blue')

def test_invalid_blue():
    assert not is_valid_cube(15, 'blue')

def test_is_possible_game_true():
    assert is_possible_game(' 3 blue, 2 green, 6 red; 10 green, 4 red, 8 blue; 2 red, 1 green, 10 blue; 1 blue, 5 green')

def test_is_possible_game_false():
    assert not is_possible_game(' 3 blue, 2 green, 6 red; 17 green, 4 red, 8 blue; 2 red, 1 green, 10 blue; 1 blue, 5 green')

def test_parse_game_possible():
    assert 87 == parse_game('Game 87: 2 red, 4 green, 2 blue; 2 blue, 6 green; 2 red, 3 blue, 3 green; 1 red, 4 green; 1 green, 2 blue, 2 red; 4 blue, 4 green')

def test_parse_game_impossible():
    assert 0 == parse_game('Game 93: 2 blue, 1 red, 3 green; 10 blue, 1 red, 10 green; 11 blue, 16 green, 4 red; 2 green, 20 blue, 7 red; 11 green, 8 red, 15 blue; 9 green, 10 blue, 1 red')

def test_advent_day2_solution_start_1():
    assert 2727 == problem_solution_start_1()

def test_advent_day2_solution_start_2():
    assert 56580 == problem_solution_start_2()