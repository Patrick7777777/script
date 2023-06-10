import itertools as it
from pprint import pprint
import json

from config import num_seconds_max, number_of_chars_in_line, number_of_words_in_phrase, gap_between_sec


def get_words(input_data: str):
    in_data = json.load(open(input_data, 'r'))
    words = []
    for c in range(len(in_data)):
        words.append(in_data[c].get('result'))
    words = list(it.chain.from_iterable(words))
    yield words


# datas = next(get_words('example.json'))
# l_in = datas


def get_seconds_chunks(sp, num_seconds):
    duration = 0
    if sp[0:1]:
        duration = sp[0].get('start')
    prev_idx = 0
    chunks = []
    for i in range(len(sp)):
        start_time = 0
        end_time = sp[i].get('end')
        if i > 0:
            start_time = sp[i-1].get('end')
            end_time = sp[i].get('end')
        duration += end_time - start_time
        if duration >= num_seconds:
            chunk, prev_idx = i - prev_idx, i
            if chunk > 0:
                chunks.append(chunk)
                break
            duration *= 0
    yield chunks


def get_letters_chunks(sp, num_of_chars):
    length = 0
    if sp[0:1]:
        length = len(sp[0].get('word'))
    prev_idx = 0
    chunks = []
    for i in range(1, len(sp)):
        length += len(sp[i].get('word'))
        if length > num_of_chars:
            chunk, prev_idx = i - prev_idx, i
            chunks.append(chunk)
            break
    yield chunks


def chunked(sp, ch: list):
    out = []
    for n in ch:
        temp, sp = sp[:n], sp[n:]
        out.append(temp)
    out.append(sp)
    yield out


def normalize(sp):
    inp = sp
    out = []
    for i in range(len(sp)):
        seconds = next(get_seconds_chunks(inp, num_seconds_max))
        letters = next(get_letters_chunks(inp, number_of_chars_in_line))
        minimum = [min([*seconds[0:1], *letters[0:1], number_of_words_in_phrase])]
        temp = next(chunked(inp, minimum[0:1]))
        ch = [*temp[0:1]]
        if temp[1:]:
            out.append(ch[0])
            inp = temp[1]
    yield [v for v in out if v]


def validation(sp, skip: float):
    out = []
    gap = 0
    for i in range(len(sp)):
        text = ' '.join([w.get('word') for w in it.chain(sp[i])])
        out.append({'result': sp[i], 'text': text})
        for j in range(len(sp[i])):
            sp[i][j]['end'] += gap
            sp[i][j]['start'] += gap
        gap += skip
    return out


# pprint(validation(next(normalize(l_in)), gap_between_sec))
# with open('output.json', 'w') as outfile:
#     json.dump(validation(next(normalize(l_in)), gap_between_sec), outfile, ensure_ascii=False, indent=4)


# normalize(l_in)
# seconds = get_seconds_chunks(l_in, num_seconds_max)
# l_out = chunked(l_in, seconds)
# pprint(l_out)












