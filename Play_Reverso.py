from Reverso import Game, Player, ChessBoard, Piece
from random import randint
from blender import bcolors

def announceWinner(winner, game):
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

def getPlayer(color, type):
	if type == 'human':
		return Player(color)
	difficulties = ['easy', 'normal', 'hard']
	diff == getDifficulty(difficulties)
	if diff == difficulties[0]:
		return randomAI(color)
	elif diff == difficulties[1]:
		return smartAI(color)
	elif diff == difficulties[2]:
		return 'class pending'


def getDifficulty(difficulties):
	while True:
		try:
			choice = int(input(f"Choose your difficulty: {"\n".join(difficulties)}\n")) - 1
			if choice in range(len(difficulties))
		except ValueError:
			continue
	return difficulties[choice]

def play():
	#get boardsize
	#initialize players 
	#initialize game
	#enter the game's main loop
	#get winner
	modes = ['1. player vs player',
	'2. player vs computer',
	'3. computer vs computer']
	modeTuples = [('human','human'),('human','ai'),('ai','ai')]
	while True: 		#One loop = One game
		print(f"{bcolors.WARNING}Let\'s play Reversi!{bcolors.ENDC}")
		while True:
			try:
				size = int(input('\nHow big(long and wide) do you want the board to be? \ne.g. for 8*8 board enter "8".\n'))
				if size > 4 and size % 2 == 0:
					mode = modeTuples[int(input(f"Select mode:{'\n'.join(modes)}")) - 1]
			except ValueError:
				continue
		p1color = ['black','white'][randint(0,1)]
		p2color = 'black' if p1color == 'white' else 'white'
		player1 = getPlayer(p1color, mode[0])
		player2 = getPlayer(p2color, mode[1])
		print(f'Player 1, ({player1.type}) is {player1.color}')
		print(f'Player 2, ({player2.type}) is {player2.color}')

		game = Game(size,player1,player2)
		winner = game.gameplay()
		announceWinner(winner, game)
		while True:
			yesNo = input('Play again? [y]/[n]')
			if yesNo.lower() in ['yes','y','no','n']:
				break

		if yesNo.lower() in ['no','n']:
			break
		#if program gets to here yesNo was 'yes' or 'y'


if __name__ == '__main__':
	play()
