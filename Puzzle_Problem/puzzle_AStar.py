import heapq


class StateNode:

    def __init__(self, data, depth, fValue):
        self.data = data
        self.depth = depth
        self.fValue = fValue

    def __lt__(self, other):
        return self.fValue < other.fValue

    def __eq__(self, other):
        return self.data == other.data

    def __hash__(self):
        return hash(str(self.data))

    def successorStates(self):
        x, y = self.findEmptySpace()  # Find Empty Space coordinates

        possibleMoves = [[x, y - 1], [x, y + 1], [x + 1, y], [x - 1, y]]
        successors = []

        for move in possibleMoves:
            if self.isValidMove(move):
                copiedState = self.copyState()  # copying the current parent state
                childState = self.swap(copiedState, x, y, move[0], move[1])  # Swapping of Space
                successorNode = StateNode(childState, self.depth + 1, 0)
                successors.append(successorNode)
        return successors

    def copyState(self):
        copy = []

        for row in self.data:
            temp = []
            for col in row:
                temp.append(col)
            copy.append(temp)
        return copy

    def findEmptySpace(self):
        for i in range(0, len(self.data)):  # row traversal
            for j in range(0, len(self.data[0])):  # column traversal
                if self.data[i][j] == 0:
                    return i, j

    def isValidMove(self, move):
        x = move[0]
        y = move[1]
        return 0 <= x < len(self.data) and 0 <= y < len(self.data)

    def swap(self, state, x1, y1, x2, y2):
        store = state[x2][y2]
        state[x2][y2] = state[x1][y1]
        state[x1][y1] = store

        return state


class Puzzle:

    # Constructor for Class Level Attributes
    def __init__(self):
        self.size = 0
        self.moves = 0
        self.initialState = []
        self.goalState = []
        self.openList = []
        self.closedList = []

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
    def readFile(self):
        with open("input.txt", "r") as file:
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

    def findPositions(self, state, value):
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == value:
                    return i, j
        return None

    def calculateHeuristic(self, start):
        h = 0
        for i in range(self.size):
            for j in range(self.size):
                if start[i][j] != 0 and start[i][j] != self.goalState[i][j]:
                    goalX, goalY = self.findPositions(self.goalState, start[i][j])
                    h += abs(goalX - i) + abs(goalY - j)  # Using Manhattan Distance to Calc Heuristics
        return h

    def calculateFValue(self, stateNode):
        return stateNode.depth + self.calculateHeuristic(stateNode.data)  # f(n) = g(n) + h(n)

    def printState(self, state):
        print("\n")
        for i in range(self.size):
            for j in range(self.size):
                print(f" {state[i][j]} ", end="")
            print()

    def solvePuzzle(self):
        self.readFile()  # Loading Data from File

        startNode = StateNode(self.initialState, 0, 0)  # Start Node Initialization
        startNode.fValue = self.calculateFValue(startNode)

        heapq.heappush(self.openList, startNode)  # Priority Queue Initialization with Start Node

        movesLeft = self.moves
        visited = set()  # Set to store visited states for redundancy check

        while self.openList:
            if movesLeft == 0:
                print("All Moves have been utilized but Goal State couldn't be reached")
                return

            minNode = heapq.heappop(self.openList)  # Get Min F-Value State Node
            movesLeft -= 1
            self.printState(minNode.data)
            print(f"\n H = {minNode.fValue} \n Moves Left = {movesLeft}")

            if self.calculateHeuristic(minNode.data) == 0:
                print(f"\n Goal State Reached using {self.moves - movesLeft} moves")
                return

            visited.add(minNode)

            for child in minNode.successorStates():
                if child not in visited:
                    child.fValue = self.calculateFValue(child)  # Find H-Val of Child Nodes / Succeeding States
                    heapq.heappush(self.openList, child)  # Push them in PRIORITY-QUEUE

            self.closedList.append(minNode)


puzzle = Puzzle()
puzzle.solvePuzzle()
