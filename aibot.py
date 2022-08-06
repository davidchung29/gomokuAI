import random
from human_player import player

class ai(player):

    def __init__(self, board, length, margin, topMargin, cells, isBlack):
        super().__init__(board, length, margin, topMargin, cells, isBlack)
        if self.isBlack:
            self.color = "b"
        else:
            self.color = "w"

    def updateBoard(self, board):
        self.board = board

    def chooseRowCol(self):
        row = random.randrange(self.cells)
        col = random.randrange(self.cells)
        return row, col

    def placePiece(self):
        row, col = self.chooseRowCol()
        while not self.isValidPiece(row, col):
            row, col = self.chooseRowCol()
        self.changeBoard(row, col)
        return row, col
    
    def changeBoard(self, row, col):
        self.board[row][col] = self.color