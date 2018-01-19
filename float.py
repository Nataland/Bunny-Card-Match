import pygame, sys
from random import randint
from pygame.locals import *

# Created by natalie on 2018-01-18

def card_display(img, x, y):
    gameDisplay.blit(img, (x, y))


def card_load(id):
    card = "./img/IMG_%s.JPG" % id
    card_load = pygame.image.load(card)
    return card_load


def card(x, y):
    for i in range(0, list_of_img_len - 1):
        bunny_img = card_load(list_of_img[i])
        card_display(bunny_img, x[i], y[i])


pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Bunny Match')
clock = pygame.time.Clock()

x = (display_width * 0.45)
y = (display_height * 0.8)

# todo: make images the same size and add them to the list, RNG to generate initial location
# todo: logic to import all image in one directory and cut images?
list_of_img = [3112, 3118, 3110, 3110, 3116, 3120, 3125]
list_of_x = [0, display_width * 0.1, display_width * 0.2,
             display_width * 0.3, display_width * 0.4, display_width * 0.5]
list_of_y = [display_height * 0.5, display_height * 0.6, display_height * 0.7,
             display_height * 0.8, display_height * 0.9, display_height]
list_of_img_len = len(list_of_img)

displaying = True

while displaying:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win = True

        print(event)

    gameDisplay.fill(white)

    # todo: make this a function with logic to bounce images
    for i in range(0, list_of_img_len - 1):
        if (list_of_x[i] >= 0) & (list_of_x[i] <= display_width):
            list_of_x[i] -= 1
        else:
            list_of_x[i] += 1
        if (list_of_y[i] >= 0) & (list_of_y[i] <= display_height):
            list_of_y[i] -= 1
        else:
            list_of_x[i] += 1
    card(list_of_x, list_of_y)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
