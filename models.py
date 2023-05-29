import google.protobuf.text_format as pbtext
import json
import ujson
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


def phrase_time(input_data: str,
                num_seconds_max,
                gap_between_sec,
                number_of_words_in_phrase,
                number_of_chars_in_line):
    datas = next(get_words(input_data))
    out = []
    length = 0
    start = 0
    gap = 0
    letters = 0
    letters_idx = 0
    for i in range(len(datas)):
        start_time, end_time = datas[i].get('start'), datas[i].get('end')

        def chunk_division(text: list, words_count):
            end = start + min([words_count, (i + 1) - start])
            temp = text[start: end]
            phrase = []

            for key, value in enumerate(temp):
                value['end'] = round((value['end'] + gap), 2)
                value['start'] = round((value['start'] + gap), 2)
                phrase.append(value.get('word'))
            out.append({"result": temp, "text": ' '.join(phrase)})
            yield end

        if letters >= number_of_chars_in_line:
            prev_idx, letters_idx = letters_idx, i
            if letters_idx - prev_idx <= number_of_words_in_phrase:
                number_of_words_in_phrase = letters_idx - prev_idx
            start = next(chunk_division(datas, number_of_words_in_phrase))
            letters = 0

        if length >= num_seconds_max:
            gap += gap_between_sec
            start = next(chunk_division(datas, number_of_words_in_phrase))
            length = 0

        elif i >= len(datas) - 1:
            diff = list(it.filterfalse(list(it.chain.from_iterable(out)).__contains__, iter(datas)))
            for j in range(len(diff)):
                if start != len(diff):
                    start = next(chunk_division(diff, number_of_words_in_phrase))
                else:
                    break
        elif length < num_seconds_max:
            length += end_time - start_time
            letters += len(datas[i].get('word'))

    pprint(out)
    return out


# get_words('test.json').__next__()
# pprint(punctuation_break('test.json').__next__())
phrase_time('test.json', 1000, 0, 1000, 27)
