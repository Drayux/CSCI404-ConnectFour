# Connect Four AI
# Artificial Intelligence: Project 2
# Liam Dempsey
# 10754465

import enum
import os

# Utility class for pretty colors in the terminal output
class colors:
    RESET = "\x1b[0m"
    RED = "\x1b[31m"
    BLUE = "\x1b[34m"

# Location within the board
class piece(enum.Enum):
    NONE = 0
    RED = 1
    BLUE = 2

# Connect-Four board itself
class board:
    # X columns by Y rows
    #
    #        0   1   2   3   4   5   ( X )
    #      _________________________
    #   3  |___|___|___|___|___|___|
    #   2  |___|___|___|___|___|___|
    #   1  |___|___|___|___|___|___|
    #   0  |___|___|___|___|___|___|
    #
    # ( Y )

    def __init__(self, x: int, y: int):
        if x < 1 or y < 1:
            raise ValueError(colors.RED + f"ERROR: Invalid board dimensions! ({x}, {y})"  + colors.RESET)

        self.width = x      # Board columns
        self.height = y     # Board rows
        self.player = 0     # Number of player to play (0 or 1)
        self.moves = 0      # Total number of moves this game

        # Board state : Saved as
        self.data = [[] for i in range(x)]
        self.log = ""

    def log(self, message: str):
        self.log += f"{message}\n"

    def clear_log(self):
        self.log = ""

    def swap_player(self):
        self.player = (self.player + 1) % 2

    def place_token(self, x: int):
        if x < 0 or x >= self.width:
            raise IndexError(colors.RED + "ERROR: Attempted to place piece out of bounds!" + colors.RESET)

        arr = self.data[x]
        if len(arr) > self.height:
            print(colors.RED + f"WARNING: No room left in row {x} for this piece!" + colors.RESET)
            return

        arr.append(piece(self.player + 1))
        self.swap_player()
        self.moves += 1

    # Evaluate the state of the board
    def evaluate(self, future = None):
        if future is not None and type(future) is not list:
            raise ValueError(colors.RED + f"ERROR: Invalid move list"  + colors.RESET)

        # Thinking something along the lines of...
        # Check every position on the board
        # If empty, continue
        # If a color, check every adjacency to a potential match
        # For every match, add a point
        # For every empty square, add half a point
        #   Maybe change this: something about (who's playing and can the space be filled/blocked)
        #   Also don't add stuff up that definitely can't be matched?
        #   Alternatively, consider simply providing more points to unblocked middle squares
        # (Reversed if match is opposite color)
        # A single string of four should be worth 16?? (so definitely prioritized)

        raise NotImplimentedError("EVALUATE BOARD STATE")

    def __str__(self):
        # Top bar
        ret = " ___"
        for i in range(self.width - 1):
            ret += "____"

        # Data
        for j in range(self.height):
            ret += "\n|"
            for i in range(self.width):
                y = self.height - j - 1
                arr = self.data[i]

                # Condition depending on board state
                if y < len(arr):
                    val = arr[y]
                    ret += f"_{colors.RED if (val == piece.RED) else colors.BLUE}X{colors.RESET}_|"
                else:
                    ret += "___|"

        # Labels
        ret += "\n ___"
        for i in range(self.width - 1):
            ret += "____"

        ret += "\n|"
        for i in range(self.width):
            ret += f" {i} |"

        ret += f"\n\nMoves: {self.moves}"
        ret += f"\nTurn: {piece(self.player + 1).name}\n"
        return ret

    def __repr__(self):
        ret = ""
        for x, arr in enumerate(self.data):
            ret += f"{x}: "
            ret += repr(arr)
            ret += "\n"

        return ret

if __name__ == "__main__":
    # Workaround for ANSI colors being weird
    os.system("")
    print("Welcome to Connect-4!")

    game = board(7, 6)

    game.place_token(3)
    game.place_token(3)
    game.place_token(1)
    game.place_token(6)
    game.place_token(3)

    print(game)
