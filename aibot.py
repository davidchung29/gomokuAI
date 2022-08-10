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
        self.abDepth = 3
        self.madeFirstMove = True
        if self.isBlack:
            self.madeFirstMove = False
        self.boardMethods = boardMethods(self.cells, self.winRows)

        self.data = dict()
        self.updateData()

    def updateBoard(self, board):
        self.board = board

    def updateData(self, entry=None): #update the data file - entry is if new board,score is added
        pass
        # f = open(f"aiData{self.cells}.csv")
        # fAdd = open(f"aiData{self.cells}.csv", "a")
        # if entry:
        #     strEntry = f"{entry[0]},{entry[1]}"
        #     fAdd.write(f"\n{strEntry}")
        # for line in f:
        #     lineData = line.strip().split(",")
        #     self.data[lineData[0]] = lineData[1]
        # f.close()
        
    #https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/ - used to read about an example of how alphabeta could be implemented in tictactoe
    #https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague - used to learn alphabeta and minimax visually
    #https://www.javatpoint.com/ai-alpha-beta-pruning#:~:text=The%20two%2Dparameter%20can%20be,along%20the%20path%20of%20Minimizer. - used for finding role of alpha and beta in pruning branches in minimax
    def miniMax(self, row, col, board, isMaxPlayer, depth, alpha, beta):
        if self.boardMethods.checkWin(row, col, self.color, board) or depth == 0:
            convertedBoard = self.boardMethods.convertBoard(board)
            if convertedBoard in self.data:
                value = self.data[convertedBoard]
            else:
                value = self.boardMethods.scoreBoard(row, col, self.color, self.oppColor, board)
                #self.updateData([convertedBoard, value])
            print(value, depth, value - (self.abDepth-depth)**2)
            return value - (self.abDepth-depth)**2
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
        row = None
        col = None
        if self.madeFirstMove:
            moves = self.boardMethods.getNearbyMoves(self.color, 1, self.board)
            currentBest = float("-inf")
            for move in moves:
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
        else:
            row, col = self.randomChoose()
            self.madeFirstMove = True
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