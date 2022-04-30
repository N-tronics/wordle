import json
import string
import copy

data = {f'{l1}{l2}':[] for l1 in string.ascii_lowercase for l2 in string.ascii_lowercase}
with open('raw_words.txt') as f:
    ln = f.readline()[:-1]
    while ln:
        if len(ln) == 5:
            data[ln[:2]].append(ln)
        ln = f.readline()[:-1]

_data = copy.deepcopy(data)
for grp, lst in _data.items():
    if len(lst) == 0: data.pop(grp)

with open('words_db.json', 'w') as f:
    json.dump(data, f, indent=4)
