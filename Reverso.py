from random import randint
from copy import deepcopy
from blender import bcolors
import math
class ChessBoard:

	def __init__(self, size = 8): #note, size must even
		if size < 4 or size % 2 != 0:
			return False
		self.board = self.makeBoard(size)
		self.size = size
		self.possiblePositions = [(x,y) for x in range(self.size) for y in range(self.size)]
		self.pieces = {}
		self.midPoints = self.getMidpoints(size)
		counter = 1
		for m in self.midPoints:
			if counter == 1 or counter == 4:
				Piece(m, 'white', self)
			else:
				Piece(m, 'black',self)
			counter += 1
		#print(self.pieces)

	def getEmpty(self):
		return len([x for x in self.possiblePositions if x not in self.pieces])

	def makeBoard(self, size):
		numBoard = [[x for x in range(1,size+1)]for y in range(1,size+1)]
		counter = 1
		for row in numBoard:
			if counter % 2 != 0:
					for square in row:
							if square % 2 != 0:
									row[row.index(square)] = "■"
							else:
									row[row.index(square)] = "□"
			else:
					for square in row:
							if square % 2 == 0:
									row[row.index(square)] = "■"
							else:
									row[row.index(square)] = "□"
			counter += 1
		return numBoard

	def refreshBoard(self):
		for rowno in range(self.size):
			for columnno in range(self.size):
				#print(rowno,columnno)
				if (rowno,columnno) in self.pieces:
					if self.pieces[(rowno,columnno)].color == 'black': 
						self.board[rowno][columnno] = 'B'
					else:
						self.board[rowno][columnno] = 'W'

	def printBoard(self):
		self.refreshBoard()
		for row in self.board: 
			print(" ".join(row))

	def printPlayerOptions(self, availableMoves):
		self.refreshBoard()
		copy = deepcopy(self.board)
		counter = 1
		for x,y in availableMoves: #if we minus one from counter we should have index for availableMoves
			copy[x][y] = str(counter)
			counter += 1
		for row in copy:
			print(" ".join(row))
		del copy


	def getMidpoints(self, size):
		halfway = int((size - 2) / 2)
		return [(halfway,halfway),(halfway,1+halfway),(1+halfway,halfway),(1+halfway,1+halfway)]
		
	def getAvailableMoves(self, player):
		#Condition 1: is on the board!
		#Condition 2: square not occupied already
		emptySquares = [t for t in self.possiblePositions if t not in self.pieces]
		availableMoves = []
		#Condition 3a: is adjacent to an enemy piece AND
		#Condition 3b: will result in enemy squares acquired
		#i.e. at the end of row/column there is piece of the same color.
		#note: [(x,y) for x,y in self.pieces] >> list of tuples! i.e. x,y refer to the tuple KEY not key and value
		for square in emptySquares:
			#print(square)
			if len(self.getFlippable(square,player)) > 0:
				availableMoves.append(square)
		return availableMoves

	def addPiece(self, piece): # ONLY called if move passes availableMoves
		self.pieces[piece.position] = piece # we use position instead of ID since position does not change and will be used alot.

	def getFlippable(self, position, player): # returns a list of postions that will be flipped given a move(which is ON the board and in an EMPTY square.
		flippablePositions = []
		myX=position[0]
		myY=position[1]
		#1. find the first piece in a line from position
		#2. get a list of the positions BETWEEN first piece
		#3. add to a list of positions to be flipped.		
		#4. repeat 8 times!
		for x,y in [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]:
			#below code executes once for each direction
			ally = None
			enemyList = []
			for d in range(1,self.size):
				squarePos = (myX+x*d, myY+y*d)
				#print(squarePos)
				if squarePos in self.pieces:
					square = self.pieces[squarePos] # extracts copy of the piece object
					if square.color == player.color:
						ally = squarePos # this may prove useful when designing an AI player
						break
					elif square.color != player.color:
						enemyList.append(squarePos)
				else: #either a blank square OR off the edge of the board.
					break  #stops counting
			#count each line
			if ally != None and enemyList:
				flippablePositions.extend(enemyList)
		return flippablePositions # list of postions to be flipped

class Piece:
	def __init__(self, position, color, board):
		self.position = position # this will never change in reverso
		self.color = color
		if position in board.possiblePositions:
			board.addPiece(self)
		else:
			raise ArithmeticError

	
	def changeColor(self):
		if self.color == 'white':
			self.color = 'black'
		else:
			self.color = 'white'

class Player:
	def __init__(self, color, type='Human'):
		self.color = color
		self.type = type
		self.score = int #NOTE: never actually call this. Use getScore instead

	def getMove(self, board, game=None): #optional argument game is only for minimax
		availableMoves = board.getAvailableMoves(self)
		if len(availableMoves) == 0:
			print(f"{self.color} has no moves!")
		else:
			board.printPlayerOptions(availableMoves)
			while True:
				choice = input(f'Enter the number of your move. ({1} - {len(availableMoves)})')
				try:
					numChoice = int(choice) - 1
					if numChoice in range(len(availableMoves)):
						move = availableMoves[numChoice]
						break
				except ValueError:
					continue
			self.makeMove(move, board)

	def makeMove(self, position, board):
		flipList = board.getFlippable(position, self)
		if len(flipList) > 0: #should always be more than 0, we already checked this 'position' with getFlippable
			#updates 1)flip board.pieces 2)flip pieces themselves 
			#3)add the actual new piece to board.pieces 4)update the physical board? -> no, that will be updated during print.
			Piece(position, self.color, board) # adds to board
			for x,y in flipList:
				if board.pieces[(x,y)].color == self.color: #one final check if the color to be flipped was ALREADY flipped then need to check isValidMove + getFlippableMoves
					raise ValueError
				else:
					board.pieces[(x,y)].color = self.color
		else:
			print('Error: printing flipList and position variables', flipList, position)
			board.printBoard()
			raise ArithmeticError

	def getScore(self, board): # updates score in self and returns that score
		score = 0
		for piece in board.pieces:
			if board.pieces[piece].color == self.color:
				score += 1
		self.score = score
		return self.score

class RandomComputerPlayer(Player):
	def __init__(self, color, type='AI'):
		super().__init__(color, type)

	def getMove(self, board, game = None): #optional game argument for Minimax
		availableMoves = board.getAvailableMoves(self)
		if len(availableMoves) == 0:
			print(f"{self.color} has no moves!")
		else:
			move = availableMoves[randint(0,len(availableMoves)-1)] # minus one because randint is INCLUSIVE
			self.makeMove(move, board)

class MinimaxPlayer(Player):
	def __init__(self, color, type='AI'):
		super().__init__(color, type)

	def getMove(self, board, game):
		availableMoves = board.getAvailableMoves(self)
		if len(availableMoves) == 0:
			print(f"{self.color} has no moves!")
		else:
			simGame = deepcopy(game)
			move = self.minimax(simGame, self.color)
			del simGame	
			self.makeMove(move, board)

	def minimax(self, simGame, currentColor):
		maxPlayer = self.color #constantly remains the current player
		otherColor = 'black' if currentColor == 'white' else 'white'
		#so we have three colours: maxPlayer, playercolor, othercolor

		#1. first we want to check if the previous move is a winner
		# this is our base case
		#we refer to otherColor to get previous move
		print(simGame.checkWinner(),simGame.winner, simGame.player1.getScore(simGame.board),simGame.player2.getScore(simGame.board), currentColor, otherColor) #DEBUGGING
		if simGame.checkWinner():
		#if simGame.winner == otherColor: #this does not tell us if otherColor is maxplayer or not
			if maxPlayer == otherColor:
				return {'position': None, 'score': 1 * (simGame.board.getEmpty() + 1)}
			else:
				return {'position': None, 'score': -1 * (simGame.board.getEmpty() + 1)}
		if simGame.board.getEmpty() == 0 or simGame.winner == 'tie':
				return {'position': None, 'score': 0}

		#2. initialize dictionaries to keep score
		if currentColor == maxPlayer:
			best = {'position': None, 'score': -math.inf}
		else:
			best = {'position': None, 'score': math.inf}
		
		#3 loop
		if len(simGame.board.getAvailableMoves(simGame.getPlayerByColor(currentColor))) > 0:
			for availableMove in simGame.board.getAvailableMoves(simGame.getPlayerByColor(currentColor)):
				#input(f'available moves: {simGame.board.getAvailableMoves(simGame.getPlayerByColor(currentColor))}')
				# step 0: save the pieces so we don't have to reflip them
				previousPieces = simGame.board.pieces
				# step 1: make a move, try that spot
				simGame.getPlayerByColor(currentColor).makeMove(availableMove, simGame.board) #we get the current player object, but player data remains static throughout the game.
				# step 2: recurse using minimax to simulate a game after making that move
				simScore = self.minimax(simGame, otherColor)
				# step 3: undo the move -> it will have to recurse here one more time for everytime you call minimax
					#a. remove piece from board.
					#b. unflip the pieces
				simGame.board.pieces = previousPieces
					#c. reset winner in case a player won
				simGame.winner == None
					#d. reset the dictionary position 
					# WHY? -> so we can evaluate that move vs the score coming from that move.
				simScore['position'] = availableMove 
				# step 4: update the dictionaries if necessary
				if currentColor == maxPlayer: #maximize
					if simScore['score'] > best['score']: # on the first run best score will be -infinity
						best = simScore
				else: #minimize the other player
					if simScore['score'] < best['score']:
						best = simScore
			else: #player passes if they have no moves
				#same as above but no makeMove
				previousPieces = simGame.board.pieces
				simScore = self.minimax(simGame, otherColor)
				simGame.board.pieces = previousPieces
				simGame.winner == None
				simScore['position'] = None
				if currentColor == maxPlayer: #maximize
					if simScore['score'] > best['score']: # on the first run best score will be -infinity
						best = simScore
				else: #minimize the other player
					if simScore['score'] < best['score']:
						best = simScore
		return best

class Game:
	def __init__(self,size,player1,player2): #players pre-initialized
		self.board = ChessBoard(size)
		self.player1 = player1
		self.player2 = player2
		self.winner = None

	def getPlayerByColor(self, color):
		if self.player1.color == color:
			return self.player1
		else:
			return self.player2

	def checkWinner(self):
		#1. check if the game is over or not
		  #Condition 1: no empty squares left
		  #Condition 2: neither p1 or p2 have an available move
		  #Actually condition 2 covers condition one
		#2. check who won
		p1Moves = self.board.getAvailableMoves(self.player1)
		p2Moves = self.board.getAvailableMoves(self.player2)
		if len(p1Moves) == 0 and len(p2Moves) == 0:
			#game has ended and now we just count the scores
			if self.player1.getScore(self.board) > self.player2.getScore(self.board):
				self.winner = 'player 1'
				return self.player1.color
			elif self.player1.getScore(self.board) < self.player2.getScore(self.board):
				self.winner = 'player 2'
				return self.player2.color
			else:
				self.winner = 'tie'
				return 'tie'
		return None

	def gameplay(self):
		#print board
		#get player's choice
		#test if valid
		#Execute if so
		#print updated board.
		#loop until winner
		#return winner
		turn = ['player 1','player 2'][randint(0,1)]
		while self.winner == None:
			self.board.printBoard()
			print(f"{self.player1.color}/Player 1 score: {self.player1.getScore(self.board)}")
			print(f"{self.player2.color}/Player 2 score: {self.player2.getScore(self.board)}")
			print(f"It is {turn}'s turn")
			#player takes their turn
			if turn == 'player 1':
				self.player1.getMove(self.board, self)
			elif turn == 'player 2':
				self.player2.getMove(self.board, self)
			else:
				raise ArithmeticError
			self.board.printBoard()
			print(f"{self.player1.color}/Player 1 score: {self.player1.getScore(self.board)}")
			print(f"{self.player2.color}/Player 2 score: {self.player2.getScore(self.board)}")
			if self.checkWinner(): #no need to return as checkWinner will update the game object directly
				return self.winner #returns to main program(play_reverso)
			turn = 'player 1' if turn =='player 2' else 'player 2'
