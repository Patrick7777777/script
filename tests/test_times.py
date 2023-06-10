import pytest
import json
from pprint import pprint


def test_times(run_parsing):
    in_datas = json.load(open('./src/test_out1.json', 'r'))
    out_datas = json.load(open('./src/test_output.json', 'r'))
    assert in_datas == out_datas


