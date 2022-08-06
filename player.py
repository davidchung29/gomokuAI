class player():
    def __init__(self, length, margin, topMargin, cells, isBlack):
        self.length = length
        self.margin = margin
        self.topMargin = topMargin
        self.cells = cells
        self.cellLength = (self.length - (2 * self.margin))/(self.cells - 1)
        self.isBlack = isBlack
        self.prevVisited = []
        if self.isBlack:
            self.color = "b"
        else:
            self.color = "w"

    def getCoords(self, x, y):
        row = roundHalfUp((x - self.margin)/self.cellLength)
        col = roundHalfUp((y - self.margin - self.topMargin)/self.cellLength)
        return row, col

    def hoveringPiece(self, x, y):
        row, col = self.getCoords(x, y)
        if self.prevVisited:
                prevRow = self.prevVisited[0]
                prevCol = self.prevVisited[1]
                board[prevRow][prevCol] = ""
        if self.isValidPiece(row, col):
            self.prevVisited = [row, col]
            self.changeBoard(row, col)

    def placePiece(self, x, y):
        row, col = self.getCoords(x, y)
        if [row, col] == self.prevVisited:
            self.prevVisited = []
            self.changeBoard(row, col)
            print(f'plauer{row, col}')
            return [row, col]
        return None

    def isValidPiece(self, row, col):
        if row < self.cells and col < self.cells:
            if board[row][col] == "":
                return True
        return False

    def changeBoard(self, row, col):
        if self.isBlack:
            board[row][col] = "b"
        else:
            board[row][col] = "w"