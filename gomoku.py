
from cgi import test
from sys import builtin_module_names
from cmu_112_graphics import *
import random, string, math, time


#################################################
# Helper Functions
#################################################

import decimal

from human_player import player
from aibot import ai
from grid_board import gridBoard
from aiTester import testAI
from boardMethods import boardMethods

def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Gomoku Game
#################################################

class message():

    def __init__(self, length, topMargin, isPlayerTurn, isPlayerBlack, player2Exist):
        self.length = length
        self.topMargin = topMargin
        self.isPlayerTurn = isPlayerTurn
        self.isPlayerBlack = isPlayerBlack
        self.player2Exist = player2Exist
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
            if self.player2Exist:
                self.textMessage = "Player 2:"
            else:
                self.textMessage = "AI:"
            if self.isPlayerBlack:
                self.textMessage += " White"
            else:
                self.textMessage += " Black"
        print(self.textMessage)

    def drawMessage(self, canvas):
        canvas.create_text(self.length/2, self.topMargin/2, text = self.textMessage, fill = "#954535", font = "Helvetica 30 bold")

class gomokuGame():

    def __init__(self, length, player2Exist): # if player2 is True, it will be a 2 player
        self.cells = 6
        self.length = length
        self.margin = 20
        self.topMargin = 50
        self.gameOver = False
        self.isPlayerBlack = bool(random.randrange(0,2))
        self.winRows = 4 # number of rows to win
        if self.isPlayerBlack:
            self.isPlayerTurn = True
        else:
            self.isPlayerTurn = False
        
        self.player2Exist = player2Exist

        self.board = [[""] * self.cells for _ in range(self.cells)]
        self.initializeClasses()

    def initializeClasses(self):
        self.boardMethods = boardMethods(self.cells, self.winRows)
        self.grid = gridBoard(self.board, self.length, self.margin, self.topMargin, self.cells)
        self.player = player(self.board, self.length, self.margin, self.topMargin, self.cells, self.isPlayerBlack)
        self.player2 = player(self.board, self.length, self.margin, self.topMargin, self.cells, not self.isPlayerBlack)
        self.aibot = ai(self.board, self.length, self.margin, self.topMargin, self.cells, not self.isPlayerBlack, self.winRows)
        self.message = message(self.length, self.topMargin, self.isPlayerTurn, self.isPlayerBlack, self.player2Exist)


    def updateBoards(self):
        self.grid.updateBoard(self.board)
        self.player.updateBoard(self.board)
        self.aibot.updateBoard(self.board)
    
    def resizeBoard(self, isIncrease):
        if isIncrease and self.cells < 20:
            self.cells += 1
            self.board = [[""] * self.cells for _ in range(self.cells)]
            self.initializeClasses()
        elif not isIncrease and self.cells > 2:
            self.cells -= 1
            self.board = [[""] * self.cells for _ in range(self.cells)]
            self.initializeClasses()

    def nextPlayer(self):
        self.isPlayerTurn = not self.isPlayerTurn
        self.message.updateMessageTurn(self.isPlayerTurn)

    def moving(self, x, y):
        if not self.gameOver:
            if self.isPlayerTurn:
                self.player.hoveringPiece(x, y)
    def movingPlayer2(self, x, y):
        if not self.gameOver:
            if not self.isPlayerTurn:
                self.player2.hoveringPiece(x, y)

    def placePlayer(self, x, y):
        if not self.gameOver:
            if self.isPlayerTurn:
                move = self.player.placePiece(x, y) #row, col
                if move == None:
                    self.message.textMessage = "Invalid Placement"
                else:
                    row, col = move[0], move[1]
                    if self.boardMethods.checkWin(row, col, self.player.color, self.board):
                        self.win(self.player)
                        print('WINNN')
                    elif self.boardMethods.checkFull(self.board):
                        self.tie()
                        print("tiee")
                    else:
                        self.nextPlayer()
    
    def placePlayer2(self, x, y):
        if not self.gameOver:
            if not self.isPlayerTurn:
                move = self.player2.placePiece(x, y) #row, col
                print(move)
                if move == None:
                    self.message.textMessage = "Invalid Placement"
                else:
                    row, col = move[0], move[1]
                    if self.boardMethods.checkWin(row, col, self.player2.color, self.board):
                        self.win(self.player2)
                        print('WINNN')
                    elif self.boardMethods.checkFull(self.board):
                        self.tie()
                        print("tiee")
                    else:
                        self.nextPlayer()
    

    def placeAI(self):
        if not self.gameOver:
            if not self.isPlayerTurn:
                row, col = self.aibot.placePiece(True)
                if self.boardMethods.checkWin(row, col, self.aibot.color, self.board):
                    self.win(self.aibot)
                    print('WINNN')
                elif self.boardMethods.checkFull(self.board):
                    self.tie()
                    print("tiee")
                else:
                    self.nextPlayer()
    
    def win(self, winner):
        self.gameOver = True
        if winner == self.player:
            self.message.textMessage = "Player "
        elif winner == self.aibot:
            self.message.textMessage = "AI "
        elif winner == self.player2:
            self.message.textMessage = "Player 2"
        if winner.color == 'w':
            color = 'White'
        elif winner.color == 'b':
            color = 'Black'
        self.message.textMessage += f"{color} Wins!!!"

    def tie(self):
        pass
def appStarted(app): #https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    length = app.width
    app.player2 = False
    gameMode = input("type 1 for 1 player, 2 for 2 player: ")
    if gameMode == "2":
        app.player2 = True
    elif gameMode == "1":
        app.player2 = False
    else:
        gameMode = input("type 1 for 1 player, 2 for 2 player: ")
    app.game = gomokuGame(length, app.player2)
    app.timerDelay = 1000

#################################################
# Control
#################################################

def mouseMoved(app, event):
    app.game.moving(event.x, event.y) # turnblack
    if app.player2:
        app.game.movingPlayer2(event.x, event.y)

def mousePressed(app, event):
    app.game.placePlayer(event.x, event.y)
    if app.player2:
        app.game.placePlayer2(event.x, event.y)

def keyPressed(app, event):
    if event.key == "r":
        appStarted(app)
    elif event.key == "Up":
        app.game.resizeBoard(True)
    elif event.key == "Down":
        app.game.resizeBoard(False)

def timerFired(app):
    if not app.player2:
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