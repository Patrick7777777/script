import itertools as it
from pprint import pprint


datas = [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}, {'10'}, {'11'}, {'12'}, {'13'}, {'14'}]
# l_out = []
l_in = []
length = 3
start = 0


# def chunked(sp, n):
#     s = 0
#     chunk = []
#     for i in range(len(sp)):
#         if bool(sp[s:s+n]):
#             # chunk.append(sp[s:s+n])
#             # yield chunk
#             chunk.append(sp[s:s+n])
#         # yield chunk
#         s += n
#     yield chunk
#     return

def chunked(sp, s, n):
    chunk = []

    if bool(sp[s:s+n]):
        # chunk.append(sp[s:s+n])
        # yield chunk
        chunk.append(sp[s:s+n])
    # yield chunk
    s += n
    # print(s)
    return chunk


# pprint(chunked(datas, 1, 3))

l_out = it.islice(datas, 0, 3)
print(list(l_out))


# for k in range(len(datas)):
#     # print(datas[k])
#     print(chunked(list(datas[k]), 4).__next__())
#     # print(datas[k])


# print(chunked(datas, 4))



    # l_out = it.filterfalse(lambda i : l_in.append(), datas)
