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
            self.oppColor = 'w'
        else:
            self.color = "w"
            self.oppColor = 'b'
        self.boardMethods = boardMethods(self.cells)

    def updateBoard(self, board):
        self.board = board
    
    def miniMax(self, row, col, board, isMaxPlayer, depth):
        if self.boardMethods.checkWin(row, col, self.color, board) or depth == 0:
            return self.boardMethods.scoreBoard(row, col, self.color, board)
        elif isMaxPlayer:
            maxUtil = -Infinity
            for move in self.boardMethods.getMoves(self.color, board):
                row = move[0]
                col = move[1]
                tempBoard = copy.deepcopy(board)
                tempBoard[row][col] = self.color
                value = self.miniMax(row, col, tempBoard, False, depth - 1) # evaluate this node
                # print(f"max{depth, maxUtil, value, row, col}")
                maxUtil = max(maxUtil, value) # return the max value
            return maxUtil
        elif not isMaxPlayer:
            minUtil = +Infinity
            for move in self.boardMethods.getMoves(self.oppColor, board):
                row = move[0]
                col = move[1]
                tempBoard = copy.deepcopy(board)
                tempBoard[row][col] = self.color
                value = self.miniMax(row, col, tempBoard, True, depth - 1) # evaluate this node
                # print(f"min{depth, minUtil, value}")
                minUtil = min(minUtil, value) # return the min value
            return minUtil

    def randomChoose(self):
        moves = self.boardMethods.getMoves(self.color, self.board)
        move = random.choice(moves)
        row, col = move[0], move[1]
        return row, col

    def chooseRowCol(self):
        print("hi")
        currentBest = -Infinity
        row = None
        col = None
        for move in self.boardMethods.getMoves(self.color, self.board):
            print(move)
            r = move[0]
            c = move[1]
            value = self.miniMax(r, c, self.board, True, 3)
            if value > currentBest:
                currentBest = value
                row = r 
                col = c
        print(row, col)
        return row, col

    def placePiece(self, miniMax = False):
        if miniMax:
            row, col = self.chooseRowCol()
        else:
            row, col = self.randomChoose()
        self.changeBoard(row, col)
        return row, col
    
    def changeBoard(self, row, col):
        self.board[row][col] = self.color