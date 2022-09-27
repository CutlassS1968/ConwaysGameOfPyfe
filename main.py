from random import randint

import pygame


class Display:
    def __init__(self, width, height, is_full_screen):

        self.width = width
        self.height = height
        self.is_full_screen = is_full_screen

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 101, 103))
        self.react = self.image.get_rect()
        self.screen = pygame.display.set_mode((self.width, self.height), self.is_full_screen)

    def get_screen(self):
        return self.screen


class Tile(pygame.Rect):

    def __init__(self, left, top, width, height, state, color):
        super().__init__(left, top, width, height)
        self.state = state
        self.color = color

    def flip_state(self):
        self.state = not self.state
        if self.state:
            self.color = (255, 255, 255)
        else:
            self.color = (0, 0, 0)

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        if self.state:
            self.color = (255, 255, 255)
        else:
            self.color = (0, 0, 0)

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color


class Game:

    def __init__(self, width, height, row_count, col_count):

        self.width = width
        self.height = height

        self.row_count = row_count
        self.col_count = col_count

        self.tiles = []
        self.tile_width = int(self.width / self.col_count)
        self.tile_height = int(self.height / self.row_count)
        self.gen_tiles()

    def gen_tiles(self):
        for i in range(self.row_count):
            temp = []
            for j in range(self.col_count):
                x = int(i * self.tile_width)
                y = int(j * self.tile_height)
                temp.append(Tile(x, y, self.tile_width, self.tile_height, False, (0, 0, 0)))
            self.tiles.append(temp)

    def check_tile(self, pos):
        for row in self.tiles:
            for tile in row:
                if tile.collidepoint(pos[0], pos[1]):
                    tile.flip_state()

    def highlight_tile(self, pos):
        for row in self.tiles:
            for tile in row:
                if tile.collidepoint(pos[0], pos[1]):
                    tile.set_color((255, 0, 0))
                else:
                    if tile.get_state():
                        tile.set_color((255, 255, 255))
                    else:
                        tile.set_color((0, 0, 0))

    def update_tiles(self):
        # This is so ugly it isn't funny, IDK why but doing it the ideal way wasn't working, pointer issue???
        # IDK because lists don't use pointers when copying/=. Changes to the tiles list during the iteration
        # were impacting other tiles during the iteration
        b_list = []
        r_list = []

        for i in range(self.row_count):
            tb_list = []
            tr_list = []
            for j in range(self.col_count):
                tb_list.append(self.tiles[i][j].get_state())
                tr_list.append(False)
            b_list.append(tb_list)
            r_list.append(tr_list)

        for i in range(self.row_count):
            for j in range(self.col_count):
                tile = b_list[i][j]
                c = 0
                # Top Left
                if i == 0 and j == 0:
                    if b_list[i + 1][j]:
                        c += 1
                    if b_list[i][j + 1]:
                        c += 1
                    if b_list[i + 1][j + 1]:
                        c += 1
                    if b_list[self.row_count - 1][j + 1]:
                        c += 1
                    if b_list[i][self.col_count - 1]:
                        c += 1
                    if b_list[self.row_count - 1][j]:
                        c += 1
                    if b_list[i + 1][self.col_count - 1]:
                        c += 1
                    if b_list[self.row_count - 1][self.col_count - 1]:
                        c += 1
                # Top Right
                elif i == self.row_count - 1 and j == 0:
                    if b_list[i - 1][j]:
                        c += 1
                    if b_list[i][j + 1]:
                        c += 1
                    if b_list[i - 1][j + 1]:
                        c += 1
                    if b_list[0][j]:
                        c += 1
                    if b_list[0][j + 1]:
                        c += 1
                    if b_list[i][self.col_count - 1]:
                        c += 1
                    if b_list[i - 1][self.col_count - 1]:
                        c += 1
                    if b_list[0][self.col_count - 1]:
                        c += 1
                # Bottom Right
                elif i == self.row_count - 1 and j == self.col_count - 1:
                    if b_list[i - 1][j]:
                        c += 1
                    if b_list[i][j - 1]:
                        c += 1
                    if b_list[i - 1][j - 1]:
                        c += 1
                    if b_list[0][j]:
                        c += 1
                    if b_list[0][j - 1]:
                        c += 1
                    if b_list[i][0]:
                        c += 1
                    if b_list[i - 1][0]:
                        c += 1
                    if b_list[0][0]:
                        c += 1
                # Bottom Left
                elif i == 0 and j == self.col_count - 1:
                    if b_list[i + 1][j]:
                        c += 1
                    if b_list[i][j - 1]:
                        c += 1
                    if b_list[i + 1][j - 1]:
                        c += 1
                    if b_list[self.row_count - 1][j]:
                        c += 1
                    if b_list[self.row_count - 1][j - 1]:
                        c += 1
                    if b_list[i][0]:
                        c += 1
                    if b_list[i + 1][0]:
                        c += 1
                    if b_list[self.row_count - 1][0]:
                        c += 1
                # Left side
                elif i == 0:
                    if b_list[i + 1][j]:
                        c += 1
                    if b_list[i][j - 1]:
                        c += 1
                    if b_list[i][j + 1]:
                        c += 1
                    if b_list[i + 1][j - 1]:
                        c += 1
                    if b_list[i + 1][j + 1]:
                        c += 1
                    if b_list[self.row_count - 1][j]:
                        c += 1
                    if b_list[self.row_count - 1][j - 1]:
                        c += 1
                    if b_list[self.row_count - 1][j + 1]:
                        c += 1
                # Top Side
                elif j == 0:
                    if b_list[i - 1][j]:
                        c += 1
                    if b_list[i + 1][j]:
                        c += 1
                    if b_list[i][j + 1]:
                        c += 1
                    if b_list[i - 1][j + 1]:
                        c += 1
                    if b_list[i + 1][j + 1]:
                        c += 1
                    if b_list[i][self.col_count - 1]:
                        c += 1
                    if b_list[i - 1][self.col_count - 1]:
                        c += 1
                    if b_list[i + 1][self.col_count - 1]:
                        c += 1
                # Right Side
                elif i == self.row_count - 1:
                    if b_list[i - 1][j]:
                        c += 1
                    if b_list[i][j - 1]:
                        c += 1
                    if b_list[i][j + 1]:
                        c += 1
                    if b_list[i - 1][j - 1]:
                        c += 1
                    if b_list[i - 1][j + 1]:
                        c += 1
                    if b_list[0][j - 1]:
                        c += 1
                    if b_list[0][j]:
                        c += 1
                    if b_list[0][j + 1]:
                        c += 1
                # Bottom Side
                elif j == self.col_count - 1:
                    if b_list[i - 1][j]:
                        c += 1
                    if b_list[i + 1][j]:
                        c += 1
                    if b_list[i][j - 1]:
                        c += 1
                    if b_list[i - 1][j - 1]:
                        c += 1
                    if b_list[i + 1][j - 1]:
                        c += 1
                    if b_list[i][0]:
                        c += 1
                    if b_list[i - 1][0]:
                        c += 1
                    if b_list[i + 1][0]:
                        c += 1
                # Center
                else:
                    if b_list[i - 1][j]:
                        c += 1
                    if b_list[i + 1][j]:
                        c += 1
                    if b_list[i][j - 1]:
                        c += 1
                    if b_list[i][j + 1]:
                        c += 1
                    if b_list[i - 1][j - 1]:
                        c += 1
                    if b_list[i - 1][j + 1]:
                        c += 1
                    if b_list[i + 1][j - 1]:
                        c += 1
                    if b_list[i + 1][j + 1]:
                        c += 1
                if tile and (c == 2 or c == 3):
                    r_list[i][j] = True
                if not tile and (c == 3):
                    r_list[i][j] = True
                if not ((tile and (c == 2 or c == 3)) or (not tile and (c == 3))):
                    r_list[i][j] = False
        for i in range(self.row_count):
            for j in range(self.col_count):
                self.tiles[i][j].set_state(r_list[i][j])

    def generate_snapshot(self):
        return self.tiles

    def reset(self):
        self.tiles.clear()
        self.gen_tiles()


def draw_frame():
    screen = display.get_screen()
    display_buffer = game.generate_snapshot()
    screen.fill((255, 255, 255))
    tile_width = width / col_count
    tile_height = height / row_count
    for row in display_buffer:
        for tile in row:
            pygame.draw.rect(screen, tile.get_color(), tile)
    for i in range(col_count + 1):
        p1 = i * tile_width, 0
        p2 = i * tile_width, height
        pygame.draw.line(screen, (15, 15, 15), p1, p2, line_width)
    for i in range(row_count + 1):
        p1 = 0, i * tile_height
        p2 = width, i * tile_height
        pygame.draw.line(screen, (15, 15, 15), p1, p2, line_width)


def rand_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


def run():
    running = True
    total_time = 0
    cur_time = pygame.time.get_ticks()
    last_time = 0
    delay = 50
    playing = False
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.check_tile(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                if event.key == pygame.K_UP:
                    delay -= 25
                if event.key == pygame.K_DOWN:
                    delay += 25
                if event.key == pygame.K_c:
                    game.reset()

        game.highlight_tile(pygame.mouse.get_pos())

        last_time = cur_time
        cur_time = pygame.time.get_ticks()
        total_time += cur_time - last_time
        if total_time > delay:
            if playing:
                game.update_tiles()
            total_time -= delay
        draw_frame()

        if not playing:
            display.get_screen().blit(font.render('Game Paused!', True, (255, 127, 0)), (10, 5))
        else:
            display.get_screen().blit(font.render('Game Running!', True, (255, 127, 0)), (10, 5))

        display.get_screen().blit(font.render('Delay: {0}'.format(delay), True, (255, 127, 0)), (10, 30))

        display.get_screen().blit(font.render('Press \'C\' to clear!', True, (255, 127, 0)), (10, 55))

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


line_width = 1
row_count = 80
col_count = 80
width = 800
height = 800
is_full_screen = False

pygame.init()
pygame.display.set_caption("Game Of Py")
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
display = Display(width, height, is_full_screen)
game = Game(width, height, row_count, col_count)
clock = pygame.time.Clock()
run()