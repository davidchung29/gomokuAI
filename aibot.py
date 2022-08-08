import random
import copy

from numpy import Infinity
from human_player import player
from boardMethods import boardMethods

class ai(player):

    def __init__(self, board, length, margin, topMargin, cells, isBlack):
        super().__init__(board, length, margin, topMargin, cells, isBlack)
        if self.isBlack:
            self.color = "b"
        else:
            self.color = "w"
        self.boardMethods = boardMethods()

    def updateBoard(self, board):
        self.board = board
    
    def miniMax(self, row, col, board, isMaxPlayer, depth):
        if self.boardMethods.checkWin(row, col, self.color, board) or depth == 0:
            return self.boardMethods.scoreBoard(row, col, self.color, board) - depth, [row, col]
        elif isMaxPlayer:
            maxUtil = -Infinity
            for move in self.boardMethods.getMoves(self.color, board):
                row = move[0]
                col = move[1]
                tempBoard = copy.deepcopy(board)
                tempBoard[row][col] = self.color
                value = self.miniMax(row, col, tempBoard, False, depth - 1) # evaluate this node
                maxUtil = max(maxUtil, value[0]) # return the max value
            return maxUtil, move
        elif not isMaxPlayer:
            minUtil = +Infinity
            for move in self.boardMethods.getMoves(self.color, board):
                row = move[0]
                col = move[1]
                tempBoard = copy.deepcopy(board)
                tempBoard[row][col] = self.color
                value = self.miniMax(row, col, tempBoard, True, depth - 1) # evaluate this node
                minUtil = min(minUtil, value[0]) # return the max value
            return minUtil, move

    def chooseRowCol(self):
        print("hi")
        currentBest = -Infinity
        print(f"current{currentBest}")
        row = None
        col = None
        for move in self.boardMethods.getMoves(self.color, self.board):
            print(move)
            r = move[0]
            c = move[1]
            value = self.miniMax(r, c, self.board, False, 1)
            if value[0] > currentBest:
                currentBest = value
                row = r 
                col = c
        return row, col

    def placePiece(self):
        row, col = self.chooseRowCol()
        self.changeBoard(row, col)
        return row, col
    
    def changeBoard(self, row, col):
        self.board[row][col] = self.color