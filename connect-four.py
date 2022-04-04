# Connect Four AI
# Artificial Intelligence: Project 2
# Liam Dempsey
# 10754465

import copy
import enum
import os

MAX_DEPTH = 8
# DIRECTIONS = [		\
# 	( 0,  1),		\
# 	( 1,  1),		\
# 	( 1,  0),		\
# 	( 1, -1)
# ]

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
		self.final = x * y 	# Maximum number of moves before game end

		# Board state : Saved as
		self.data = [[] for i in range(x)]
		self.log = ""

	def copy(self):
		new = board(self.width, self.height)

		new.player = self.player
		new.moves = self.moves
		new.data = copy.deepcopy(self.data)

		return new

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
		if len(arr) >= self.height:
			raise IndexError(f"Row is full ({x})")

			# Old interface
			print(colors.RED + f"WARNING: No room left in row {x} for this piece!" + colors.RESET)
			return

		arr.append(piece(self.player + 1))
		self.swap_player()
		self.moves += 1

	# Helper function for the static state evaluation
	def evaluate_arr(self, arr):
		redScore = 0
		blueScore = 0

		# Intermediate values
		indexes = []
		lastindex = 0
		matchlen = 0
		prevtoken = piece.RED		# Should be only red or blue, so assume RED

		# Iterate input array
		for x, token in enumerate(arr):
			if token == piece.NONE:
				matchlen = 0
				continue

			# Opposite color token
			if token != prevtoken:
				# Determine value of match
				length = x - lastindex

				# Update values
				lastindex = x
				matchlen = 0

				# Maximum local value is 0 if length < 4 (because len - 3)
				if length >= 4:
					maxval = 0
					for index in indexes:
						distance = min(index, length - index - 1)
						val = min(distance, length - 3)
						maxval = max(val, maxval)

					if prevtoken == piece.RED: redScore += len(indexes) * maxval
					else: blueScore += len(indexes) * maxval		# If first token in blue, len(indexes will be 0)

				indexes = []
				# Skip remaining tokens if no match possible
				if (len(arr) - x) < 4: return redScore, blueScore

			# Check if match is made
			matchlen += 1
			if matchlen >= 4:
				if token == piece.RED: return 24, 0
				else: return 0, 24

			indexes.append(x - lastindex)
			prevtoken = token

		# Final evaluation
		length = len(arr) - lastindex
		if length >= 4:
			maxval = 0
			for index in indexes:
				distance = min(index, length - index - 1)
				val = min(distance + 1, length - 3)
				maxval = max(val, maxval)
				# print(f"length: {length}\ndistance: {distance}\nval: {val}\nmaxval: {maxval}")

			if prevtoken == piece.RED: redScore += len(indexes) * maxval
			else: blueScore += len(indexes) * maxval

		return redScore, blueScore

	# Evaluate the state of the board (new evaluation)
	def evaluate(self):
		redScore = 0
		blueScore = 0

		# Check for matches horizontally
		for y in range(self.height):
			row = []

			for x in range(self.width):
				token = piece.NONE

				# If token does not exist, array location is out of bounds
				try: token = self.data[x][y]
				except IndexError: pass

				row.append(token)

			# print(row)
			score = self.evaluate_arr(row)
			redScore += score[0]
			blueScore += score[1]

		# Check for matches vertically
		for row in self.data:
			rowcp = copy.copy(row)
			for x in range(self.height - len(row)): rowcp.append(piece.NONE)

			score = self.evaluate_arr(rowcp)
			redScore += score[0]
			blueScore += score[1]

		# Check matches diagonally (up-left)
		for x in range(3, 9):
			row = []

			for y in range(self.height):
				xi = x - y
				if xi < 0: break
				if xi >= self.width: continue

				token = piece.NONE
				try: token = self.data[xi][y]
				except IndexError: pass

				row.append(token)

			score = self.evaluate_arr(row)
			redScore += score[0]
			blueScore += score[1]

		# Check matches diagonally (up-right)
		for x in range(-2, 4):
			row = []

			for y in range(self.height):
				xi = x + y
				if xi < 0: continue
				if xi >= self.width: break

				token = piece.NONE
				try: token = self.data[xi][y]
				except IndexError: pass

				row.append(token)

			score = self.evaluate_arr(row)
			redScore += score[0]
			blueScore += score[1]

		return redScore - blueScore

	# Evaluate the state of the board
	'''
	def evaluate(self):
		redScore = 0
		blueScore = 0

		# UP, UP-RIGHT, RIGHT, DOWN-RIGHT, DOWN, DOWN-LEFT, LEFT, UP-LEFT
		directions = [		\
			( 0,  1),		\
			( 1,  1),		\
			( 1,  0),		\
			( 1, -1)		\
			# ( 0, -1),		\
			# (-1, -1),		\
			# (-1,  0),		\
			# (-1,  1)		\
		]

		# Prevents high evaluations for long strings of pieces
		matches = {}
		matches[piece.RED] = {}
		matches[piece.BLUE] = {}

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

						matchExists = False
						try:
							coord = matches[token][dir]
							if coord == (xi, yi): matchExists = True

						except KeyError: pass

						if ttoken != token or matchExists:
							dirscore = 0
							break

						dirscore *= 3

					# Update the intermediate score
					score += dirscore

					# Add relevant squares to the match blocker
					if dirscore > 25:
						xi = x + 3 * dir[0]
						yi = y + 3 * dir[1]
						matches[token][(dir[0] * -1, dir[1] * -1)] = (xi, yi)

				# Update the color score
				if token == piece.RED: redScore += score
				elif token == piece.BLUE: blueScore += score

		return redScore - blueScore'''

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


# Tree to house board states (saves duplication of processes)
class tree:
	def __init__(self, b):
		self.board = b
		self.children = []

	# Generate the future states
	def procreate(self):
		# Failsafe so children are not duplicated
		if len(self.children) > 0: return

		for i in range(self.board.width):
			new = self.board.copy()
			try: new.place_token(i)
			except IndexError: continue
			self.children.append(tree(new))

	# Perform a minimax evaluation to determine the next best move
	# Returns FALSE if game end
	def advance(self, debug = False):
		global MAX_DEPTH

		# Do not advance the board if no further progress can be made
		if self.board.moves >= self.board.final:
			print("WARNING: End of game (no further moves)")
			return False

		# Ensure that the tree has children to evaluate
		self.procreate()

		# Perform minimax evaluation on each child
		bestEval = float('-inf')	# Value of best move so far
		bestIndex = 0				# Index of best move so far
		print(f" -- MOVE {self.board.moves + 1} EVALUATION --")

		maxPlayer = True if (self.board.player == 0) else False
		if not maxPlayer: bestEval *= -1
		for x, child in enumerate(self.children):
			if debug: eval = child.board.evaluate()
			else: eval = child.evaluate(MAX_DEPTH - 1, float('-inf'), float('inf'), not maxPlayer)

			# Debug output
			print(f"Column: {x} | Evaluation: {eval}")

			if maxPlayer and eval > bestEval:
				bestEval = eval
				bestIndex = x

			elif not maxPlayer and eval < bestEval:
				bestEval = eval
				bestIndex = x
		print()

		# Advance the board
		new = self.children[bestIndex]
		self.board = new.board
		self.children = new.children
		return True

	# Minimax function itself
	def evaluate(self, depth, alpha, beta, maxPlayer):
		if depth == 0 or self.board.moves == self.board.final:
			return self.board.evaluate()

		self.procreate()

		# Maximizing player
		if maxPlayer:
			maxEval = float('-inf')
			for child in self.children:
				eval = child.evaluate(depth - 1, alpha, beta, False)
				maxEval = max(maxEval, eval)
				alpha = max(alpha, eval)
				if beta <= alpha: break
			return maxEval

		# Minimizing player
		else:
			minEval = float('inf')
			for child in self.children:
				eval = child.evaluate(depth - 1, alpha, beta, True)
				minEval = min(minEval, eval)
				beta = min(beta, eval)
				if beta <= alpha: break
			return minEval


if __name__ == "__main__":
	# Workaround for ANSI colors being weird
	os.system("")
	print("Welcome to Connect-4!")

	init = board(7, 6)
	# init.data[0].append(piece.BLUE)
	# init.data[1].append(piece.BLUE)
	# init.data[2].append(piece.RED)
	# init.data[3].append(piece.RED)
	# init.data[4].append(piece.RED)
	# init.data[0].append(piece.BLUE)
	# init.data[0].append(piece.RED)
	# init.data[0].append(piece.RED)
	# init.data[0].append(piece.RED)
	# init.data[6].append(piece.RED)
	# print(init)
	# exit()

	# Tree type used to advance the board state
	game = tree(init)
	print(game.board)

	while True:
		input("Press any key to continue...\n")
		game.advance(False)
		print(game.board)
