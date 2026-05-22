import random
import json
import os
import time
from collections import Counter


# ============================================================
# PROFESSIONAL PYTHON DICE GAME
# ============================================================
# This version uses only the original 6-sided dice art.
# Features:
# - Original d6 ASCII dice art
# - Player name
# - Roll history
# - JSON save system
# - Statistics
# - Guess the total mode
# - Target score mode
# - Player vs Computer mode
# - Best-of-3 match mode
# ============================================================


SAVE_FILE = "dice_game_save.json"


class Colors:
    GREEN = "\033[92m"   # Good result / win
    RED = "\033[91m"     # Bad result / error
    YELLOW = "\033[93m"  # Warning / tie
    BLUE = "\033[94m"    # Player name
    CYAN = "\033[96m"    # Title
    RESET = "\033[0m"    # Reset color back to normal


# Original 6-sided dice art.
# Each key is the dice value.
# Each value is a tuple made out of strings.
dice_art = {
    1: (
        "┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘",
    ),
    2: (
        "┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘",
    ),
    3: (
        "┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘",
    ),
    4: (
        "┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘",
    ),
    5: (
        "┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘",
    ),
    6: (
        "┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘",
    )
}


def load_data():
    """Loads saved player data from the JSON file."""

    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as file:
                return json.load(file)

        except json.JSONDecodeError:
            print(f"{Colors.YELLOW}Save file was damaged. Starting fresh.{Colors.RESET}")

    return {
        "player_name": "",
        "roll_history": [],
        "wins": 0,
        "losses": 0,
        "ties": 0,
        "current_streak": 0,
        "best_streak": 0
    }


def save_data(data):
    """Saves player data to the JSON file."""

    with open(SAVE_FILE, "w") as file:
        json.dump(data, file, indent=4)


def show_title():
    """Displays the game title."""

    print(f"{Colors.CYAN}")
    print("====================================")
    print("        PROFESSIONAL DICE GAME")
    print("====================================")
    print(f"{Colors.RESET}")


def show_menu():
    """Displays the main menu."""

    print("\nMain Menu")
    print("1. Roll dice")
    print("2. Guess the total mode")
    print("3. Target score mode")
    print("4. Player vs Computer")
    print("5. Best-of-3 match")
    print("6. Statistics screen")
    print("7. View roll history")
    print("8. Clear roll history")
    print("9. Reset all saved data")
    print("10. Exit")


def get_player_name(data):
    """Gets the player's name if it is not already saved."""

    if data["player_name"] == "":
        name = input("Enter your player name: ").strip()

        if name == "":
            name = "Player"

        data["player_name"] = name
        save_data(data)

    print(f"\nWelcome, {Colors.BLUE}{data['player_name']}{Colors.RESET}!")


def get_int_input(prompt, minimum=None, maximum=None):
    """Gets a valid whole number from the player."""

    while True:
        try:
            number = int(input(prompt))

            if minimum is not None and number < minimum:
                print(f"{Colors.YELLOW}Please enter a number greater than or equal to {minimum}.{Colors.RESET}")

            elif maximum is not None and number > maximum:
                print(f"{Colors.YELLOW}Please enter a number less than or equal to {maximum}.{Colors.RESET}")

            else:
                return number

        except ValueError:
            print(f"{Colors.RED}Invalid input. Please enter a whole number.{Colors.RESET}")


def roll_dice(num_of_dice):
    """
    Rolls 6-sided dice.

    num_of_dice means how many dice the player wants to roll.
    The value will always be between 1 and 6.
    """

    dice = []

    for die in range(num_of_dice):
        dice.append(random.randint(1, 6))

    return dice


def rolling_animation():
    """Shows a small rolling animation."""

    print()

    for dots in range(1, 4):
        print(f"Rolling{'.' * dots}")
        time.sleep(0.4)


def display_dice(dice):
    """
    Displays the dice side by side using the original dice art.

    dice is a list of rolled values.
    Example:
    [4, 2, 6]
    """

    print("\nYour roll:\n")

    for line in range(5):
        for die in dice:
            print(dice_art[die][line], end=" ")
        print()


def show_roll_result(dice):
    """Shows total, highest, lowest, and average."""

    total = sum(dice)
    highest = max(dice)
    lowest = min(dice)
    average = total / len(dice)

    print(f"\nDice values: {dice}")
    print(f"Total: {total}")
    print(f"Highest die: {highest}")
    print(f"Lowest die: {lowest}")
    print(f"Average: {average:.2f}")


def show_critical_message(dice):
    """Shows special messages for lucky or unlucky rolls."""

    if len(dice) >= 2:
        if dice.count(6) == len(dice):
            print(f"{Colors.GREEN}Critical roll! All sixes! Very lucky!{Colors.RESET}")

        elif dice.count(1) == len(dice):
            print(f"{Colors.RED}Snake eyes! All ones! Bad luck!{Colors.RESET}")

    if max(dice) == 6:
        print(f"{Colors.GREEN}Nice! You rolled at least one six.{Colors.RESET}")


def save_roll_to_history(data, dice, mode):
    """
    Saves one roll into roll history.

    dice stores the rolled values.
    total stores the sum of the dice.
    mode stores which game mode created the roll.
    """

    roll_data = {
        "dice": dice,
        "total": sum(dice),
        "mode": mode
    }

    data["roll_history"].append(roll_data)
    save_data(data)


def update_streak(data, player_won):
    """Updates the player's current and best win streak."""

    if player_won:
        data["current_streak"] += 1

        if data["current_streak"] > data["best_streak"]:
            data["best_streak"] = data["current_streak"]

    else:
        data["current_streak"] = 0


def normal_roll_mode(data):
    """Basic dice rolling mode."""

    num_of_dice = get_int_input("How many dice do you want to roll?: ", 1, 10)

    rolling_animation()

    dice = roll_dice(num_of_dice)

    display_dice(dice)
    show_roll_result(dice)
    show_critical_message(dice)

    save_roll_to_history(data, dice, "Normal Roll")


def guess_total_mode(data):
    """The player guesses the total before rolling."""

    num_of_dice = get_int_input("How many dice do you want to roll?: ", 1, 10)

    lowest_possible = num_of_dice
    highest_possible = num_of_dice * 6

    print(f"\nPossible total range: {lowest_possible} to {highest_possible}")

    guess = get_int_input("Guess the total: ", lowest_possible, highest_possible)

    rolling_animation()

    dice = roll_dice(num_of_dice)
    total = sum(dice)

    display_dice(dice)
    show_roll_result(dice)

    if guess == total:
        print(f"{Colors.GREEN}Correct! You guessed the exact total!{Colors.RESET}")
        data["wins"] += 1
        update_streak(data, True)

    else:
        print(f"{Colors.RED}Wrong guess. The total was {total}.{Colors.RESET}")
        data["losses"] += 1
        update_streak(data, False)

    save_roll_to_history(data, dice, "Guess Total")
    save_data(data)


def target_score_mode(data):
    """The player keeps rolling until reaching a target score."""

    num_of_dice = get_int_input("How many dice per roll?: ", 1, 10)
    target_score = get_int_input("Choose a target score: ", 10, 1000)

    current_score = 0
    turns = 0

    print(f"\nTry to reach {target_score} points!")

    while current_score < target_score:
        input("\nPress Enter to roll...")

        rolling_animation()

        dice = roll_dice(num_of_dice)
        total = sum(dice)

        turns += 1
        current_score += total

        display_dice(dice)

        print(f"Roll total: {total}")
        print(f"Current score: {current_score}/{target_score}")

        save_roll_to_history(data, dice, "Target Score")

    print(f"{Colors.GREEN}\nYou reached the target score in {turns} turns!{Colors.RESET}")


def player_vs_computer_mode(data):
    """Player and computer roll dice against each other."""

    num_of_dice = get_int_input("How many dice per player?: ", 1, 10)

    input("\nPress Enter to roll for you and the computer...")

    rolling_animation()

    player_dice = roll_dice(num_of_dice)
    computer_dice = roll_dice(num_of_dice)

    player_total = sum(player_dice)
    computer_total = sum(computer_dice)

    print(f"\n{data['player_name']}'s roll:")
    display_dice(player_dice)
    print(f"Your total: {player_total}")

    print("\nComputer's roll:")
    display_dice(computer_dice)
    print(f"Computer total: {computer_total}")

    if player_total > computer_total:
        print(f"{Colors.GREEN}\nYou win!{Colors.RESET}")
        data["wins"] += 1
        update_streak(data, True)

    elif player_total < computer_total:
        print(f"{Colors.RED}\nComputer wins!{Colors.RESET}")
        data["losses"] += 1
        update_streak(data, False)

    else:
        print(f"{Colors.YELLOW}\nIt's a tie!{Colors.RESET}")
        data["ties"] += 1

    save_roll_to_history(data, player_dice, "Player vs Computer")
    save_data(data)


def best_of_three_match(data):
    """Best-of-3 match mode."""

    num_of_dice = get_int_input("How many dice per player?: ", 1, 10)

    player_score = 0
    computer_score = 0
    round_number = 1

    print("\nBest-of-3 match started!")

    while player_score < 2 and computer_score < 2:
        input(f"\nPress Enter to play round {round_number}...")

        rolling_animation()

        player_dice = roll_dice(num_of_dice)
        computer_dice = roll_dice(num_of_dice)

        player_total = sum(player_dice)
        computer_total = sum(computer_dice)

        print(f"\nRound {round_number}")

        print(f"\n{data['player_name']}'s roll:")
        display_dice(player_dice)
        print(f"Total: {player_total}")

        print("\nComputer's roll:")
        display_dice(computer_dice)
        print(f"Total: {computer_total}")

        if player_total > computer_total:
            print(f"{Colors.GREEN}You win this round!{Colors.RESET}")
            player_score += 1

        elif player_total < computer_total:
            print(f"{Colors.RED}Computer wins this round!{Colors.RESET}")
            computer_score += 1

        else:
            print(f"{Colors.YELLOW}Round tied. No points given.{Colors.RESET}")

        save_roll_to_history(data, player_dice, "Best-of-3 Match")

        print(f"Score: {data['player_name']} {player_score} - Computer {computer_score}")

        round_number += 1

    if player_score > computer_score:
        print(f"{Colors.GREEN}\nYou won the match!{Colors.RESET}")
        data["wins"] += 1
        update_streak(data, True)

    else:
        print(f"{Colors.RED}\nComputer won the match!{Colors.RESET}")
        data["losses"] += 1
        update_streak(data, False)

    save_data(data)


def statistics_screen(data):
    """Shows player statistics."""

    history = data["roll_history"]

    print("\n========== STATISTICS ==========")
    print(f"Player name: {data['player_name']}")
    print(f"Wins: {data['wins']}")
    print(f"Losses: {data['losses']}")
    print(f"Ties: {data['ties']}")
    print(f"Current win streak: {data['current_streak']}")
    print(f"Best win streak: {data['best_streak']}")
    print(f"Total rolls saved: {len(history)}")

    if not history:
        print("No roll statistics yet.")
        return

    totals = [roll["total"] for roll in history]
    all_dice_values = []

    for roll in history:
        all_dice_values.extend(roll["dice"])

    best_roll = max(totals)
    worst_roll = min(totals)
    average_total = sum(totals) / len(totals)
    most_common_value = Counter(all_dice_values).most_common(1)[0][0]

    print(f"Best roll total: {best_roll}")
    print(f"Worst roll total: {worst_roll}")
    print(f"Average roll total: {average_total:.2f}")
    print(f"Most common dice value: {most_common_value}")


def view_history(data):
    """Displays saved roll history."""

    history = data["roll_history"]

    if not history:
        print("\nNo roll history yet.")
        return

    print("\n========== ROLL HISTORY ==========")

    for index, roll in enumerate(history, start=1):
        print(
            f"{index}. Mode: {roll['mode']} | "
            f"Dice: {roll['dice']} | "
            f"Total: {roll['total']}"
        )


def clear_history(data):
    """Clears only the roll history."""

    confirm = input("Are you sure you want to clear roll history? (yes/no): ").lower()

    if confirm == "yes":
        data["roll_history"] = []
        save_data(data)
        print(f"{Colors.GREEN}Roll history cleared.{Colors.RESET}")

    else:
        print("Cancelled.")


def reset_all_data(data):
    """Resets all saved data."""

    confirm = input("Are you sure you want to reset everything? (yes/no): ").lower()

    if confirm == "yes":
        data["player_name"] = ""
        data["roll_history"] = []
        data["wins"] = 0
        data["losses"] = 0
        data["ties"] = 0
        data["current_streak"] = 0
        data["best_streak"] = 0

        save_data(data)

        print(f"{Colors.GREEN}All saved data has been reset.{Colors.RESET}")

    else:
        print("Cancelled.")


def main():
    """Main function that controls the game."""

    data = load_data()

    show_title()
    get_player_name(data)

    running = True

    while running:
        show_menu()
        choice = input("\nChoose an option: ")

        if choice == "1":
            normal_roll_mode(data)

        elif choice == "2":
            guess_total_mode(data)

        elif choice == "3":
            target_score_mode(data)

        elif choice == "4":
            player_vs_computer_mode(data)

        elif choice == "5":
            best_of_three_match(data)

        elif choice == "6":
            statistics_screen(data)

        elif choice == "7":
            view_history(data)

        elif choice == "8":
            clear_history(data)

        elif choice == "9":
            reset_all_data(data)

        elif choice == "10":
            print(f"\n{Colors.CYAN}Thanks for playing, {data['player_name']}!{Colors.RESET}")
            running = False

        else:
            print(f"{Colors.RED}Invalid choice. Please choose a valid menu option.{Colors.RESET}")


main()
