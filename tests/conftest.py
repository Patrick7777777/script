import pytest

from functions import get_words, chunked


@pytest.fixture(params=['./tests/src/test_in.json'])
def words(request):
    return next(get_words(request.param))


# def make_expected(path):
#     wrds = next(get_words(path))
#     chnks = next(chunked(wrds, [1, 3]))
#     print(chnks)
#
#
# make_expected('./tests/src/test_in.json')

