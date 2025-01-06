import random

class Grid:
    def __init__(self, size):
        if size not in [2, 4, 6]:
            raise ValueError("Grid size must be 2, 4, or 6")
            
        self.size = size
        self.guesses = 0
        self.pairs_found = 0
        self.minimum_guesses = (size * size) // 2
        self.initialize_grid()

    def initialize_grid(self):
        # Create pairs of numbers
        total_cells = self.size * self.size
        numbers = list(range(total_cells // 2)) * 2
        random.shuffle(numbers)
        
        # Create the hidden grid with randomly distributed pairs
        self.hidden = [numbers[i:i+self.size] for i in range(0, total_cells, self.size)]
        
        # Create the visible grid (mask) with X's
        self.mask = [['X'] * self.size for _ in range(self.size)]
        
    def is_valid_coordinate(self, row, col):
        # Convert column letter to number if it's a string
        if isinstance(col, str):
            if not col.isalpha():
                return False
            col_num = ord(col.upper()) - ord('A')
        else:
            col_num = col
            
        # Check if coordinates are within grid bounds
        if not (0 <= row < self.size and 0 <= col_num < self.size):
            return False
            
        return True

    def reveal_position(self, row, col):
        if isinstance(col, str):
            col = ord(col.upper()) - ord('A')
        self.mask[row][col] = str(self.hidden[row][col])
        return self.hidden[row][col]

    def hide_position(self, row, col):
        if isinstance(col, str):
            col = ord(col.upper()) - ord('A')
        self.mask[row][col] = 'X'

    def check_match(self, pos1, pos2):
        row1, col1 = pos1
        row2, col2 = pos2
        
        if isinstance(col1, str):
            col1 = ord(col1.upper()) - ord('A')
        if isinstance(col2, str):
            col2 = ord(col2.upper()) - ord('A')
            
        return self.hidden[row1][col1] == self.hidden[row2][col2]

    def is_game_complete(self):
        return all(cell != 'X' for row in self.mask for cell in row)

    def get_score(self):
        if self.guesses == 0:
            return 0
        return (self.minimum_guesses / self.guesses) * 100

    def print_grid(self):
        # Print column headers
        columns = [f"[{chr(65+i)}]" for i in range(self.size)]
        print("    " + " ".join(columns))
        
        # Print rows with row numbers
        for i in range(self.size):
            print(f"[{i}] ", end=" ")
            print("   ".join(str(self.mask[i][j]) for j in range(self.size)))
