import pygame


class MemoryGameDrawing:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 40)
        screen_info = pygame.display.Info()
        self.screen_width = int(screen_info.current_w * 0.4)
        self.screen_height = int(screen_info.current_h * 0.7)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.bg_color = pygame.Color(240, 230, 220)
        self.hidden_color = pygame.Color('grey')
        self.text_color = pygame.Color('black')
        self.cols = self.game.cols
        self.rows = self.game.rows
        self.card_width = self.screen_width // self.cols
        self.card_height = self.screen_height // self.rows - 10
        self.card_size = min(self.screen_width // self.cols, self.screen_height // self.rows) - 40
        self.btn_2player_rect = None
        self.btn_1player_rect = None
        self.home_btn = pygame.Rect(0, 0, 100, 50)
        # gaps for each axis for centering the cards position.
        self.y_gap = 70
        self.x_gap = 80
        self.reset_button_rect = pygame.Rect(0, 0, 1, 1)  # Placeholder initialization
        self.btn_time_attack_rect = None  # New button for Time Attack mode
        self.start_image = pygame.image.load('./res/intro-image.png')
        self.start_image_rect = self.start_image.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 - 150))
        self.btn_voice_control_rect = None
        self.microphone_icon = pygame.image.load(
            './res/voice control.jpg').convert_alpha()  # Convert_alpha for transparency
        self.microphone_icon = pygame.transform.scale(self.microphone_icon, (30, 30))  # Adjust size as needed
        self.buttons_color = pygame.Color(128, 0, 32)  # Bordeaux

    def draw_reset_button(self, btn_text="Reset"):
        button_width = 150
        button_height = 40
        button_x = self.screen_width / 2 - button_width / 2
        button_y = self.screen_height - button_height - 20
        self.reset_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, self.buttons_color, self.reset_button_rect)
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
        # Single and Multiplayer buttons settings
        btn_1p_width = 130
        btn_height = 45
        btn_1p_x = self.screen_width / 4 - btn_1p_width / 2 - 50
        btn_2p_x = self.screen_width * 3 / 4 - btn_1p_width / 2 + 50
        btn_y = self.screen_height / 2 - btn_height / 2
        self.btn_1player_rect = pygame.Rect(btn_1p_x, btn_y, btn_1p_width, btn_height)
        self.btn_2player_rect = pygame.Rect(btn_2p_x, btn_y, btn_1p_width + 15, btn_height)

        pygame.draw.rect(self.screen, self.buttons_color, self.btn_1player_rect)
        pygame.draw.rect(self.screen, self.buttons_color, self.btn_2player_rect)

        text_1p = self.font.render("1 Player", True, pygame.Color('white'))
        text_2p = self.font.render("2 Players", True, pygame.Color('white'))

        self.screen.blit(text_1p, (btn_1p_x + 10, btn_y + 10))
        self.screen.blit(text_2p, (btn_2p_x + 10, btn_y + 10))
        # Attack Time button
        btn_time_attack_width = 170
        btn_time_attack_height = 40
        btn_time_attack_x = self.screen_width / 2 - btn_time_attack_width / 2
        self.btn_time_attack_rect = pygame.Rect(btn_time_attack_x, btn_y, btn_time_attack_width,
                                                btn_time_attack_height)
        pygame.draw.rect(self.screen, self.buttons_color, self.btn_time_attack_rect)
        text_time_attack = self.font.render("Time Attack", True, pygame.Color('white'))
        self.screen.blit(text_time_attack, (btn_time_attack_x + 10, btn_y + 10))

        # Voice control button
        btn_voice_control_width = 225
        btn_voice_control_height = 35
        btn_voice_control_x = btn_1p_x - 35
        btn_voice_control_y = self.btn_1player_rect.bottom + 20  # Place below the 1-Player button
        self.btn_voice_control_rect = pygame.Rect(btn_voice_control_x, btn_voice_control_y,
                                                  btn_voice_control_width,
                                                  btn_voice_control_height)
        pygame.draw.rect(self.screen, self.buttons_color, self.btn_voice_control_rect)
        text_voice_control = self.font.render("Voice Control", True, pygame.Color('white'))
        self.screen.blit(text_voice_control, (btn_voice_control_x + 40, btn_voice_control_y + 10))
        icon_pos = self.btn_voice_control_rect.topleft + pygame.Vector2(4, 3.5)
        self.screen.blit(self.microphone_icon, icon_pos)

    def draw_cards(self):
        margin = 5  # A small margin between cards

        for index in list(self.game.flip_states.keys()):
            self.game.flip_states[index] += 0.02  # Adjust this value to control the speed of the flip
            if self.game.flip_states[index] >= 1:
                self.game.flip_states.pop(index)  # Remove from flip_states if flip is complete

        for row in range(self.rows):
            for col in range(self.cols):
                index = row * self.cols + col
                # Calculate x and y position of the card with margins
                x_pos = col * self.card_size + margin + self.x_gap
                y_pos = row * self.card_size + margin + self.y_gap
                card_rect = pygame.Rect(x_pos, y_pos, self.card_size - margin * 2,
                                        self.card_size - margin * 2)

                if index in self.game.flip_states:
                    progress = self.game.flip_states[index]
                    # Calculate current width based on flip progress
                    current_width = int(card_rect.width * progress)
                    # Adjust x position to keep the card centered
                    adjusted_rect = pygame.Rect(card_rect.x + (card_rect.width - current_width) // 2, card_rect.y,
                                                current_width, card_rect.height)
                    pygame.draw.rect(self.screen, self.game.colors[index], adjusted_rect)
                elif index in self.game.matches or index in self.game.selected:
                    pygame.draw.rect(self.screen, self.game.colors[index], card_rect)
                else:
                    pygame.draw.rect(self.screen, self.hidden_color, card_rect)

                pygame.draw.rect(self.screen, self.text_color, card_rect, 3)  # Card border

                # Check if voice control mode is active and draw the card number for a more accessible game.
                if self.game.is_voice_control_active:
                    number_text = self.font.render(str(index + 1), True,
                                                   self.text_color)  # Index + 1 to start numbers from 1
                    text_rect = number_text.get_rect(topright=(card_rect.right - 5, card_rect.top + 5))
                    self.screen.blit(number_text, text_rect)

                self.game.update_and_show_timer()

    def draw_home_button(self):
        if self.game.player_count > 0:
            # Adjust button position and dimensions as needed
            self.home_btn.topleft = (10, 10)  # Example position: top-left corner
            pygame.draw.rect(self.screen, self.buttons_color, self.home_btn)
            text_surface = self.font.render("Home", True, pygame.Color('white'))
            text_rect = text_surface.get_rect(center=self.home_btn.center)
            self.screen.blit(text_surface, text_rect)

    def draw_current_player_indicator(self):
        x = self.reset_button_rect.x - 20
        y = 20

        if self.game.player_count == 2:
            display_text = f"Player {self.game.current_player}'s Turn"
            text_surface = self.font.render(display_text, True, self.text_color)
            self.screen.blit(text_surface, (x, y))
