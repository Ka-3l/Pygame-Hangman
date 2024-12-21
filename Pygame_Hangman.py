import pygame
import random
import os

pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Hangman')

FPS = 30
clock = pygame.time.Clock()
run = True
lives = 7
os.chdir(r'C:\Users\asus\Desktop\Coding Stuff\Hangman_Assets')

# fonts
font_heading = pygame.font.SysFont('Myfont-Regular', 200)
font_sub = pygame.font.SysFont('Myfont-Regular', 100)

#images
hangman_images = [
    pygame.transform.scale(pygame.image.load(f'hangman{i}.png'), (500, 551))
    for i in range(8)
]

letters = list('abcdefghijklmnopqrstuvwxyz')
hangman_letters = [
    pygame.transform.scale(pygame.image.load(f'letter_{letter}.png'), (120, 110))
    for letter in letters
]
letter_blank = pygame.transform.scale(pygame.image.load('letter_blank.png'), (120,110))
letter_wrong = pygame.transform.scale(pygame.image.load('letter_wrong.png'), (130,145))
underline = pygame.image.load('underline.png')

#word categories
categories = {
    "Math": ['ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', 'ABSCISSA',
             'ORDINATE', 'CARTESIAN', 'PYTHAGOREAN', 'GEOMETRY', 'CALCULUS', 'TRIANGLE', 'ANGLE'],
    "Programming": ['PYTHON', 'FUNCTION', 'STRING', 'FLOAT', 'TUPLE', 'SET', 'LIST', 'CSS',
                    'FLOWCHART', 'PROGRAM', 'SOFTWARE', 'INTEGER', 'BINARY', 'BOOLEAN'],
    "Science": ['ORGANIC', 'CHEMISTRY', 'BIOLOGY', 'HYDROCARBON', 'CATENATION', 'ELEMENT',
                'HYDROGEN', 'CARBON', 'CHLORINE', 'NITROGEN', 'ARGON', 'SOLID', 'LIQUID',
                'GAS', 'PLASMA', 'MATTER', 'MASS'],
}

# button variables
radius = 60
start_x = WIDTH // 14
start_y = 800
buttons = []
for i in range(26):
    x = start_x + (start_x * (i % 13))
    y = start_y + (start_x * (i // 13))
    buttons.append({'rect':pygame.Rect(x - radius, y - radius, radius * 2, radius * 2), 'letter': (letters[i]).upper(), 'state': False })

# button click checker
correct_guess = set()
def button_clicked(mouse_pos): 
    ''' Checks if a letter button has been clicked'''
    global lives
    for button in buttons:
        if button['rect'].collidepoint(mouse_pos) and button['state'] == False:
            button['state'] = True
            letter = button['letter']
            if letter in hangman_word:
                correct_guess.add(letter)
            else:
                lives -= 1

# Category choice
text_hangman = font_heading.render('Hangman!', 1, (0,0,0))
text_choose = font_sub.render('Pick a category:', 1, (0,0,0))

def render_categories():
    '''Render category buttons and return their rectangle'''
    spacing = 200  
    total_width = sum(font_sub.size(category)[0] for category in categories) + spacing * (len(categories) - 1)
    x_start = WIDTH // 2 - total_width // 2 
    y_start = 500

    rects = {}
    current_x = x_start 

    for category, words in categories.items():
        text = font_sub.render(category, True, (0, 0, 0))
        rect = pygame.Rect(current_x, y_start, text.get_width(), text.get_height())
        screen.blit(text, (current_x, y_start))
        rects[category] = rect
        current_x += text.get_width() + spacing 

    return rects

def pick_category():
    '''Handle category selection and return the chosen word'''
    while True:
        screen.fill((255, 255, 255))
        screen.blit(text_hangman, (WIDTH // 2 - text_hangman.get_width() // 2, 100))
        screen.blit(text_choose, (WIDTH // 2 - text_choose.get_width() // 2, 130 + text_hangman.get_height()))
        rects = render_categories()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for category, rect in rects.items():
                    if rect.collidepoint(event.pos):
                        return list(random.choice(categories[category]))

def reset_game():
    '''Reset game variables for a new round'''
    global lives, correct_guess, hangman_word, buttons
    lives = 7
    correct_guess.clear()
    hangman_word = pick_category()
    # Reset button states
    for button in buttons:
        button['state'] = False

hangman_word = pick_category()

# Displays an underline asset for each letter in hangman word
max_width = WIDTH - (300 + hangman_images[0].get_width())
rect_x = 200 + hangman_images[0].get_width()
rect_y = 100
underline_rect = pygame.Rect(rect_x, rect_y, max_width, hangman_images[0].get_height())

max_underline_width = max_width // (len(hangman_word) + 1)
spacing = max_underline_width // 5

total_width = max_underline_width * len(hangman_word) + spacing * (len(hangman_word) - 1)
if total_width > max_width:
    spacing = (max_width - (max_underline_width * len(hangman_word))) // (len(hangman_word) - 1)
    total_width = (max_underline_width * len(hangman_word)) + (spacing * (len(hangman_word) - 1))

max_underline_height = underline.get_height()
start_underline_x = rect_x + (max_width - total_width) // 2
underline_y = rect_y + (hangman_images[0].get_height() - max_underline_height)//2


font_letter_display = pygame.font.SysFont('Myfont-Regular', max_underline_width)

# main loop
while run:
    clock.tick(FPS)
    screen.fill((255,255,255))

    # buttons, hangman image
    screen.blit(hangman_images[lives], (100,100))

    for i, button in enumerate(buttons):
        rect = button['rect']
        letter = button['letter']
        x, y = rect.center
        if not button['state']:
            screen.blit(hangman_letters[i], (x - radius, y - radius))
        elif button['letter'] in hangman_word:
            screen.blit(letter_blank, (x - radius, y - radius))
        else:
            screen.blit(letter_wrong, (x - radius - 5, y - radius - 20))

    # underline display
    for i, letter in enumerate(hangman_word):
        start_x = start_underline_x + i * (max_underline_width + spacing)
        underline_scaled = pygame.transform.scale(underline, (max_underline_width, max_underline_height))
        if letter in correct_guess:
            text = font_letter_display.render(letter, 1, (0,0,0))
            screen.blit(text, (start_x + (max_underline_width - text.get_width())//2, underline_y - (text.get_height())//2))
        else:
            screen.blit(underline_scaled, (start_x, underline_y))

    pygame.display.update() 

    # lose checker
    if lives == 0:
        screen.fill((255,255,255))
        lose_text = font_heading.render('You Lose!', 1,(0,0,0))
        screen.blit(lose_text, ((WIDTH - lose_text.get_width() )//2, (HEIGHT - lose_text.get_height())//2))
        pygame.display.update() 
        pygame.time.delay(3000)
        reset_game()

    # win checker
    elif all(letter in correct_guess for letter in hangman_word):
        screen.fill((255,255,255))
        win_text = font_heading.render('You Win!', 1,(0,0,0))
        screen.blit(win_text, ((WIDTH - win_text.get_width() )//2, (HEIGHT - win_text.get_height())//2))
        pygame.display.update()
        pygame.time.delay(3000) 
        reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos() 
            button_clicked(mouse_pos)
pygame.quit()