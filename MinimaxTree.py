import GameNetwork as Net
import random as rand
from BoardGame import GameBoard
import threading

BLACK = 0
WHITE = 1


def alphabeta(board, move, maximize, alpha, beta, depthLeft):
    #board = GameBoard(board)
    board.MakeMove(move.fromX, move.fromY, move.toX, move.toY)
    winner = board.GetWinner()
    if winner != None:
        board.Undo()
        return 1 if winner == BLACK else -1
    if depthLeft == 0:
        board.Undo()
        return Net.Predict(board)
    moves = findmoves(board)
    if maximize:
        val = -2
        for m in moves:
            val = max(val, alphabeta(board, m, not maximize, alpha, beta, depthLeft - 1))
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        board.Undo()
        return val
    else:
        val = 2
        for m in moves:
            val = min(val, alphabeta(board, m, not maximize, alpha, beta, depthLeft - 1))
            beta = min(beta, val)
            if alpha >= beta:
                break
        board.Undo()
        return val


def pickmove(board):
    moves = findmoves(board)
    results = dict()

    n = len(moves) // 8 if len(moves) >= 8 else len(moves)
    moves = [moves[i*n: (i + 1)*n] for i in range((len(moves) + n - 1) // n)]
    threads = []

    for i in range(8):
        threads.append(threading.Thread(target=evaluate, args=(board, moves[i], results)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    if board.CurrentTurn == BLACK:
        return max(results, key=results.get)
    else:
        return min(results, key=results.get)


def evaluate(board, moves, results):
    #print(moves)
    #print(results)
    board = GameBoard(board)
    for m in moves:
        val = alphabeta(board, m, board.CurrentTurn, -2, 2, 3)
        results.update({m: val})

def findmoves(board):
    if board.CurrentTurn == BLACK:
        pieces = board.BlackPieces
    else:
        pieces = board.WhitePieces

    moves = []
    for p in pieces:
        up = 1
        while CanKeepGoing(board, p.X, p.Y, p.X, p.Y + up):
            if p.X != 3 or p.Y + up != 3:
                moves.append(Move(p.X, p.Y, p.X, p.Y + up))
            up += 1
        down = 1
        while CanKeepGoing(board, p.X, p.Y, p.X, p.Y - down):
            if p.X != 3 or p.Y - down != 3:
                moves.append(Move(p.X, p.Y, p.X, p.Y - down))
            down += 1
        left = 1
        while CanKeepGoing(board, p.X, p.Y, p.X - left, p.Y):
            if p.X - left != 3 or p.Y != 3:
                moves.append(Move(p.X, p.Y, p.X - left, p.Y))
            left += 1
        right = 1
        while CanKeepGoing(board, p.X, p.Y, p.X + right, p.Y):
            if p.X + right != 3 or p.Y != 3:
                moves.append(Move(p.X, p.Y, p.X + right, p.Y))
            right += 1

    return moves


class Move:
    def __init__(self, fromX, fromY, toX, toY):
        self.fromX = fromX
        self.fromY = fromY
        self.toX = toX
        self.toY = toY

    def __str__(self):
        return str((self.fromX, self.fromY, self.toX, self.toY))


def CanKeepGoing(board, fromX, fromY, toX, toY):
    if board.IsValidMove(fromX, fromY, toX, toY):
        return True
    elif toX == 3 and toY == 3 and board.Board[3][3] is None:
        return True
    else:
        return False

'''def findmoves(board):
    if board.CurrentTurn == BLACK:
        pieces = board.BlackPieces
    else:
        pieces = board.WhitePieces

    quota = 16
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
    return moves'''
