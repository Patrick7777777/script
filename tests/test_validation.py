import pytest
import json

from functions import validation, normalize


@pytest.mark.parametrize(
    'num_chars, time, num_words, gap', [
        (40, 2, 40, 0),
        (40, 1, 40, 0),
        (40, 0, 40, 0)
    ])
def test_validation(num_chars, time, num_words, gap, words):
    result = validation(next(normalize(words, num_chars, time, num_words)), gap)
    assert result == json.load(open('tests/src/test_1_expected.json', 'r'))




