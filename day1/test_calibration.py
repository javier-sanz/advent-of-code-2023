import re
from functools import reduce 

digit_pattern = re.compile('([0-9])')

digit_number_table ={
    "one":"1",
    "two":"2",
    "three":"3",
    "four":"4",
    "five":"5",
    "six":"6",
    "seven":"7",
    "eight":"8",
    "nine":"9",
}

def digit_name_to_number(digit):
    if digit in digit_number_table:
        return digit_number_table[digit]
    return digit

def get_digits_from_line(line: str):
    return digit_pattern.findall(line)

def get_digits_and_name_from_line(line: str):
    digits = []
    for i in range(len(line)):
        for x in digit_number_table:
            if line[i].isdigit():
                digits.append(line[i])
                continue

            if x == line[i:i+len(x)]:
                digits.append(x)
    return digits
    
def get_calibration_digit(line: str, get_digits_func):
    all_digits = get_digits_func(line)
    calibration_digits = 0
    if len(all_digits) > 0 :
        digits = digit_name_to_number(all_digits[0])
        if len(all_digits) > 1:
            digits += digit_name_to_number(all_digits[-1])
        else :
            digits += digits
        calibration_digits = int(digits)
    return calibration_digits

def sum_calibration_values(pattern):
    lines = []
    with open('./day1/input') as advent_problem_input:
        lines = advent_problem_input.read().split('\n')
    calibration_numbers = list(map(lambda x: get_calibration_digit(x, pattern), lines))
    return reduce(lambda a, b: a + b, calibration_numbers)

############### TEST CASES ################        

def test_digit_to_number_names():
    for number_name in digit_number_table:
        assert digit_name_to_number(number_name) == digit_number_table[number_name]

def test_digit_to_number_number():
    assert digit_name_to_number("4") == "4"

def test_calibration_digit_no_digit():
    assert get_calibration_digit('foo', get_digits_and_name_from_line) == 0

def test_calibration_digit_no_empty():
    assert get_calibration_digit('', get_digits_and_name_from_line) == 0

def test_calibration_only_digit_but_digit_name():
    assert get_calibration_digit("none", get_digits_from_line) == 0

def test_calibration_only_digit_digit_name():
    assert get_calibration_digit("1n2one", get_digits_from_line) == 12

def test_calibration_one_digit_name():
    assert get_calibration_digit("none", get_digits_and_name_from_line) == 11

def test_calibration_one_digit():
    assert get_calibration_digit("1", get_digits_and_name_from_line) == 11

def test_calibration_one_case_1():
    assert get_calibration_digit("ninevgvrhtsrrnbnxg2fourvlqkdqxxqcmfqbbmx3", get_digits_and_name_from_line) == 93

def test_calibration_one_case_2():
    assert get_calibration_digit("sevenmqfkvscjj56", get_digits_and_name_from_line) == 76

def test_calibration_one_case_3():
    assert get_calibration_digit("six4onedhsevencngfntnsss8", get_digits_and_name_from_line) == 68

def test_calibration_one_case_4():
    assert get_calibration_digit("2342343", get_digits_and_name_from_line) == 23

def test_calibration_one_case_5():
    assert get_calibration_digit("eight3fiveninefivemtxm9eightwot", get_digits_and_name_from_line) == 82

def test_advent_day2_solution_start_1():
    assert 54630 == sum_calibration_values(get_digits_from_line)

def test_advent_day2_solution_start_2():
    assert 54770 == sum_calibration_values(get_digits_and_name_from_line)