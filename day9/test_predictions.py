import numpy as np
import pandas as pd

from io import StringIO

def forward_diff_func(vector: np.array):
    return np.ediff1d(vector)

def backwards_diff_func(vector: np.array):
    return np.ediff1d(vector)

def get_line_diff(line : np.array, diff_func, back=False):
    list_of_diffs = [line]
    current_diff = line
    while np.any(current_diff):
        current_diff = diff_func(current_diff)
        list_of_diffs.append(current_diff)

    predicted_diff = 0
    total_diffs = len(list_of_diffs)
    for i in range(total_diffs - 1, 0, -1):
        if not back:
            predicted_diff = list_of_diffs[i-1][-1] + predicted_diff 
        else:
            predicted_diff = list_of_diffs[i-1][0] - predicted_diff 
    return predicted_diff

def get_forward_prediction(df: pd.DataFrame):
    total_prediction = 0
    for index, row in df.iterrows():
        total_prediction += get_line_diff(np.array(row), forward_diff_func)
    return total_prediction

def get_backwards_predictions(df: pd.DataFrame):
    total_prediction = 0
    for index, row in df.iterrows():
        flipped_row = row #np.flip(np.array(row))
        total_prediction += get_line_diff(flipped_row, backwards_diff_func, back=True)
    return total_prediction

############### TEST CASES ################        

def test_get_line_diff_case1():
   assert 18 == get_line_diff(np.array([0, 3, 6, 9, 12, 15]), forward_diff_func)
        
def test_get_line_diff_case2():
   assert 28 == get_line_diff(np.array([1, 3, 6, 10, 15, 21]), forward_diff_func)

def test_get_line_diff_case3():
   assert 68 == get_line_diff(np.array([10, 13, 16, 21, 30, 45]), forward_diff_func)
   
def test_get_line_diff_backwards_case1():
   assert 5 == get_line_diff(np.array([10, 13, 16, 21, 30, 45]), backwards_diff_func,
                              True)

def test_star1():
    df_input = pd.read_csv('day9/input', header=None, sep=' ')
    assert 1666172641 == get_forward_prediction(df_input)

def test_backwards_prediction_example():
    map_example_text = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''
    mem_input = StringIO(map_example_text)
    df_input = pd.read_csv(mem_input, header=None, sep=' ')
    assert 2 == get_backwards_predictions(df_input)

def test_star2():
    df_input = pd.read_csv('day9/input', header=None, sep=' ')
    assert 933 == get_backwards_predictions(df_input)