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
	def evaluate(self):
		redScore = 0
		blueScore = 0

		# UP, UP-RIGHT, RIGHT, DOWN-RIGHT, DOWN, DOWN-LEFT, LEFT, UP-LEFT
		directions = [		\
			( 0,  1),		\
			( 1,  1),		\
			( 1,  0),		\
			( 1, -1),		\
			( 0, -1),		\
			(-1, -1),		\
			(-1,  0),		\
			(-1,  1)		\
		]

		# -- EVALUATION FUNCTION ALGORITHM --
		# Each token is worth one point if a match is possible in its direction
		# i.e. one in the middle can potentially match 8* directions
		# 	whereas one in the corner could only match in 3
		# Do not evaluate "middle" positions, as this is handled implicitly when checking other tokens
		# For each existing potential match in a row: row doubles in value:
		# 	1 token -> 1, 2 -> 2, 3 -> 4, 4 -> 8

		# Potential adjustments?
		#  + 1 point for each token that could appear there next round
		#  - 1 point for each token that could block it next round???
		#
		#  *2/+16 if a match is guaranteed (i.e. two empty rows of three)

		# -- Iterate every position on the board --
		# 'x' is current column number
		for x in range(self.width):
			arr = self.data[x]
			for y, token in enumerate(arr):
				# Starts with bottom left and works up and then right
				if token == piece.NONE:
					print("WARNING: Board state may be invalid!")
					continue;

				# Begin counting up the token score
				score = 0

				# Iterate directions
				for dir in directions:
					dirscore = 1
					for i in range(3):
						xi = x + (3 - i) * dir[0]
						yi = y + (3 - i) * dir[1]

						# Make sure match is possible on board
						if xi < 0 or yi < 0 or xi >= self.width or yi >= self.height:
							dirscore = 0
							break

						ttoken = None
						try: ttoken = self.data[xi][yi]
						except IndexError: continue

						if ttoken == token: multiplier *= 2
						else:
							dirscore = 0
							break

					# Update the intermediate score
					score += dirscore

				# Update the color score
				if token == piece.RED: redScore += score
				elif token == piece.BLUE: blueScore += score

		return redScore - blueScore

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
		ret += f"\nTurn: {piece(self.player + 1).name}"
		ret += f"\nEvaluation: {self.evaluate()}\n"
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

	game.place_token(1)
	game.place_token(3)
	print(game)
	exit()

	game.place_token(1)
	game.place_token(6)
	game.place_token(3)

	print(game)
