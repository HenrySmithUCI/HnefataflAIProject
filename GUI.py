import tkinter as tk
import BoardGame
import MinimaxTree

BLACK = 0
WHITE = 1
WIDTH = 700
HEIGHT = 700

class GUI:
    def run(self):
        self.root = tk.Tk()
        self.setup()
        tk.mainloop()

    def setup(self):
        self.frame = tk.Frame(self.root)
        self.frame.grid(padx = 10, pady = 10)
        self.root.resizable(False, False)
        self.player = tk.IntVar()
        tk.Label(self.frame, text = "Play as: ").grid(column = 0, row = 0, columnspan = 2)
        tk.Radiobutton(self.frame, text = "Black", variable = self.player, value = BLACK).grid(column = 0, row = 1)
        tk.Radiobutton(self.frame, text = "White", variable = self.player, value = WHITE).grid(column = 1, row = 1)
        tk.Button(self.frame, text = "Start", command = self.startGame).grid(column = 0, row = 2, columnspan = 2)

    def startGame(self):
        self.frame.destroy()
        self.canvas = tk.Canvas(self.root, height = HEIGHT, width = WIDTH, bg = 'antique white')
        self.canvas.grid(column = 0, row = 0)
        self.bottomText = tk.StringVar()
        tk.Label(self.root, textvariable = self.bottomText, font = (None, 16, 'bold')).grid(column = 0, row = 1)
        self.colWidth = WIDTH / 7
        self.board = BoardGame.GameBoard()
        self.pieceSelected = None
        self.gameOver = False
        self.drawBoard()
        if self.player.get() != self.board.CurrentTurn:
            self.bottomText.set("Thinking...")
            self.aiMove()
        self.drawBoard()
        self.bottomText.set("Select piece to move")
        self.root.bind("<ButtonRelease-1>", self.onClick)

    def aiMove(self):
        move = MinimaxTree.pickmove(self.board)
        self.board.MakeMove(move.fromX, move.fromY, move.toX, move.toY)
    
    def drawBoard(self):
        self.canvas.delete("all")
        for i in range(7):
            self.canvas.create_line(0, self.colWidth * (i + 1), WIDTH, self.colWidth * (i + 1))
            self.canvas.create_line(self.colWidth * (i + 1), 0, self.colWidth * (i + 1), HEIGHT)
        for piece in self.board.Pieces:
            if piece.Alive:
                x = self.colWidth * piece.X
                y = self.colWidth * piece.Y
                self.canvas.create_oval(x, y, x + self.colWidth, y + self.colWidth, \
                                        fill = 'black' if piece.Team == BLACK else 'white')
                if piece.IsKing:
                    self.canvas.create_line(x, y + self.colWidth / 2, x + self.colWidth, y + self.colWidth / 2, width = 2)
                    self.canvas.create_line(x + self.colWidth / 2, y, x + self.colWidth / 2, y + self.colWidth, width = 2)
        if self.pieceSelected:
            x = self.colWidth * self.pieceSelected[0]
            y = self.colWidth * self.pieceSelected[1]
            self.canvas.create_rectangle(x, y, x + self.colWidth, y + self.colWidth, outline = 'red', width = 2)

    def onClick(self, event):
        if event.widget == self.canvas and self.board.CurrentTurn == self.player.get():
            self.handleClick(int(event.x // self.colWidth), int(event.y // self.colWidth))

    def handleClick(self, x, y):
        if not self.gameOver:
            if self.pieceSelected == None:
                for piece in self.board.Pieces:
                    if piece.Team == self.player.get() and piece.X == x and piece.Y == y:
                        self.pieceSelected = [x, y]
                        self.bottomText.set("Select destination")
                        self.drawBoard()
            elif self.pieceSelected[0] == x and self.pieceSelected[1] == y:
                self.pieceSelected = None
                self.bottomText.set("Select piece to move")
                self.drawBoard()
            else:
                if self.board.MakeMove(self.pieceSelected[0], self.pieceSelected[1], x, y):
                    winner = self.board.GetWinner()
                    self.pieceSelected = None
                    self.drawBoard()
                    if winner != None:
                        self.bottomText.set(("Black" if winner == BLACK else "White") + " wins.")
                        self.gameOver = True
                    else:
                        self.bottomText.set("Thinking...")
                        self.aiMove()
                        self.drawBoard()
                        winner = self.board.GetWinner()
                        if winner != None:
                            self.bottomText.set(("Black" if winner == BLACK else "White") + " wins.")
                            self.gameOver = True
                        else:
                            self.bottomText.set("Select piece to move")

app = GUI()
app.run()
