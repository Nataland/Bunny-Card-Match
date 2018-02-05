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
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
mmm_orange = (255, 136, 17)
mmm_orange_lite = (255, 157, 60)
mmm_yellow = (244, 208, 111)
mmm_blue = (157, 217, 210)
mmm_cream = (255, 248, 240)
mmm_purple = (57, 47, 90)
mmm_purple_lite = (93, 84, 120)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Bunny Memory-Match')
clock = pygame.time.Clock()

win = False
run = True
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
start_screen = True


def text_objects(text, font, colour):
    text_surface = font.render(text, True, colour)
    return text_surface, text_surface.get_rect()


def draw_start_screen(mouse, level):
    gameDisplay.fill(mmm_purple)
    draw_text(mmm_yellow, "fonts/ARCADE.TTF", 200, "MIFFY", (display_width / 2), 100)
    draw_text(mmm_yellow, "fonts/ARCADE.TTF", 58, "MEMORY-MATCH", (display_width / 2), 145)
    draw_text(mmm_cream, "fonts/ARCADE.TTF", 35, "Easy", (display_width / 2) + 26, 215)
    draw_text(mmm_cream, "fonts/ARCADE.TTF", 35, "Medium", (display_width / 2) + 26, 250)
    draw_text(mmm_cream, "fonts/ARCADE.TTF", 35, "Hard", (display_width / 2) + 26, 285)
    draw_interactive_button(mouse, 300, 50, 340, mmm_orange, mmm_orange_lite)
    draw_interactive_button(mouse, 300, 50, 410, mmm_orange, mmm_orange_lite)
    draw_interactive_button(mouse, 300, 50, 480, mmm_orange, mmm_orange_lite)
    pygame.draw.circle(gameDisplay, mmm_cream, (int(display_width / 2) - 56, 210), 9, 3)
    pygame.draw.circle(gameDisplay, mmm_cream, (int(display_width / 2) - 56, 245), 9, 3)
    pygame.draw.circle(gameDisplay, mmm_cream, (int(display_width / 2) - 56, 280), 9, 3)
    select_level()


def select_level():
    if level == 0:
        h = 210
    elif level == 1:
        h = 245
    else:
        h = 280
    pygame.draw.circle(gameDisplay, mmm_cream, (int(display_width / 2) - 56, h), 2)


def draw_win_screen():
    gameDisplay.fill(mmm_purple)
    draw_text(mmm_yellow, "fonts/ARCADE.TTF", 150, "Congrats!", (display_width / 2), 100)
    draw_text(mmm_yellow, "fonts/ARCADE.TTF", 58, "You found all the pieces", (display_width / 2), 170)


def draw_text(colour, font, size, content, center_x, center_y):
    text = pygame.font.Font(font, size)
    text_surf, text_rect = text_objects(content, text, colour)
    text_rect.center = (center_x, center_y)
    gameDisplay.blit(text_surf, text_rect)


def draw_interactive_button(mouse, w, h, y, colour, secondary_colour):
    # Todo: add text to the buttons, choose content, text size and text font
    x = display_width / 2 - w / 2
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, secondary_colour, (x, y, w, h))
    else:
        pygame.draw.rect(gameDisplay, colour, (x, y, w, h))


# Todo: randomize which bundle the images come from
def load_card_face(image_id):
    card = "./bundle1/img%s.JPG" % image_id
    img = pygame.image.load(card)
    return img


def load_card_back():
    card = "./cardback/card_back1.JPG"
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


def check_win():
    is_win = True
    for item in concealed:
        if isinstance(item, int):
            is_win = False
    return is_win


# run game using a while loop
while run:
    ev = pygame.event.get()
    key = pygame.key.get_pressed()
    for event in ev:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if start_screen:
                if event.key == pygame.K_RETURN:
                    start_screen = False
                elif event.key == pygame.K_DOWN:
                    if level == 0 or level == 1:
                        level += 1
                elif event.key == pygame.K_UP:
                    if level == 1 or level == 2:
                        level -= 1
                elif event.key == pygame.K_ESCAPE:
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
    win = check_win()

    mouse = pygame.mouse.get_pos()
    if start_screen:
        draw_start_screen(mouse, level)
    elif not win:
        load_images()
    else:
        draw_win_screen()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
