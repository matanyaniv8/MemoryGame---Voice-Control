import pygame
import random
import sys
from MemoryGameDrawing import MemoryGameDrawing
from VoiceControl import VoiceControl


class MemoryGame:
    def __init__(self):
        pygame.init()
        self.colors = [pygame.Color('red'), pygame.Color('green'), pygame.Color('blue'), pygame.Color('yellow'),
                       pygame.Color('cyan'), pygame.Color('magenta'), pygame.Color('orange'),
                       pygame.Color('purple')] * 2
        random.shuffle(self.colors)
        self.rows = 4
        self.cols = 4
        self.time_between_flips = 1000
        self.selected = []
        self.matches = set()
        self.start_ticks = pygame.time.get_ticks()
        self.match_sound = pygame.mixer.Sound('./res/match_sound.wav')
        self.player_count = 0  # Initial state, not yet chosen
        self.current_player = 1
        # flip animation member
        self.flip_states = {}  # Tracks whether a card is flipping, and its progress
        # Attack mode members
        self.is_time_attack = False
        self.time_attack_limit = 60  # Starting time limit for Time Attack mode
        # Voice Recognition Initialization
        self.vc = None
        self.is_voice_control_active = False
        self.drawing = MemoryGameDrawing(self)  # Pass the game instance to Drawing

    def update_and_show_timer(self):
        """
        Updates the timer and shows the current time of the game since the player/s started to play.
        """
        current_ticks = pygame.time.get_ticks()
        elapsed_seconds = (current_ticks - self.start_ticks) // 1000
        if self.is_time_attack:
            # For Time Attack mode, calculate the remaining time
            remaining_time = self.time_attack_limit - elapsed_seconds
            if remaining_time < 0:
                remaining_time = 0  # Prevent displaying negative time
            timer_text = f"Time Left: {remaining_time // 60}:{remaining_time % 60:02d}"
        else:
            # For normal mode, display the elapsed time
            timer_text = f"Time: {elapsed_seconds // 60}:{elapsed_seconds % 60:02d}"
        text_surface = self.drawing.font.render(timer_text, True, self.drawing.text_color)
        self.drawing.screen.blit(text_surface, (10, self.drawing.screen_height - 50))  # Position for the standard timer

    def reset_game(self):
        """
        Resets the game state and updates the voice control system if needed.
        """
        random.shuffle(self.colors)
        self.matches.clear()
        self.selected.clear()
        self.start_ticks = pygame.time.get_ticks()
        self.current_player = 1  # Reset to player 1 for a new game
        if self.is_voice_control_active:
            self.is_voice_control_active = False
            self.vc = None

    def check_for_match(self):
        """
        Checks if the two selected cards have the same color.
        """
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
        """
        Checks if the game is over (all the cards have been discovered).
        """
        return len(self.matches) == len(self.colors)

    def handle_voice_event(self, current_time, flip_back_time, number):
        """
        Handle voice events sends from the VoiceControl to the pygame event handler.
        :param current_time: Current program time.
        :param flip_back_time: Time to flip back the cards.
        :param number: Number recognized by the voice control mechanism.
        :return: The update time to flip back the selected cards.
        """
        if self.is_voice_control_active and not flip_back_time:
            if number != -1:
                number -= 1  # Adjust command index to match card index
                if number < len(self.colors) and number not in self.matches and number not in self.selected:
                    self.selected.append(number)
                    self.flip_states[number] = 0  # Start flipping animation
                    if self.check_for_match():
                        # If cards don't match, set flip_back_time to give users a chance to see the second card
                        flip_back_time = current_time + self.time_between_flips
        return flip_back_time

    def handle_cards_pressing(self, current_time, flip_back_time, x_coords, y_coords):
        """
        Handles cards pressing if voice control is not ON.
        :return: Time to flip back the cards
        """
        margin = 5  # Assuming this is the same margin used in draw_cards
        col = (x_coords - margin - self.drawing.x_gap) // self.drawing.card_size
        row = (y_coords - margin - self.drawing.y_gap) // self.drawing.card_size
        index = row * self.cols + col
        if index < len(self.colors) and index not in self.matches and index not in self.selected:
            self.selected.append(index)
            self.flip_states[index] = 0  # Start flipping animation with initial progress as 0
            if self.check_for_match():
                flip_back_time = current_time + self.time_between_flips
        return flip_back_time

    def handle_home_btn_pressing(self):
        """
        Handles home button pressing
        """
        # return to the initial screen
        self.player_count = 0  # Resetting game mode selection
        self.is_time_attack = False  # If using Time Attack mode
        if self.vc is not None:
            self.vc.stop_listening()
        self.reset_game()

    def handle_menu_btn_pressing(self, x_coord, y_coord):
        """
        Handles menu button pressing given a pygame.MOUSEBUTTONDOWN event has occurred.
        """
        if self.drawing.btn_voice_control_rect.collidepoint(x_coord, y_coord) and not self.is_voice_control_active:
            self.player_count = 1
            self.is_voice_control_active = True
            self.vc = VoiceControl()
            self.vc.start_listening()
        elif self.drawing.btn_1player_rect.collidepoint(x_coord, y_coord):
            self.player_count = 1
        elif self.drawing.btn_2player_rect.collidepoint(x_coord, y_coord):
            self.player_count = 2
        # Attack Mode
        elif self.drawing.btn_time_attack_rect.collidepoint(x_coord, y_coord):
            self.player_count = 1
            self.is_time_attack = True
            self.time_attack_limit = 60  # Reset the time limit for a new game
            self.start_ticks = pygame.time.get_ticks()  # Restart the timer

    def handle_events(self, current_time, flip_back_time):
        """
        Handles events received from the pygame.
        :param current_time: game current time
        :param flip_back_time: remaining time to flip back the cards,
        :return: the update remaining time left until cards need to be flipped
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # After the game loop, ensure to stop listening
                if self.vc is not None:
                    self.vc.stop_listening()
                pygame.quit()
                sys.exit()
            # Voice control event
            elif event.type == VoiceControl.VOICE_RECOGNIZE_EVENT_TYPE:
                flip_back_time = self.handle_voice_event(current_time, flip_back_time, event.data)
            # Mouse button event handling
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.drawing.home_btn.collidepoint((x, y)):
                    self.handle_home_btn_pressing()
                # Show the initial menu
                if self.player_count == 0:
                    self.handle_menu_btn_pressing(x, y)
                # Reset button been pressed
                elif self.drawing.reset_button_rect.collidepoint(x, y):
                    self.reset_game()
                # card pressing
                elif self.player_count and not flip_back_time and not self.is_voice_control_active:
                    flip_back_time = self.handle_cards_pressing(current_time, flip_back_time, x, y)

        return flip_back_time

    def run(self):
        """
        Main loop of the game.
        """
        running = True
        flip_back_time = 0
        while running:
            current_time = pygame.time.get_ticks()
            self.drawing.screen.fill(self.drawing.bg_color)

            if self.player_count == 0:  # Player hasn't chosen a mode yet
                self.drawing.screen.blit(self.drawing.start_image, self.drawing.start_image_rect)
                self.drawing.draw_player_choice_buttons()
            else:
                self.drawing.draw_home_button()
                # Checks if chosen cards need to be released
                if flip_back_time and current_time >= flip_back_time:
                    self.selected.clear()
                    flip_back_time = None
                    if self.player_count == 2:
                        self.current_player = 2 if self.current_player == 1 else 1
                # Updates Board at every iteration
                self.drawing.draw_cards()
                self.drawing.draw_current_player_indicator()
                # Draw reset btn or Well-Done message if all cards matched
                if self.is_game_over():
                    self.drawing.draw_well_done_msg()
                    if self.is_time_attack:
                        self.time_attack_limit -= 5  # Decrease time limit for the next gam
                        self.reset_game()  # Reset the game for the next round
                        self.start_ticks = pygame.time.get_ticks()  # Restart the timer for the new game
                else:
                    self.drawing.draw_reset_button()

            # Handling events - main game logic
            flip_back_time = self.handle_events(current_time, flip_back_time)
            pygame.display.flip()

        # After the game loop, ensure to stop listening
        if self.vc is not None:
            self.vc.stop_listening()


if __name__ == '__main__':
    game = MemoryGame()
    game.run()
