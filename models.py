import logging
import math
import textwrap
import numpy as np
import ujson
import google.protobuf.text_format as pbtext
from protobuf_to_dict import protobuf_to_dict, dict_to_protobuf
import json
import itertools as it
import re
from pprint import pprint


def get_words(input_data: str):
    in_data = json.load(open(input_data, 'r'))
    words = []
    for i in range(len(in_data)):
        words.append(in_data[i].get('result'))
    words = list(it.chain.from_iterable(words))
    yield words


def chunked(sp, n):
    return [sp[i:i + n] for i in range(0, len(sp), n)]


def punctuation_break(input_data: str):
    datas = next(get_words(input_data))
    out = []
    start = 0
    for i in range(len(datas)):
        word = datas[i].get('word')
        if re.findall('[!?.]', word):
            out.append(datas[start: i + 1])
            start = i + 1
        elif i == len(datas) - 1:
            out.append(datas[start: i + 1])
    yield out


def phrase_time(input_data: str, num_seconds_max, gap_between_sec):
    datas = next(get_words(input_data))
    out = []
    length = 0
    start = 0
    for i in range(len(datas)):
        start_time, end_time = datas[i].get('start'), datas[i].get('end')
        # print(length, datas[i])
        if length <= num_seconds_max:
            length += end_time - start_time
        if length > num_seconds_max:
            temp = datas[start: i + 1]
            out.append(temp)
            print([d.get('word') for d in temp])
            start = i + 1
            length = 0
        if i == len(datas) - 1:
            temp = datas[start: i + 1]
            # _temp = [d.get('word') for d in temp]
            out.append(temp)
            # print(temp)
    # pprint(out)
    return out


# pprint(get_words('test.json').__next__())
# pprint(punctuation_break('test.json').__next__())
phrase_time('test_1.json', 3, 0.2)
