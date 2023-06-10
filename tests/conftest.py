import pytest
import json


from pprint import pprint
from functions import validation, normalize, get_words
from config import gap_between_sec


@pytest.fixture
def run_parsing():
    datas = next(get_words('./src/test_in1.json'))
    valid_datas = validation(next(normalize(datas)), gap_between_sec)
    # pprint(valid_datas)
    with open('./src/test_output.json', 'w') as outfile:
        json.dump(valid_datas, outfile, ensure_ascii=False, indent=2)
