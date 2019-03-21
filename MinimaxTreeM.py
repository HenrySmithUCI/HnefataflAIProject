import GameNetwork as Net
import random as rand
from BoardGame import GameBoard
import threading

BLACK = 0
WHITE = 1


def alphabeta(board, alpha = -2, beta = 2, depthLeft = 4):
    #board = GameBoard(board)
    winner = board.GetWinner()
    if winner != None:
        return (-1 if (winner == WHITE) else 1), None, "Win condition"
    if depthLeft == 0:
        return float(Net.Predict(board)), None, "Net prediction"
    moves = findmoves(board)
    bMove = None
    hist = 'depthLeft = ' + str(depthLeft) + '\n'
    if board.CurrentTurn == BLACK:
        hist += 'Black selecting from:\n'
        val = -2
        bHist = ''
        for m in moves:
            board.MakeMove(m.fromX, m.fromY, m.toX, m.toY)
            rVal, _, h = alphabeta(board, alpha, beta, depthLeft - 1)
            hist += str(m) + ': ' + str(rVal) + '\n'
            if rVal > val:
                val = rVal
                bHist = h
                bMove = m
            board.Undo()
            alpha = max(alpha, val)
            if alpha >= beta:
                hist += 'pruned\n'
                break
        hist += "selected " + str(bMove) + ", " + str(val) + "\nHistory:\n" + bHist
        return val, bMove, hist
    else:
        hist += 'White selecting from:\n'
        val = 2
        bHist = ''
        for m in moves:
            board.MakeMove(m.fromX, m.fromY, m.toX, m.toY)
            rVal, _, h = alphabeta(board, alpha, beta, depthLeft - 1)
            hist += str(m) + ': ' + str(rVal) + '\n'
            if rVal < val:
                val = rVal
                bHist = h
                bMove = m
            board.Undo()
            beta = min(beta, val)
            if alpha >= beta:
                hist += 'pruned\n'
                break
        hist += "selected " + str(bMove) + ", " + str(val) + "\nHistory:\n" + bHist
        return val, bMove, hist


def pickmove(board, depth = 3):
    allMoves = findmoves(board)
    results = dict()

    #m = len(moves)
    #n = m // 8 if m >= 8 else 1
    #moves = [moves[i*n: (i + 1)*n] for i in range((m + n - 1) // n)]
    moves = [list() for i in range(8)]
    for (i, move) in enumerate(allMoves):
        moves[i % 8].append(move)
    while len(moves[-1]) == 0:
        moves.pop()
    threads = []

    for moveList in moves:
        threads.append(threading.Thread(target=evaluate, args=(board, moveList, results, depth)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    if board.CurrentTurn == BLACK:
        for m in allMoves:
            print(m)
        ret = max(results, key=results.get)
        for (k, v) in results.items():
            print(k, v, sep = ": ")
        print(ret, results[ret])
        return ret
    else:
        for m in allMoves:
            print(m)
        ret = min(results, key=results.get)
        for (k, v) in results.items():
            print(k, v, sep = ": ")
        print(ret, results[ret])
        return ret


def evaluate(board, moves, results, depth):
    #print(moves)
    #print(results)
    board = GameBoard(board)
    for m in moves:
        board.MakeMove(m.fromX, m.fromY, m.toX, m.toY)
        val = alphabeta(board, True if board.CurrentTurn == BLACK else False, -2, 2, depth)
        board.Undo()
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
            if p.X != 3 or p.Y + up != 3 or p.IsKing:
                moves.append(Move(p.X, p.Y, p.X, p.Y + up))
            up += 1
        down = 1
        while CanKeepGoing(board, p.X, p.Y, p.X, p.Y - down):
            if p.X != 3 or p.Y - down != 3 or p.IsKing:
                moves.append(Move(p.X, p.Y, p.X, p.Y - down))
            down += 1
        left = 1
        while CanKeepGoing(board, p.X, p.Y, p.X - left, p.Y):
            if p.X - left != 3 or p.Y != 3 or p.IsKing:
                moves.append(Move(p.X, p.Y, p.X - left, p.Y))
            left += 1
        right = 1
        while CanKeepGoing(board, p.X, p.Y, p.X + right, p.Y):
            if p.X + right != 3 or p.Y != 3 or p.IsKing:
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
