import pytest
import json
import pprint
from functions import validation, normalize
from tests.config import LENGTH_OF_JSON, NUMBER_OF_LETTERS, NUMBER_OF_SECONDS


def test_generate_expected(generate_expected):
    pass


# test for words in line
@pytest.mark.parametrize(
    'num_chars, time, gap', [
        (2000, 2000, 0),
    ])
def test_validation_words(num_chars, time, gap, words):
    for i in range(1, LENGTH_OF_JSON + 1):
        result = validation(next(normalize(words, num_chars, time, i)), gap)
        assert result == json.load(open(f'tests/src/test_{i}_expected.json', 'r'))


# test for numbers of chars in line
@pytest.mark.parametrize(
    'time, num_words, gap', [
        (2000, 2000, 0)
    ])
def test_validation_chars(time, num_words, gap, words):
    for i in range(1, LENGTH_OF_JSON + 1):
        result = validation(next(normalize(words, i*NUMBER_OF_LETTERS, time, num_words)), gap)
        assert result == json.load(open(f'tests/src/test_{i}_expected.json', 'r'))


# test for time in line
@pytest.mark.parametrize(
    'num_chars, num_words, gap', [
        (2000, 2000, 0)
    ])
def test_validation_time(num_chars, num_words, gap, words):
    for i in range(1, LENGTH_OF_JSON+1):
        result = validation(next(normalize(words, num_chars, i*NUMBER_OF_SECONDS, num_words)), gap)
        with open(f'./tests/src/test_{i}_result.json', 'w') as outfile:
            json.dump(result, outfile, ensure_ascii=False, indent=2)
        assert result == json.load(open(f'tests/src/test_{i}_expected.json', 'r'))




# test for validation one word and gap 0.5s
# @pytest.mark.parametrize(
#     'num_chars, time, num_words, gap', [
#         # letters
#         (2, 20, 20, 0.5),
#         # time
#         (20, 2, 20, 0.5),
#         # words
#         (20, 20, 1, 0.5)
#     ])
# def test_validation_one_word_gap_05(num_chars, time, num_words, gap, words):
#     result = validation(next(normalize(words, num_chars, time, num_words)), gap)
#     assert result == json.load(open('tests/src/test_1_gap_05_expected.json', 'r'))
