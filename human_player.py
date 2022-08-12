import decimal

def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

class player():
    def __init__(self, board, length, margin, topMargin, cells, isBlack):
        self.board = board
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

    def updateBoard(self, board):
        self.board = board

    def getCoords(self, x, y):
        row = roundHalfUp((x - self.margin)/self.cellLength)
        col = roundHalfUp((y - self.margin - self.topMargin)/self.cellLength)
        return row, col

    def hoveringPiece(self, x, y):
        row, col = self.getCoords(x, y)
        if self.prevVisited:
                prevRow = self.prevVisited[0]
                prevCol = self.prevVisited[1]
                self.board[prevRow][prevCol] = ""
        if self.isValidPiece(row, col):
            self.prevVisited = [row, col]
            self.changeBoard(row, col)
        print(self.prevVisited, row, col)

    def placePiece(self, x, y):
        row, col = self.getCoords(x, y)
        print(self.prevVisited)
        if [row, col] == self.prevVisited:
            self.prevVisited = []
            self.changeBoard(row, col)
            return [row, col]
        return None

    def isValidPiece(self, row, col):
        if row < self.cells and col < self.cells:
            if self.board[row][col] == "":
                return True
        return False

    def changeBoard(self, row, col):
        if self.isBlack:
            self.board[row][col] = "b"
        else:
            self.board[row][col] = "w"