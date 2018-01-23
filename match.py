import pygame
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

concealed = original
flipped = []


def load_card_face(image_id):
    card = "./img/img%s.JPG" % image_id
    img = pygame.image.load(card)
    return img


def load_card_back():
    card = "./cardback/card_back.JPG"
    img = pygame.image.load(card)
    return img


def load_images():
    for w in range(6):
        for h in range(4):
            img_id = original[h * 6 + w]
            if img_id in concealed:
                img = load_card_back()
            else:
                img = load_card_face(original[img_id])
            gameDisplay.blit(img, (w * image_width, h * image_height))


def identify_card(position_pressed):
    x_coord = int(position_pressed[0] / image_width)
    y_coord = int(position_pressed[1] / image_height)
    card = (x_coord, y_coord)
    return card


first_flip = True
card_flipped = (10, 10)

# run game using a while loop
while not win:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win = True

        # Todo: read mouse click
        # if event.type == pygame.MOUSEBUTTONUP:
        #     clicked_position = pygame.mouse.get_pos()
        #     card_flipped = identify_card(clicked_position)
        #     print(card_flipped)
        #     if first_flip:
        #         first_card = card_flipped
        #         first_flip = False
        #     else:
        #         second_card = card_flipped
        #         if first_card == second_card:
        #             flipped.append(second_card)
        #             if second_card in concealed:
        #                 concealed.remove(second_card)
        #         first_flip = False

        print(event)

    load_images()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
