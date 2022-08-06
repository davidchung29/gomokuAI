class gridBoard():
    def __init__(self, board, length, margin, topMargin, cells):
        self.board = board
        self.length = length
        self.margin = margin
        self.topMargin = topMargin
        self.cells = cells
        self.cellLength = (self.length - (2 * self.margin))/(self.cells - 1)

        self.pieceR = self.cellLength/2 - 3
        self.isGameOver = False 
        self.winRow = 5 # 5 in a row

    def updateBoard(self, board):
        self.board = board

    # get point where lines intersect (where you place pieces)
    def getCellPoint(self, row, col):
        x = self.margin + (self.cellLength * row)
        y = self.topMargin + self.margin + (self.cellLength * col)
        return x, y

    # get coords for cell
    def getCell(self, row, col):
        x0, y0 = self.getCellPoint(row, col)
        x1, y1 = self.getCellPoint(row+1, col+1)
        return x0, y0, x1, y1

    def checkConsecutive(self, L, color): 
                                   # crow,ccol are center values
        count = 0
        for i in range(len(L)):
            if L[i] == color:
                count += 1
            else:
                count = 0
            if count == self.winRow:
                return True

    def checkWin(self, row, col, color): #row and col are for last placed piece
        winRow = 5
        surrRange = winRow - 1
        minRow = max((row - surrRange), 0)
        maxRow = min((row + surrRange), self.cells - 1)
        minCol = max((col - surrRange), 0)
        maxCol = min((col + surrRange), self.cells - 1)

        hList = self.board[row][minCol:maxCol+1]
        vList = []
        for i in range(minRow,maxRow+1):
            vList.append(self.board[i][col])
        d1List = []
        d2List = []
        #use largest min and smallest max so that u search inside the board

        corner1 = min(row - minRow, col - minCol) #top left 
        corner2 = min(col - minCol, maxRow - row) #top right
        corner3 = min(maxRow - row, maxCol - col) #bottom right
        corner4 = min(maxCol - col, row - minRow) #bottom left
        for i in range(corner3 + corner1 + 1):
            startRow = row - corner1
            startCol = col - corner1
            d1List.append(self.board[startRow + i][startCol + i])
        for i2 in range(corner2 + corner4 + 1):
            startRow = row - corner4
            startCol = col + corner4
            print(row, col, corner2, corner4, i2)
            d2List.append(self.board[startRow + i2][startCol - i2])
        for L in [hList, vList, d1List, d2List]:
            if self.checkConsecutive(L, color):
                return True


    # DRAW FUNCTIONS

    def drawScreen(self, canvas):
        canvas.create_rectangle(0, self.topMargin, self.length, self.length + self.topMargin, fill = "#F5F5DC")
        self.drawBoard(canvas)
        self.drawPieces(canvas)

    def drawBoard(self, canvas):
        for row in range(self.cells - 1):
            for col in range(self.cells - 1):
                x0, y0, x1, y1 = self.getCell(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, outline = "black")

    def drawPieces(self, canvas):
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