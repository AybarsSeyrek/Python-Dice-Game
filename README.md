# Python-Dice-Game
A terminal-based Python dice game with ASCII dice art, multiple game modes, roll history, statistics, and JSON save data. The game uses ASCII art to visually display 6-sided dice rolls. It also includes multiple game modes, player statistics, roll history, win/loss tracking, streak tracking, and a JSON save system. The goal of this project is to practice Python fundamentals while making a small program that feels more like a complete game.

---

## Features

- Roll one or more 6-sided dice
- ASCII dice art display
- Player name system
- Main menu system
- Input validation
- Roll history
- Clear roll history option
- Reset all saved data option
- JSON save system
- Statistics screen
- Guess the total mode
- Target score mode
- Player vs Computer mode
- Best-of-3 match mode
- Win, loss, and tie tracking
- Current win streak tracking
- Best win streak tracking
- Color-coded terminal output
- Rolling animation effect

---

## Game Modes

### 1. Normal Roll Mode

The player chooses how many dice to roll. The game displays the dice using ASCII art and shows the total, highest die, lowest die, and average.

### 2. Guess the Total Mode

The player guesses the total before rolling. If the guessed number matches the dice total, the player wins.

### 3. Target Score Mode

The player keeps rolling until they reach a chosen target score. The game tracks how many turns it takes to reach the target.

### 4. Player vs Computer Mode

The player and the computer roll the same number of dice. The higher total wins.

### 5. Best-of-3 Match Mode

The player and computer play rounds until one side wins 2 rounds.

---

## Python Concepts Demonstrated

This project was built to practice and demonstrate beginner-to-intermediate Python concepts in one complete terminal-based program.

### Core Python Syntax

- Variables for tracking dice rolls, totals, wins, losses, ties, and streaks
- Constants such as `SAVE_FILE`
- `if`, `elif`, and `else` statements for menu choices and game results
- Comparison operators for checking winners
- String formatting with f-strings

### Data Structures

- Dictionaries for dice ASCII art and saved player data
- Lists for storing dice rolls and roll history
- Nested data stored in JSON format

### Functions

The program is divided into functions to keep the code organized and reusable.

Examples:

- `roll_dice()` rolls the dice
- `display_dice()` prints the ASCII dice art
- `normal_roll_mode()` handles basic rolling
- `guess_total_mode()` handles the guessing mode
- `player_vs_computer_mode()` handles player vs computer gameplay
- `statistics_screen()` displays saved player statistics

### Loops

- `while` loops are used to keep the main menu running
- `for` loops are used to roll multiple dice
- `for` loops are also used to print dice art line by line

### File Handling

The game uses file handling to save and load player data.

The save file is called:

```text
dice_game_save.json
