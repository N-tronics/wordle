import pygame
import logging as lg
from random import choice as rchoice
from json import load as jload
from sys import exit as sys_exit

pygame.font.init()

lg.basicConfig(filename='wordle_game.log', level=lg.DEBUG, filemode='w', format='%(levelname)s - %(message)s')
with open('words_db.json') as f:
    WORD_SET = jload(f)

COLORS = {
    -1: (127, 127, 127),
    0: (70, 70, 70),
    1: (175, 175, 0),
    2: (0, 200, 0)
}


class Vec2():
    def __init__(self, x, y):
        self.x, self.y = x, y

    def get_tuple(self):
        return self.x, self.y

    def __repr__(self):
        return f'[{self.x} {self.y}]'


class Wordle():
    def __init__(self):
        self.WIN_DIMENS = Vec2(500, 650)
        self.WIN = pygame.display.set_mode(self.WIN_DIMENS.get_tuple())
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.char_font = pygame.font.SysFont('chandas', 64)
        self.msg_font = pygame.font.SysFont('chandas', 32)
        pygame.display.set_caption('Wordle')

        self.grid = [[Vec2('', -1) for _ in range(5)] for _ in range(6)]
        self.line = self.col = 0
        self.grid_offset = Vec2(25, 25)
        self.cell_spacing = 20
        self.cell_size = Vec2(74, 75) 
        self.msg = ''
        self.game_over = False

        self.selected_word = rchoice(sum([v for _,v in WORD_SET.items()], []))

    def insert_character(self, char):
        self.grid[self.line][self.col].x = char
        self.col += 1

    def remove_character(self):
        self.col -= 1
        self.grid[self.line][self.col].x = ''

    def in_words(self, wrd):
        return wrd in WORD_SET[wrd[:2]]

    def check_word(self):
        wrd = ''
        for c in self.grid[self.line]:
            wrd += c.x
        if not self.in_words(wrd):
            return
        lg.info(f'Evaluating word {wrd}')
        ignoreIdxs = []
        sel_wrd = list(self.selected_word)
        for i in range(5):
            if self.grid[self.line][i].x == sel_wrd[i]:
                self.grid[self.line][i].y = 2
                ignoreIdxs.append(i)
        for i in sorted(ignoreIdxs, reverse=True):
            sel_wrd.pop(i)
        for i in range(5):
            if i in ignoreIdxs: continue
            if self.grid[self.line][i].x in sel_wrd:
                self.grid[self.line][i].y = 1
                ignoreIdxs.append(i)
                sel_wrd.remove(self.grid[self.line][i].x)
        for i in range(5):
            if i in ignoreIdxs: continue
            self.grid[self.line][i].y = 0

        if wrd == self.selected_word:
            lg.info(f'Correct Word: {wrd}')
            self.msg = 'Correct!'
            self.game_over = True
        elif self.line == 5:
            self.msg = 'Correct!'
            self.msg = f'The word was \'{self.selected_word}\'!'
            self.game_over = True

        self.line += 1
        self.col = 0 

    def draw(self):
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                char = self.char_font.render(col.x.upper(), True, (255, 255, 255))
                rect = Vec2(
                    self.grid_offset.x + (self.cell_size.x * j) + (self.cell_spacing * j - 1 if j > 0 else 0),
                    self.grid_offset.y + (self.cell_size.y * i) + (self.cell_spacing * i - 1 if i > 0 else 0)
                )
                pygame.draw.rect(self.WIN, COLORS[col.y], (
                    *rect.get_tuple(),
                    *self.cell_size.get_tuple()
                ))
                self.WIN.blit(char, (
                    rect.x + self.cell_size.x // 2 - char.get_width() // 2,
                    12 + rect.y + self.cell_size.y // 2 - char.get_height() // 2
                ))
        msg = self.msg_font.render(self.msg, True, (255, 255, 255))
        self.WIN.blit(msg, (
            self.WIN_DIMENS.x // 2 - msg.get_width() // 2,
            625 - msg.get_height() // 2
        ))

        pygame.display.update()

    def start(self):
        lg.info('Starting Wordle')
        lg.info(f'Selected word: {self.selected_word}')
        while True:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    lg.info('Quitting Wordle')
                    pygame.quit()
                    sys_exit(0)
                if event.type == pygame.KEYUP and not self.game_over:
                    if event.key == pygame.K_BACKSPACE and self.col > 0:
                        lg.info('Backspace')
                        self.remove_character()
                        lg.info(self.grid)
                    elif event.key >= pygame.K_a and event.key <= pygame.K_z and self.col < 5:
                        lg.info(f'key press: {chr(event.key)}')
                        self.insert_character(chr(event.key))
                        lg.info(self.grid)
                    elif event.key == pygame.K_RETURN and self.col == 5:
                        lg.info('Enter')
                        self.check_word()
                        lg.info(self.grid)
            self.draw()


if __name__ == '__main__':
    wd = Wordle()
    wd.start()
