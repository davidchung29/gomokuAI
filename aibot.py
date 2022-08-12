import random
import copy

from human_player import player
from boardMethods import boardMethods


class ai(player):

    def __init__(self, board, length, margin, topMargin, cells, isBlack, playerTurn, winRows, flipMode):
        super().__init__(board, length, margin, topMargin, cells, isBlack)
        if self.isBlack:
            self.color = "b"
            self.oppColor = 'w'
        else:
            self.color = "w"
            self.oppColor = 'b'
        self.winRows = winRows
        self.abDepth = 3
        self.madeFirstMove = playerTurn
        self.board = board
        self.boardMethods = boardMethods(self.cells, self.winRows)
        self.flipMode = flipMode

        self.data = dict()
        f = open(f"aiData5.csv")

    def updateData(self): #update the data file - write what is in current file onto variable, which is returned, and onto the file, write everthing in self.data
        fAdd = open(f"aiData5.csv", "w")
        if self.data:
            for element in self.data:
                fAdd.write(f'{element}, {self.data[element]}\n')
        fAdd.close()
        
    #https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/ - used to read about an example of how alphabeta could be implemented in tictactoe
    #https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague - used to learn alphabeta and minimax visually
    #https://www.javatpoint.com/ai-alpha-beta-pruning#:~:text=The%20two%2Dparameter%20can%20be,along%20the%20path%20of%20Minimizer. - used for finding role of alpha and beta in pruning branches in minimax
    def miniMax(self, row, col, board, isMaxPlayer, depth, alpha, beta):
        if self.boardMethods.checkWin(row, col, self.color, board) or self.boardMethods.checkWin(row, col, self.oppColor, board) or depth == 0:
            convertedBoard = self.boardMethods.convertBoard(board)
            if self.data and (convertedBoard in self.data):
                value = self.data[convertedBoard]
            else:
                value = self.boardMethods.scoreBoard(row, col, self.color, self.oppColor, board)
                self.data[convertedBoard] = value
            return int(value) - (self.abDepth-depth)
        elif isMaxPlayer:
            maxUtil = float("-inf")
            for move in self.boardMethods.getNearbyMoves(2, board):
                row = move[0]
                col = move[1]
                tempBoard = copy.deepcopy(board)
                tempBoard[row][col] = self.color
                if self.flipMode: # flip the board if the user chose flip board
                    resBoard = self.boardMethods.flipCoords(col, tempBoard)
                    for r in range(len(tempBoard)):
                        for c in range(len(tempBoard[r])):
                            tempBoard[r][c] = resBoard[r][c]
                value = self.miniMax(row, col, tempBoard, False, depth - 1, alpha, beta) # evaluate this node
                maxUtil = max(maxUtil, value) # return the max value
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return maxUtil
        elif not isMaxPlayer:
            minUtil = float("inf")
            for move in self.boardMethods.getNearbyMoves(2, board):
                row = move[0]
                col = move[1]
                tempBoard = copy.deepcopy(board)
                tempBoard[row][col] = self.oppColor
                if self.flipMode: # flip the board if the user chose flip board
                    resBoard = self.boardMethods.flipCoords(col, tempBoard)
                    for r in range(len(tempBoard)):
                        for c in range(len(tempBoard[r])):
                            tempBoard[r][c] = resBoard[r][c]
                value = self.miniMax(row, col, tempBoard, True, depth - 1, alpha, beta) # evaluate this node
                # print(f"min{depth, minUtil, value}")
                minUtil = min(minUtil, value) # return the min value
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return minUtil

    def randomChoose(self):
        moves = self.boardMethods.getMoves(self.board)
        move = random.choice(moves)
        row, col = move[0], move[1]
        return row, col

    def chooseRowCol(self):
        row = None
        col = None
        if self.madeFirstMove:
            moves = self.boardMethods.getNearbyMoves(2, self.board)
            currentBest = float("-inf")
            for move in moves:
                r = move[0]
                c = move[1]
                tempBoard = copy.deepcopy(self.board)
                tempBoard[r][c] = self.color
                value = self.miniMax(r, c, tempBoard, False, self.abDepth, float("-inf"), float("inf"))
                #print(move, value)
                if value > currentBest:
                    currentBest = value
                    row = r 
                    col = c
        else:
            row, col = self.randomChoose()
            self.madeFirstMove = True
        return row, col

    def placePiece(self, miniMax):
        if miniMax:
            row, col = self.chooseRowCol()
        else:
            row, col = self.randomChoose()
        print(row, col)
        self.board[row][col] = self.color
        return row, col
    