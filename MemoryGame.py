import pygame
import random

pygame.init()

screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

bg_color = pygame.Color('white')
hidden_color = pygame.Color('grey')
text_color = pygame.Color('black')
colors = [pygame.Color('red'), pygame.Color('green'), pygame.Color('blue'), pygame.Color('yellow'),
          pygame.Color('cyan'), pygame.Color('magenta'), pygame.Color('orange'), pygame.Color('purple')]
colors *= 2  # Duplicate colors for pairs

rows = 4
cols = 4
card_width = screen_width // cols
card_height = screen_height // rows
hidden = True
matches = set()
selected = []

random.shuffle(colors)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and len(selected) < 2:
            x, y = event.pos
            col_index = x // card_width
            row_index = y // card_height
            index = row_index * cols + col_index  # Adjusted calculation
            if index not in matches and index not in selected:
                selected.append(index)
            if len(selected) == 2 and colors[selected[0]] == colors[selected[1]]:
                matches.update(selected)
                selected = []
            elif len(selected) == 2:
                pygame.time.wait(500)  # Wait half a second
                selected = []

    screen.fill(bg_color)
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            rect = pygame.Rect(col * card_width, row * card_height, card_width, card_height)
            if index in matches or index in selected:
                pygame.draw.rect(screen, colors[index], rect)
            else:
                pygame.draw.rect(screen, hidden_color, rect)
            pygame.draw.rect(screen, text_color, rect, 3)  # Draw border

    pygame.display.flip()

pygame.quit()
