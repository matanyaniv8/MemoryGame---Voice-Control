import pygame
import random
import sys


class MemoryGame:
    def __init__(self):
        pygame.init()
        screen_info = pygame.display.Info()
        self.screen_width = int(screen_info.current_w * 0.5)
        self.screen_height = int(screen_info.current_h * 0.5)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.bg_color = pygame.Color('white')
        self.hidden_color = pygame.Color('grey')
        self.text_color = pygame.Color('black')
        self.colors = [pygame.Color('red'), pygame.Color('green'), pygame.Color('blue'), pygame.Color('yellow'),
                       pygame.Color('cyan'), pygame.Color('magenta'), pygame.Color('orange'),
                       pygame.Color('purple')] * 2
        self.rows = 4
        self.cols = 4
        self.card_width = self.screen_width // self.cols
        self.card_height = self.screen_height // self.rows - 10
        self.selected = []
        self.matches = set()
        random.shuffle(self.colors)
        self.font = pygame.font.Font(None, 36)
        self.start_ticks = pygame.time.get_ticks()
        self.match_sound = pygame.mixer.Sound('./res/match_sound.wav')
        self.reset_button_rect = pygame.Rect(0, 0, 1, 1)  # Placeholder initialization

    def draw_reset_button(self, btn_text="Reset"):
        button_width = 120
        button_height = 40
        button_x = 0.5  # Left for Reset, center for Play Again
        button_y = self.screen_height - button_height

        reset_button_color = pygame.Color('dodgerblue')
        reset_button_rect = pygame.draw.rect(self.screen, reset_button_color,
                                             (button_x, button_y, button_width, button_height))
        text_surface = self.font.render(btn_text, True, pygame.Color('white'))
        text_rect = text_surface.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2))
        self.screen.blit(text_surface, text_rect)
        return reset_button_rect

    def reset_game(self):
        random.shuffle(self.colors)
        self.matches.clear()
        self.selected.clear()
        self.start_ticks = pygame.time.get_ticks()

    def draw_cards(self, selected_cards, current_time):
        for row in range(self.rows):
            for col in range(self.cols):
                index = row * self.cols + col
                rect = pygame.Rect(col * self.card_width, row * self.card_height, self.card_width, self.card_height)
                if index in self.matches or index in selected_cards:
                    pygame.draw.rect(self.screen, self.colors[index], rect)
                else:
                    pygame.draw.rect(self.screen, self.hidden_color, rect)
                pygame.draw.rect(self.screen, self.text_color, rect, 3)
                # Updates and show timer
                self.update_and_show_timer(current_time)

    def update_and_show_timer(self, current_time):
        # Timer display at the bottom of the screen
        seconds = (current_time - self.start_ticks) // 1000  # Convert milliseconds to seconds
        timer_text = f"Time: {seconds // 60}:{seconds % 60:02d}"
        text_surface = self.font.render(timer_text, True, self.text_color)
        timer_x = self.screen_width // 2 - text_surface.get_width() // 2
        timer_y = self.screen_height - text_surface.get_height() - 10
        self.screen.blit(text_surface, (timer_x, timer_y))

    def check_completion(self):
        return len(self.matches) == len(self.colors)

    def run(self):
        running = True
        flip_back_time = 0
        waiting_to_flip_back = False

        while running:
            current_time = pygame.time.get_ticks()

            if waiting_to_flip_back and current_time >= flip_back_time:
                self.selected.clear()  # Reset selected cards
                waiting_to_flip_back = False  # No longer waiting

            self.reset_button_rect = self.draw_reset_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.check_completion():
                        if self.reset_button_rect.collidepoint(x, y):
                            self.reset_game()
                    if self.reset_button_rect.collidepoint(x, y):
                        self.reset_game()
                    elif not waiting_to_flip_back:  # Handle game logic here
                        col_index = x // self.card_width
                        row_index = y // self.card_height
                        index = row_index * self.cols + col_index
                        if index not in self.matches and index not in self.selected:
                            self.selected.append(index)
                        if len(self.selected) == 2:
                            print(len(self.selected))
                            if self.check_completion():
                                self.selected.clear()
                            elif self.colors[self.selected[0]] == self.colors[self.selected[1]]:
                                self.matches.update(self.selected)
                                self.selected.clear()
                                self.match_sound.play()
                            else:
                                flip_back_time = current_time + 1000
                                waiting_to_flip_back = True

            self.screen.fill(self.bg_color)
            # Draw cards on board and update timer
            self.draw_cards(self.selected, current_time)

            if self.check_completion():
                message_surface = self.font.render('Well done!', True, self.text_color)
                message_rect = message_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
                self.screen.blit(message_surface, message_rect)
                self.reset_button_rect = self.draw_reset_button('Play Again')
            else:
                self.draw_reset_button('Reset')

            pygame.display.flip()


if __name__ == '__main__':
    game = MemoryGame()
    game.run()
