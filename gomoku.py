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

    def checkWin(self, row, col): #row and col are for last placed piece
        if (row - 4)< 0:
            minRow = 0
        else:
            minRow = row - 4
        if (row + 4) > self.cells:
            maxRow = self.cells
        if (col - 4) < 0:
            minCol = 0
        if (col + 4) > self.cells:
            minCol = self.cells



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
            return True

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
    
    def changeBoard(self, row, col):
        board[row][col] = self.color


class message():

    def __init__(self, length, topMargin, isPlayerTurn, isPlayerBlack):
        self.length = length
        self.topMargin = topMargin
        self.isPlayerTurn = isPlayerTurn
        self.isPlayerBlack = isPlayerBlack
        self.textMessage = ""
        self.updateMessage(self.isPlayerTurn)


    def updateMessage(self, isPlayerTurn):
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
        self.message.updateMessage(self.isPlayerTurn)


    def moving(self, x, y):
        if self.isPlayerTurn:
            self.player.hoveringPiece(x, y)

    def placePlayer(self, x, y):
        if self.isPlayerTurn:
            if not self.player.placePiece(x, y):
                self.message.textMessage = "Invalid Placement"
            else:
                self.nextPlayer()

    def placeAI(self):
        if not self.isPlayerTurn:
            self.aibot.placePiece()
            self.nextPlayer()
    
    def win (self, winner):
        pass


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
    app.game.message.drawMessage(canvas)
    app.game.grid.drawScreen(canvas)


def main():
    runApp(width=600, height=650)

if __name__ == '__main__':
    main()