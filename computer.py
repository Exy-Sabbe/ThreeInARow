import random

def DecideMove(board):
    squares = board.GetEmptySquares()
    randSquare = random.randint(0, len(squares) - 1)
    return squares[randSquare]