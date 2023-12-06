#######################################
#   DPRL Assignment 3, Connect Four   #
#   Austin Dickerson                  #
#######################################
from clockManager import clockManager
import numpy as np
import pickle, copy, time
from tqdm import tqdm
from colorama import Style, Fore

class boardState():

    def __init__(self):
        self.wins = 0
        self.draws = 0
        self.losses = 0

        self.visits = 0
        self.ratio = 0
        self.winProb = 0

    def update(self, outcome):
        self.visits += 1
        if outcome == 0: self.draws += 1
        if outcome == 1: self.wins += 1
        if outcome == 2: self.losses += 1

        self.ratio = self.wins / self.visits
        self.winProb = self.wins / max((self.wins + self.losses),1)


class gameBoard():

    def __init__(self, advancedTrain=False):
        self.columns = [0,1,2,3,4,5,6]
        self.gameBoard = np.zeros((6,7))
        self.boardStates = {}
        self.advancedTrain = advancedTrain
        self.human = False
        self.exploring = False
        self.visualize = False
        self.exploitativeSampling = False

    def initializeGameState(self, iters, filename, previousPolicy=False):
        self.clockManager = clockManager(filename)
        if self.human or self.testPhase or self.visualize: # Load the policy for the Computer
            with open(f'{filename}.pkl', 'rb') as file:
                self.boardStates = pickle.load(file)

        if self.advancedTrain: # Use previous policy for opponent in training to develop more advanced policy
            try:
                with open(f'{previousPolicy}.pickle', 'rb') as file:
                    self.boardStates = pickle.load(file)
            except Exception as e:
                print("Starting From Scratch")

        self.filename = filename
        self.iters = iters
        self.wins = 0
        self.loss = 0
        self.draw = 0

        self.winsTest = 0
        self.lossTest = 0
        self.drawTest = 0

        self.policyTimer = self.clockManager.makeTimer('Policy Timer')
        self.winCheckTimer = self.clockManager.makeTimer('Win Check Timer')
        self.updateTimer = self.clockManager.makeTimer('Board Update Timer')

    # 
    def humanPlay(self, filename):
        self.testPhase=False
        self.human = True
        self.initializeGameState(0, filename)
        while self.human:
            self.newGame()

    # Gives readouts for the decision process4
    def visualizePerformance(self, filename, previousPolicy=False):
        self.testPhase = False
        self.visualize = True
        self.initializeGameState(0, filename, previousPolicy)
        self.newGame()

    # Test out the policy algorithm without exploration for testing
    def testPerformance(self, iters, filename, previousPolicy=False):
        self.testPhase = True
        self.initializeGameState(iters, filename, previousPolicy)
        for i in tqdm(range(iters)): # Runs the training loop and tests appropriately
            self.count = i
            self.newGame()

        self.conclude()


    # Explore using UTC algorithm
    def explore(self, iters, filename, previousPolicy=False, exploitativeSampling=False):
        self.exploring = True
        self.testPhase = False
        self.exploitativeSampling = exploitativeSampling
        self.initializeGameState(iters, filename, previousPolicy)

        self.winsSample = 0
        self.lossSample = 0
        self.drawSample = 0

        self.sampling = False
        self.testPhase = False
        self.samplePerformance = []

        for i in tqdm(range(iters)): # Runs the training loop and tests appropriately
            self.count = i
            self.samplingLoop()
            if i == iters - int(iters/20):
                self.testPhase = True
            self.newGame()

        self.conclude()
        

    # Initialize game variables
    def newGame(self):

        self.moveIters = 0 
        self.gameBoard = np.zeros((6,7))
        self.boardMap = [[],[],[],[],[],[],[]]
        self.gameState = [] # Tracks all columns moves, i.e. [*,*,*,*,*,*,*]
        self.winner = False
        self.onPolicyAction = True # Tracks when the learner is still on policy
        self.newLeaf = False
        self.secondLeaf = False
        self.leafDepth =False   # Tracks the depth of the leaf from this run so the correct number of game states are updated 
        self.choice = False
        self.gamePlay()


    # Play out one game 
    def gamePlay(self):

        if self.human:
            print("ZEROS are Empty, TWO is YOU, ONE is the COMPUTER")
            time.sleep(1)
            self.humanTurn(True)
        else:
            self.randomTurn(2)

        while not self.winner:
            if self.human:
                print(f'{self.renderGameboard()}\n')
                time.sleep(2)

            self.onPolicy(1) # Choose and execute agent's move

            if self.winner: break

            if self.human:  # 
                self.humanTurn()
                if self.winner: print("You Win!")

            elif self.advancedTrain: # Use previous policy for training opponent
                self.onPolicy(2)

            else:
                self.randomTurn(2) # Choose and execute computer's move


    # Make a choice that maximizes the value of the next option
    def onPolicy(self, player):
        self.policyTimer.start()
        actionScores = []
        gameStates = []
        
        if self.visualize:
            time.sleep(3)
            print(self.renderGameboard())

        # Calculate the UCT value for any child nodes
        if self.onPolicyAction and f'{self.boardMap}' in self.boardStates:

            for i in range(7): # Create child nodes and search for the in the Monte Carlo Tree
                node = copy.deepcopy(self.boardMap.copy())
                nodeActions = copy.deepcopy(self.gameState.copy())
                if len(node[i]) == 0:
                    node[i] = [player]
                else:
                    node[i].append(player)
                nodeActions.append(i)

                # Check if childrens node have been visited before
                if f'{node}' in self.boardStates:
                    if player == 1:
                        ratio = self.boardStates[f'{node}'].ratio
                    else:
                        ratio = 1 - self.boardStates[f'{node}'].ratio

                    exploration = np.sqrt(2) * np.sqrt(np.log(self.boardStates[f'{self.boardMap}'].visits) / self.boardStates[f'{node}'].visits)

                    # Only add the exploration term during training
                    actionScore = ratio if self.testPhase or self.human or (self.exploitativeSampling and self.sampling) or self.visualize else ratio + exploration
                    actionScores.append(actionScore)

                elif self.testPhase or len(node[i]) > 6 or self.human or self.visualize or (self.exploitativeSampling and self.sampling):
                    actionScores.append(0)  # Don't explore infeasible moves, or while either testing or playing a human
                else:
                    actionScores.append(99999)  # Greedy Optimism for unvisited nodes

                gameStates.append(nodeActions)

        # Random Rollout if no children
        if len(actionScores) == 0 or all(score == 99999 for score in actionScores) or all(score == 0 for score in actionScores):
            if self.visualize:
                print('Off Policy')
            self.onPolicyAction = False
            self.randomTurn(player)
            return
        
        if self.visualize:
            print(f'Win Probabilities for the next set of moves are: {actionScores}, selecting highest {max(actionScores)}')
        
        if max(actionScores) == 9999:
            self.onPolicyAction = False

        choice = gameStates[actionScores.index(max(actionScores))][-1]
        self.choice = choice
        self.policyTimer.stop()
        self.completeMove(choice, player)


    # Run a sample of the algorithm's performance ten times during the training
    def samplingLoop(self):
        if any(self.count%(int(self.iters/100)) == x for x in range(int(self.iters/10000))) and self.count/(int(self.iters/100)) > 1:
            self.sampling = True
        else:
            self.sampling = False
        if self.count%(int(self.iters/100)) == int(self.iters/10000)+1 and self.count/(self.iters/100) > 1:
            self.sampleSummary()

    # Summarize and store last sampling run
    def sampleSummary(self):
        winRate = self.winsSample/int(self.iters/10000)
        print(f'{int(self.iters/10000)} samples with Win Rate: {winRate}')
        self.samplePerformance.append(winRate)
        self.winsSample = 0
        self.lossSample = 0
        self.drawSample = 0

    # Log the node being visited
    def makeLog(self):
        if len(self.gameState)%2 == 0:
            self.boardMap[self.gameState[-1]].append(1)
        else:
            self.boardMap[self.gameState[-1]].append(2)

        # Store a dictionary entry for the correct depths of decision tree
        if not self.newLeaf:
            self.leafDepth = self.moveIters
            self.map()
        elif self.moveIters == (self.leafDepth+1): # Additional entry for the opponent's move
            self.map()
            self.secondLeaf = True

        self.moveIters += 1

    # Map the actions to a specific board state shared by some other combinations of the same length
    def map(self):
        if f'{self.boardMap}' not in self.boardStates.keys():
            self.newLeaf = True
            self.boardStates[f'{self.boardMap}'] = boardState()
    

    # Carry out updates and check for a winner after a move
    def completeMove(self, choice, player):
        row = self.checkCol(choice)
        self.gameState.append(choice)
        self.gameBoard[row, choice] = player
        self.makeLog()
        self.winCheck([row, choice], player)
        self.drawCheck()

    # Takes the game state and changes player's moves to red and blue characters
    def renderGameboard(self, winner=False):
        gameBoard = str(self.gameBoard)
        stringList = [char for char in gameBoard]
        stringList2 = []

        for item in stringList: # Takes the gameboard and adds color for player's moves
            if item == str(1):
                item = Style.BRIGHT+Fore.RED+'1'+Style.RESET_ALL
            elif item == str(2):
                item = Style.BRIGHT+Fore.BLUE+'2'+Style.RESET_ALL
            elif winner == 2 and item == str(0): # Animation to clarify win
                item = Fore.GREEN+'2'+Style.RESET_ALL
            elif winner == 1 and item == str(0): # Animation to clarify loss
                item = Fore.YELLOW+'1'+Style.RESET_ALL
            stringList2.append(item)

        newString = ''.join(stringList2)
        return newString
    

    # Person vs. AI play
    def humanTurn(self, first=False):
        if first:
            print(f'\n{self.renderGameboard()}\n')
            choice = input("What will you do?")
        else:
            print(f'{self.renderGameboard()}\n')
            choice = input("What will you do next?")

        try:
            choice = int(choice)
        except Exception:
            choice = input("Try Again")
            choice = int(choice)

        while self.gameBoard[0, choice-1] != 0:
            choice = int(input("The last one was full, What will you do next?"))

        self.completeMove(choice-1, 2)

    # Computer Player selects Random action
    def randomTurn(self, player):
        # Choose the move and corresponding position
        index = np.random.randint(0,7)
        while self.gameBoard[0, index] != 0:
            index = np.random.randint(0,7)
        self.completeMove(index, player)


    # Update the game's outcome for previous states
    def updateBoards(self, ending):
            self.updateTimer.start()
            temporaryMap = [[],[],[],[],[],[],[]]
            if self.secondLeaf:
                depth = self.leafDepth + 1
            elif self.newLeaf:
                depth = self.leafDepth
            else:
                depth = self.moveIters

            for i in range(depth):
                if i >= len(self.gameState):
                    continue

                if i%2 == 0:
                    temporaryMap[self.gameState[i]].append(2)
                else:
                    temporaryMap[self.gameState[i]].append(1)

                # Record the result for each visited state object
                if ending == 0:
                    self.boardStates[f'{temporaryMap}'].update(0)
                elif ending == 1:
                    self.boardStates[f'{temporaryMap}'].update(1)
                elif ending == 2:
                    self.boardStates[f'{temporaryMap}'].update(2)

            self.updateTimer.stop()


    # Find the first open space in the selected column or return False if it is full
    def checkCol(self, index):
        if self.gameBoard[0,int(index)] == 0:
            placed = False
            row = 5
            while not placed:
                if self.gameBoard[int(row), int(index)] == 0:
                    return row
                row -= 1
        else:
            return False

    # Make sure there are still spaces left and end the game if necessary
    def drawCheck(self):
        if all(x != 0 for x in self.gameBoard[0,:]):
            self.winner = True
            self.draw += 1
            if self.testPhase:
                self.drawTest += 1
            if self.exploring:
                if self.sampling:
                    self.drawSample += 1
            self.updateBoards(0)

    # Check if the last move caused 4 in a row
    def winCheck(self, lastPlay, player):
        self.winCheckTimer.start()
        gb = self.gameBoard
        row = lastPlay[0]
        col = lastPlay[1]

        # Four potentially winning segments of four include the new move per angle
        for i in range(4):

            # Horizontal Check
            if col - i >= 0 and col - i + 3 <= 6:
                if gb[row,(col-i)] == gb[row,(col-i+1)] == gb[row,(col-i+2)] == gb[row,(col-i+3)]:
                    self.winCleric(player)
                    self.winCheckTimer.stop()
                    return

            # Vertical Check
            if row - i >= 0 and row - i + 3 <= 5:
                if gb[(row-i),col] == gb[(row-i+1),col] == gb[(row-i+2),col] == gb[(row-i+3),col]:
                    self.winCleric(player)
                    self.winCheckTimer.stop()
                    return

            # Diagonally Down
            if row - i >= 0 and col - i >= 0 and row - i + 3 <= 5 and col - i + 3 <= 6:
                if gb[(row-i),(col-i)] == gb[(row-i+1),(col-i+1)] == gb[(row-i+2),(col-i+2)] == gb[(row-i+3),(col-i+3)]:
                    self.winCleric(player)
                    self.winCheckTimer.stop()
                    return
            
            # Diagonally Up
            if row + i <= 5 and col - i >= 0 and row + i - 3 >= 0 and col - i + 3 <= 6:
                if gb[(row+i),(col-i)] == gb[(row+i-1),(col-i+1)] == gb[(row+i-2),(col-i+2)] == gb[(row+i-3),(col-i+3)]:
                    self.winCleric(player)
                    self.winCheckTimer.stop()
                    return


    # Make appropriate updates after a winner       
    def winCleric(self, player):
        # Propagate the reward through all previous states
        if player == 2:
            self.makeLog()            
        self.updateBoards(player)

        # Tally appropriate end-game stats
        self.wins += player == 1
        self.loss += player != 1

        if self.exploring:
            if self.testPhase:
                self.winsTest += player == 1
                self.lossTest += player != 1
            if self.sampling:
                self.winsSample += player == 1
                self.lossSample += player != 1

        self.winner = True  
        if self.human or self.visualize: print(f'\n{self.renderGameboard(player)} \n')     
        

    # Gather statistics about performance and computation time to save
    def conclude(self):
        print(f'Win percentage: {np.round((self.wins/self.iters),3)}')
        print(f'Loss percentage: {np.round((self.loss/self.iters),3)}')
        print(f'Draw percentage: {np.round((self.draw/self.iters),3)}')

        print(f'Test Win percentage: {np.round((self.winsTest/int(self.iters/20)),3)}')
        print(f'Test Loss percentage: {np.round((self.lossTest/int(self.iters/20)),3)}')
        print(f'Test Draw percentage: {np.round((self.drawTest/int(self.iters/20)),3)}')

        if self.exploring:
            print(f'Sampling Loop Summary: {np.round((self.samplePerformance),3)}')

        if not self.human:
            with open(f'{self.filename}.pkl', 'wb') as handle:
                pickle.dump(self.boardStates, handle, protocol=pickle.HIGHEST_PROTOCOL)

            if self.exploring:
                np.savetxt(f'{self.filename}_samples.csv', np.array(self.samplePerformance))

        self.clockManager.tallyCompare()

###################################################################################################

if __name__ == '__main__':
    # Train the agent against a random computer
    connectFour = gameBoard()
    connectFour.explore(10000000, 'Test_(10M)', previousPolicy=False, exploitativeSampling=True)

    connectFour.visualizePerformance('Test_(10M)')

    # Train two agents acting on their own policies against each other
    connectFourAdvanced = gameBoard(advancedTrain=True)
    connectFourAdvanced.explore(10000000, 'Test_(10M)_Advanced')

    connectFourAdvanced.visualizePerformance('Test_(10M)_Advanced')

    # Test against a person
    connectFourAdvanced.humanPlay('Test_Advanced_(10M)')
