import pygame
import random
import sys


class MemoryGame:
    def __init__(self):
        pygame.init()
        screen_info = pygame.display.Info()
        self.screen_width = int(screen_info.current_w * 0.4)
        self.screen_height = int(screen_info.current_h * 0.8)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.bg_color = pygame.Color('white')
        self.hidden_color = pygame.Color('grey')
        self.text_color = pygame.Color('black')
        self.colors = [pygame.Color('red'), pygame.Color('green'), pygame.Color('blue'), pygame.Color('yellow'),
                       pygame.Color('cyan'), pygame.Color('magenta'), pygame.Color('orange'),
                       pygame.Color('purple')] * 2
        self.btn_2player_rect = None
        self.btn_1player_rect = None
        self.home_btn = pygame.Rect(0, 0, 100, 50)
        self.rows = 4
        self.cols = 4
        self.card_width = self.screen_width // self.cols
        self.card_height = self.screen_height // self.rows - 10
        self.card_size = min(self.screen_width // self.cols, self.screen_height // self.rows) - 40
        # gaps for each axis for centering the cards position.
        self.y_gap = 70
        self.x_gap = 80
        self.selected = []
        self.matches = set()
        random.shuffle(self.colors)
        self.font = pygame.font.Font(None, 40)
        self.start_ticks = pygame.time.get_ticks()
        self.match_sound = pygame.mixer.Sound('./res/match_sound.wav')
        self.reset_button_rect = pygame.Rect(0, 0, 1, 1)  # Placeholder initialization
        self.player_count = 0  # Initial state, not yet chosen
        self.current_player = 1
        # flip animation member
        self.flip_states = {}  # Tracks whether a card is flipping, and its progress
        # Attack mode members
        self.btn_time_attack_rect = None  # New button for Time Attack mode
        self.is_time_attack = False
        self.time_attack_limit = 60  # Starting time limit for Time Attack mode
        self.start_image = pygame.image.load('./res/intro-image.png')
        self.start_image_rect = self.start_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2- 150))

    def draw_reset_button(self, btn_text="Reset"):
        button_width = 150
        button_height = 40
        button_x = self.screen_width / 2 - button_width / 2
        button_y = self.screen_height - button_height - 20
        self.reset_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, pygame.Color('dodgerblue'), self.reset_button_rect)
        text_surface = self.font.render(btn_text, True, pygame.Color('white'))
        text_rect = text_surface.get_rect(center=self.reset_button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_well_done_msg(self):
        message_text = "Well Done!"
        message_font = pygame.font.Font(None, 50)  # You can adjust the size as needed
        message_surface = message_font.render(message_text, True, pygame.Color('white'))
        message_rect = message_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2))

        # Calculate background rectangle size with some padding
        bg_rect = pygame.Rect(0, 0, message_rect.width + 20, message_rect.height + 20)
        bg_rect.center = message_rect.center  # Align the center of both rects

        # Draw the background rectangle with blue margins
        pygame.draw.rect(self.screen, pygame.Color('dodgerblue'), bg_rect)

        # Now blit the text surface onto the screen, centered within the blue rectangle
        self.screen.blit(message_surface, message_rect)
        # Changing the reset button text to "Play again"
        self.draw_reset_button("Play again")

    def draw_player_choice_buttons(self):
        btn_1p_width = 130
        btn_height = 40
        btn_1p_x = self.screen_width / 4 - btn_1p_width / 2
        btn_2p_x = self.screen_width * 3 / 4 - btn_1p_width / 2
        btn_y = self.screen_height / 2 - btn_height / 2
        self.btn_1player_rect = pygame.Rect(btn_1p_x, btn_y, btn_1p_width, btn_height)
        self.btn_2player_rect = pygame.Rect(btn_2p_x, btn_y, btn_1p_width + 15, btn_height)

        pygame.draw.rect(self.screen, pygame.Color('skyblue'), self.btn_1player_rect)
        pygame.draw.rect(self.screen, pygame.Color('skyblue'), self.btn_2player_rect)

        text_1p = self.font.render("1 Player", True, pygame.Color('white'))
        text_2p = self.font.render("2 Players", True, pygame.Color('white'))

        self.screen.blit(text_1p, (btn_1p_x + 10, btn_y + 10))
        self.screen.blit(text_2p, (btn_2p_x + 10, btn_y + 10))

        btn_time_attack_width = 170
        btn_time_attack_height = 40
        btn_time_attack_x = self.screen_width / 2 - btn_time_attack_width / 2
        self.btn_time_attack_rect = pygame.Rect(btn_time_attack_x, btn_y, btn_time_attack_width,
                                                btn_time_attack_height)
        pygame.draw.rect(self.screen, pygame.Color('skyblue'), self.btn_time_attack_rect)
        text_time_attack = self.font.render("Time Attack", True, pygame.Color('white'))
        self.screen.blit(text_time_attack, (btn_time_attack_x + 10, btn_y + 10))

    def draw_cards(self):
        margin = 5  # A small margin between cards

        for index in list(self.flip_states.keys()):
            self.flip_states[index] += 0.01  # Adjust this value to control the speed of the flip
            if self.flip_states[index] >= 1:
                self.flip_states.pop(index)  # Remove from flip_states if flip is complete

        for row in range(self.rows):
            for col in range(self.cols):
                index = row * self.cols + col
                # Calculate x and y position of the card with margins
                x_pos = col * self.card_size + margin + self.x_gap
                y_pos = row * self.card_size + margin + self.y_gap
                card_rect = pygame.Rect(x_pos, y_pos, self.card_size - margin * 2, self.card_size - margin * 2)

                if index in self.flip_states:
                    progress = self.flip_states[index]
                    # Calculate current width based on flip progress
                    current_width = int(card_rect.width * progress)
                    # Adjust x position to keep the card centered
                    adjusted_rect = pygame.Rect(card_rect.x + (card_rect.width - current_width) // 2, card_rect.y,
                                                current_width, card_rect.height)
                    pygame.draw.rect(self.screen, self.colors[index], adjusted_rect)
                elif index in self.matches or index in self.selected:
                    pygame.draw.rect(self.screen, self.colors[index], card_rect)
                else:
                    pygame.draw.rect(self.screen, self.hidden_color, card_rect)

                pygame.draw.rect(self.screen, self.text_color, card_rect, 3)  # Card border
                self.update_and_show_timer()

    def draw_home_button(self):
        if self.player_count > 0:
            # Adjust button position and dimensions as needed
            self.home_btn.topleft = (10, 10)  # Example position: top-left corner
            pygame.draw.rect(self.screen, pygame.Color('skyblue'), self.home_btn)
            text_surface = self.font.render("Home", True, pygame.Color('white'))
            text_rect = text_surface.get_rect(center=self.home_btn.center)
            self.screen.blit(text_surface, text_rect)

    def update_and_show_timer(self):
        current_ticks = pygame.time.get_ticks()
        elapsed_seconds = (current_ticks - self.start_ticks) // 1000

        if self.is_time_attack:
            # For Time Attack mode, calculate the remaining time
            remaining_time = self.time_attack_limit - elapsed_seconds
            if remaining_time < 0:
                remaining_time = 0  # Prevent displaying negative time

            # Format the remaining time as minutes:seconds
            timer_text = f"Time Left: {remaining_time // 60}:{remaining_time % 60:02d}"
        else:
            # For normal mode, display the elapsed time
            timer_text = f"Time: {elapsed_seconds // 60}:{elapsed_seconds % 60:02d}"

        # Render the timer text and display it on the screen
        text_surface = self.font.render(timer_text, True, self.text_color)
        self.screen.blit(text_surface, (10, self.screen_height - 50))  # Position for the standard timer

    def draw_current_player_indicator(self):
        x = self.reset_button_rect.x - 20

        y = 20
        if self.player_count == 2:
            display_text = f"Player {self.current_player}'s Turn"
            text_surface = self.font.render(display_text, True, self.text_color)
            self.screen.blit(text_surface, (x, y))

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

    def is_game_over(self):
        return len(self.matches) == len(self.colors)

    def handle_events(self, current_time, flip_back_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.btn_time_attack_rect.collidepoint(x, y):
                    self.player_count = 1
                    self.is_time_attack = True
                    self.reset_game()
                    self.time_attack_limit = 60  # Reset the time limit for a new game
                    self.start_ticks = pygame.time.get_ticks()  # Restart the timer

                if self.home_btn.collidepoint((x, y)):
                    # Logic to return to the initial screen
                    self.player_count = 0  # Resetting game mode selection
                    self.is_time_attack = False  # If using Time Attack mode

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
                    col = (x - margin - self.x_gap) // self.card_size
                    row = (y - margin - self.y_gap) // self.card_size
                    index = row * self.cols + col
                    if index < len(self.colors) and index not in self.matches and index not in self.selected:
                        self.selected.append(index)
                        self.flip_states[index] = 0  # Start flipping animation with initial progress as 0
                        if self.check_for_match():
                            flip_back_time = current_time + 1000

        return flip_back_time

    def run(self):
        running = True
        flip_back_time = None

        while running:
            current_time = pygame.time.get_ticks()
            self.screen.fill(self.bg_color)

            if self.player_count == 0:  # Player hasn't chosen a mode yet
                self.screen.blit(self.start_image, self.start_image_rect)
                self.draw_player_choice_buttons()
            else:
                self.draw_home_button()
                if flip_back_time and current_time >= flip_back_time:
                    self.selected.clear()
                    flip_back_time = None
                    if self.player_count == 2:
                        self.current_player = 2 if self.current_player == 1 else 1

                self.draw_cards()
                self.draw_current_player_indicator()
                # Draw reset btn or Well Done message
                if self.is_game_over():  # All cards matched
                    self.draw_well_done_msg()
                    if self.is_time_attack:
                        self.time_attack_limit -= 5  # Decrease time limit for the next game, adjust value as needed
                        self.reset_game()  # Reset the game for the next round
                        self.start_ticks = pygame.time.get_ticks()  # Restart the timer for the new game
                else:
                    self.draw_reset_button()

            # Handling events - main game logic
            flip_back_time = self.handle_events(current_time, flip_back_time)

            pygame.display.flip()


if __name__ == '__main__':
    game = MemoryGame()
    game.run()
