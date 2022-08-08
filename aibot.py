import random
import copy

from human_player import player
from boardMethods import boardMethods

class ai(player):

    def __init__(self, board, length, margin, topMargin, cells, isBlack, winRows):
        super().__init__(board, length, margin, topMargin, cells, isBlack)
        if self.isBlack:
            self.color = "b"
            self.oppColor = 'w'
        else:
            self.color = "w"
            self.oppColor = 'b'
        self.winRows = winRows
        self.abDepth = 4
        self.boardMethods = boardMethods(self.cells, self.winRows)

    def updateBoard(self, board):
        self.board = board
        
    #https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/ 
    #https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague
    def miniMax(self, row, col, board, isMaxPlayer, depth, alpha, beta):
        if self.boardMethods.checkWin(row, col, self.color, board) or depth == 0:
            value = self.boardMethods.scoreBoard(row, col, self.color, board) - (self.abDepth-depth)
            return value
        elif isMaxPlayer:
            maxUtil = float("-inf")
            for move in self.boardMethods.getMoves(self.color, board):
                row = move[0]
                col = move[1]
                tempBoard = copy.deepcopy(board)
                tempBoard[row][col] = self.color
                value = self.miniMax(row, col, tempBoard, False, depth - 1, alpha, beta) # evaluate this node
                maxUtil = max(maxUtil, value) # return the max value
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return maxUtil
        elif not isMaxPlayer:
            minUtil = float("inf")
            for move in self.boardMethods.getMoves(self.oppColor, board):
                row = move[0]
                col = move[1]
                tempBoard = copy.deepcopy(board)
                tempBoard[row][col] = self.oppColor
                value = self.miniMax(row, col, tempBoard, True, depth - 1, alpha, beta) # evaluate this node
                # print(f"min{depth, minUtil, value}")
                minUtil = min(minUtil, value) # return the min value
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return minUtil

    def randomChoose(self):
        moves = self.boardMethods.getMoves(self.color, self.board)
        move = random.choice(moves)
        row, col = move[0], move[1]
        return row, col

    def chooseRowCol(self):
        print("hi")
        currentBest = float("-inf")
        row = None
        col = None
        for move in self.boardMethods.getMoves(self.color, self.board):
            r = move[0]
            c = move[1]
            tempBoard = copy.deepcopy(self.board)
            tempBoard[r][c] = self.color
            value = self.miniMax(r, c, tempBoard, False, self.abDepth, float("-inf"), float("inf"))
            print(move, value)
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