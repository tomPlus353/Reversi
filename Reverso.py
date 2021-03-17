from random import randint
from copy import deepcopy
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
						self.board[rowno][columnno] = '⚫'
					else:
						self.board[rowno][columnno] = '⚪'

	def printBoard(self):
		self.refreshBoard()
		for row in self.board: 
			print("".join(row))

	def printPlayerOptions(self, availableMoves):
		self.refreshBoard()
		copy = deepcopy(self.board)
		counter = 1
		for x,y in availableMoves: #if we minus one from counter we should have index for availableMoves
			copy[x][y] = str(counter)
			counter += 1
		for row in copy:
			print("".join(row))
		print('Is copy the same as self.board?', copy == self.board)


	def getMidpoints(self, size):
		halfway = int((size - 2) / 2)
		return [(halfway,halfway),(halfway,1+halfway),(1+halfway,halfway),(1+halfway,1+halfway)]
	
	def isValidMove(self, position, player): #self = board
		#Condition 1: is on the board!
		if position not in self.possiblePositions:
			return False
		
		#Condition 2: square not occupied already
		if position in self.pieces: #piece = unique position
			return False
		#Condition 3a: is adjacent to an enemy piece AND
		#Condition 3b: will result in enemy squares acquired
		#i.e. at the end of row/column there is piece of the same color.
		#note: [(x,y) for x,y in self.pieces] >> list of tuples! i.e. x,y refer to the tuple KEY not key and value

##		myX = position[0]
##		myY = position[1]
##		adjacentMoves = [(myX+1,myY),(myX-1,myY),(myX-1,myY-1),(myX-1,myY+1),(myX,myY+1),(myX,myY-1),(myX+1,myY-1),(myX+1,myY-1)]
##		while True:
##			for square in adjacentMoves:
##				if square in self.pieces:
##					if self.pieces[square].color != player.color: #e.g if player is black and adjacent piece is white
##						break
##			return False
		#position has cleared 3a now test 3b
		flippablePositions = self.getFlippable(position,player)
		#print('flippable positions after return within isValidMove:',flippablePositions)
		if len(flippablePositions) > 0: # will return false if no flippable postions
			return flippablePositions
		else:
			return False 
		
	def getAvailableMoves(self, player):
		#print('getAvailableMoves called!')
		emptySquares = [t for t in self.possiblePositions if t not in self.pieces]
		#print('emptySquares: ', emptySquares)
		availableMoves = []
		for square in emptySquares:
			#print(square)
			if self.isValidMove(square,player):
				availableMoves.append(square)
		return availableMoves

	def addPiece(self, piece): # ONLY called if move passes isValidMove
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


#board = ChessBoard(size=20)
#board.printEmpty()


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

	def makeMove(self, position, board):
		validList = board.isValidMove(position, self)
		if validList != False: #self=player
			#updates 1)flip board.pieces 2)flip pieces themselves 
			#3)add the actual new piece to board.pieces 4)update the physical board? -> no, that will be updated during print.
			Piece(position, self.color, board) # adds to board
			for x,y in validList:
				if board.pieces[(x,y)].color == self.color: #one final check if the color to be flipped was ALREADY flipped then need to check isValidMove + getFlippableMoves
					raise ValueError
				else:
					board.pieces[(x,y)].color = self.color
		else:
			return False # user should be prompted for other move
			

	def getScore(self, board): # updates score in self and returns that score
		score = 0
		for piece in board.pieces:
			if board.pieces[piece] == self.color:
				score += 1

		self.score = score
		return self.score

class Game:

	def __init__(self,size,player1,player2): #players pre-initialized
		self.board = ChessBoard(size)
		self.player1 = player1
		self.player2 = player2
		self.winner = None

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
				return True
			elif self.player1.getScore(self.board) < self.player2.getScore(self.board):
				self.winner = player2
				return True
			else:
				self.winner = 'tie'
				return True
		return False 


		

	def gameplay(self):
		#print board 
	######NOTE get available moves and have the user select them.########################
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
				availableMoves = self.board.getAvailableMoves(self.player1) #BUG HERE
				if len(availableMoves) == 0:
					print(f"{self.player1} has no moves!")
				else:
					self.board.printPlayerOptions(availableMoves)
					while True:
						choice = input(f'Enter the number of your move. ({1} - {len(availableMoves)})')
						try:
							numChoice = int(choice) - 1
							if numChoice in range(len(availableMoves)):
								move = availableMoves[numChoice]
								break
						except ValueError:
							continue
					self.player2.makeMove(move, self.board)
			elif turn == 'player 2':
				availableMoves = self.board.getAvailableMoves(self.player2)
				if len(availableMoves) == 0:
					print(f"{self.player2} has no moves!")
				else:
					self.board.printPlayerOptions(availableMoves)
					while True:
						choice = input(f'Enter the number of your move. ({1} - {len(availableMoves)})')
						try:
							numChoice = int(choice) - 1
							if numChoice in range(len(availableMoves)):
								move = availableMoves[numChoice]
								break
						except ValueError:
							continue
					self.player2.makeMove(move, self.board)
			else:
				raise ArithmeticError
			self.board.printBoard()
			print(f"{self.player1.color}/Player 1 score: {self.player1.getScore(self.board)}")
			print(f"{self.player2.color}/Player 2 score: {self.player2.getScore(self.board)}")
			if self.checkWinner(): #no need to return as checkWinner will update the game object directly
				return self.winner #returns to main program(play_reverso)
			else:
				if turn == 'player 1':
					turn = 'player 2'
				else:
					turn = 'player 1'











	
		
		
		
		
		
