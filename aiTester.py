import random
from shutil import move

from aibot import ai
from grid_board import gridBoard
from cmu_112_graphics import *
from boardMethods import boardMethods

class testAI():

    def __init__(self, length):
        self.cells = 5
        self.length = length
        self.gameOver = False
        self.margin = 20
        self.topMargin = 50
        self.isPlayerBlack = True
        if self.isPlayerBlack:
            self.isPlayerTurn = True
        else:
            self.isPlayerTurn = False
        self.winRows = 3

        self.board = [[""] * self.cells for _ in range(self.cells)]
        self.boardMethods = boardMethods(self.cells, winRows=3)
        self.playerAIBot = ai(self.board, self.length, self.margin, self.topMargin, self.cells, self.isPlayerBlack, self.winRows) # substitute for human player
        self.aibot = ai(self.board, self.length, self.margin, self.topMargin, self.cells, not self.isPlayerBlack, self.winRows)
        self.grid = gridBoard(self.board, self.length, self.margin, self.topMargin, self.cells)


    def updateBoards(self):
        self.grid.updateBoard(self.board)
        self.playerAIBot.updateBoard(self.board)
        self.aibot.updateBoard(self.board)

    def nextPlayer(self):
        self.isPlayerTurn = not self.isPlayerTurn

    def placeAIPlayer(self):
        if not self.gameOver:
            if self.isPlayerTurn:
                row, col = self.playerAIBot.placePiece(False)
                if self.boardMethods.checkWin(row, col, self.playerAIBot.color, self.board):
                    self.win(self.playerAIBot)
                    print('WINNN PLAYER AI BOT')
                elif self.boardMethods.checkFull(self.board):
                    self.tie()
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
                else:
                    self.nextPlayer()
    
    def win(self, winner):
        self.gameOver = True
        if winner == self.playerAIBot:
            message = "Player AI"
        elif winner == self.aibot:
            message = "AI "
        if winner.color == 'w':
            color = 'White'
        elif winner.color == 'b':
            color = 'Black'
        message += f"{color} Wins!!!"

        return message
    def tie(self):
        self.gameOver = True
        message = "Tie"

def appStarted(app):
    length = app.width
    app.game = testAI(length)
    app.timerDelay = 500
    app.paused = False


#################################################
# Control
#################################################

def keyPressed(app, event):
    if event.key == "r":
        appStarted(app)
    elif event.key == "p":
        app.paused = not app.paused

def timerFired(app):
    if not app.paused:
        app.game.placeAI()
        app.game.placeAIPlayer()

#################################################
# View
#################################################

def redrawAll(app, canvas):
    app.game.grid.drawScreen(canvas)


def main():
    runApp(width=600, height=650)


if __name__ == '__main__':
    main()