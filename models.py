import logging
import math
import textwrap
import numpy as np
import ujson
import json
import google.protobuf.text_format as pbtext
from protobuf_to_dict import protobuf_to_dict, dict_to_protobuf
import itertools as it
import re
from pprint import pprint


def get_words(input_data: str):
    in_data = json.load(open(input_data, 'r'))
    words = []
    for i in range(len(in_data)):
        words.append(in_data[i].get('result'))
    words = list(it.chain.from_iterable(words))
    # pprint(words)
    return words


def chunked(sp, n):
    return [sp[i:i + n] for i in range(0, len(sp), n)]


def punctuation_break(input_data: str):
    datas = get_words(input_data)
    out = []
    length = 0
    start = 0
    for i in range(len(datas)):
        word = datas[i].get('word')
        if re.findall('[!?.,]', word):
            length = i - length
            out.append(datas[start: i + 1])
            start = i + 1
    return out





# print(chunked(get_words('test.json'), 2))
pprint(punctuation_break('test.json'))
