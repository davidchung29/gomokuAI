import copy

class boardMethods():
    ## Functions for AI to use with board
    def __init__(self, cells):
        self.cells = cells

    def convertBoard(self, board):
        result = ''
        for row in range(self.cells):
            for col in range(self.cells):
                if board[row][col] == "":
                    result += '.'
                else:
                    result += board[row][col]
        return result
    
    def getMoves(self, color, board):
        moves = [] #moves with which row, col, piece was added
        for row in range(self.cells):
            for col in range(self.cells):
                tempBoard = copy.deepcopy(board)
                if tempBoard[row][col] == "":
                    tempBoard[row][col] = color
                    moves.append([row, col])
        return moves

    ## Functions for scoring a board including if a player won  

    def scoreBoard(self, row, col, color, board):
        # iterate through consecutives and add to score
        # return score
        # dont have to call for every move
        score = 0
        for cons in range(4,0,-1):
            if self.getSurr(row, col, color, board, cons):
                score += cons ** 2
                break
        if self.getSurr(row, col, color, board, 5):
            score += 1000
        return score

    def checkWin(self, row, col, color, board): #row and col are for last placed piece
        return self.getSurr(row, col, color, board, self.cells)
    
    def getSurr(self, row, col, color, board, rowCount):
        winRow = 5
        surrRange = winRow - 1
        minRow = max((row - surrRange), 0)
        maxRow = min((row + surrRange), self.cells - 1)
        minCol = max((col - surrRange), 0)
        maxCol = min((col + surrRange), self.cells - 1)

        hList = board[row][minCol:maxCol+1]
        vList = []
        for i in range(minRow,maxRow+1):
            vList.append(board[i][col])
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
            d1List.append(board[startRow + i][startCol + i])
        for i2 in range(corner2 + corner4 + 1):
            startRow = row - corner4
            startCol = col + corner4
            d2List.append(board[startRow + i2][startCol - i2])
        for L in [hList, vList, d1List, d2List]:
            if self.checkConsecutive(L, color, rowCount):
                return True

    def checkConsecutive(self, L, color, rowCount): 
                                   # crow,ccol are center values
        count = 0
        for i in range(len(L)):
            if L[i] == color:
                count += 1
            else:
                count = 0
            if count == rowCount:
                return True 