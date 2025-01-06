import os
import sys
import time
from grid import Grid

def clear_screen():
    """Clear the terminal screen."""
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix/Linux/MacOS
    else:
        os.system('clear')

def print_title():
    print("-----------------------")
    print("|    Brain Buster    |")
    print("-----------------------")

def print_menu():
    print("\n1. Let me select two elements")
    print("2. Uncover one element for me")
    print("3. I give up - reveal the grid!")
    print("4. New game")
    print("5. Exit")
    print("\nSelect: ",)

def get_valid_coordinate(grid, prompt):
    while True:
        try:
            coordinate = input(prompt).strip()
            if len(coordinate) < 2:
                print("Invalid format. Please use format: letter number (e.g., A0)")
                continue
                
            row = int(coordinate[1:])
            col = coordinate[0]
            
            if not grid.is_valid_coordinate(row, col):
                print(f"Invalid coordinates. Please use row (0-{grid.size-1}) and column (A-{chr(65+grid.size-1)})")
                continue
                
            return row, col
            
        except ValueError:
            print("Invalid format. Please use format: letter number (e.g., A0)")
def play_game(grid_size):
    game = Grid(grid_size)
    
    while True:
        clear_screen()
        print_title()
        game.print_grid()
        print_menu()
        
        try:
            choice = input().strip()
            
            if choice == '1':  # Select two elements
                clear_screen()
                print_title()
                
                
                # Get first coordinate without showing grid
                coordinate1 = get_valid_coordinate(game, "\nEnter first position (e.g., A0): ")
                num1 = game.reveal_position(*coordinate1)
                
                # Get second coordinate without showing grid
                coordinate2 = get_valid_coordinate(game, "Enter second position (e.g., B0): ")
                
                # Check if same cell selected
                if coordinate1 == coordinate2:
                    print("Cannot select the same cell twice!")
                    game.hide_position(*coordinate1)
                    time.sleep(2)
                    continue
                
                num2 = game.reveal_position(*coordinate2)
                game.guesses += 1
                
                clear_screen()
                print_title()
                game.print_grid()
                
                if game.check_match(coordinate1, coordinate2):
                    print("\nMatch found!")
                    time.sleep(2)
                    game.pairs_found += 1
                else:
                    print("\nNo match!")
                    time.sleep(2)
                    game.hide_position(*coordinate1)
                    game.hide_position(*coordinate2)
                
                if game.is_game_complete():
                    if game.guesses > 0:
                        print(f"\nCongratulations! You've won with a score of {game.get_score():.1f}")
                    else:
                        print("\nGame complete, but no score awarded as no guesses were made!")
                    input("\nPress Enter to continue...")
                    return
                
            # Rest of the code remains the same
            elif choice == '2':  # Uncover one element
                coord = get_valid_coordinate(game, "\nEnter position (e.g., A0): ")
                game.reveal_position(*coord)
                game.guesses += 2  # Counts as two guesses
                
                if game.is_game_complete():
                    clear_screen()
                    print_title()
                    game.print_grid()
                    if game.guesses <= grid_size:
                        print(f"\nCongratulations! You've won with a score of {game.get_score():.1f}")
                    else:
                        print("You cheated - LOSER! Your score is 0!")
                    input("\nPress Enter to continue...")
                    return
                
            elif choice == '3':  # Reveal grid
                for i in range(grid_size):
                    for j in range(grid_size):
                        game.reveal_position(i, j)
                clear_screen()
                print_title()
                game.print_grid()
                print("\nGame Over!")
                input("\nPress Enter to continue...")
                return
                
            elif choice == '4':  # New game
                game.initialize_grid()
                game.guesses = 0
                game.pairs_found = 0
                
            elif choice == '5':  # Exit
                print("\nThanks for playing!")
                sys.exit(0)
                
            else:
                print("Invalid choice! Please select 1-5")
                time.sleep(2)
                
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
            time.sleep(2)

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['2', '4', '6']:
        print("Usage: python3 game.py [2|4|6]")
        sys.exit(1)
        
    grid_size = int(sys.argv[1])
    play_game(grid_size)

if __name__ == "__main__":
    main()