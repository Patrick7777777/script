import pytest
import json
import itertools as it

from functions import get_words, chunked


@pytest.fixture(params=['./tests/src/test_in.json'])
def words(request):
    return next(get_words(request.param))


@pytest.fixture(params=[1, 2, 3, 4])
def generate_expected(request):
    path = './tests/src/test_in.json'
    n = request.param
    out = []
    words = next(get_words(path))
    chunked_words = [words[i:i + n] for i in range(0, len(words), n)]
    for el in chunked_words:
        text = ' '.join([w.get('word') for w in it.chain(el)])
        out.append({'result': el, 'text': text})
    with open(f'./tests/src/test_{n}_expected.json', 'w') as outfile:
        json.dump(out, outfile, ensure_ascii=False, indent=2)

