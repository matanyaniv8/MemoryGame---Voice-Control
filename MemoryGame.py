import pygame
import random
import sys


class MemoryGame:
    def __init__(self):
        pygame.init()
        screen_info = pygame.display.Info()
        self.screen_width = int(screen_info.current_w * 0.5)
        self.screen_height = int(screen_info.current_h * 0.8)
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
        self.card_size = min(self.screen_width // self.cols, self.screen_height // self.rows) - 15
        self.selected = []
        self.matches = set()
        random.shuffle(self.colors)
        self.font = pygame.font.Font(None, 40)
        self.start_ticks = pygame.time.get_ticks()
        self.match_sound = pygame.mixer.Sound('./res/match_sound.wav')
        self.reset_button_rect = pygame.Rect(0, 0, 1, 1)  # Placeholder initialization
        self.player_count = 0  # Initial state, not yet chosen
        self.current_player = 1

    def draw_reset_button(self, btn_text="Reset"):
        button_width = 120
        button_height = 40
        button_x = self.screen_width / 2 - button_width / 2
        button_y = self.screen_height - button_height - 20
        self.reset_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, pygame.Color('dodgerblue'), self.reset_button_rect)
        text_surface = self.font.render(btn_text, True, pygame.Color('white'))
        text_rect = text_surface.get_rect(center=self.reset_button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_player_choice_buttons(self):
        btn_1p_width = 120
        btn_1p_height = 40
        btn_1p_x = self.screen_width / 4 - btn_1p_width / 2
        btn_2p_x = self.screen_width * 3 / 4 - btn_1p_width / 2
        btn_y = self.screen_height / 2 - btn_1p_height / 2
        self.btn_1player_rect = pygame.Rect(btn_1p_x, btn_y, btn_1p_width, btn_1p_height)
        self.btn_2player_rect = pygame.Rect(btn_2p_x, btn_y, btn_1p_width, btn_1p_height)

        pygame.draw.rect(self.screen, pygame.Color('skyblue'), self.btn_1player_rect)
        pygame.draw.rect(self.screen, pygame.Color('skyblue'), self.btn_2player_rect)

        text_1p = self.font.render("1 Player", True, pygame.Color('white'))
        text_2p = self.font.render("2 Players", True, pygame.Color('white'))

        self.screen.blit(text_1p, (btn_1p_x + 10, btn_y + 10))
        self.screen.blit(text_2p, (btn_2p_x + 10, btn_y + 10))

    def draw_cards(self):
        margin = 5  # A small margin between cards
        for row in range(self.rows):
            for col in range(self.cols):
                index = row * self.cols + col
                # Calculate x and y position of the card with margins
                x_pos = col * self.card_size + margin
                y_pos = row * self.card_size + margin
                rect = pygame.Rect(x_pos, y_pos, self.card_size - margin * 2, self.card_size - margin * 2)
                if index in self.matches or index in self.selected:
                    pygame.draw.rect(self.screen, self.colors[index], rect)
                else:
                    pygame.draw.rect(self.screen, self.hidden_color, rect)
                pygame.draw.rect(self.screen, self.text_color, rect, 3)  # Card border
                self.update_and_show_timer()

    def update_and_show_timer(self):
        current_ticks = pygame.time.get_ticks()
        elapsed_seconds = (current_ticks - self.start_ticks) // 1000
        timer_text = f"Time: {elapsed_seconds // 60}:{elapsed_seconds % 60:02d}"
        text_surface = self.font.render(timer_text, True, self.text_color)
        self.screen.blit(text_surface, (10, self.screen_height - 30))  # Positioning the timer at the bottom left

    def draw_current_player_indicator(self):
        if self.player_count == 2:
            display_text = f"Player {self.current_player}'s Turn"
            text_surface = self.font.render(display_text, True, self.text_color)
            self.screen.blit(text_surface, (10, 10))

    def reset_game(self):
        random.shuffle(self.colors)
        self.matches.clear()
        self.selected.clear()
        self.start_ticks = pygame.time.get_ticks()
        self.current_player = 1  # Reset to player 1 for a new game

    def check_for_match(self):
        if len(self.selected) == 2:
            index1, index2 = self.selected
            if self.colors[index1] == self.colors[index2]:
                self.matches.update(self.selected)
                self.match_sound.play()
                if self.player_count == 1 or (self.player_count == 2 and len(self.matches) < len(self.colors)):
                    self.selected.clear()  # Clear selection only if the game continues
            else:
                return True  # Indicates a need to flip back cards
        return False

    def run(self):
        running = True
        flip_back_time = None

        while running:
            current_time = pygame.time.get_ticks()
            self.screen.fill(self.bg_color)

            if self.player_count == 0:  # Player hasn't chosen single or two-player mode yet
                self.draw_player_choice_buttons()
            else:
                if flip_back_time and current_time >= flip_back_time:
                    self.selected.clear()
                    flip_back_time = None
                    if self.player_count == 2:
                        self.current_player = 2 if self.current_player == 1 else 1

                self.draw_cards()
                self.draw_current_player_indicator()
                self.draw_reset_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.player_count == 0:
                        if self.btn_1player_rect.collidepoint(x, y):
                            self.player_count = 1
                            self.reset_game()
                        elif self.btn_2player_rect.collidepoint(x, y):
                            self.player_count = 2
                            self.reset_game()
                    elif self.reset_button_rect.collidepoint(x, y):
                        self.reset_game()
                    elif self.player_count and not flip_back_time:
                        margin = 5  # Assuming this is the same margin used in draw_cards
                        col = (x - margin) // self.card_size
                        row = (y - margin) // self.card_size
                        index = row * self.cols + col
                        if index < len(self.colors) and index not in self.matches and index not in self.selected:
                            self.selected.append(index)
                            if self.check_for_match():
                                flip_back_time = current_time + 1000

            pygame.display.flip()


if __name__ == '__main__':
    game = MemoryGame()
    game.run()
