import math

import pytest
import json
import itertools as it

from functions import get_words
from tests.config import LENGTH_OF_JSON, NUMBER_OF_LETTERS, NUMBER_OF_SECONDS


@pytest.fixture(params=['./tests/src/test_in.json'])
def words(request):
    return next(get_words(request.param))


@pytest.fixture(params=[i for i in range(1, LENGTH_OF_JSON+1)])
def generate_expected(request):
    result = []
    text = ''
    start = math.ceil(LENGTH_OF_JSON + NUMBER_OF_SECONDS)
    end = start + NUMBER_OF_SECONDS

    for i in range(LENGTH_OF_JSON):
        result.append({"conf": 0.6, "end": end, "start": start, 'word': 'x'*NUMBER_OF_LETTERS})
        end += NUMBER_OF_SECONDS
        start += NUMBER_OF_SECONDS
        text = ' '.join([w.get('word') for w in it.chain(result)])
    inp = [{'result': result, 'text': text.rstrip()}]
    with open('./tests/src/test_in.json', 'w') as outfile:
        json.dump(inp, outfile, ensure_ascii=False, indent=2)

    n = request.param
    out = []
    words = next(get_words('./tests/src/test_in.json'))
    chunked_words = [words[i:i + n] for i in range(0, len(words), n)]
    for el in chunked_words:
        text = ' '.join([w.get('word') for w in it.chain(el)])
        out.append({'result': el, 'text': text})
    with open(f'./tests/src/test_{n}_expected.json', 'w') as outfile:
        json.dump(out, outfile, ensure_ascii=False, indent=2)
    return out


