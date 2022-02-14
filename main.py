import pygame
import os
import sys


global stad
stad = 1
size = width, height = 900, 550
screen = pygame.display.set_mode(size)
running = True


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_screen():
    pygame.font.init()
    fon = pygame.transform.scale(load_image('fon.png'), size)
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 30)
    text_coord = 25
    all_group = pygame.sprite.Group()
    fonp = pygame.sprite.Sprite()
    fonp.image = pygame.transform.scale(load_image("fonp.png"), (300, 150))
    all_group.add(fonp)
    fonp.rect = fonp.image.get_rect()
    fonp.rect.x = 300
    fonp.rect.y = 400
    all_group.draw(screen)


def get_click(mouse_pos):
    global stad
    cell = mouse_pos
    if (cell[0] >= 300 and cell[1] >= 400) and (cell[0] <= 600 and cell[1] <= 550) and stad == 1:
        stad = 2


class Wall(pygame.sprite.Sprite):
    image = load_image("wall.png")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Wall.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y - 50

    def update(self, *cords):
        self.rect = self.rect.move(*cords)


class Floor(pygame.sprite.Sprite):
    image = load_image("floor.png")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Floor.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *cords):
        self.rect = self.rect.move(*cords)


class Finish(pygame.sprite.Sprite):
    image = load_image("Finish.png")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Finish.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self, *cords):
        self.rect = self.rect.move(*cords)


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")
    image_move = load_image("player_move.png")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def collide(self, object):
        for i in object:
            if pygame.sprite.collide_mask(self, i):
                return True
        return False

    def update(self, *cords):
        self.rect = self.rect.move(*cords)

    def animation(self, move):
        if move != (0, 0):
            self.image = Player.image_move
        else:
            self.image = Player.image


def maze(screen):
    form = 50
    layer3_sprites = pygame.sprite.Group()
    layer2_sprites_standing = pygame.sprite.Group()
    layer1_sprites = pygame.sprite.Group()
    layer_for_finish = pygame.sprite.Group()
    screen.fill(pygame.Color("grey"))
    map = open("map1.txt", encoding="utf8").readlines()
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == "W":
                Wall(x * form, y * form, layer3_sprites)
            if map[y][x] == "f":
                Floor(x * form, y * form, layer1_sprites)
            elif map[y][x] == "S":
                Floor(x * form, y * form, layer1_sprites)
                start_x, start_y = x, y
            elif map[y][x] == "F":
                Finish(x * form, y * form, layer_for_finish)
                pass
    player = Player(375, 375, layer2_sprites_standing)
    Player(375, 375, layer2_sprites_standing)
    layer1_sprites.update(start_x * -form + 400, start_y * -form + 425)
    layer3_sprites.update(start_x * -form + 400, start_y * -form + 425)
    layer_for_finish.update(start_x * -form + 400, start_y * -form + 425)
    run = True
    clock = pygame.time.Clock()
    v = 6
    pygame.key.set_repeat(1, 10)
    fps = 60
    while run:
        move = 0, 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_UP]:
                move = 0, int(v)
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_DOWN]:
                move = 0, int(-v)
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_LEFT]:
                move = int(v), 0
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_RIGHT]:
                move = int(-v), 0
        if player.collide(layer_for_finish):
            run = False
        screen.fill(pygame.Color("grey"))
        if player.collide(layer3_sprites):
            move = -1 * move[0], -1 * move[1]
        layer3_sprites.update(move)
        layer1_sprites.update(move)
        layer_for_finish.update(move)
        if player.collide(layer3_sprites):
            move = -1 * move[0], -1 * move[1]
            layer3_sprites.update(move)
            layer1_sprites.update(move)
            layer_for_finish.update(move)
        player.animation(move)
        layer1_sprites.draw(screen)
        layer_for_finish.draw(screen)
        layer2_sprites_standing.draw(screen)
        layer3_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
        global stad
        stad = 3
    pass


def end():
    fon = pygame.transform.scale(load_image('end.png'), size)
    screen.blit(fon, (0, 0))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            get_click(event.pos)
    if stad == 1:
        start_screen()
    elif stad == 2:
        maze(screen)
    elif stad == 3:
        end()
    pygame.display.flip()
pygame.quit()