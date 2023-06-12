import pytest
import json

from functions import validation, normalize


# test for one word in line
@pytest.mark.parametrize(
    'num_chars, time, num_words, gap', [
        # letters
        (2, 20, 20, 0),
        (1, 20, 20, 0),
        (0, 20, 20, 0),
        # time
        (40, 2, 40, 0),
        (40, 1, 40, 0),
        (40, 0, 40, 0),
        # words
        (40, 40, 1, 0)
    ])
def test_validation_one_word(num_chars, time, num_words, gap, words):
    result = validation(next(normalize(words, num_chars, time, num_words)), gap)
    assert result == json.load(open('tests/src/test_1_expected.json', 'r'))


# test for two words in line
@pytest.mark.parametrize(
    'num_chars, time, num_words, gap', [
        # letters
        (6, 40, 40, 0),
        # time
        (40, 4, 40, 0),
        # words
        (40, 40, 2, 0)
    ])
def test_validation_two_words(num_chars, time, num_words, gap, words):
    result = validation(next(normalize(words, num_chars, time, num_words)), gap)
    assert result == json.load(open('tests/src/test_2_expected.json', 'r'))


# test for three words in line
@pytest.mark.parametrize(
    'num_chars, time, num_words, gap', [
        # letters
        (9, 40, 40, 0),
        # time
        (40, 6, 40, 0),
        # words
        (40, 40, 3, 0)
    ])
def test_validation_three_words(num_chars, time, num_words, gap, words):
    result = validation(next(normalize(words, num_chars, time, num_words)), gap)
    assert result == json.load(open('tests/src/test_3_expected.json', 'r'))


# test for four words in line
@pytest.mark.parametrize(
    'num_chars, time, num_words, gap', [
        # letters
        (12, 40, 40, 0),
        # time
        (40, 8, 40, 0),
        # words
        (40, 40, 4, 0)
    ])
def test_validation_four_words(num_chars, time, num_words, gap, words):
    result = validation(next(normalize(words, num_chars, time, num_words)), gap)
    assert result == json.load(open('tests/src/test_4_expected.json', 'r'))


# test for validation one word and gap 0.5s
@pytest.mark.parametrize(
    'num_chars, time, num_words, gap', [
        # letters
        (2, 40, 40, 0.5),
        # time
        (40, 2, 40, 0.5),
        # words
        (40, 40, 1, 0.5)
    ])
def test_validation_one_word_gap_05(num_chars, time, num_words, gap, words):
    result = validation(next(normalize(words, num_chars, time, num_words)), gap)
    assert result == json.load(open('tests/src/test_1_gap_05_expected.json', 'r'))
