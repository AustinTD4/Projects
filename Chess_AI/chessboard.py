import numpy as np

class chessboard():
    '''
    An Array Class that contains each board position's tile color used to render the board
    All board positions are listed as empty of containing a specific piece
    The point values and color of each piece are listed here
    Tokens for tracking the game state are here
    ''' 
    def __init__(self):
        # Piece IDs
        self.pawns = [7,1]
        self.rooks = [8,2]
        self.knights = [9,3]
        self.bishops = [10,4]
        self.queens = [11,5]
        self.kings = [12,6]
        
        # Board square colors
        self.colorKey = np.zeros((8,8), dtype=int)
        self.fillKey()

        # Piece positions
        self.assignPieces()
        
        self.untouched = [True, True, True, True, True, True]
        self.coordinates = [[0,7],[7,7],[3,7],[0,0],[7,0],[3,0]]

        # Game State tokens
        self.selected=False
        self.lastMove = False
        self.enPissantPos = False
        self.promotedPawn = False
        self.mateChecking = False
        self.checkmate = False
        self.blackKing = [3,0]
        self.whiteKing = [3,7]
        self.kingCoord = [self.whiteKing, self.blackKing]
        self.lastClick = False
        self.highlighted = []
        self.checklist = []
        self.castle = []
        self.blackPoints = 0
        self.whitePoints = 0

        # Check tokens
        self.check = False
        self.checkPos = [9,9]
        self.kingPos = False
        self.attackLine = [[9,9]]

        # Pin tokens
        self.pinned = [[9,9]]
        self.pinner = [[9,9]]
        self.pinnerPos = []
        self.pinLines = [[[9,9]]]
        self.highlightedPin = []

        # Value and color of pieces
        self.pieceKey = {
            0: [0, 2],
            1: [1, 0],
            7: [1, 1],
            2: [5, 0],
            8: [5, 1],
            3: [3, 0],
            9: [3, 1],
            4: [3, 0],
            10: [3, 1],
            5: [9, 0],
            11: [9, 1],
            6: [999, 0],
            12: [999, 1]
        }

        # Variables and tokens for the AI
        self.catalog = False
        self.catalogPieces = []
        self.tempMoves = []
        self.catalogMoveOptions = []

    def fillKey(self):
        count = 0
        for i in range(8):
            for j in range(8):
                count += 1
                if count%2 == 1:
                    self.colorKey[i,j] = 1
                if j == 7: count += 1

    def assignPieces(self):
        # Piece positions
        self.board = np.zeros((8,8), dtype=int)
        self.board[:,1] = 7
        self.board[:,6] = 1
        self.board[0,0] = 8 
        self.board[7,0] = 8
        self.board[0,7] = 2
        self.board[7,7] = 2
        self.board[1,0] = 9 
        self.board[6,0] = 9
        self.board[1,7] = 3
        self.board[6,7] = 3
        self.board[2,0] = 10 
        self.board[5,0] = 10
        self.board[2,7] = 4 
        self.board[5,7] = 4
        self.board[4,0] = 11
        self.board[4,7] = 5
        self.board[3,0] = 12
        self.board[3,7] = 6

