
import numpy as np
import pandas as pd


from functools import reduce 
from io import StringIO

card_conversion = {
    "1" : 0,
    "2" : 1,
    "3" : 2,
    "4" : 3,
    "5" : 4,
    "6" : 5,
    "7" : 6,
    "8" : 7,
    "9" : 8,
    "T" : 9,
    "J" : 10,
    "Q" : 11,
    "K" : 12,
    "A" : 13,    
}

card_conversion_jokers = {
    "1" : 1,
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "T" : 10,
    "J" : 0,
    "Q" : 11,
    "K" : 12,
    "A" : 13,    
}

play_ranking = {
    "FiveOf": 6,
    "FourOf": 5,
    "Full": 4,
    "ThreeOf": 3,
    "DoublePair": 2,
    "Pair": 1,
    "HighC": 0,
}

ranking_play = {
    6: "FiveOf",
    5: "FourOf",
    4: "Full",
    3: "ThreeOf",
    2: "DoublePair",
    1: "Pair",
    0: "HighC",
}

def get_hand(hand: str):
    hand_count = np.zeros(len(card_conversion), dtype='int')
    for c in hand:
        hand_count[card_conversion[c]] += 1
    if np.where(hand_count == 5)[0].shape[0] > 0:
        return "FiveOf"
    elif np.where(hand_count == 4)[0].shape[0] > 0:
        return "FourOf"
    elif np.where(hand_count == 3)[0].shape[0] > 0 and np.where(hand_count == 2)[0].shape[0]:
        return "Full"
    elif np.where(hand_count == 3)[0].shape[0] > 0 and not np.where(hand_count == 2)[0].shape[0]:
        return "ThreeOf"
    elif np.where(hand_count == 2)[0].shape[0] == 2:
        return "DoublePair"
    elif not np.where(hand_count == 3)[0].shape[0] > 0 and np.where(hand_count == 2)[0].shape[0]:
        return "Pair"
    else:
        return "HighC"
       
def get_hand_with_jokers(hand: str):
    hand_count = np.zeros(len(card_conversion), dtype='int')
    num_j = 0
    for c in hand:
        if c != 'J':
            hand_count[card_conversion[c]] += 1
        else:
            num_j += 1
    if np.where(hand_count == 5)[0].shape[0] > 0:
        hand_no_j = "FiveOf"
    elif np.where(hand_count == 4)[0].shape[0] > 0:
        hand_no_j = "FourOf"
    elif np.where(hand_count == 3)[0].shape[0] > 0 and np.where(hand_count == 2)[0].shape[0]:
        hand_no_j = "Full"
    elif np.where(hand_count == 3)[0].shape[0] > 0 and not np.where(hand_count == 2)[0].shape[0]:
        hand_no_j = "ThreeOf"
    elif np.where(hand_count == 2)[0].shape[0] == 2:
        hand_no_j = "DoublePair"
    elif not np.where(hand_count == 3)[0].shape[0] > 0 and np.where(hand_count == 2)[0].shape[0]:
        hand_no_j = "Pair"
    else:
        hand_no_j = "HighC"

    if num_j > 0:
        if hand_no_j == "FourOf":
            hand_no_j = "FiveOf"
        elif hand_no_j == "ThreeOf":
            hand_no_j = ranking_play[4 + num_j]
        elif hand_no_j == "DoublePair":
            hand_no_j = 'Full'
        elif hand_no_j == "Pair":
            if num_j == 1:
                 hand_no_j = "ThreeOf"
            else:
                hand_no_j = ranking_play[3 + num_j]
        elif hand_no_j == "HighC":
            if num_j == 1:
                hand_no_j = "Pair"
            elif num_j == 2:
                hand_no_j = "ThreeOf"
            elif num_j == 5:
                hand_no_j = "FiveOf"
            else:
                hand_no_j = ranking_play[2 + num_j]
    return hand_no_j
            

def hand_n(hand):
    hand_value = 0
    hand_string = hand[0]
    for i in range(len(hand_string)):
        hand_value += (card_conversion[hand_string[i]] + 1) * round(14 ** (len(hand_string) - i))
    return hand_value

def hand_ranking(hand):
    hand_value = 0
    hand_string = hand[0]
    for i in range(len(hand_string)):
        hand_value += (card_conversion_jokers[hand_string[i]] + 1) * round(14 ** (len(hand_string) - i))
    return hand_value

def rank_and_value(list_of_hands: list, hand_func, hand_rank_func):
    ranking_by_hand = [[],[],[],[],[],[],[],]
    ranking = []
    for play in list_of_hands:
        ranking_by_hand[play_ranking[hand_func(play[0])]].append(play)
    for i in range(len(ranking_by_hand)):
        ranking_by_hand[i].sort(key=hand_rank_func)
        ranking = ranking + ranking_by_hand[i]
    total_ranking = 0
    for i in range(len(ranking)):
        total_ranking += ranking[i][1] * (i + 1)
    return total_ranking
    
############### TEST CASES ################        

def test_get_hand_five_of():
    assert "FiveOf" == get_hand('55555')

def test_get_hand_four_of():
    assert "FourOf" == get_hand('TTTT8')

def test_get_hand_full():
    assert "Full" == get_hand('KKKAA')

def test_get_hand_three_of():
    assert "ThreeOf" == get_hand('QQQ76')

def test_get_hand_pair():
    assert "Pair" == get_hand('JJ123')

def test_get_hand_double_pair():
    assert "DoublePair" == get_hand('KK677')

def test_get_hand_high_card():
    assert "HighC" == get_hand('45678')

def test_get_hand_with_jokers_HighC_1J():
    assert "Pair" == get_hand_with_jokers('J8123')

def test_get_hand_with_jokers_HighC_2J():
    assert "ThreeOf" == get_hand_with_jokers('JJ123')

def test_get_hand_with_jokers_Full():
    assert "Full" == get_hand_with_jokers('KKKAA')

def test_get_hand_with_jokers_DoublePair():
    assert "Full" == get_hand_with_jokers('KKJAA')

def test_get_hand_with_jokers_Pair_1J():
    assert "ThreeOf" == get_hand_with_jokers('KKJ76')

def test_get_hand_with_jokers_Pair_2J():
    assert "FourOf" == get_hand_with_jokers('KKJJ6')

def test_get_hand_with_jokers_Pair_3J():
    assert "FiveOf" == get_hand_with_jokers('KKJJJ')

def test_get_hand_with_jokers_HighC_3J():
    assert "FourOf" == get_hand_with_jokers('JJJ23')

def test_get_hand_with_jokers_HighC_4J():
    assert "FiveOf" == get_hand_with_jokers('JJJJ3')

def test_get_hand_with_jokers_ThreeOf_1J():
    assert "FourOf" == get_hand_with_jokers('KKKJA')

def test_get_hand_with_jokers_ThreeOf_2J():
    assert "FiveOf" == get_hand_with_jokers('KKKJJ')

def test_get_hand_with_jokers_FourOf_1J():
    assert "FiveOf" == get_hand_with_jokers('KKKKJ')

def test_get_hand_with_jokers_FourOf_5J():
    assert "FiveOf" == get_hand_with_jokers('JJJJJ')

def test_rank_value_example():
    map_example_text = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
    mem_input = StringIO(map_example_text)
    assert 6440 == rank_and_value([('32T3K', 765),('T55J5', 684),
                                   ('KK677', 28), ('KTJJT', 220), ('QQQJA', 483)],
                                   get_hand, hand_n)
    
def test_rank_value_example_with_jokers():
    assert 5905 == rank_and_value([('32T3K', 765),('T55J5', 684),
                                   ('KK677', 28), ('KTJJT', 220), ('QQQJA', 483)],
                                   get_hand_with_jokers, hand_ranking)


def test_star1():
    df_input = pd.read_csv('day7/input', header=None, names=['hand', 'bet'], sep=' ')
    assert 253603890 == rank_and_value(list(zip(df_input['hand'], df_input['bet'])), 
                                        get_hand, hand_n)

def test_star2():
    df_input = pd.read_csv('day7/input', header=None, names=['hand', 'bet'], sep=' ')
    assert 253630098 == rank_and_value(list(zip(df_input['hand'], df_input['bet'])), 
                                       get_hand_with_jokers, hand_ranking)