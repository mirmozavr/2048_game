import pygame as pg
import sys
import random
import time

color = {'FRAME': (128, 128, 128),
         'BLACK_TEXT': (80, 80, 80),
         'WHITE_TEXT': (255, 255, 255),
         'GREEN': (50, 255, 150),
         'BLUE': (30, 45, 255),
         'LightSalmon': (255, 160, 122),
         None: (250, 240, 230),
         2: (255, 235, 205),
         4: (255, 222, 173),
         8: (255, 160, 122),
         16: (255, 127, 80),
         32: (255, 99, 71),
         64: (255, 69, 0),
         128: (255, 165, 0),
         256: (230, 190, 75),
         512: (204, 204, 0),
         1024: (189, 183, 107),
         2048: (102, 205, 170),
         4096: (0, 128, 128),
         8192: (0, 206, 209),
         16384: (0, 206, 209),
         }
font_size = {
    1: 56,
    2: 56,
    3: 46,
    4: 32,
    5: 28,
}
pg.init()
pg.display.set_caption('2048')

PLATES = 4  # number of plates on one side
PLATE_SIZE = 80
MARGIN = 15
GAP = 2
SIDE = PLATES * PLATE_SIZE + MARGIN * 2 + GAP * (PLATES - 1)
SCREEN_SIZE = (SIDE, SIDE + 30)

timer = pg.time.Clock()
screen = pg.display.set_mode(SCREEN_SIZE)
arial_italic = pg.font.SysFont('arial', size=20, bold=True, italic=True)


class Tile:

    def __init__(self, row, column, value=None):
        self.row, self.column, self.value = row, column, value

    def draw(self):
        corner_x = self.row * PLATE_SIZE + MARGIN + GAP * self.row
        corner_y = self.column * PLATE_SIZE + MARGIN + GAP * self.column
        tile_color = color[self.value]
        pg.draw.rect(screen, tile_color,
                     (corner_x, corner_y,
                      PLATE_SIZE, PLATE_SIZE), border_radius=5)
        fs = len(str(self.value))  # font size defined by length of self.value
        arial = pg.font.SysFont('arial', size=font_size[fs], bold=True)
        fc = color['BLACK_TEXT'] if self.value and self.value < 5 else color['WHITE_TEXT']  # font color
        text = arial.render('' if self.value is None else str(self.value), True, fc)
        text_position = text.get_rect(centerx=corner_x + PLATE_SIZE // 2, centery=corner_y + PLATE_SIZE // 2)
        screen.blit(text, text_position)

    def __str__(self):
        """Utility"""
        return f'row {self.column}, col {self.row}, val {self.value}'


# initiate field
field = [[Tile(i, j) for i in range(PLATES)] for j in range(PLATES)]


def choose_empty_spot():
    while True:
        x = random.randint(0, PLATES - 1)
        y = random.randint(0, PLATES - 1)
        if field[x][y].value is None:
            return x, y


def check_lost():
    for i in range(PLATES):
        for j in range(PLATES):
            if field[i][j].value is None:
                return False

            for ii, jj in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                if 0 <= ii <= PLATES -1 and 0 <= jj <= PLATES -1:
                    if field[i][j].value == field[ii][jj].value:
                        return False

    return True  # game is lost, no free space


def draw_all_tiles():
    for i in range(PLATES):
        for j in range(PLATES):
            field[i][j].draw()


def draw_score():
    text = arial_italic.render(f'Score: {total_score}', True, color['WHITE_TEXT'])
    text_position = text.get_rect(x=20, y=SIDE - 5)
    screen.blit(text, text_position)


def game_over():
    end_game = arial_italic.render(f'GAME OVER', True, color['WHITE_TEXT'], (70, 70, 70))
    text_position = end_game.get_rect(centerx=SIDE // 2, centery=SIDE // 2)
    screen.blit(end_game, text_position)
    timer.tick(30)
    pg.display.update()
    time.sleep(5)
    quit()


total_score = 0
start = True
while True:
    screen.fill(color['FRAME'])

    # spawn first 2 tiles
    if start:
        for _ in range(2):
            x, y = choose_empty_spot()
            field[x][y].value = random.choice([2, 4])
        start = False

    # draw all tiles
    draw_all_tiles()

    # draw score
    draw_score()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        elif event.type == pg.KEYDOWN: # and event.key in (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT):  # == pg.KEYDOWN:
            movement = False
            if event.key == pg.K_UP:
                for _ in range(PLATES):
                    for row in range(PLATES - 1):
                        for col in range(PLATES):
                            if field[row][col].value is None and field[row + 1][col].value is not None:
                                field[row][col].value, field[row + 1][col].value = field[row + 1][col].value, \
                                                                                   field[row][col].value
                                movement = True
                            elif field[row][col].value is None:
                                pass
                            elif field[row][col].value == field[row + 1][col].value:
                                field[row][col].value *= 2
                                total_score += field[row][col].value
                                field[row + 1][col].value = None
                                movement = True
            elif event.key == pg.K_DOWN:
                for _ in range(PLATES):
                    for row in range(PLATES - 1, 0, -1):
                        for col in range(PLATES):
                            if field[row][col].value is None and field[row - 1][col].value is not None:
                                field[row][col].value, field[row - 1][col].value = field[row - 1][col].value, \
                                                                                   field[row][col].value
                                movement = True
                            elif field[row][col].value is None:
                                pass
                            elif field[row][col].value == field[row - 1][col].value:
                                field[row][col].value *= 2
                                total_score += field[row][col].value
                                field[row - 1][col].value = None
                                movement = True

            elif event.key == pg.K_LEFT:
                for _ in range(PLATES):
                    for row in range(PLATES):
                        for col in range(PLATES - 1):
                            if field[row][col].value is None and field[row][col + 1].value is not None:
                                field[row][col].value, field[row][col + 1].value = field[row][col + 1].value, \
                                                                                   field[row][col].value
                                movement = True
                            elif field[row][col].value is None:
                                pass
                            elif field[row][col].value == field[row][col + 1].value:
                                field[row][col].value *= 2
                                total_score += field[row][col].value
                                field[row][col + 1].value = None
                                movement = True

            elif event.key == pg.K_RIGHT:
                for _ in range(PLATES):
                    for row in range(PLATES):
                        for col in range(PLATES - 1, 0, -1):
                            if field[row][col].value is None and field[row][col - 1].value is not None:
                                field[row][col].value, field[row][col - 1].value = field[row][col - 1].value, \
                                                                                   field[row][col].value
                                movement = True
                            elif field[row][col].value is None:
                                pass
                            elif field[row][col].value == field[row][col - 1].value:
                                field[row][col].value *= 2
                                total_score += field[row][col].value
                                field[row][col - 1].value = None
                                movement = True
            # actions if tiles moved
            if movement:
                x, y = choose_empty_spot()
                field[x][y].value = random.choice([2, 4])

                # check if no free space to spawn numbers
                if check_lost():
                    draw_all_tiles()
                    timer.tick(30)
                    pg.display.update()
                    time.sleep(1)
                    game_over()

    timer.tick(30)
    pg.display.update()
