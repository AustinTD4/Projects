import numpy as np
#import tensorflow as tf
from chessboard import chessboard
import pygame, copy, time, random

class chessUI(chessboard):
    '''
    A Class that opens a visual Chess game in pygame
    All methods related to gameplay are here

    '''
    def __init__(self, visual=True):
        super().__init__()

        # pygame variables
        self.black = (0,0,0) 
        self.white = (255,255,255)
        self.colors = [self.white, self.black]
        self.visual = visual
        self.directions = [-1, 1]
        self.antiColor = [1,0]
        self.borders = [25,95,165,235,305,375,445,515]
        self.pawnPromoteSelection = [[165,645],[235,645],[305,645],[375,645]]
        self.playBlack = False
        self.AI = True

    def renderBoard(self):
        self.visualBoard.fill(self.black) 
        count = 0
        for i in self.borders:
            for j in self.borders:
                count += 1
                if count%2 == 0:
                    pygame.draw.rect(self.visualBoard, self.white, pygame.Rect(i,j,70,70)) 
                if j == 515: count += 1

        for i in range(8):
            for j in [0, 1, 6, 7]:
                self.drawPiece(i, j)
        
    def drawPiece(self, xInd: int, yInd: int):
        piece = self.board[xInd,yInd]
        color = self.pieceKey[piece][1]
        x = self.borders[xInd]
        y = self.borders[yInd]
        if piece == 1 or piece == 7: self.drawPawn(x, y, color)
        elif piece == 2 or piece == 8: self.drawRook(x, y, color)
        elif piece == 3 or piece == 9: self.drawKnight(x, y, color)
        elif piece == 4 or piece == 10: self.drawBishop(x, y, color)
        elif piece == 5 or piece == 11: self.drawQueen(x, y, color)
        elif piece == 6 or piece == 12: self.drawKing(x, y, color)

    def drawPawn(self, x: int, y: int, color: int):
        pygame.draw.circle(self.visualBoard, self.colors[color-1], (x+35, y+35), 22) 
        pygame.draw.circle(self.visualBoard, self.colors[color], (x+35, y+35), 20) 

    def drawRook(self, x: int, y: int, color: int):
        pygame.draw.rect(self.visualBoard, self.colors[color-1], (x+13, y+8, 44, 54))
        pygame.draw.rect(self.visualBoard, self.colors[color], (x+15, y+10, 40, 50))

    def drawKnight(self, x: int, y: int, color: int):
        pygame.draw.rect(self.visualBoard, self.colors[color-1], (x+18, y+53, 34, 15))
        pygame.draw.polygon(self.visualBoard, self.colors[color-1], [(x+40, y+17), (x+22, y+55), (x+48, y+55)])
        pygame.draw.polygon(self.visualBoard, self.colors[color-1], [(x+15, y+18), (x+44, y+10), (x+46, y+32)])
        pygame.draw.rect(self.visualBoard, self.colors[color], (x+20, y+55, 30, 11))
        pygame.draw.polygon(self.visualBoard, self.colors[color], [(x+40, y+19), (x+25, y+53), (x+45, y+53)])
        pygame.draw.polygon(self.visualBoard, self.colors[color], [(x+18, y+18), (x+42, y+12), (x+44, y+30)])

    def drawBishop(self, x: int, y: int, color: int):
        pygame.draw.rect(self.visualBoard, self.colors[color-1], (x+20, y+53, 30, 15))
        pygame.draw.polygon(self.visualBoard, self.colors[color-1], [(x+35, y+15), (x+22, y+55), (x+48, y+55)])
        pygame.draw.circle(self.visualBoard, self.colors[color-1], (x+35, y+15), 10)
        pygame.draw.rect(self.visualBoard, self.colors[color], (x+22, y+55, 26, 11))
        pygame.draw.polygon(self.visualBoard, self.colors[color], [(x+35, y+17), (x+25, y+53), (x+45, y+53)])
        pygame.draw.circle(self.visualBoard, self.colors[color], (x+35, y+15), 8)
        pygame.draw.circle(self.visualBoard, self.colors[color-1], (x+32, y+12), 4)

    def drawQueen(self, x: int, y: int, color: int):
        pygame.draw.rect(self.visualBoard, self.colors[color-1], (x+20, y+53, 30, 15))
        pygame.draw.polygon(self.visualBoard, self.colors[color-1], [(x+35, y+25), (x+22, y+55), (x+48, y+55)])
        pygame.draw.circle(self.visualBoard, self.colors[color-1], (x+35, y+25), 12)
        pygame.draw.circle(self.visualBoard, self.colors[color-1], (x+35, y+12), 8)
        pygame.draw.rect(self.visualBoard, self.colors[color], (x+22, y+55, 26, 11))
        pygame.draw.polygon(self.visualBoard, self.colors[color], [(x+35, y+27), (x+25, y+53), (x+45, y+53)])
        pygame.draw.circle(self.visualBoard, self.colors[color], (x+35, y+25), 10)
        pygame.draw.circle(self.visualBoard, self.colors[color], (x+35, y+12), 6)

    def drawKing(self, x: int, y: int, color: int):
        pygame.draw.rect(self.visualBoard, self.colors[color-1], (x+20, y+53, 30, 15))
        pygame.draw.polygon(self.visualBoard, self.colors[color-1], [(x+35, y+25), (x+22, y+55), (x+48, y+55)])
        pygame.draw.circle(self.visualBoard, self.colors[color-1], (x+35, y+25), 12)
        pygame.draw.polygon(self.visualBoard, self.colors[color-1], [(x+25, y+25), (x+35, y+15), (x+15, y+8)]) 
        pygame.draw.polygon(self.visualBoard, self.colors[color-1], [(x+45, y+25), (x+35, y+15), (x+55, y+8)]) 
        pygame.draw.polygon(self.visualBoard, self.colors[color-1], [(x+25, y+20), (x+45, y+20), (x+35, y+1)])        
        pygame.draw.rect(self.visualBoard, self.colors[color], (x+22, y+55, 26, 11))
        pygame.draw.polygon(self.visualBoard, self.colors[color], [(x+35, y+27), (x+25, y+53), (x+45, y+53)])
        pygame.draw.circle(self.visualBoard, self.colors[color], (x+35, y+25), 10)
        pygame.draw.polygon(self.visualBoard, self.colors[color], [(x+27, y+25), (x+33, y+15), (x+17, y+10)]) 
        pygame.draw.polygon(self.visualBoard, self.colors[color], [(x+43, y+25), (x+37, y+15), (x+53, y+10)]) 
        pygame.draw.polygon(self.visualBoard, self.colors[color], [(x+27, y+20), (x+43, y+20), (x+35, y+3)]) 

    def fillPosition(self, x: int, y: int):
        pygame.draw.rect(self.visualBoard, self.colors[self.colorKey[x,y]], pygame.Rect(self.borders[x], self.borders[y], 70, 70))
        if self.board[x, y] != 0:
            self.drawPiece(x, y)

    def highlightPosition(self, x: int, y: int):
        if self.visual:
            pygame.draw.rect(self.visualBoard, (180,0,0), pygame.Rect(self.borders[x], self.borders[y], 70, 70))
        self.highlighted.append([x,y])
        if self.visual and self.board[x, y] != 0:
            self.drawPiece(x, y)

    def turnComplete(self, xInd: int, yInd: int):
        for coordinates in self.highlighted:
            self.fillPosition(coordinates[0], coordinates[1])

        self.highlighted = []
        self.castle = []

        if self.moved:
            self.selected=False
            self.moves += 1
        else:
            self.selected=True
            if self.pieceKey[self.board[xInd,yInd]][1] == self.moves%2:
                pygame.draw.rect(self.visualBoard, (255,0,0), 
                                (self.borders[xInd], self.borders[yInd], 70, 70)) 
                self.highlighted.append([xInd, yInd])

                if self.board[xInd, yInd] != 0:
                    self.drawPiece(xInd, yInd)
                    self.highlighted.append([xInd, yInd])
                    self.highlightMoves(xInd, yInd)

        self.lastClick = [xInd, yInd]

    def movePiece(self, x: int, y: int, prev=False, override=False):
        if not prev:
            prev = self.lastClick

        if [x,y] in self.highlighted or override:
            if prev and (x != prev[0] or y != prev[1]):
                self.moved = True

                # Tally points captured
                if self.pieceKey[self.board[x,y]][1] == 0: self.blackPoints += self.pieceKey[self.board[x,y]][0]
                elif self.pieceKey[self.board[x,y]][1] == 1: self.whitePoints += self.pieceKey[self.board[x,y]][0]
                
                self.board[x, y] = self.board[prev[0], prev[1]]
                self.board[prev[0], prev[1]] = 0
                self.fillPosition(prev[0], prev[1])
                self.fillPosition(x, y)
                color = self.pieceKey[self.board[x,y]][1]

                if self.board[x, y] == 6: self.whiteKing = [x, y]
                elif self.board[x, y] == 12: self.blackKing = [x, y]
                self.kingCoord = [self.whiteKing, self.blackKing]

                if not self.isUnthreatened(self.kingCoord[color][0], self.kingCoord[color][1], color): 
                    if self.board[x,y] in self.rooks or self.board[x,y] in self.queens or self.board[x,y] in self.bishops:
                        self.checkCleric(x, y,  axis=True)
                    else:
                        self.checkCleric(x, y, axis=False)

                if prev in self.coordinates:
                    self.untouched[self.coordinates.index(prev)] = False
                self.lastMove = [prev,[x,y]]

                if self.moved: 
                    self.kingPing(self.antiColor[color])

        if (y == 0 or y == 7) and (self.board[x,y] == 1 or self.board[x,y] == 7): 
            self.promotePawn(x, y, self.pieceKey[self.board[x,y]][1])

        self.highlightMoves(x, y, light=False)

    def pinCheck(self, x: int, y: int, newX: int, newY: int):
        color = self.pieceKey[self.board[x,y]][1]
        positions = [self.whiteKing, self.blackKing]
        boardCopy = copy.deepcopy(self.board)
        boardCopy[x,y] = 0
        boardCopy[newX, newY] = self.pawns[color-1]
        if self.isUnthreatened(positions[color][0], positions[color][1], color, boardCopy): return False
        else: return True

    def interpolate(self):
        self.attackLine = []
        distX = np.abs(self.checkPos[0] - self.kingPos[0])
        distY = np.abs(self.checkPos[1] - self.kingPos[1])

        for i in range(1, max(distX, distY)):
            if distX == distY: self.attackLine.append([min(self.checkPos[0]+i, self.kingPos[0]+i), min(self.checkPos[1]+i, self.kingPos[1]+i)]) 
            elif distX > distY: self.attackLine.append([min(self.checkPos[0]+i, self.kingPos[0]+i), min(self.checkPos[1], self.kingPos[1])])
            else: self.attackLine.append([min(self.checkPos[0], self.kingPos[0]), min(self.checkPos[1]+i, self.kingPos[1]+i)])

    def kingPing(self, color: int):
        self.pinned = []
        self.pinLines = []
        self.pinner = []
        displacements = [[-1,0],[1,0],[0,-1],[0,1],[-1,-1],[1,-1],[-1,1],[1,1]]
        position = self.kingCoord[color]
        oX = position[0]
        oY = position[1]
        count = 0
        for pair in displacements:
            pin = False
            pinLine = []
            allies = 0
            x = oX
            y = oY
            deltaX = pair[0]
            deltaY = pair[1]

            # Follow the axis until another piece is found
            while 7 >= x+deltaX >= 0 and 7 >= y+deltaY >= 0 and self.board[x+deltaX,y+deltaY] == 0:
                x += deltaX
                y += deltaY
                pinLine.append([x,y])
            x += deltaX
            y += deltaY

            if 7 >= x >= 0 and 7 >= y >= 0 and self.pieceKey[self.board[x,y]][1] == color:
                allies += 1 
                allyX = x
                allyY = y

            # Follow the axis beyond the first piece
            while (allies == 1 and 7 >= x+deltaX >= 0 and 7 >= y+deltaY >= 0 and self.board[x+deltaX,y+deltaY] == 0):
                x += deltaX
                y += deltaY
                pinLine.append([x,y])
            x += deltaX
            y += deltaY
            pinLine.append([x,y])

            if count < 4 and 7 >= x >= 0 and 7 >= y >= 0 and self.pieceKey[self.board[x,y]][1] != color and allies == 1 and (self.board[x,y] in self.rooks or self.board[x,y] in self.queens):
                print("Pin1")
                pin = True
                self.pinner.append([x,y])
                self.pinned.append([allyX, allyY])
            elif count >= 4 and 7 >= x >= 0 and 7 >= y >= 0 and self.pieceKey[self.board[x,y]][1] != color and allies == 1 and (self.board[x,y] in self.bishops or self.board[x,y] in self.queens):
                print("Pin2")
                pin = True
                self.pinner.append([x,y])
                self.pinned.append([allyX, allyY])

            count += 1
            if pin == True: self.pinLines.append(pinLine)            

    def isUnthreatened(self, x: int, y: int, color: int, board=[[99]]):
        if board[0][0] == 99:
            board = self.board
        directions = ([-1,0],[1,0],[0,-1],[0,1],[-1,-1],[-1,1],[1,-1],[1,1])
        oX = x
        oY = y

        for i in range(8):
            direction = directions[i]
            x = oX
            y = oY
            x += direction[0]
            y += direction[1]
            if (7 >= x >= 0 and 7 >= y >= 0 and (board[x,y] == self.kings[color] or 
                (direction[1] == self.directions[color] and board[x,y] == self.pawns[color] and i >= 4))):
                print(f'{x}, {y} threat1')
                return False
            
            while 7 >= x >= 0 and 7 >= y >= 0 and board[x,y] == 0:
                x += direction[0]
                y += direction[1]

            if 7 >= x >= 0 and 7 >= y >= 0 and self.pieceKey[self.board[x,y]][1] != color:
                if (((board[x,y] in self.rooks or board[x,y] in self.queens and i < 4) or 
                    (board[x,y] in self.bishops or board[x,y] in self.queens and i >= 4))
                                                 and self.pieceKey[board[x,y]][1] != color):
                    print(f'{x}, {y} threat2')
                    return False

        coordinates = [[oX-1,oY-2],[oX+1,oY-2],[oX-2,oY-1],[oX-2,oY+1],[oX-1,oY+2],[oX+1,oY+2],[oX+2,oY-1],[oX+2,oY+1]]
        for pair in coordinates:
            if 0 <= pair[0] <= 7 and 0 <= pair[1] <= 7 and board[pair[0],pair[1]] == self.knights[color]:
                print(f'{x}, {y} threat3')
                return False
            
        return True               

    def playFromCheck(self, x: int, y: int):
        self.movePiece(x, y)
        if self.moved:
            self.check = False
            self.attackLine = [[9,9]]
            self.checkPos = [9,9]
            self.kingPos = False

    def checkCleric(self, x: int, y: int, axis=False):
        kings = [self.blackKing, self.whiteKing]
        self.check = True
        coords = self.pawnPromoteSelection
        pygame.draw.rect(self.visualBoard, self.black, pygame.Rect(coords[0][0], coords[0][1], 280, 70))
        self.displayText('Check')
        self.checkPos = [x,y]
        color = self.pieceKey[self.board[x,y]][1]
        self.kingPos = kings[color]
        if axis:
            self.interpolate()

        self.mateCheck(color)

    def mateCheck(self, color: int):
        print('Matecheck')
        self.movesPossible = False
        self.mateChecking = True
        pieces = [[1,2,3,4,5,6],[7,8,9,10,11,12]]
        for i in range(8):
            if self.movesPossible: break
            for j in range(8):
                if self.movesPossible: break
                if self.board[i,j] in pieces[color-1]:
                    self.highlightMoves(i, j, light=True)
        print(f'Moves: {self.movesPossible}')
        if not self.movesPossible:
            self.displayText('Checkmate')
            self.checkmate = True
            self.check = False

        self.mateChecking = False

    def catalogMoves(self, color: int):
        self.catalogPieces = []
        self.catalogMoveOptions = []
        self.catalog = True
        pieces = [[1,2,3,4,5,6],[7,8,9,10,11,12]]
        for i in range(8):
            for j in range(8):
                if self.board[i,j] in pieces[color-1]:
                    self.highlightMoves(i, j, light=True)

        print(self.catalogPieces)
        print(self.catalogMoveOptions)
        self.catalog = False

    def AI_turn(self, color: int, epsilon: float):

        if random.random() < epsilon:
            self.randomMove()

        else:
            self.policyMoves(color)

        pygame.display.update()
        if self.check:
            self.check = False

    def randomMove(self):
        time.sleep(1)
        ind = random.randint(0,len(self.catalogPieces)-1)
        pygame.draw.rect(self.visualBoard, (255,0,0), (self.borders[self.catalogPieces[ind][0]], 
                                                self.borders[self.catalogPieces[ind][1]], 70, 70)) 
        self.drawPiece(self.catalogPieces[ind][0], self.catalogPieces[ind][1])
        pygame.display.update()
        ind2 = random.randint(0,len(self.catalogMoveOptions[ind])-1)

        time.sleep(1)
        print(self.catalogMoveOptions[ind][ind2][0])
        print(self.catalogMoveOptions[ind][ind2][1])
        self.movePiece(self.catalogMoveOptions[ind][ind2][0], self.catalogMoveOptions[ind][ind2][1], 
                                                                self.catalogPieces[ind], override=True)
        self.turnComplete(self.catalogMoveOptions[ind][ind2][0], self.catalogMoveOptions[ind][ind2][1])

    def policyMoves(self, color: int):
        batch = []
        fullOpportunities = []

        # Iterates over each piece with legal moves
        for i in range(len(self.catalogPieces)):
            opportunities = []
            pieceValue = self.pieceKey[self.board[self.catalogPieces[i][0],self.catalogPieces[i][1]]][0]
            nonthreat = self.isUnthreatened(self.catalogPieces[i][0],self.catalogPieces[i][1], color)

            # Taken heuristic value of each move for the piece
            for j in range(len(self.catalogMoveOptions[i])):
                opportunityValue = self.pieceKey[self.board[self.catalogMoveOptions[i][j][0],self.catalogMoveOptions[i][j][1]]][0]
                if self.isUnthreatened(self.catalogMoveOptions[i][j][0], self.catalogMoveOptions[i][j][1], color): 
                    if nonthreat:
                        opportunities.append(opportunityValue)
                    else:
                        opportunities.append(opportunityValue+pieceValue)
                else: 
                    opportunities.append(opportunityValue-pieceValue)

            ind = opportunities.index(max(opportunities))
            batch.append(opportunities[ind])
            fullOpportunities.append(opportunities)
        print(f'Batch {batch}')

        if max(batch) == 0:
            self.randomMove()
            return

        piece = self.catalogPieces[batch.index(max(batch))]
        ind = batch.index(max(batch))
        moveTo = self.catalogMoveOptions[ind][fullOpportunities[ind].index(max(fullOpportunities[ind]))]
        print(f'Value: {max(batch)}')
        time.sleep(1)
        pygame.draw.rect(self.visualBoard, (255,0,0), (self.borders[piece[0]], 
                                                self.borders[piece[1]], 70, 70)) 
        self.drawPiece(piece[0], piece[1])
        pygame.display.update()

        time.sleep(1)
        self.movePiece(moveTo[0], moveTo[1], self.catalogPieces[ind], override=True)
        self.turnComplete(moveTo[0], moveTo[1])

    def promotePawn(self, x: int, y: int, color: int):
        self.promotedPawn = True
        self.promotedPawnCoord = [x,y]
        self.promotedPawnPos = [self.borders[x],self.borders[y]]
        self.promoColor = color
        coords = self.pawnPromoteSelection
        pygame.draw.rect(self.visualBoard, self.white, pygame.Rect(coords[0][0], coords[0][1], 280, 70))
        self.drawKnight(coords[0][0], coords[0][1], color)
        self.drawBishop(coords[1][0], coords[1][1], color)
        self.drawRook(coords[2][0], coords[2][1], color)
        self.drawQueen(coords[3][0], coords[3][1], color)        

    def enPissant(self, x: int, y: int):
        self.displayText('En Pissant')
        color = self.pieceKey[self.board[self.lastClick[0], self.lastClick[1]]][1]
        self.movePiece(x, y)
        if color == 0: self.whitePoints += 1
        else: self.blackPoints += 1
        self.board[self.enPissantPos[0], self.enPissantPos[1]-self.directions[color]] = 0
        self.fillPosition(self.enPissantPos[0], self.enPissantPos[1]-self.directions[color])
        self.enPissantPos = False

    def castleCheck(self, color: int, rows: list):
        newPos = [1,5]
        fullGroups = [[0,1,2,3],[3,4,5,6,7]]
        groups = [[1,2],[4,5,6]]
        for count, group in enumerate(groups):
            if (all(self.board[i, rows[color]] == 0 for i in group) and all(self.isUnthreatened(j, rows[color], color) for j in fullGroups[count])  
                                                                            and self.untouched[count+color*3]):
                if self.catalog: 
                    self.tempMoves.append([newPos[count], rows[color]]) 
                else: 
                    self.highlightPosition(newPos[count], rows[color])
                    self.castle.append([newPos[count], rows[color]])

    def castling(self, coordinate: list):
        self.displayText('Castling')
        self.movePiece(coordinate[0], coordinate[1], [3, coordinate[1]])
        if coordinate[0] == 1: self.movePiece(coordinate[0]+1, coordinate[1], [0, coordinate[1]])
        else: self.movePiece(coordinate[0]-1, coordinate[1], [7, coordinate[1]])

    def highlightMoves(self, x: int, y: int, light=True):
        self.tempMoves = []
        pin = False
        piece = self.board[x,y]
        color = self.pieceKey[piece][1]
        for i in range(len(self.pinned)):
            if [x,y] == self.pinned[i]:
                if not self.catalog and light: self.displayText('This Piece is Pinned')
                pin = True
                self.highlightedPin = self.pinLines[i]
                self.pinnerPos = self.pinner[i]
    
        if piece == 1 or piece == 7 and not pin: self.movesPawn(x, y, color, light)
        elif piece == 1 or piece == 7: self.pinnedPawn(x, y, color)
        elif piece == 2 or piece == 8: self.movesRook(x, y, color, light, pin)
        elif piece == 3 or piece == 9: self.movesKnight(x, y, color, light, pin)
        elif piece == 4 or piece == 10: self.movesBishop(x, y, color, light, pin)
        elif piece == 5 or piece == 11: self.movesQueen(x, y, color, light, pin)
        elif piece == 6 or piece == 12: self.movesKing(x, y, color, light)

        if self.catalog and len(self.tempMoves) != 0:
            self.catalogPieces.append([x,y])
            self.catalogMoveOptions.append(self.tempMoves)
        self.tempMoves = []

    def extendMovesAxis(self, x: int, y: int, color: int, deltaX: int, deltaY: int, highlight=True, pin=False):
        oX = x
        oY = y

        combinedList = self.attackLine + self.checkPos
        while 7 >= x+deltaX >= 0 and 7 >= y+deltaY >= 0 and self.board[x+deltaX,y+deltaY] == 0:
            if highlight and ((not self.check and not pin) or (not pin and [x+deltaX, y+deltaY] in combinedList) or 
                                                            (not self.check and [x+deltaX, y+deltaY] in self.highlightedPin)):
                if self.mateChecking: self.movesPossible = True
                elif self.catalog: self.tempMoves.append([x+deltaX,y+deltaY])
                else: self.highlightPosition(x+deltaX,y+deltaY)
            x += deltaX
            y += deltaY
        x += deltaX
        y += deltaY

        if 7 >= x >= 0 and 7 >= y >= 0:
            if (highlight and self.pieceKey[self.board[x,y]][1] != color and ((not self.check and not pin) or 
                    (not pin and [x, y] in combinedList) or (not self.check and [x, y] in self.highlightedPin))): 
                if self.mateChecking: self.movesPossible = True
                elif self.catalog: self.tempMoves.append([x,y]) 
                else: self.highlightPosition(x,y)
            elif not highlight and self.board[x,y] == self.kings[color] and not self.check: 
                self.checkPos = [oX,oY]
                self.checkCleric(oX, oY, axis=True)

    def pinnedPawn(self, x: int, y: int, color: int):
        directions = [-1, 1]
        if not self.check and self.board[x, y+directions[color]] == 0 and [x, y+directions[color]] in self.highlightedPin:
            if self.mateChecking: 
                self.movesPossible = True 
                return
            elif self.catalog: self.tempMoves.append([x,y+directions[color]])
            else: self.highlightPosition(x,y+directions[color])

            if self.board[x, y+directions[color]*2] == 0 and [x, y+directions[color]] in self.highlightedPin:
                self.highlightPosition(x, y+directions[color]*2)

        for offset in [-1,1]:
            if (0 <= x+offset <= 7 and not self.check and [x+offset, y+directions[color]] == self.pinnerPos):
                if self.mateChecking: self.movesPossible = True 
                elif self.catalog: self.tempMoves.append([x+offset,y+directions[color]])
                else: self.highlightPosition(x+offset,y+directions[color])

    def movesPawn(self, x: int, y: int, color: int, light: bool):
        directions = [-1, 1]
        positions = [6, 1]
        enemy = [7,1]

        if light and self.board[x, y+directions[color]] == 0 and (not self.check or [x, y+directions[color]] in self.attackLine):
                if not self.check or [x, y+directions[color]] in self.attackLine: 
                    if self.mateChecking: self.movesPossible = True 
                    elif self.catalog: self.tempMoves.append([x,y+directions[color]])
                    else: self.highlightPosition(x,y+directions[color])

                if y == positions[color] and self.board[x, y+directions[color]*2] == 0:
                    if not self.check or [x, y+directions[color]*2] in self.attackLine:
                        if self.mateChecking: self.movesPossible = True 
                        elif self.catalog: self.tempMoves.append([x,y+directions[color]*2])
                        else: self.highlightPosition(x,y+directions[color]*2)

        if self.lastMove:
            for offset in [-1,1]:
                if (0 <= x+offset <= 7 and self.pieceKey[self.board[x+offset, y+directions[color]]][1] != color 
                                                                       and self.board[x+offset, y+directions[color]] != 0):
                    
                    if light and (not self.check or [x+offset, y+directions[color]] == self.checkPos): 
                        if self.mateChecking: self.movesPossible = True 
                        elif self.catalog: self.tempMoves.append([x+offset,y+directions[color]])
                        else: self.highlightPosition(x+offset, y+directions[color])
                    
                    elif self.board[x+offset,y+directions[color]] == self.kings[color] and not self.check: 
                        self.checkCleric(x, y)

            if (np.abs(self.lastMove[0][1] - self.lastMove[1][1]) == 2 and light 
                and self.board[self.lastMove[1][0], self.lastMove[1][1]] == enemy[color]):
                for i in [0,1]:
                    if self.lastMove[1][1] == y and self.lastMove[1][0] + directions[i] == x:
                        if self.catalog: 
                            self.tempMoves.append([x,y+directions[color]])
                        else: 
                            self.highlightPosition(self.lastMove[1][0], y+directions[color])
                            self.enPissantPos = [self.lastMove[1][0], y+directions[color]]

    def movesRook(self, x: int, y: int, color: int, light: bool, pin: bool):
        self.extendMovesAxis(x, y, color, -1, 0, light, pin)
        self.extendMovesAxis(x, y, color, 1, 0, light, pin)
        self.extendMovesAxis(x, y, color, 0, -1, light, pin)
        self.extendMovesAxis(x, y, color, 0, 1, light, pin)

    def movesKnight(self, x: int, y: int, color: int, light: bool, pin: bool):
        coordinates = [[x-1,y-2],[x+1,y-2],[x-2,y-1],[x-2,y+1],[x-1,y+2],[x+1,y+2],[x+2,y-1],[x+2,y+1]]
        for pair in coordinates:

            if 0 <= pair[0] <= 7 and 0 <= pair[1] <= 7 and self.pieceKey[self.board[pair[0],pair[1]]][1] != color:
                combinedCoordinates = (self.attackLine + [self.checkPos])

                if light and ((not self.check and not pin) or (not pin and pair in combinedCoordinates) or 
                                                            (not self.check and pair in self.highlightedPin)):
                    if self.mateChecking: self.movesPossible = True 
                    elif self.catalog: self.tempMoves.append([pair[0], pair[1]])
                    else: self.highlightPosition(pair[0],pair[1])

                elif self.board[pair[0],pair[1]] == self.kings[color] and not self.check: 
                    self.checkCleric(x, y)

    def movesBishop(self, x: int, y: int, color: int, light: bool, pin: bool):
        self.extendMovesAxis(x, y, color, -1, -1, light, pin)
        self.extendMovesAxis(x, y, color, 1, -1, light, pin)
        self.extendMovesAxis(x, y, color, -1, 1, light, pin)
        self.extendMovesAxis(x, y, color, 1, 1, light, pin)

    def movesQueen(self, x: int, y: int, color: int, light: bool, pin: bool):
        self.extendMovesAxis(x, y, color, -1, 0, light, pin)
        self.extendMovesAxis(x, y, color, 1, 0, light, pin)
        self.extendMovesAxis(x, y, color, 0, -1, light, pin)
        self.extendMovesAxis(x, y, color, 0, 1, light, pin)
        self.extendMovesAxis(x, y, color, -1, -1, light, pin)
        self.extendMovesAxis(x, y, color, 1, -1, light, pin)
        self.extendMovesAxis(x, y, color, -1, 1, light, pin)
        self.extendMovesAxis(x, y, color, 1, 1, light, pin)

    def movesKing(self, x: int, y: int, color: int, light: bool):
        rows = [7,0]
        index = [2,5]
        if x == 3 and y == rows[color] and self.untouched[index[color]]: 
            self.castleCheck(color, rows)

        displacements = [[-1,0],[1,0],[0,-1],[0,1],[-1,-1],[1,-1],[-1,1],[1,1]]
        boardCopy = copy.deepcopy(self.board)
        boardCopy[self.kingCoord[color][0], self.kingCoord[color][1]] = 0
        for pair in displacements:
            if 7 >= x+pair[0] >= 0 and 7 >= y+pair[1] >= 0:    
                if light and self.pieceKey[self.board[x+pair[0],y+pair[1]]][1] != color and self.isUnthreatened(x+pair[0],y+pair[1], color, boardCopy):
                    if self.mateChecking: self.movesPossible = True 
                    elif self.catalog: self.tempMoves.append([x+pair[0], y+pair[1]])
                    else: self.highlightPosition(x+pair[0], y+pair[1])

    def displayText(self, text: str):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(text, True, self.white, self.black)
        textRect = text.get_rect()
        textRect.center = (305, 680)
        self.visualBoard.blit(text, textRect)

    def startScreen(self):
        self.visualBoard.fill(self.black)
        texts = ['Welcome To ChessBot', '  Play as White  ', '  Play as Black  ', '  Two Player  ']
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(texts[0], True, self.white, self.black)
        textRect = text.get_rect()
        textRect.center = (305, 150)
        self.visualBoard.blit(text, textRect)
        text = font.render(texts[1], True, self.white, (50, 50, 50))
        textRect = text.get_rect()
        textRect.center = (305, 350)
        self.visualBoard.blit(text, textRect)
        text = font.render(texts[2], True, self.white, (50, 50, 50))
        textRect = text.get_rect()
        textRect.center = (305, 450)
        self.visualBoard.blit(text, textRect)
        text = font.render(texts[3], True, self.white, (50, 50, 50))
        textRect = text.get_rect()
        textRect.center = (305, 550)
        self.visualBoard.blit(text, textRect)
        pygame.display.update()

        choice = False
        while not choice: 
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickX, clickY = event.pos
                    if 155 <= clickX <= 455 and 300 <= clickY <= 600:
                        choice = True
                        if 300 <= clickX < 400:
                            continue
                        elif 400 <= clickY < 500:
                            self.playBlack = True
                        elif 500 <= clickY < 600:
                            self.AI = False

    def play(self):
        pygame.font.init()
        pygame.mixer.init()

        try:
            pygame.mixer.music.load("03_Nocturne.mp3")
            pygame.mixer.music.play()
        except pygame.error as e:
            print("Error loading or playing music file:", e)

        self.moves = 0
        self.visualBoard = pygame.display.set_mode((610,750)) 
        pygame.display.set_caption("CHESS") 
        
        exit = False
        self.startScreen()
        self.renderBoard()
        pygame.display.update()
        if self.playBlack: 
            self.catalogMoves(1)
            self.AI_turn(color=1, epsilon=0.0)

        while not exit: 
            for event in pygame.event.get():
                self.moved = False

                if event.type == pygame.QUIT:
                    exit = True

                if event.type == pygame.MOUSEBUTTONDOWN and not self.promotedPawn:
                    if self.checkmate:
                        self.assignPieces()
                        self.renderBoard()
                        self.untouched = [True, True, True, True, True, True]
                        self.checkmate = False
                        self.moves = 0

                    clickX, clickY = event.pos
                    if 25 <= clickX <= 585 and 25 <= clickY <= 585: 
                        pygame.draw.rect(self.visualBoard, self.black, pygame.Rect(0,610,610,140))
                        temp = [25, 95, 165, 235, 305, 375, 445, 515, clickX]
                        temp.sort()
                        xInd = temp.index(clickX)-1
                        temp = [25, 95, 165, 235, 305, 375, 445, 515, clickY]
                        temp.sort()
                        yInd = temp.index(clickY)-1

                        if self.check and self.selected and self.board[self.lastClick[0],self.lastClick[1]] != 0: self.playFromCheck(xInd, yInd)
                        elif [xInd, yInd] in self.castle: self.castling([xInd, yInd])
                        elif [xInd, yInd] == self.enPissantPos: self.enPissant(xInd, yInd)
                        elif self.lastClick != False: self.movePiece(xInd, yInd)

                        self.turnComplete(xInd, yInd)
                        pygame.display.update() 

                        if not self.checkmate and self.AI and (not self.playBlack and self.moves%2 != 0) or (self.playBlack and self.moves%2 == 0):
                            self.catalogMoves(self.pieceKey[self.board[self.lastClick[0], self.lastClick[1]]][1])
                            if self.playBlack: self.AI_turn(color=1, epsilon=0.0)
                            else: self.AI_turn(color=0, epsilon=0.0)

                # Handles pawn promotion
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clickX, clickY = event.pos
                    color = self.pieceKey[self.board[self.lastClick[0],self.lastClick[1]]][1]
                    if 165 <= clickX <= 445 and 645 <= clickY <= 715:
                        axis = True
                        if 165 <= clickX < 235:
                            self.board[self.promotedPawnCoord[0],self.promotedPawnCoord[1]] = self.knights[color-1]
                            axis = False
                        elif 235 <= clickX < 305:
                            self.board[self.promotedPawnCoord[0],self.promotedPawnCoord[1]] = self.bishops[color-1]
                        elif 305 <= clickX < 375:
                            self.board[self.promotedPawnCoord[0],self.promotedPawnCoord[1]] = self.rooks[color-1]
                        elif 375 <= clickX < 445:
                            self.board[self.promotedPawnCoord[0],self.promotedPawnCoord[1]] = self.queens[color-1]

                        self.fillPosition(self.promotedPawnCoord[0], self.promotedPawnCoord[1])
                        self.promotedPawn = False
                        if not self.isUnthreatened(self.kingCoord[color-1][0], self.kingCoord[color-1][1], self.antiColor[color]):
                            self.checkCleric(self.lastClick[0], self.lastClick[1], axis)

            pygame.display.update() 


visual = chessUI()
visual.play()