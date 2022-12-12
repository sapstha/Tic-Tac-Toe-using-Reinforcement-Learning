import numpy as np
import pickle

# Initialize the number of rows and columns
NUMBER_OF_COLUMNS = 3
NUMBER_OF_ROWS = 3

class Player:

    # Default constructor
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.exp_rate = exp_rate
        # List to record all the positions taken
        self.states = []
        self.decay_gamma = 0.9
        self.lr = 0.2
        self.states_value = {}  # dict to map state to value

    # Method to decide which action to take further
    def decideAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # Choose a random action , random index
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            # Iterate over all possible positions
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                if value >= value_max:
                    value_max = value
                    action = p
        return action

    # Function to get the hash value of board
    def getHash(self, board):
        boardHash = str(board.reshape(NUMBER_OF_COLUMNS * NUMBER_OF_ROWS))
        return boardHash

    # Function to reset states
    def reset(self):
        self.states = []

    # Function to provide reward to the model
    # As the game ends, backpropagate and update state value
    def feedReward(self, reward):
        # Reverse iterate over states
        for st in reversed(self.states):
            # If state is null
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            # Calculate state value
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    # Append a hash state to state
    def addState(self, state):
        self.states.append(state)

    # Function to load Policy for the Player, as a Pickle file
    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()

    # Function to save Policy for the Player, as a Pickle file
    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

# Class for Human Player
class HumanPlayer:

    # Default constructor
    def __init__(self, name):
        self.name = name

    # Method to choose which action to take further
    def decideAction(self, positions):
        while True:
            row = int(input("Input your action row:"))
            col = int(input("Input your action col:"))
            action = (row, col)
            if action in positions:
                return action

    # Method to reset the states
    def reset(self):
        pass # Method does not validate for human beings

    # As the game ends, backpropagate and update state value
    def feedReward(self, reward):
        pass # Method does not validate for human beings

    # Append the state
    def addState(self, state):
        pass # Method does not validate for human beings

# Class for State
class State:

    # Default constructor
    def __init__(self, p1, p2):
        self.board = np.zeros((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS))
        self.p1 = p1
        self.p2 = p2
        self.playerSymbol = 1
        self.boardHash = None
        self.isEnd = False

    # Function to get the hash value of board
    def getHash(self):
        self.boardHash = str(self.board.reshape(NUMBER_OF_COLUMNS * NUMBER_OF_ROWS))
        return self.boardHash

    # Check and return available positions
    def availablePositions(self):
        positions = []
        for i in range(NUMBER_OF_ROWS):
            for j in range(NUMBER_OF_COLUMNS):
                if self.board[i, j] == 0:
                    positions.append((i, j))  # need to be tuple
        return positions

    # Declare winner
    def winner(self):
        # Scan rows for winner
        for i in range(NUMBER_OF_ROWS):
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1
        # Scan cols for winner
        for i in range(NUMBER_OF_COLUMNS):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
        # Scan diagonals for winner
        diag_sum1 = sum([self.board[i, i] for i in range(NUMBER_OF_COLUMNS)])
        diag_sum2 = sum([self.board[i, NUMBER_OF_COLUMNS - i - 1] for i in range(NUMBER_OF_COLUMNS)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        # If diagonal is occupied by same player
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1
        # Condition for Game Tie
        # No more available positions left
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        # Game has not yet ended
        self.isEnd = False
        return None

    # Function to reset the board
    def reset(self):
        self.board = np.zeros((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    # Give reward at the end of the game
    def giveReward(self):
        # Get winner
        result = self.winner()
        # Backpropagate Reward
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)

    # Function to update the state
    def updateState(self, position):
        # Lock position for player
        self.board[position] = self.playerSymbol
        # Switch turns between players
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    # Function to play a game
    def play(self, rounds=100):
        # Iterate over those number of rounds
        for i in range(rounds):
            if i % 1000 == 0:
                print("Rounds {}".format(i))
            # Play until end state is not yet achieved
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.decideAction(positions, self.board, self.playerSymbol)
                # Decide an action and upate the board state
                self.updateState(p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)

                # Check the current board status if it is end
                win = self.winner()
                if win is not None:
                    # Ended with p1 either win or draw
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
                else:
                    # Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.decideAction(positions, self.board, self.playerSymbol)
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)

                    win = self.winner()
                    if win is not None:
                        # ended with p2 either win or draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    # Play against human
    def play2(self):
        while not self.isEnd:
            # Player 1's turn
            positions = self.availablePositions()
            p1_action = self.p1.decideAction(positions, self.board, self.playerSymbol)
            # Decide an action and upate the board state
            self.updateState(p1_action)
            self.showBoard()

            # Check the current board status if it is end
            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                # Player 2
                positions = self.availablePositions()
                p2_action = self.p2.decideAction(positions)

                self.updateState(p2_action)
                self.showBoard()
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break

    # Function to display the current board status
    def showBoard(self):
        # p1: x  p2: o
        for i in range(0, NUMBER_OF_ROWS):
            print('-------------')
            out = '| '
            for j in range(0, NUMBER_OF_COLUMNS):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')





if __name__ == "__main__":
    # Training phase
    p1 = Player("p1")
    p2 = Player("p2")

    st = State(p1, p2)
    print("training...")
    # Train the model using 50000 random games
    st.play(5000)

    # Play against human
    p1 = Player("computer", exp_rate=0)
    p1.loadPolicy("policy_p1")

    p2 = HumanPlayer("human")

    st = State(p1, p2)
    st.play2()