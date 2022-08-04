from sys import builtin_module_names
from cmu_112_graphics import *
import random, string, math, time


#################################################
# Helper Functions
#################################################

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Gomoku Game
#################################################


class gridBoard():
    def __init__(self, length, margin, topMargin, cells):
        self.length = length
        self.margin = margin
        self.topMargin = topMargin
        self.cells = cells
        self.cellLength = (self.length - (2 * self.margin))/(self.cells - 1)

        self.pieceR = self.cellLength/2 - 3
        self.isGameOver = False 
        self.winRow = 5 # 5 in a row

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
            print(row, col, corner2, corner4, i2)
            d2List.append(board[startRow + i2][startCol - i2])
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
                piece = board[row][col]
                cx, cy = self.getCellPoint(row, col)
                if piece == "w":
                    canvas.create_oval(cx - self.pieceR, cy - self.pieceR,
                                       cx + self.pieceR, cy + self.pieceR,
                                       fill = "white")
                elif piece == "b":
                    canvas.create_oval(cx - self.pieceR, cy - self.pieceR,
                                       cx + self.pieceR, cy + self.pieceR,
                                       fill = "black")

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

class ai(player):

    def __init__(self, length, margin, topMargin, cells, isBlack):
        super().__init__(length, margin, topMargin, cells, isBlack)
        if self.isBlack:
            self.color = "w"
        else:
            self.color = "b"


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
        board[row][col] = self.color


class message():

    def __init__(self, length, topMargin, isPlayerTurn, isPlayerBlack):
        self.length = length
        self.topMargin = topMargin
        self.isPlayerTurn = isPlayerTurn
        self.isPlayerBlack = isPlayerBlack
        self.textMessage = ""
        self.updateMessageTurn(self.isPlayerTurn)


    def updateMessageTurn(self, isPlayerTurn):
        self.isPlayerTurn = isPlayerTurn
        if self.isPlayerTurn:
            self.textMessage = "Player:"
            if self.isPlayerBlack:
                self.textMessage += " Black"
            else:
                self.textMessage += " White"
        else:
            self.textMessage = "AI:"
            if self.isPlayerBlack:
                self.textMessage += " White"
            else:
                self.textMessage += " Black"

    def drawMessage(self, canvas):
        canvas.create_text(self.length/2, self.topMargin/2, text = self.textMessage, fill = "#954535", font = "Helvetica 30 bold")

class gomokuGame():

    def __init__(self, length):
        self.cells = 15
        self.length = length
        self.margin = 20
        self.topMargin = 50
        self.gameOver = False
        self.isPlayerBlack = bool(random.randrange(0,2))
        if self.isPlayerBlack:
            self.isPlayerTurn = True
        else:
            self.isPlayerTurn = False
        global board
        board = [[""] * self.cells for _ in range(self.cells)]

        self.grid = gridBoard(self.length, self.margin, self.topMargin, self.cells)

        self.player = player(self.length, self.margin, self.topMargin, self.cells, self.isPlayerBlack)
        self.message = message(self.length, self.topMargin, self.isPlayerTurn, self.isPlayerBlack)
        self.aibot = ai(self.length, self.margin, self.topMargin, self.cells, self.isPlayerBlack)


    def nextPlayer(self):
        self.isPlayerTurn = not self.isPlayerTurn
        self.message.updateMessageTurn(self.isPlayerTurn)

    def moving(self, x, y):
        if not self.gameOver:
            if self.isPlayerTurn:
                self.player.hoveringPiece(x, y)

    def placePlayer(self, x, y):
        if not self.gameOver:
            if self.isPlayerTurn:
                move = self.player.placePiece(x, y) #row, col
                if move == None:
                    self.message.textMessage = "Invalid Placement"
                else:
                    row, col = move[0], move[1]
                    if self.grid.checkWin(row, col, self.player.color):
                        self.win(self.player)
                        print('WINNN')
                    else:
                        self.nextPlayer()

    def placeAI(self):
        if not self.gameOver:
            if not self.isPlayerTurn:
                row, col = self.aibot.placePiece()
                if self.grid.checkWin(row, col, self.aibot.color):
                    self.win(self.player)
                    print('WINNN')
                else:
                    self.nextPlayer()
    
    def win(self, winner):
        self.gameOver = True
        if winner == self.player:
            self.message.textMessage = "Player "
        elif winner == self.player:
            self.message.textMessage = "AI "
        if winner.color == 'w':
            color = 'White'
        elif winner.color == 'b':
            color = 'Black'
        self.message.textMessage += f"{color} Wins!!!"

def appStarted(app):
    length = app.width
    app.game = gomokuGame(length)

#################################################
# Control
#################################################

def mouseMoved(app, event):
    app.game.moving(event.x, event.y) # turnblack

def mousePressed(app, event):
    app.game.placePlayer(event.x, event.y)

def timerFired(app):
    app.game.placeAI()

#################################################
# View
#################################################

def redrawAll(app, canvas):
    print(app.game.message.textMessage)
    app.game.message.drawMessage(canvas)
    app.game.grid.drawScreen(canvas)


def main():
    runApp(width=600, height=650)

if __name__ == '__main__':
    main()