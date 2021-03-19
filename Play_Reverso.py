from Reverso import Game, Player, ChessBoard, Piece
from random import randint
from blender import bcolors

def pvp():
	#get boardsize
	#initialize players 
	#initialize game
	#enter the game's main loop
	#get winner
	

	while True: 		#One loop = One game
		print(f"{bcolors.WARNING}Let\'s play Reversi!{bcolors.ENDC}")
		while True:
			try:
				size = int(input('\nHow big(long and wide) do you want the board to be? \ne.g. for 8*8 board enter "8".\n'))
				if size > 4 and size % 2 == 0:
					break
			except ValueError:
				continue
		p1color = ['black','white'][randint(0,1)]
		player1 = Player(p1color)
		print(f'Player 1 is {player1.color}')
		if player1.color == 'black':
			player2 = Player('white')
			print(f'Player 2 is {player2.color}')
		elif player1.color == 'white':
			player2 = Player('black')
			print(f'Player 2 is {player2.color}')

		game = Game(size,player1,player2)
		winner = game.gameplay()
		if winner == 'player 1':
			print('player 1 is the winner!')
			print(f"{game.player1.color}/Player 1 score: {game.player1.getScore(game.board)}")
			print(f"{game.player2.color}/Player 2 score: {game.player2.getScore(game.board)}")
		elif winner == 'player 2':
			print('player2 is the winner!')
			print(f"{game.player1.color}/Player 1 score: {game.player1.getScore(game.board)}")
			print(f"{game.player2.color}/Player 2 score: {game.player2.getScore(game.board)}")
		elif winner == 'tie':
			print('It\'s a tie!')
			print(f"{game.player1.color}/Player 1 score: {game.player1.getScore(game.board)}")
			print(f"{game.player2.color}/Player 2 score: {game.player2.getScore(game.board)}")
		yesNo = False
		while True:
			yesNo = input('Play again? [y]/[n]')
			if yesNo in ['yes','y','no','n']:
				break

		if yesNo.lower() in ['no','n']:
			break	#if program gets to here yesNo was 'yes' or 'y'






if __name__ == '__main__':
	pvp()
