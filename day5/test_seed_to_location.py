import re
import portion as P

from io import StringIO
from functools import reduce 

def source_to_dest_map_line(elem_id: int, dest_range: int, source_range: int, range_len: int) -> int:
    if elem_id >= source_range and elem_id < source_range + range_len:
        return dest_range +  elem_id - source_range
    return None

def source_to_dest_map(elem_map: list, elem_id: int) -> int:
    for elem_map_line in elem_map:
        possible_dest = source_to_dest_map_line(elem_id, elem_map_line[0], elem_map_line[1], elem_map_line[2])
        if possible_dest:
            return possible_dest
    return elem_id

def parse_input(input) -> list:
    number_pattern = re.compile('(\d+)')
    seeds_line = input.readline()
    seeds = list(map(lambda x: int(x), number_pattern.findall(seeds_line)))
    elem_to_elem_maps = []
    i = -1
    for line in input:
        if len(line) > 1:
            if line[0].isdigit():
                elem_to_elem_maps[i].append(list(map(lambda x: int(x), number_pattern.findall(line))))
            else:
                i += 1
                elem_to_elem_maps.append([])
    return seeds, elem_to_elem_maps     

def get_lowest_location(input, expand=(lambda x: x)) -> int:
    seeds, elem_to_elem_maps = parse_input(input)
    source_dest = expand(seeds)
    for elem_to_elem_map in elem_to_elem_maps:
        source_dest = list(map(lambda x: source_to_dest_map(elem_to_elem_map, x), source_dest))
    return min(source_dest)

def expand_seeds(input_seeds) -> list:
    expanded_seeds = []
    for i in range(0, len(input_seeds), 2):
        expanded_seed = []
        for j in range(input_seeds[i], input_seeds[i] + input_seeds[i + 1]):
            expanded_seed.append(j)
        expanded_seeds.append(expanded_seed)
    return reduce(lambda x, y: x + y, expanded_seeds, [])

def get_expanded_lowest_location(input) -> int:
    return get_lowest_location(input, expand_seeds)

############## Efficient solution to second problem #############

def expand_seeds_ranges(input_seeds) -> list:
    expanded_seeds = []
    for i in range(0, len(input_seeds), 2):
        expanded_seeds.append(P.openclosed(input_seeds[i], input_seeds[i] + input_seeds[i + 1]))
    return expanded_seeds

def source_to_dest_map_line_ranges(elem_interval: P.interval, 
                                   dest_range: int, source_range: int, range_len: int):
    map_interval = P.openclosed(source_range, source_range + range_len)
    intersection = elem_interval & map_interval
    if not intersection.empty:
        return P.openclosed(dest_range +  intersection.lower - source_range, 
                            dest_range +  intersection.upper - source_range),\
                            elem_interval - map_interval
    return P.empty(), elem_interval

def source_to_dest_map_ranges(elem_map: list, elem_interval: P.interval) -> P.interval:
    dest_intersections =[]
    remaining_interval = elem_interval
    for elem_map_line in elem_map:
        dest_intersection, remaining_interval = \
            source_to_dest_map_line_ranges(remaining_interval, 
                                           elem_map_line[0], 
                                           elem_map_line[1], 
                                           elem_map_line[2])
        dest_intersections.append(dest_intersection)
    return reduce(lambda a, b: a | b, dest_intersections, remaining_interval)

def get_lowest_location_with_ranges(input) -> int:
    seeds, elem_to_elem_maps = parse_input(input)
    source_dest = expand_seeds_ranges(seeds)
    for elem_to_elem_map in elem_to_elem_maps:
        source_dest = list(map(lambda x: source_to_dest_map_ranges(elem_to_elem_map, x), source_dest))
    return min(min(source_dest)).lower

############### TEST CASES ################        

def test_source_to_dest_map_line_case1():
    assert 53 == source_to_dest_map_line(51, 52, 50 , 48)

def test_source_to_dest_map_line_case2():
    assert not source_to_dest_map_line(48, 52, 50 , 48)

def test_source_to_dest_map_line_case3():
    assert 99 == source_to_dest_map_line(97, 52, 50 , 48)

def test_source_to_dest_map_line_case4():
    assert not source_to_dest_map_line(98, 52, 50 , 48)

def test_source_to_dest_map_case1():
    assert 81 == source_to_dest_map([(50, 98, 2), (52, 50, 48)], 79)

def test_source_to_dest_map_case2():
    assert 14 == source_to_dest_map([(50, 98, 2), (52, 50, 48)], 14)

def test_source_to_dest_map_case3():
    assert 51 == source_to_dest_map([(50, 98, 2), (52, 50, 48)], 99)

map_example_text = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''

def test_get_seeds_from_input():
    mem_input = StringIO(map_example_text)
    seeds, mapping = parse_input(mem_input)
    assert [79, 14, 55, 13] == seeds
    assert [[50, 98, 2], [52, 50, 48]] == mapping[0]
    assert [0, 15, 37] == mapping[1][0]

def test_get_lowest_location():
    mem_input = StringIO(map_example_text)
    assert 35 == get_lowest_location(mem_input)

def test_start1():
    with open('./day5/input') as advent_problem_input:
        assert 226172555 == get_lowest_location(advent_problem_input)
         
def test_expanded_seeds():
    expanded_seeds = expand_seeds([79, 14, 55, 13])
    assert 92 == expanded_seeds[13]
    assert 55 == expanded_seeds[14]
    assert 67 == expanded_seeds[-1]

def test_get_lowest_location_expanded():
    mem_input = StringIO(map_example_text)
    assert 46 == get_expanded_lowest_location(mem_input)

# Never ends XD
def _test_start2():
    with open('./day5/input') as advent_problem_input:
        assert 226172555 == get_expanded_lowest_location(advent_problem_input)

def test_get_lowest_location_expanded_ranges():
    assert [P.openclosed(79, 93), P.openclosed(55, 68)] == expand_seeds_ranges([79, 14, 55, 13])   

def test_source_to_dest_map_line_ranges_case1():
    intersection, remaining = source_to_dest_map_line_ranges(P.openclosed(79, 93), 52, 50 , 48)
    assert P.openclosed(81, 95) == intersection
    assert remaining.empty

def test_source_to_dest_map_line_ranges_case2():
    intersection, remaining = source_to_dest_map_line_ranges(P.openclosed(79, 93), 50, 98 , 2)
    assert intersection.empty
    assert remaining == P.openclosed(79, 93)

def test_source_to_dest_map_line_ranges_case3():
    intersection, remaining = source_to_dest_map_line_ranges(P.openclosed(79, 93), 52, 80 , 10)
    assert P.openclosed(52, 62) == intersection
    assert  P.openclosed(79, 80) |  P.openclosed(90, 93) == remaining
    
def test_source_to_dest_map_ranges_case1():
    assert P.openclosed(81,95) == source_to_dest_map_ranges([(50, 98, 2), (52, 50, 48)], P.openclosed(79, 93))

def test_source_to_dest_map_ranges_case2():
    assert P.openclosed(57, 70) == source_to_dest_map_ranges([(50, 98, 2), (52, 50, 48)], P.openclosed(55, 68))

def test_source_to_dest_map_ranges_case3():
    assert P.openclosed(40,50) | P.openclosed(52,70)== source_to_dest_map_ranges([(50, 98, 2), (52, 50, 48)], P.openclosed(40, 68))

def test_get_lowest_location_with_ranges():
    mem_input = StringIO(map_example_text)
    assert 46 == get_lowest_location_with_ranges(mem_input)

def test_efficient_start2():
    with open('./day5/input') as advent_problem_input:
        assert 47909639 == get_lowest_location_with_ranges(advent_problem_input)