import GameNetwork as Net
import random as rand
from BoardGame import GameBoard

BLACK = 0
WHITE = 1


def alphabeta(board, move, maximize, alpha, beta, depthLeft):
    board = GameBoard(board)
    board.MakeMove(move.fromX, move.fromY, move.toX, move.toY)
    winner = board.GetWinner()
    if winner != None:
        return 1 if winner == BLACK else -1
    if depthLeft == 0:
        return Net.Predict(board)
    moves = findmoves(board)
    if maximize:
        val = -2
        for m in moves:
            val = max(val, alphabeta(board, m, not maximize, alpha, beta, depthLeft - 1))
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return val
    else:
        val = 2
        for m in moves:
            val = min(val, alphabeta(board, m, not maximize, alpha, beta, depthLeft - 1))
            beta = min(beta, val)
            if alpha >= beta:
                break
        return val


def pickmove(board):
    moves = findmoves(board)
    currentpick = None
    if(board.CurrentTurn == BLACK):
        val = -2
        for m in moves:
            temp = alphabeta(board, m, True, -2, 2, 3)
            if temp > val:
                val = temp
                currentpick = m
    else:
        val = 2
        for m in moves:
            temp = alphabeta(board, m, False, -2, 2, 3)
            if temp < val:
                val = temp
                currentpick = m
    return currentpick


'''def findmoves(board):
    if board.CurrentTurn == BLACK:
        pieces = board.BlackPieces
    else:
        pieces = board.WhitePieces

    moves = []
    for p in pieces:
        up = 1
        while board.IsValidMove(p.X, p.Y, p.X, p.Y + up):
            moves.append(Move(p.X, p.Y, p.X, p.Y + up))
            up += 1
        down = 1
        while board.IsValidMove(p.X, p.Y, p.X, p.Y - down):
            moves.append(Move(p.X, p.Y, p.X, p.Y - down))
            down += 1
        left = 1
        while board.IsValidMove(p.X, p.Y, p.X - left, p.Y):
            moves.append(Move(p.X, p.Y, p.X - left, p.Y))
            left += 1
        right = 1
        while board.IsValidMove(p.X, p.Y, p.X + right, p.Y):
            moves.append(Move(p.X, p.Y, p.X + right, p.Y))
            right += 1

    return moves'''''


class Move:
    def __init__(self, fromX, fromY, toX, toY):
        self.fromX = fromX
        self.fromY = fromY
        self.toX = toX
        self.toY = toY

    def __str__(self):
        return str((self.fromX, self.fromY, self.toX, self.toY))


def findmoves(board):
    if board.CurrentTurn == BLACK:
        pieces = board.BlackPieces
    else:
        pieces = board.WhitePieces

    quota = 6
    directions = ['up', 'down', 'left', 'right']
    moves = []
    while quota > 0:
        p = rand.choice(pieces)
        d = rand.choice(directions)
        if d == 'up':
            n = rand.randint(0, p.Y)
            temp = Move(p.X, p.Y, p.X, n)
        elif d == 'down':
            n = rand.randint(p.Y, 7)
            temp = Move(p.X, p.Y, p.X, n)
        elif d == 'left':
            n = rand.randint(0, p.X)
            temp = Move(p.X, p.Y, n, p.Y)
        else:
            n = rand.randint(p.X, 7)
            temp = Move(p.X, p.Y, n, p.Y)

        if board.IsValidMove(temp.fromX, temp.fromY, temp.toX, temp.toY):
            moves.append(temp)
            quota -= 1
    return moves
