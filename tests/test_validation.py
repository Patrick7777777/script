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



