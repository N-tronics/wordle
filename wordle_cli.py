import json
import logging as lg
import random

lg.basicConfig(filename='wordle_cli.log', level=lg.DEBUG, filemode='w', format='%(levelname)s - %(message)s')

WORDS_DB = 'words_db.json'
grid = [[['_', 0] for _ in range(5)] for _ in range(6)]
with open(WORDS_DB, 'r') as f:
    words = json.load(f)


def _in_words(wrd, start=0, end=len(words) - 1):
    if start > end:
        return False
    mid = (start + end) // 2
    if wrd == words[mid]:
        return True
    elif wrd > words[mid]:
        return _in_words(wrd, mid + 1, end)
    else:
        return _in_words(wrd, start, mid - 1)


def print_grid():
    for row in grid:
        for col in row:
            if col[1] == 1:
                color = 33
            elif col[1] == 2:
                color = 32
            else:
                color = 90
            print(f'\033[{color}m{col[0]}\033[m', end=' ')
        print()


if __name__ == '__main__':
    selectedWord = random.choice(sum([v for _, v in words.items()], []))
    lg.info(f'Selected Word: \'{selectedWord}\'')

    ln = 0
    checked_indexes = []
    print_grid()
    while ln < 6:
        inputWrd = input('> ')
        if len(inputWrd) != 5 and inputWrd not in words[inputWrd[:2]]:
            print("Invalid word! Try again\n")
            continue
        lg.debug(f'Input: {inputWrd}')

        checked_indexes.clear()
        sWord = list(selectedWord)
        iWord = list(inputWrd)
        for i in range(5):
            grid[ln][i][0] = iWord[i]
            if sWord[i] == iWord[i]:
                grid[ln][i][1] = 2
                checked_indexes.append(i)
        lg.debug(f'checked_indexes: {checked_indexes}, sWord: {sWord}, iWord: {iWord}')
        for idx in sorted(checked_indexes, reverse=True):
            sWord.pop(idx)
        lg.debug(f'sWord: {sWord}')
        for i in range(5):
            if i in checked_indexes:
                continue
            if iWord[i] in sWord:
                grid[ln][i][1] = 1
                sWord.remove(iWord[i])
                lg.debug(f'yellow {iWord[i]}, {sWord}')
                continue

        print_grid()
        if inputWrd == selectedWord:
            print(f'\n\033[32mCongratulations! The word was \'{selectedWord}\'!\033[m')
            exit()

        ln += 1
        print()

    print(f'\033[31mThe word was \'{selectedWord}\'. Good Try!\033[m')
