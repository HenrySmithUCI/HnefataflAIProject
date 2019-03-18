import GameNetwork as Net

BLACK = 0
WHITE = 1


def alphabeta(board, move, max, alpha, beta, depthLeft):
    board.MakeMove(move.fromX, move.fromY, move.toX, move.toY)
    winner = board.getewinner()
    if winner is not None:
        return winner
    if depthLeft == 0:
        return Net.Predict(board)
    moves = findmoves(board)
    if max:
        val = -2
        for m in moves:
            val = max(val, alphabeta(board, m, not max, alpha, beta, depthLeft - 1))
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return val
    else:
        val = 2
        for m in moves:
            val = min(val, alphabeta(board, m, not max, alpha, beta, depthLeft - 1))
            beta = min(beta, val)
            if alpha >= beta:
                break
        return val


def pickmove(board):
    moves = findmoves(board)
    currentpick = None
    val = 2
    for m in moves:
        temp = alphabeta(board, m, True, -2, 2, 5)
        if temp > val:
            val = temp
            currentpick = m
    return currentpick


def findmoves(board):
    if board.CurrentTurn == BLACK:
        pieces = board.BlackPieces
    else:
        pieces = board.WhitePieces

    moves = []
    for p in pieces:
        up = 1
        while board.IsValidMove(p.fromX, p.fromY, p.toX, p.toY + up):
            moves.append(move(p.fromX, p.fromY, p.toX, p.toY + up))
            up += 1
        down = 1
        while board.IsValidMove(p.fromX, p.fromY, p.toX, p.toY - down):
            moves.append(move(p.fromX, p.fromY, p.toX, p.toY - down))
            down += 1
        left = 1
        while board.IsValidMove(p.fromX, p.fromY, p.toX - left, p.toY):
            moves.append(move(p.fromX, p.fromY, p.toX - left, p.toY))
            left += 1
        right = 1
        while board.IsValidMove(p.fromX, p.fromY, p.toX + right, p.toY):
            moves.append(move(p.fromX, p.fromY, p.toX + right, p.toY + u))
            right += 1

    return moves


class Move:
    def __init__(self, fromX, fromY, toX, toY):
        self.fromX = fromX
        self.fromY = fromY
        self.toX = toX
        self.toY = toY
