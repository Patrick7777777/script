import pytest

from functions import get_words


@pytest.fixture(params=['./tests/src/test_in.json'])
def words(request):
    return next(get_words(request.param))


