import copy
import heapq
import time 
import numpy as np
class Node: 
    def __init__(self, data, depth, fValue, parent=None):
        self.data = data
        self.depth = depth
        self.fValue = fValue
        self.parent = parent

    def __lt__(self, other):
        return self.fValue < other.fValue
    
    def __eq__(self, other):
        return self.data == other.data
    
    def __hash__(self):
        return hash(tuple(map(tuple, self.data)))
    
    def find(self, puzzle, empty_space):
        """Find the empty space"""
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puzzle[i][j] == empty_space:
                    return i, j
                
    def copy(self, puzzle):
        temp = copy.deepcopy(puzzle)
        return temp
                
    def move_empty(self, puzzle, x1, y1, x2, y2):
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data): 
            temp_puzzle = []
            temp_puzzle = self.copy(puzzle)
            temp = temp_puzzle[x2][y2]
            temp_puzzle[x2][y2] = temp_puzzle[x1][y1]
            temp_puzzle[x1][y1] = temp
            return temp_puzzle
        else:
            return None

    def generate_child(self):
        x, y = self.find(self.data, "0")
        pos_list = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
        children = []
        for i in pos_list:
            child = self.move_empty(self.data, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.depth + 1, 0, self)
                children.append(child_node)

        return children

class Puzzle: 
    def __init__(self, size):
        self.size = size
        self.open = []
        self.closed = set()
    
    def read_input(self):
        puzzle = []
        for i in range(0, self.size):
            temp = input().split(" ")
            puzzle.append(temp)
        return puzzle
    
    def f_func(self, start_node, goal_node, heuristic):
        return self.h_func(start_node.data, goal_node, heuristic) + start_node.depth
    
    def h_func(self, start, goal, heuristic):
        """Calculates difference between puzzles, use h1 or h2 depending on user input"""
        if heuristic == "h1":
            # start = [[int(col) for col in row] for row in start]
            # goal = [[int(col) for col in row] for row in goal]
            temp = 0
            for i in range(0, 3):
                for j in range(0, 3):
                    if start[i][j] != goal[i][j] and start[i][j] != "0": # Then a tile is missplaced
                        temp += 1
            return temp
        elif heuristic == "h2":
            manhattan_distance = 0;
            start = [[int(col) for col in row] for row in start]
            goal = [[int(col) for col in row] for row in goal]
            for i in range(0, self.size):
                for j in range(0, self.size):
                    if start[i][j] == 0:
                        continue
                    current_row = i
                    current_col = j
                    desired_row = (start[i][j] - 1) // self.size
                    desired_col = (start[i][j] - 1) % self.size
                    manhattan_distance += abs(desired_row - current_row) + abs(desired_col - current_col)
            return manhattan_distance

    def printMoves(self, node):
        if node is None:
            print("No solution found.")
            return
        solution = []
        while node is not None:
            solution.append(node.data)
            node = node.parent
        solution.reverse()
        print("Solution:")
        for i in solution:
            print("\n  | ")
            print("  | ")
            print(" \'/ \n")
            for row in i:
                print(" ".join(str(cell) for cell in row))

    
    def solve(self):
        start_time = time.process_time()
        print("Enter a start state matrix (empty space: 0): ")
        start_state = self.read_input()
        print("Enter a goal state matrix (empty space: 0): ")
        goal_state = self.read_input()
        print("Enter a heuristic: ")
        print("Missplaced tiles: h1")
        print("Manhattan distance: h2")
        heuristic = input()

        start = Node(start_state, 0, 0)
        start.fValue = self.f_func(start, goal_state, heuristic)
        heapq.heappush(self.open, start)
        print("\n\n")

        # List for the moves to the solution
        moves = []
        
        while len(self.open) > 0:
            current = heapq.heappop(self.open)
                
            if np.array_equal(current.data, goal_state):
                elapsed_time = time.process_time() - start_time
                self.printMoves(current)
                return current.depth, elapsed_time, moves

            self.closed.add(tuple(map(tuple, current.data)))
            
            for i in current.generate_child():
                i.fValue = self.f_func(i, goal_state, heuristic)
                    
                if tuple(map(tuple, i.data)) not in self.closed:
                    heapq.heappush(self.open, i)
                    moves.append(i)

        elapsed_time = time.process_time() - start_time

        self.printMoves(current)

        return current.depth, elapsed_time, moves

puz = Puzzle(3)
cost, duration, moves = puz.solve()
print(f"\n\nSolution found in ({cost}) moves")
# print(f"\n\n ({moves}) moves")
print(f"\n\nSolution found in ({duration}) seconds")



