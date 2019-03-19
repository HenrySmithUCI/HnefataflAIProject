BLACK = 0
WHITE = 1


class Piece:
    def __init__(self, game, team, posX, posY, isKing=False, alive = True):
        self.Game = game
        self.Team = team
        self.X = posX
        self.Y = posY
        self.IsKing = isKing
        self.Alive = True

class Move:
    def __init__(self, fromX, fromY, toX, toY, piecesKilled = []):
        self.fromX = fromX
        self.fromY = fromY
        self.toX = toX
        self.toY = toY
        self.piecesKilled = piecesKilled

class GameBoard:
    def __init__(self, copy = None):
        board = []

        for x in range(7):
            board.append([])
            for y in range(7):
                board[x].append(None)
        
        if(copy == None):
            self.CurrentTurn = BLACK
            self.History = []
            self.Pieces = [
                Piece(self, BLACK, 3, 0),
                Piece(self, BLACK, 3, 1),
                Piece(self, BLACK, 0, 3),
                Piece(self, BLACK, 1, 3),
                Piece(self, BLACK, 3, 5),
                Piece(self, BLACK, 3, 6),
                Piece(self, BLACK, 5, 3),
                Piece(self, BLACK, 6, 3),

                Piece(self, WHITE, 3, 3, True),
                Piece(self, WHITE, 3, 2),
                Piece(self, WHITE, 3, 4),
                Piece(self, WHITE, 2, 3),
                Piece(self, WHITE, 4, 3)
            ]
        else:
            self.CurrentTurn = copy.CurrentTurn
            self.History = []
            self.Pieces = []
            for p in copy.Pieces:
                self.Pieces.append(Piece(self, p.Team, p.X, p.Y, p.IsKing, p.Alive))
            
        for p in self.Pieces:
            board[p.X][p.Y] = p

        self.Board = board
        self.BlackPieces = self.Pieces[:8]
        self.WhiteKing = self.Pieces[8]
        self.WhitePieces = self.Pieces[-5:]f

    def Undo(self):
        if(len(self.History) == 0):
            return
        move = self.History.pop()
        movedP = self.Board[move.toX][move.toY]
        movedP.posX = move.fromX
        movedP.posY = move.fromY
        self.Board[move.toX][move.toY] = None
        self.Board[move.fromX][move.fromY] = movedP
        for p in move.piecesKilled:
            p.Alive = True
            self.Board[p.PosX][p.PosY] = p
        if (self.CurrentTurn == WHITE):
            self.CurrentTurn = BLACK
        elif (self.CurrentTurn == BLACK):
            self.CurrentTurn = WHITE
        

    def __str__(self):
        s = "/ 0 1 2 3 4 5 6\n"
        for y in range(7):
            s += str(y) + " "
            for x in range(7):
                p = self.Board[x][y]
                if (p == None):
                    if ((x == 0 and y == 0) or
                            (x == 6 and y == 0) or
                            (x == 0 and y == 6) or
                            (x == 6 and y == 6) or
                            (x == 3 and y == 3)):
                        s += "X "
                    else:
                        s += "O "
                elif (p.Team == BLACK):
                    s += "B "
                elif (p.Team == WHITE):
                    if (p.IsKing):
                        s += "K "
                    else:
                        s += "W "
            s += "\n"
        return s

    def IsValidMove(self, fromX, fromY, toX, toY, getReason = False):
        if(getReason == False):
            return IsValidMove(fromX, fromY, toX, toY, True)[0]

        # Positions out of Bounds
        if (fromX < 0 or fromX > 6 or fromY < 0 or fromY > 6 or
                toX < 0 or toX > 6 or toY < 0 or toY > 6):
            return (False,"Positions out of Bounds")

        fromP = self.Board[fromX][fromY]
        toP = self.Board[toX][toY]

        # Either from is empty or to is not
        if fromP is None or toP is not None:
            return (False,"Either from is empty or to is not")

        # Cannot move to the center
        if toX == 3 and toY == 3:
            return (False,"Cannot move to the center")

        # Wrong Piece Moving
        if fromP.Team != self.CurrentTurn:
            return (False,"Wrong Piece Moving")

        # Unless from is the king, cannot move to corners
        if (not fromP.IsKing):
            if ((toX == 0 and toY == 0) or
                    (toX == 0 and toY == 6) or
                    (toX == 6 and toY == 0) or
                    (toX == 6 and toY == 6)):
                return (False,"Unless from is the king, cannot move to corners")

        if (fromX == toX):
            # Both Equal
            if (fromY == toY):
                return (False,"Both Equal")

            for y in range(min(fromY, toY), max(fromY, toY)):
                if (y == fromY):
                    continue
                # There is a piece between from and to
                if (self.Board[fromX][y] != None):
                    return (False,"There is a piece between from and to")
        else:
            # Both Unequal
            if (fromY != toY):
                return (False,"Both Unequal")

            for x in range(min(fromX, toX), max(fromX, toX)):
                if (x == fromX):
                    continue
                # There is a piece between from and to
                if (self.Board[x][fromY] != None):
                    return (False,"There is a piece between from and to")

        return (True,"Move is Valid")

    def MakeMove(self, fromX, fromY, toX, toY, check=True):
        if (check):
            if (not self.IsValidMove(fromX, fromY, toX, toY)):
                return False

        move = Move(fromX, fromY, toX, toY)
        fromP = self.Board[fromX][fromY]
        self.Board[fromX][fromY] = None
        self.Board[toX][toY] = fromP

        fromP.X = toX
        fromP.Y = toY

        for pos in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            toCap = (toX + pos[0], toY + pos[1])  # what is to be captured
            checkCap = (toX + pos[0] * 2, toY + pos[1] * 2)  # the piece on the other side of being capped

            # No capturing against the center (The center itself can be captured though)
            if (checkCap[0] == 3 and checkCap[1] == 3):
                continue

            # if the cap or the check cap out of bounds
            if (toCap[0] < 0 or toCap[0] > 6 or toCap[1] < 0 or toCap[1] > 6 or
                    checkCap[0] < 0 or checkCap[0] > 6 or checkCap[1] < 0 or checkCap[1] > 6):
                continue

            capP = self.Board[toCap[0]][toCap[1]]

            # Corners count as valid check Pieces
            if ((checkCap[0] == 0 and checkCap[1] == 0) or
                    (checkCap[0] == 0 and checkCap[1] == 6) or
                    (checkCap[0] == 6 and checkCap[1] == 0) or
                    (checkCap[0] == 6 and checkCap[1] == 6)):
                checkP = Piece(self, fromP.Team, checkCap[0], checkCap[1])
            else:
                checkP = self.Board[checkCap[0]][checkCap[1]]

            # if there are no pieces either to be capped or to cap with
            if (capP == None or checkP == None):
                continue

            if ((not capP.Team == fromP.Team) and checkP.Team == fromP.Team):
                capP.Alive = False
                move.piecesKilled.append(self.Board[toCap[0]][toCap[1]])
                if (capP.IsKing == False):
                    self.Board[toCap[0]][toCap[1]] = None

        if (self.CurrentTurn == WHITE):
            self.CurrentTurn = BLACK
        elif (self.CurrentTurn == BLACK):
            self.CurrentTurn = WHITE

        self.History.append(move)

        return True

    def GetWinner(self):
        kingX = self.WhiteKing.X
        kingY = self.WhiteKing.Y

        if ((kingX == 0 and kingY == 0) or
                (kingX == 0 and kingY == 6) or
                (kingX == 0 and kingY == 0) or
                (kingX == 6 and kingY == 6)):
            return WHITE

        if (not self.WhiteKing.Alive):
            return BLACK

        return None


if __name__ == "__main__":
    g = GameBoard()
    i = ""
    while True:
        print(str(g)[:-1])

        while True:
            if g.CurrentTurn == BLACK:
                print("Black's Turn")
            elif (g.CurrentTurn == WHITE):
                print("White's Turn")
            else:
                print("No One's Turn?")

            try:
                i = input()
                if (i == "QUIT"):
                    break
                if (i == "UNDO"):
                    break
                
                s = i.split(" ")

                fromX = int(s[0])
                fromY = int(s[1])
                toX = int(s[2])
                toY = int(s[3])
            except:
                print("Error")
                continue

            if (g.IsValidMove(fromX, fromY, toX, toY)):
                break

            print("Invalid Move!")
            print(g.GetReasonInvalid(fromX, fromY, toX, toY))

        if (i == "QUIT"):
            break
        
        if (i == "UNDO"):
            g.Undo()
        else:
            g.MakeMove(fromX, fromY, toX, toY, False)

        winner = g.GetWinner()
        if (winner != None):
            break

    if (winner == WHITE):
        print("White Wins")
    elif (winner == BLACK):
        print("Black Wins")
    else:
        print("Draw")
