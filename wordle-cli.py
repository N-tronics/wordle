import json
import logging as lg
import random

lg.basicConfig(filename='wordle-log.log', level=lg.DEBUG, filemode='w', format='%(levelname)s - %(message)s')

WORDS_DB = 'words_db.json'
words = None
grid = [[['_', 0] for _ in range(5)] for _ in range(6)]
with open(WORDS_DB, 'r') as f:
    words = json.load(f)


def _inWords(wrd, start=0, end=len(words)-1):
    if start > end: return False
    mid = (start + end) // 2
    if wrd == words[mid]:
        return True
    elif wrd > words[mid]:
        return _inWords(wrd, mid + 1, end)
    else:
        return _inWords(wrd, start, mid - 1)


def inWords(wrd):
    return wrd in words[wrd[:2]]


def printGrid():
    for row in grid:
        for col in row:
            color = ''
            if col[1] == 1: color = 33
            elif col[1] == 2: color = 32
            else: color = 90
            print(f'\033[{color}m{col[0]}\033[m', end=' ')
        print()


def ignore(lst, idxs):
    for i in idxs:
        lst.pop(i)
    return lst


if __name__ == '__main__':
    selectedWord = random.choice(sum([v for _,v in words.items()], []))
    lg.info(f'Selected Word: \'{selectedWord}\'')
    prevWrd = ''

    parsed = []
    ln = 0
    printGrid()
    while ln < 6:
        inputWrd = input('> ')
        if len(inputWrd) != 5 and not inWords(inputWrd):
            print("Invalid word! Try again\n")
            continue
        lg.debug(f'Input: {inputWrd}')

        parsed.clear()
        prevWrd = inputWrd
        for i in range(5):
            inputChr = inputWrd[i]
            grid[ln][i][0] = inputChr
            # Greens
            if inputChr == selectedWord[i]:
                grid[ln][i][1] = 2
                parsed.append(i)
                lg.debug(f'green, parsed:- {i}: {inputChr}')
            # Yellows
            elif i not in parsed:
                for j in range(5):
                    if j not in parsed:
                        if inputChr == selectedWord[j]:
                            grid[ln][i][1] = 1
                            parsed.append(j)
                            lg.debug(f'yellow, parsed:- {j}: {inputChr}')
                            break
        print()
        printGrid()
        if prevWrd == selectedWord:
            print(f'\033[32mCongratulations! The word was \'{selectedWord}\'!\033[m')
            exit()

        ln += 1

    print(f'\n\033[31mThe word was \'{selectedWord}\'. Good Try!\033[m')            
