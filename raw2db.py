import json
import string
import copy
import sys


data = {f'{l1}{l2}': [] for l1 in string.ascii_lowercase for l2 in string.ascii_lowercase}
with open('raw_words.txt') as f:
    ln = f.readline()[:-1]
    while ln:
        if len(ln) == 5 and ln not in data[ln[:2]]:
            data[ln[:2]].append(ln)
        ln = f.readline()[:-1]


if len(sys.argv) >= 2 and sys.argv[1] == 'txt':
    with open('words_db.txt', 'w') as f:
        for _, wrds in data.items():
            for wrd in sorted(set(wrds)):
                f.write(f'{wrd}\n')
else:
    _data = copy.deepcopy(data)
    for grp, lst in _data.items():
        if len(lst) == 0:
            data.pop(grp)
        else:
            data[grp] = sorted(set(lst))

    with open('words_db.json', 'w') as f:
        json.dump(data, f, indent=4)
