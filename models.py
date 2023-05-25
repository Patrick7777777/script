import google.protobuf.text_format as pbtext
import json
import itertools as it
import re
from pprint import pprint
from protobuf_to_dict import protobuf_to_dict, dict_to_protobuf


def get_words(input_data: str):
    in_data = json.load(open(input_data, 'r'))
    words = []
    for i in range(len(in_data)):
        words.append(in_data[i].get('result'))
    words = list(it.chain.from_iterable(words))
    yield words


def chunked(sp, n):
    return [sp[i:i + n] for i in range(0, len(sp), n)]


def punctuation_break(input_data):
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
    gap = 0
    for i in range(len(datas)):
        start_time, end_time = datas[i].get('start'), datas[i].get('end')

        def duration_count(text):
            words_count = 7
            end = start + min([words_count, (i + 1) - start])
            temp = text[start: end]
            for key, value in enumerate(temp):
                value['end'] = round((value['end'] + gap), 2)
                value['start'] = round((value['start'] + gap), 2)
            out.append(temp)
            return end

        if length < num_seconds_max:
            length += end_time - start_time
        if length >= num_seconds_max:
            gap += gap_between_sec
            start = duration_count(datas)
            length = 0
        if i == len(datas) - 1:
            diff = list(it.filterfalse(list(it.chain.from_iterable(out)).__contains__, iter(datas)))
            for j in range(len(diff)):
                start = duration_count(datas)
    pprint(list(filter(None, out)))
    return list(filter(None, out))


# pprint(get_words('test.json').__next__())
# pprint(punctuation_break('test.json').__next__())
phrase_time('test_1.json', 1, 5)
