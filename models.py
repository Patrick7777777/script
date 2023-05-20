import logging
import math
import textwrap
import numpy as np
import ujson
import json
import google.protobuf.text_format as pbtext
from protobuf_to_dict import protobuf_to_dict, dict_to_protobuf
import itertools as it
from pprint import pprint


def get_words(input_data: str):
    in_data = json.load(open(input_data, 'r'))
    words = []
    for i in range(len(in_data)):
        words.append(in_data[i].get('result'))
    words = list(it.chain.from_iterable(words))
    pprint(words)
    return words







get_words('test.json')
