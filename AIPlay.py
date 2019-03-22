import MinimaxTreeM as MinimaxTree
import BoardGame

wins = {'Black':{'random':0, 'nn':0}, 'White':{'random':0, 'nn':0}}

BLACK = 0
WHITE = 1

for i in range(6):
    randomBlack = i % 2
    print('Black' if randomBlack else 'White', 'playing random')
    b = BoardGame.GameBoard()
    while b.GetWinner() == None:
        print(str(b)[:-2])
        print(("Black" if b.CurrentTurn == BLACK else "White") + "'s turn")
        random = (b.CurrentTurn == BLACK and randomBlack) or (b.CurrentTurn == WHITE and not randomBlack)
        _, move, _ = MinimaxTree.alphabeta(b, rand = random)
        b.MakeMove(move.fromX, move.fromY, move.toX, move.toY)
        print(move)
    winner = b.GetWinner()
    print('Black' if winner == BLACK else 'White', 'wins')
    wins['Black' if winner == BLACK else 'White']['random' if winner != randomBlack else 'nn'] += 1

print("Neural network wins as")
print("Black:", wins['Black']['nn'])
print("White:", wins['White']['nn'])
print("Random wins as")
print("Black:", wins['Black']['random'])
print("White:", wins['White']['random'])
