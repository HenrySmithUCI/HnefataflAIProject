import MinimaxTree
import BoardGame

b = BoardGame.GameBoard()

while True:
    print(str(b)[:-2])
    print("thinking...")
    move = MinimaxTree.pickmove(b)
    b.MakeMove(move.fromX, move.fromY, move.toX, move.toY)
    print(move)
