
# Memory Game in Pygame

This Memory Game is developed using Pygame and features both single-player and multiplayer modes. In single-player mode, you can choose from a classic game or a time attack mode where you must complete the board within a set time. Additionally, the single-player mode supports voice control using the Vosk speech recognition model. For multiplayer fun, two players can compete with each other, with the player making a successful match taking another turn immediately.

## Features

- **Single Player Modes:**
  - **Classic:** Play at your own pace and try to clear the board.
  - **Time Attack:** Complete the board within the time limit.
  - **Voice Control:** Use voice commands to play the game using the Vosk speech recognition model.
  
- **Multiplayer Mode:**
  - **2 Player:** Compete against another player. If you match cards, you continue with another turn.

## Prerequisites

- Python 3.x
- Pygame
- Vosk Speech Recognition Toolkit

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/matanyaniv8/MemoryGame---Voice-Control.git
   cd memory-game-pygame
   ```

2. **Install dependencies:**
   ```bash
   pip install pygame vosk
   ```

3. **Download the Vosk model:**
   - Visit [Vosk Model Page](https://alphacephei.com/vosk/models) and download `vosk-model-small-en-us-0.15`.
   - Extract the model to the project directory.

4. **Run the game:**
   ```bash
   python main.py
   ```

## How to Play

### Single Player
- **Classic Mode:** Simply select two cards to try to find a match.
- **Time Attack Mode:** You are racing against the clock to clear the board before time runs out.
- **Voice Control Mode:** Speak the positions of the cards to flip them (e.g., "one three" for row 1, column 3).

### Multiplayer
- Take turns selecting two cards. If you find a match, you get another turn. The player with the most matches at the end wins.



## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
