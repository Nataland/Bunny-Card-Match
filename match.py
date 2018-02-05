import pygame
import time
from random import shuffle

# Created by natalie on 2018-01-18

pygame.init()

display_width = 900
display_height = 600
image_width = 150
image_height = 150
level = 1  # Todo: add logic to allow user to select level

# set up the difficulty for each level
if level == 0:
    num_image_in_a_row = 3
    num_image_in_a_column = 2
elif level == 1:
    num_image_in_a_row = 6
    num_image_in_a_column = 4
elif level == 2:
    num_image_in_a_row = 12
    num_image_in_a_column = 8

# colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Bunny Match')
clock = pygame.time.Clock()

win = False
original = []

# initialize the position of all concealed images
for i in range(12):
    original.append(i)
    original.append(i)

shuffle(original)

concealed = list(original)
flipped = []
found = []
missed = 0
first_card = []
has_first = False
has_second = False
second_card = []
first_flip_time = 0
second_flip_time = 0
show_time = 1


# Todo: randomize which bundle the images come from
def load_card_face(image_id):
    card = "./bundle2/img%s.JPG" % image_id
    img = pygame.image.load(card)
    return img


def load_card_back():
    card = "./cardback/card_back2.JPG"
    img = pygame.image.load(card)
    return img


def calculate_coord(index):
    y = int(index / 6)
    x = index - y * 6
    return [x, y]


def load_images():
    for n, j in enumerate(concealed):
        card_coord = calculate_coord(n)
        if (j == 's') or (j == 'f'):
            img = load_card_face(original[n])
        else:
            img = load_card_back()
        gameDisplay.blit(img, (card_coord[0] * image_width, card_coord[1] * image_height))


def identify_card(position_pressed):
    x_coord = int(position_pressed[0] / image_width)
    y_coord = int(position_pressed[1] / image_height)
    card = [x_coord, y_coord]
    return card


def calculate_index(card_pos):
    return card_pos[1] * 6 + card_pos[0]


def show_card(card_pos):
    if card_pos:
        concealed[calculate_index(card_pos)] = 's'


def flip_card(card_pos):
    if card_pos:
        concealed[calculate_index(card_pos)] = 'f'


def hide_card(card_pos):
    if card_pos:
        ind = calculate_index(card_pos)
        if concealed[ind] == 's':
            concealed[ind] = original[ind]


def check_same(card1, card2):
    if card1 and card2:
        return original[calculate_index(card1)] == original[calculate_index(card2)]


# run game using a while loop
while not win:
    ev = pygame.event.get()
    key = pygame.key.get_pressed()
    for event in ev:
        if event.type == pygame.QUIT:
            win = True
        elif event.type == pygame.MOUSEBUTTONUP:
            card_flipped = identify_card(pygame.mouse.get_pos())
            card_index = calculate_index(card_flipped)
            if concealed[card_index] != 's' and concealed[card_index] != 'f':
                if not has_first:
                    first_flip_time = time.time()
                    first_card = card_flipped
                    show_card(card_flipped)
                    is_first_flip = False
                    has_first = True
                elif not has_second:
                    second_flip_time = time.time()
                    second_card = card_flipped
                    show_card(card_flipped)
                    has_second = True

    if has_first and has_second and check_same(first_card, second_card):
        flip_card(first_card)
        flip_card(second_card)
    if has_second and (time.time() - second_flip_time > show_time):
        hide_card(second_card)
        hide_card(first_card)
        has_first = has_second = False
    load_images()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
