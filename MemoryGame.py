import pygame
import random
import sys  # Import sys module

pygame.init()

# Get user's screen size
infoObject = pygame.display.Info()
screen_width = infoObject.current_w
screen_height = infoObject.current_h

# Example: Decide to use 50% of the screen width and 50% of the screen height for the board
screen_width = int(screen_width * 0.5)
screen_height = int(screen_height * 0.5)

# Load matching sound effect.
match_sound = pygame.mixer.Sound('./res/match_sound.wav')

bg_color = pygame.Color('white')
hidden_color = pygame.Color('grey')
text_color = pygame.Color('black')
colors = [pygame.Color('red'), pygame.Color('green'), pygame.Color('blue'), pygame.Color('yellow'),
          pygame.Color('cyan'), pygame.Color('magenta'), pygame.Color('orange'), pygame.Color('purple')]
colors *= 2  # Duplicate colors for pairs

rows = 4
cols = 4
card_width = screen_width // cols
card_height = screen_height // rows - 10
screen = pygame.display.set_mode((screen_width, screen_height))
matches = set()
selected = []

random.shuffle(colors)

# Initialize font for timer
font = pygame.font.Font(None, 36)

# Start time
start_ticks = pygame.time.get_ticks()

# Added for flip back mechanism
flip_back_time = 0
waiting_to_flip_back = False

running = True
while running:
    current_time = pygame.time.get_ticks()
    if waiting_to_flip_back and current_time >= flip_back_time:
        selected = []  # Reset selected cards
        waiting_to_flip_back = False  # No longer waiting

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and len(selected) < 2 and not waiting_to_flip_back:
            x, y = event.pos
            col_index = x // card_width
            row_index = y // card_height
            index = row_index * cols + col_index
            if index not in matches and index not in selected:
                selected.append(index)
            if len(selected) == 2:
                if colors[selected[0]] == colors[selected[1]]:
                    matches.update(selected)
                    selected = []
                    # Play the match sound
                    match_sound.play()
                else:
                    flip_back_time = current_time + 1000  # Set flip back time to 1 second later
                    waiting_to_flip_back = True

    screen.fill(bg_color)
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            rect = pygame.Rect(col * card_width, row * card_height, card_width, card_height)
            if index in matches or index in selected:
                pygame.draw.rect(screen, colors[index], rect)
            else:
                pygame.draw.rect(screen, hidden_color, rect)
            pygame.draw.rect(screen, text_color, rect, 3)

    # Timer display at the bottom of the screen
    seconds = (current_time - start_ticks) // 1000  # Convert milliseconds to seconds
    timer_text = f"Time: {seconds // 60}:{seconds % 60:02d}"
    text_surface = font.render(timer_text, True, text_color)
    timer_x = screen_width // 2 - text_surface.get_width() // 2
    timer_y = screen_height - text_surface.get_height() - 10
    screen.blit(text_surface, (timer_x, timer_y))

    pygame.display.flip()
