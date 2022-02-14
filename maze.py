import sys
import os
import pygame
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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


def maze(screen, map):
    end = True
    back_color = "black"
    form = 50
    layer3_sprites = pygame.sprite.Group()
    layer2_sprites_standing = pygame.sprite.Group()
    layer1_sprites = pygame.sprite.Group()
    layer_for_finish = pygame.sprite.Group()
    screen.fill(pygame.Color(back_color))
    map = open(map, encoding="utf8").readlines()
    start_and_finish = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == "W":
                Wall(x * form, y * form, layer3_sprites)
            if map[y][x] == "f":
                Floor(x * form, y * form, layer1_sprites)
            elif map[y][x] == "S":
                Floor(x * form, y * form, layer1_sprites)
                start_and_finish.append((x, y))
    #                Finish(x * form, y * form, layer_for_finish)
    cord = random.randint(0, len(start_and_finish) - 1)
    start_x, start_y = start_and_finish[cord]
    del start_and_finish[cord]
    finish_x, finish_y = start_and_finish[random.randint(0, len(start_and_finish) - 1)]
    Finish(finish_x * form, finish_y * form, layer_for_finish)
    player = Player(375, 375, layer2_sprites_standing)
    Player(375, 375, layer2_sprites_standing)
    layer1_sprites.update(start_x * -form + 400, start_y * -form + 425)
    layer3_sprites.update(start_x * -form + 400, start_y * -form + 425)
    layer_for_finish.update(start_x * -form + 400, start_y * -form + 425)
    run = True
    clock = pygame.time.Clock()
    fps = 60
    v = 25
    pygame.key.set_repeat(1, 5)
    while run:
        move = 0, 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                end = False
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_UP]:
                move = 0, int(v / (fps / 30))
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_DOWN]:
                move = 0, int(-v / (fps / 30))
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_LEFT]:
                move = int(v / (fps / 30)), 0
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_RIGHT]:
                move = int(-v / (fps / 30)), 0
        if player.collide(layer_for_finish):
            run = False
        screen.fill(pygame.Color(back_color))
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
        layer3_sprites.draw(screen)
        layer_for_finish.draw(screen)
        layer2_sprites_standing.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    return end


def end_screen(screen, time):
    end = True
    back_color = "black"
    screen.fill(pygame.Color(back_color))
    font = pygame.font.Font(None, 50)
    text = font.render(time, True, (100, 255, 100))
    text_x = 800 // 2 - text.get_width() // 2
    text_y = 850 // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))
    text = font.render("Заново", True, (100, 255, 100))
    text_x = 800 - text.get_width()
    text_y = 850 - text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_RIGHT]:
                run = False
            if event.type == pygame.QUIT:
                run = False
                end = False
            if event.type == event.type == pygame.MOUSEBUTTONDOWN:
                if 800 - text.get_width() < event.pos[0] < 800 and 850 - text.get_height() < event.pos[1] < 850:
                    run = False
    return end


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 850))
    #    start_screen()
    run = True
    while run:
        start_time = pygame.time.get_ticks()
        if not maze(screen, "map1.txt"):
            run = False
        finish_time = pygame.time.get_ticks()
        time = F"""Время:   {str((finish_time - start_time) // 60000)}:{str((finish_time - start_time) // 1000 % 60)}"""
        start_time = pygame.time.get_ticks()
        if not end_screen(screen, time):
            run = False
        end_screen(screen, time)
    pygame.quit()