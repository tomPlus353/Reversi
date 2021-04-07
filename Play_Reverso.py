from Reverso import Game, Player, RandomComputerPlayer, MinimaxPlayer, AlphaBetaPlayer, ChessBoard, Piece
from random import randint
from time import perf_counter

def announceWinner(winner, game):
    if winner == 'player 1':
        print('player 1 is the winner!')
    elif winner == 'player 2':
        print('player2 is the winner!')
    elif winner == 'tie':
        print('It\'s a tie!')
    else:
        print("winner is incorrect value")
        raise ArithmeticError
    print(f"{game.player1.color}/Player 1 score: {game.player1.getScore(game.board)}")
    print(f"{game.player2.color}/Player 2 score: {game.player2.getScore(game.board)}")

def getPlayer(color, type):
    if type == 'human':
            return Player(color)
    else:
        #assign difficulty
        difficulties = ['\n 1. easy\n', '2. normal\n', '3. hard\n']
        while True:
            try:
                choice = int(input(f"Choose your difficulty: {''.join(difficulties)}"))
                choice = choice - 1
                if choice in range(len(difficulties)):
                    break
            except ValueError:
                continue
        if choice == 0:
            print("choice = ",choice)
            return AlphaBetaPlayer(color, difficulty = 1)
        elif choice == 1:
            print("choice = ",choice)
            return AlphaBetaPlayer(color) # default difficulty of 3
        elif choice == 2:
            print("choice = ",choice)
            return AlphaBetaPlayer(color, difficulty=5) 
            #Note: MUST pass in explicit keyword argument. 
            #This overwrites default difficulty 3 becomes 5

def play():
    #get boardsize
    #initialize players
    #initialize game
    #enter the game's main loop
    #get winner
    printBoard = True
    modes = ['\n1. player vs player\n',
    '2. player vs computer\n',
    '3. computer vs computer\n']
    modeTuples = [('human','human'),('human','ai'),('ai','ai')]
    while True:         #One loop = One game
        print(f"Let\'s play Reversi!")
        while True:
            try:
                size = int(input('\nHow big(long and wide) do you want the board to be? \ne.g. for 8*8 board enter "8".\n'))
                if size >= 4 and size % 2 == 0:
                    modeChoice = int(input(f"Select mode:{''.join(modes)}")) - 1
                    if modeChoice in range(len(modes)):
                        mode = modeTuples[modeChoice]
                        break
            except ValueError:
                print('Invalid number')
                continue
        p1color = ['black','white'][randint(0,1)]
        p2color = 'black' if p1color == 'white' else 'white'
        player1 = getPlayer(p1color, mode[0]) # human or ai
        player2 = getPlayer(p2color, mode[1]) # human or ai
        print(f'Player 1, ({player1.type}) is {player1.color}')
        print(f'Player 2, ({player2.type}) is {player2.color}')
        game = Game(size,player1,player2)
        start = perf_counter()
        if modeChoice == 2:
            winner = game.gameplay(printBoard = False)
        else:
            winner = game.gameplay()
        timeTaken = perf_counter() - start
        print(f"Time taken: {timeTaken}")
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
