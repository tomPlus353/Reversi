# Reversi
Creating a python reversi with customizable board size and a choice of players

Reversi is also called Othello. In some cases I refer to it as "reverso" because this name makes more sense to me

Tasks completed so far.

1. Class System for Game, player, board, piece 
2. Human players
3. Random Computer player(Super easy) 
4. Minimax Computer player(easy) 
5. Minimax Computer player(medium)
6. Minimax Computer player(hard)

Minimax calculates the best move from at a given number of moves ahead.

The "best move" is not so easy to determine. We can use the game score, ie how many pieces on the board are your color. However this ignores the strategic importance of various positions such as the edges and the corners. This importance declines towards the endgame, usually defined as the last 20 moves of the game.

To help combat this I created a function to acquire a players 'adjusted score'. It takes into account the high strategic value of corners and edges. Corners are weighted 5x a regular square and edges 3x. This weighting is reduced in the endgame.

This weighting helps. At a depth of 10(where the computer can see 10 moves ahead) the computer beat me, whereas the I can easily beat a computer that has no concept of long term strategic importance of corners and edges.

Further improvements to add

1. Extensive testing
2. Alpha/beta pruning to conserve computing power, allowing for more depth.
3. Refine algorithm through trial and error.
4. As an advanced step, use machine learning to create a model the computer can reference.





