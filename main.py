#!/usr/bin/env python3

import os
import time
from hangman import HangmanGame, GameLevel, GameState


def clear_screen():
    # Works on both Windows and Unix systems
    os.system('cls' if os.name == 'nt' else 'clear')


def display_welcome():
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
    # Keep asking until we get a valid choice
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
    print("\n" + "=" * 50)
    
    # Show current level
    level_name = "BASIC" if game.level == GameLevel.BASIC else "INTERMEDIATE"
    print(f"📊 Level: {level_name}")
    
    # Show lives with heart symbols
    hearts = "❤️ " * game.lives + "🖤 " * (6 - game.lives)
    print(f"❤️  Lives: {hearts}({game.lives}/6)")
    
    # Show timer if it's running
    remaining = game.get_remaining_time()
    if remaining is not None:
        print(f"⏱️  Time: {remaining}s")
    
    print()
    
    # Show the word with guessed letters revealed
    display_word = game.get_display_word()
    print(f"🎯 Word: {display_word}")
    print()
    
    # Show what letters have been guessed so far
    guessed = game.get_guessed_letters()
    if guessed:
        print(f"📝 Guessed: {', '.join(guessed)}")
    else:
        print("📝 Guessed: (none yet)")
    
    print("=" * 50)


def get_user_guess() -> str:
    while True:
        try:
            print("\n💭 Make your guess!")
            print("💡 Enter a single letter, or 'quit' to exit")
            
            guess = input("Your guess: ").strip().lower()
            
            if guess == 'quit':
                return 'QUIT'
            
            # Make sure it's exactly one letter
            if len(guess) != 1 or not guess.isalpha():
                print("❌ Please enter exactly one letter!")
                continue
            
            return guess.upper()
            
        except (KeyboardInterrupt, EOFError):
            return 'QUIT'


def display_result(game: HangmanGame):
    print("\n" + "=" * 50)
    
    if game.state == GameState.WON:
        print("🎉 CONGRATULATIONS! YOU WON! 🎉")
        print(f"✨ You guessed: {game.get_target_answer()}")
    elif game.state == GameState.LOST:
        print("💀 GAME OVER! 💀")
        print(f"😢 The answer was: {game.get_target_answer()}")
    
    print("=" * 50)


def play_again() -> bool:
    while True:
        choice = input("\n🎮 Play again? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("❌ Please enter 'y' for yes or 'n' for no.")


def play_game():
    # Set up a new game
    level = get_level_choice()
    game = HangmanGame(level)
    
    # Main game loop - keep going while game is active
    while game.state == GameState.PLAYING:
        display_game_state(game)
        
        # Start the timer for this guess
        game.start_timer()
        
        guess = None
        start_time = time.time()
        
        print(f"\n⏱️  You have {game.timer_duration} seconds to guess...")
        
        # Get the user's guess
        guess = get_user_guess()
        
        # Check if user wants to quit
        if guess == 'QUIT':
            print("\n👋 Thanks for playing!")
            return False
        
        # Check if time ran out
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
        
        time.sleep(1)  # Pause so user can see the result
    
    # Game is over, show the result
    display_result(game)
    return True


def main():
    display_welcome()
    
    try:
        # Keep playing until user decides to quit
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
