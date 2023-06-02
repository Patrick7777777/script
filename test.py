import itertools as it
from pprint import pprint
import json


number_of_chars_in_line = 100
number_of_words_in_phrase = 4
num_seconds_max = 100
gap_between_sec = 0.15


def get_words(input_data: str):
    in_data = json.load(open(input_data, 'r'))
    words = []
    for c in range(len(in_data)):
        words.append(in_data[c].get('result'))
    words = list(it.chain.from_iterable(words))
    yield words


datas = next(get_words('test_1.json'))
l_in = datas


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
                # break
            duration = 0
    return chunks


def get_letters_chunks(sp, num_of_chars):
    length = 0
    if sp[0:1]:
        length = len(sp[0].get('word'))
    prev_idx = 0
    chunks = []
    for i in range(1, len(sp)):
        length += len(sp[i].get('word'))
        if length > num_of_chars - len(sp[i]):
            chunk, prev_idx = i - prev_idx, i
            chunks.append(chunk)
            length = len(sp[i].get('word'))
    return chunks


def chunked(sp, ch: list):
    out = []
    for n in ch:
        temp, sp = sp[:n], sp[n:]
        out.append(temp)
    out.append(sp)
    return out


def normalize(sp):
    inp = sp
    out = []
    for i in range(len(sp)):
        seconds = get_seconds_chunks(inp, num_seconds_max)
        letters = get_letters_chunks(inp, number_of_chars_in_line)
        print(seconds[0:1], letters[0:1], number_of_words_in_phrase)
        minimum = [min([*seconds[0:1], *letters[0:1], number_of_words_in_phrase])]
        print(minimum)
        temp = chunked(inp, minimum[0:1])
        ch = [*temp[0:1]]
        if bool(temp[1:]):
            out.append(ch[0])
            inp = temp[1]
    pprint(out)
    return out


normalize(l_in)




# print('letters', letters)


# seconds = get_seconds_chunks(l_in, num_seconds_max)
# l_out = chunked(l_in, seconds)
# pprint(l_out)












