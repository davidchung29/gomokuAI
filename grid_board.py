import copy

class gridBoard():
    def __init__(self, board, length, margin, topMargin, cells):
        self.board = board
        self.boardScore = 0
        self.length = length
        self.margin = margin
        self.topMargin = topMargin
        self.cells = cells
        self.cellLength = (self.length - (2 * self.margin))/(self.cells - 1)

        self.pieceR = self.cellLength/3
        self.isGameOver = False 

    def updateBoard(self, board):
        self.board = board

    ## Functions to get coordinates on Board
    
    def getCellPoint(self, row, col): # get point where lines intersect (where you place pieces)
        x = self.margin + (self.cellLength * row)
        y = self.topMargin + self.margin + (self.cellLength * col)
        return x, y

    def getCell(self, row, col): # get coords for cell
        x0, y0 = self.getCellPoint(row, col)
        x1, y1 = self.getCellPoint(row+1, col+1)
        return x0, y0, x1, y1

    # DRAW FUNCTIONS

    def drawScreen(self, canvas):
        canvas.create_rectangle(0, self.topMargin, self.length, self.length + self.topMargin, fill = "#F5F5DC")
        self.drawBoard(canvas)
        self.drawPieces(canvas)

    def drawBoard(self, canvas): #https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
        for row in range(self.cells - 1):
            for col in range(self.cells - 1):
                x0, y0, x1, y1 = self.getCell(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, outline = "black")

    def drawPieces(self, canvas): #https://www.cs.cmu.edu/~112/notes/notes-graphics.html
        for row in range(self.cells):
            for col in range(self.cells):
                piece = self.board[row][col]
                cx, cy = self.getCellPoint(row, col)
                if piece == "w":
                    canvas.create_oval(cx - self.pieceR, cy - self.pieceR,
                                       cx + self.pieceR, cy + self.pieceR,
                                       fill = "white")
                elif piece == "b":
                    canvas.create_oval(cx - self.pieceR, cy - self.pieceR,
                                       cx + self.pieceR, cy + self.pieceR,
                                       fill = "black")