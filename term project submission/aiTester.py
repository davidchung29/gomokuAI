
from aibot import ai
from grid_board import gridBoard
from cmu_112_graphics import *
from boardMethods import boardMethods


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
            self.textMessage = "Player AI: Black"
        else:
            self.textMessage = "AI Bot: White"

    def drawMessage(self, canvas):
        canvas.create_text(self.length/2, self.topMargin/2, text = self.textMessage, fill = "#954535", font = "Helvetica 30 bold")

class testAI():

    def __init__(self, length, flip):
        self.cells = 6
        self.length = length
        self.gameOver = False
        self.margin = 30
        self.topMargin = 50
        self.isPlayerBlack = True
        self.isPlayerTurn = True
        self.winRows = 4
        
        self.flipMode = flip # toggle to turn on flip

        self.board = [[""] * self.cells for _ in range(self.cells)]
        self.boardMethods = boardMethods(self.cells, self.winRows)
        self.playerAIBot = ai(self.board, self.length, self.margin, self.topMargin, self.cells, self.isPlayerBlack, self.isPlayerTurn, self.winRows, self.flipMode) # substitute for human player
        self.aibot = ai(self.board, self.length, self.margin, self.topMargin, self.cells, not self.isPlayerBlack, self.isPlayerTurn, self.winRows, self.flipMode)
        self.grid = gridBoard(self.board, self.length, self.margin, self.topMargin, self.cells)
        self.message = message(self.length, self.topMargin, self.isPlayerTurn, self.isPlayerBlack)


    def updateBoards(self):
        self.grid.updateBoard(self.board)
        self.playerAIBot.updateBoard(self.board)
        self.aibot.updateBoard(self.board)

    def nextPlayer(self):
        self.isPlayerTurn = not self.isPlayerTurn
        self.message.updateMessageTurn(self.isPlayerTurn)

    def placeAIPlayer(self):
        if not self.gameOver:
            player = self.playerAIBot
            oppPlayer = self.aibot
            if self.isPlayerTurn:
                row, col = self.playerAIBot.placePiece(False)
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
                elif self.boardMethods.checkWin(row, col, self.playerAIBot.color, self.board):
                    self.win(self.playerAIBot)
                elif self.boardMethods.checkFull(self.board):
                    self.tie()
                else:
                    self.nextPlayer()

    def placeAI(self):
        if not self.gameOver:
            player = self.aibot
            oppPlayer = self.playerAIBot
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
        if winner == self.playerAIBot:
            self.message.textMessage = "Player AI"
        elif winner == self.aibot:
            self.message.textMessage = "AI Bot "
        if winner.color == 'w':
            color = 'White'
        elif winner.color == 'b':
            color = 'Black'
        self.message.textMessage += f"{color} Wins!!!"
        self.aibot.updateData()

    def tie(self):
        self.gameOver = True
        self.message.textMessage += f"Tie"
        self.aibot.updateData()

def appStarted(app):
    length = app.width
    app.timerDelay = 1000
    app.paused = False
    app.flip = False
    while True:
        flipBoard = input("Play with flip? (the horizontal line for the placed piece will flip) type y/n: ")
        if flipBoard == 'y':
            app.flip = True
            break
        elif flipBoard == 'n':
            app.flip = False
            break
    app.game = testAI(length, app.flip)


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
    app.game.message.drawMessage(canvas)


def main():
    runApp(width=600, height=650)


if __name__ == '__main__':
    main()