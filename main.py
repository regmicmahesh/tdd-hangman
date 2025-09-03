#!/usr/bin/env python3
"""
Simple Hangman Game - Main Module

A console-based Hangman game with timer functionality.
Supports basic (single word) and intermediate (phrase) levels.
"""

import os
import time
from hangman import HangmanGame, GameLevel, GameState


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def display_welcome():
    """Display welcome message."""
    clear_screen()
    print("=" * 50)
    print("🎯 WELCOME TO HANGMAN! 🎯")
    print("=" * 50)
    print()
    print("Rules:")
    print("• Guess the hidden word/phrase letter by letter")
    print("• You have 6 lives (wrong guesses)")
    print("• You have 15 seconds per guess")
    print("• Find the word before your lives run out!")
    print()


def get_level_choice() -> GameLevel:
    """Get difficulty level choice from user."""
    while True:
        print("Choose difficulty level:")
        print("1. Basic (Single Words)")
        print("2. Intermediate (Phrases)")
        print()

        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            return GameLevel.BASIC
        elif choice == "2":
            return GameLevel.INTERMEDIATE
        else:
            print("❌ Invalid choice! Please enter 1 or 2.\n")


def display_game_state(game: HangmanGame):
    """Display current game state."""
    print("\n" + "=" * 50)

    # Display level and lives
    level_name = "BASIC" if game.level == GameLevel.BASIC else "INTERMEDIATE"
    print(f"📊 Level: {level_name}")

    hearts = "❤️ " * game.lives + "🖤 " * (6 - game.lives)
    print(f"❤️  Lives: {hearts}({game.lives}/6)")

    # Display timer if active
    remaining = game.get_remaining_time()
    if remaining is not None:
        print(f"⏱️  Time: {remaining}s")

    print()

    # Display the word/phrase
    display_word = game.get_display_word()
    print(f"🎯 Word: {display_word}")
    print()

    # Display guessed letters
    guessed = game.get_guessed_letters()
    if guessed:
        print(f"📝 Guessed: {', '.join(guessed)}")
    else:
        print("📝 Guessed: (none yet)")

    print("=" * 50)


def get_user_guess() -> str:
    """Get a guess from the user."""
    while True:
        try:
            print("\n💭 Make your guess!")
            print("💡 Enter a single letter, or 'quit' to exit")

            guess = input("Your guess: ").strip().lower()

            if guess == "quit":
                return "QUIT"

            if len(guess) != 1 or not guess.isalpha():
                print("❌ Please enter exactly one letter!")
                continue

            return guess.upper()

        except (KeyboardInterrupt, EOFError):
            return "QUIT"


def display_result(game: HangmanGame):
    """Display game result."""
    print("\n" + "=" * 50)

    if game.state == GameState.WON:
        print("🎉 CONGRATULATIONS! YOU WON! 🎉")
        print(f"✨ You guessed: {game.get_target_answer()}")
    elif game.state == GameState.LOST:
        print("💀 GAME OVER! 💀")
        print(f"😢 The answer was: {game.get_target_answer()}")

    print("=" * 50)


def play_again() -> bool:
    """Ask if user wants to play again."""
    while True:
        choice = input("\n🎮 Play again? (y/n): ").strip().lower()
        if choice in ["y", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False
        else:
            print("❌ Please enter 'y' for yes or 'n' for no.")


def play_game():
    """Play a single game session."""
    level = get_level_choice()
    game = HangmanGame(level)

    while game.state == GameState.PLAYING:
        display_game_state(game)

        # Start timer for this guess
        game.start_timer()

        # Get user guess with simple timer checking
        guess = None
        start_time = time.time()

        print(f"\n⏱️  You have {game.timer_duration} seconds to guess...")

        # Simple input loop with timeout checking
        guess = get_user_guess()

        if guess == "QUIT":
            print("\n👋 Thanks for playing!")
            return False

        # Check if time is up
        if game.is_time_up():
            print("\n⏰ Time's up! You lose a life.")
            game.handle_timeout()
            continue

        # Process the guess
        try:
            is_correct = game.make_guess(guess)

            if is_correct:
                print("✅ Great guess! Letter found!")
            else:
                print("❌ Sorry, that letter is not in the word.")

        except ValueError as e:
            print(f"❌ Error: {e}")

        # Brief pause to show result
        time.sleep(1)

    # Display final result
    display_result(game)
    return True


def main():
    """Main game loop."""
    display_welcome()

    try:
        while True:
            if not play_game():
                break

            if not play_again():
                break

        print("\n" + "=" * 50)
        print("👋 Thanks for playing Hangman!")
        print("🎯 Come back anytime for more word guessing fun!")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing!")


if __name__ == "__main__":
    main()
