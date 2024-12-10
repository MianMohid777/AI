import heapq


class StateNode:
    def __init__(self, data, depth, fValue):
        self.data = data
        self.depth = depth
        self.fValue = fValue

    def __lt__(self, other):
        return self.fValue < other.fValue

    def __eq__(self, other):
        return tuple(map(tuple, self.data)) == tuple(map(tuple, other.data))

    def __hash__(self):
        return hash(tuple(map(tuple, self.data)))

    def successorStates(self):
        x, y = self.findEmptySpace()
        possibleMoves = [[x, y - 1], [x, y + 1], [x + 1, y], [x - 1, y]]
        successors = []

        for move in possibleMoves:
            if self.isValidMove(move):
                childState = self.copyState()
                self.swap(childState, x, y, move[0], move[1])
                successorNode = StateNode(childState, self.depth + 1, 0)
                successors.append(successorNode)
        return successors

    def copyState(self):
        return [row.copy() for row in self.data]

    def findEmptySpace(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.data[i][j] == 0:
                    return i, j
        return None

    def isValidMove(self, move):
        x, y = move
        return 0 <= x < len(self.data) and 0 <= y < len(self.data[0])

    def swap(self, state, x1, y1, x2, y2):
        state[x1][y1], state[x2][y2] = state[x2][y2], state[x1][y1]
        return state


class Puzzle:

    # Constructor for Class Level Attributes
    def __init__(self):
        self.size = 0
        self.moves = 0
        self.initialState = []
        self.goalState = []

    # Method to populate state arrays
    def populateState(self, stateArray, rows):
        for i in range(len(rows)):
            print(rows[i])
            cols = rows[i].split(",")
            initArr = []
            for j in range(self.size):
                initArr.append(int(cols[j]))
            stateArray.append(initArr)  # Add the row to the state array

    # Method to read file
    def readFile(self, fileName):
        with open(fileName, "r") as file:
            lineCount = 1
            for line in file:
                if len(line.strip()) > 0:  # Skip empty lines
                    parseLine = (line.split("=")[1].strip())
                    if lineCount == 1:
                        self.size = int(parseLine)  # Set size
                    elif lineCount == 2:
                        self.moves = int(parseLine)  # Set moves
                    elif lineCount == 3:
                        rows = parseLine.split(" ")
                        self.populateState(self.initialState, rows)  # Populate initialState
                        print("Initial State:", self.initialState)
                    elif lineCount == 4:
                        rows = parseLine.split(" ")
                        self.populateState(self.goalState, rows)  # Populate goalState
                        print("Goal State:", self.goalState)

                    lineCount += 1  # Line Count Track

    def findPositions(self, value):
        for i in range(self.size):
            for j in range(self.size):
                if self.goalState[i][j] == value:
                    return i, j
        return None

    def calculate_Manhattan_Heuristic(self, start):
        h = 0
        for i in range(self.size):
            for j in range(self.size):
                if start[i][j] != 0 and start[i][j] != self.goalState[i][j]:
                    goalX, goalY = self.findPositions(start[i][j])
                    h += abs(goalX - i) + abs(goalY - j)  # Using Manhattan Distance to Calc Heuristics
        return h

    def calculateMisplaced_Heuristic(self, start):
        h = 0
        for i in range(self.size):
            for j in range(self.size):
                if start[i][j] != 0 and start[i][j] != self.goalState[i][j]:
                    h += 1  # Using Misplaced Tiles to Calc Heuristics
        return h

    def calculateFValue(self, stateNode, heuristic):
        if heuristic == "Manhattan":
            return stateNode.depth + self.calculate_Manhattan_Heuristic(stateNode.data)  # f(n) = g(n) + h(n)
        elif heuristic == "Misplaced":
            return stateNode.depth + self.calculateMisplaced_Heuristic(stateNode.data)
        else:
            return None

    def printState(self, state):
        print("\n")
        for i in range(self.size):
            for j in range(self.size):
                print(f" {state[i][j]} ", end="")
            print()

    def solvePuzzle(self, fileName):
        self.readFile(fileName)  # Loading Data from File

        startNode = StateNode(self.initialState, 0, 0)  # Start Node Initialization
        startNode.fValue = self.calculate_Manhattan_Heuristic(startNode.data)

        openList = []
        heapq.heappush(openList, startNode)  # Priority Queue Initialization with Start Node and Open-List Set

        movesLeft = self.moves
        visited = set()  # Set to store visited states for redundancy check

        while openList:

            if movesLeft == 0:
                print("All Moves have been utilized but Goal State couldn't be reached")
                return

            minNode = heapq.heappop(openList)  # Get Min F-Value State Node
            self.printState(minNode.data)
            print(f"\n H = {minNode.fValue} \n Moves Left = {movesLeft}")

            # Convert current state to a hashable tuple for comparison
            current_state_tuple = tuple(map(tuple, minNode.data))

            # Check if goal state is reached
            if current_state_tuple == tuple(map(tuple, self.goalState)):
                print(f"\n Goal State Reached using {minNode.depth} moves")
                return

            movesLeft -= 1

            # Add current state to visited
            visited.add(current_state_tuple)

            for child in minNode.successorStates():
                # Convert child state to hashable tuple
                child_state_tuple = tuple(map(tuple, child.data))

                # Check if state has not been visited before
                if child_state_tuple not in visited:
                    child.fValue = self.calculateFValue(child, "Manhattan")
                    heapq.heappush(openList, child)

                # Calculate f-value
                child.fValue = child.depth + self.calculate_Manhattan_Heuristic(child.data)

                # Add to open set if not already present or with better f-value
                if child not in openList:
                    heapq.heappush(openList, child)


puzzle = Puzzle()
puzzle.solvePuzzle("input3.txt")  # Calling Puzzle Solver
