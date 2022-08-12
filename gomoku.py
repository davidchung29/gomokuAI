
from cmu_112_graphics import *
import random


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
                self.textMessage = "AI Bot:"
            if self.isPlayerBlack:
                self.textMessage += " White"
            else:
                self.textMessage += " Black"

    def drawMessage(self, canvas):
        canvas.create_text(self.length/2, self.topMargin/2, text = self.textMessage, fill = "#954535", font = "Helvetica 30 bold")

class gomokuGame():

    def __init__(self, length, player2Exist, flipMode): # if player2 is True, it will be a 2 player
        self.cells = 6
        self.length = length
        self.margin = 40
        self.topMargin = 50
        self.gameOver = False
        self.isPlayerBlack = True
        self.winRows = 4 # number of rows to win
        self.isPlayerTurn = bool(random.randrange(0,2))
        
        self.player2Exist = player2Exist
        self.flipMode = flipMode

        self.board = [[""] * self.cells for _ in range(self.cells)]
        self.initializeClasses()

    def initializeClasses(self): # needed when you resize a board, to update certain values
        self.boardMethods = boardMethods(self.cells, self.winRows)
        self.grid = gridBoard(self.board, self.length, self.margin, self.topMargin, self.cells)
        self.player = player(self.board, self.length, self.margin, self.topMargin, self.cells, self.isPlayerBlack)
        self.player2 = player(self.board, self.length, self.margin, self.topMargin, self.cells, not self.isPlayerBlack)
        self.aibot = ai(self.board, self.length, self.margin, self.topMargin, self.cells, not self.isPlayerBlack, self.isPlayerTurn, self.winRows, self.flipMode)
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

    def moving(self, x, y, humanPlayer):
        if not self.gameOver:
            humanPlayer.hoveringPiece(x, y)

    def placePlayer(self, x, y, humanPlayer):
        if not self.gameOver:
            if humanPlayer == self.player:
                oppPlayer = self.player2 if self.player2Exist else self.aibot
            else:
                oppPlayer = self.player
            move = humanPlayer.placePiece(x, y) #row, col
            if move == None:
                self.message.textMessage = "Invalid Placement"
            else:
                row, col = move[0], move[1]
                flipWin = None
                if self.flipMode:
                    resBoard = self.boardMethods.flipCoords(col, self.board)
                    for r in range(len(self.board)):
                        for c in range(len(self.board[r])):
                            self.board[r][c] = resBoard[r][c]
                    flipWin = self.boardMethods.checkWinAll(self.board, humanPlayer.color, oppPlayer.color)
                if self.flipMode and flipWin:
                    if flipWin == humanPlayer.color:
                        self.win(humanPlayer)
                    elif flipWin == oppPlayer.color:
                        self.win(oppPlayer)
                elif self.boardMethods.checkWin(row, col, humanPlayer.color, self.board):
                    self.win(humanPlayer)
                elif self.boardMethods.checkFull(self.board):
                    self.tie()
                else:
                    self.nextPlayer()
    
    

    def placeAI(self):
        if not self.gameOver:
            player = self.aibot
            oppPlayer = self.player
            if not self.isPlayerTurn:
                row, col = self.aibot.placePiece(True)
                if self.flipMode:
                    resBoard = self.boardMethods.flipCoords(col, self.board)
                    for r in range(len(self.board)):
                        for c in range(len(self.board[r])):
                            self.board[r][c] = resBoard[r][c]
                    flipWin = self.boardMethods.checkWinAll(self.board, player.color, oppPlayer.color)
                if self.flipMode and flipWin:
                    if flipWin == player.color:
                        self.win(player)
                    elif flipWin == oppPlayer.color:
                        self.win(oppPlayer)
                if self.boardMethods.checkWin(row, col, self.aibot.color, self.board):
                    self.win(self.aibot)
                elif self.boardMethods.checkFull(self.board):
                    self.tie()
                else:
                    self.nextPlayer()
    
    def win(self, winner):
        self.gameOver = True
        if winner == self.player:
            self.message.textMessage = "Player "
        elif winner == self.aibot:
            self.message.textMessage = "AI "
        elif winner == self.player2:
            self.message.textMessage = "Player 2 "
        if winner.color == 'w':
            color = 'White'
        elif winner.color == 'b':
            color = 'Black'
        self.message.textMessage += f"{color} Wins!!!"
        self.aibot.updateData()

    def tie(self):
        self.mnessage = "Tie - Board is full"
        self.aibot.updateData()
def appStarted(app): #https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    length = app.width
    app.player2 = False
    app.flip = False
    while True:
        gameMode = input("Type 1 for 1 player, 2 for 2 player: ")
        if gameMode == "2":
            app.player2 = True
            break
        elif gameMode == "1":
            app.player2 = False
            break
    while True:
        flipBoard = input("Play with flip? (the horizontal line for the placed piece will flip) type y/n: ")
        if flipBoard == 'y':
            app.flip = True
            break
        elif flipBoard == 'n':
            app.flip = False
            break
    app.game = gomokuGame(length, app.player2, app.flip)
    app.timerDelay = 1000

#################################################
# Control
#################################################

def mouseMoved(app, event):
    if app.game.isPlayerTurn:
        app.game.moving(event.x, event.y, app.game.player) # turnblack
    elif app.player2:
        app.game.moving(event.x, event.y, app.game.player2)

def mousePressed(app, event):
    if app.game.isPlayerTurn:
        app.game.placePlayer(event.x, event.y, app.game.player)
    elif app.player2:
        app.game.placePlayer(event.x, event.y, app.game.player2)

def keyPressed(app, event):
    if event.key == "r":
        appStarted(app)
    elif event.key == "s":
        app.game.aibot.updateData()
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