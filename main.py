import copy
import heapq

class Node: 
    def __init__(self, data, depth, fValue):
        self.data = data
        self.depth = depth
        self.fValue = fValue

    def __lt__(self, other):
        return self.fValue < other.fValue
    
    def find(self, puzzle, empty_space):
        """Find the empty space"""
        temp = []
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puzzle[i][j] == empty_space:
                    return i, j
                
    def copy(self, puzzle):
        # temp = []
        # for i in puzzle:
        #     x = []
        #     for j in i:
        #         x.append(j)
        #     temp.append(x)
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
        pos_list = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]
        children = []
        for i in pos_list:
            child = self.move_empty(self.data, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.depth + 1, 0)
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
    
    def f_func(self, start_node, goal_node):
        return self.h_func(start_node.data, goal_node) + start_node.depth
    
    def h_func(self, start, goal):
        """Calculates difference between puzzles"""
        temp = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if start[i][j] != goal[i][j] and start[i][j] != 0: # Then a tile is missplaced
                    temp += 1
        return temp
    
    def solve(self):
        print("Enter a start state matrix (empty space: 0): ")
        start_state = self.read_input()
        print("Enter a goal state matrix (empty space: 0): ")
        goal_state = self.read_input()

        start = Node(start_state, 0, 0)
        start.fValue = self.f_func(start, goal_state)
        heapq.heappush(self.open, start)
        print("\n\n")
        
        while True:
            current = heapq.heappop(self.open)
            print("")
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            for i in current.data:
                for j in i: 
                    print(j, end=" ")
                print("")
            if self.h_func(current.data, goal_state) == 0:
                break
            for i in current.generate_child():
                i.fValue = self.f_func(i, goal_state)
                heapq.heappush(self.open, i)
            self.closed.add(current)
        # print("Enter a start state matrix (empty space: 0): ")
        # start_state = self.read_input()
        # print("Enter a goal state matrix (empty space: 0): ")
        # goal_state = self.read_input()

        # start = Node(start_state, 0, 0)
        # start.fValue = self.f_func(start, goal_state)
        # self.open.append(start)
        # print("\n\n")
        
        # while True:
        #     current = self.open[0]
        #     print("")
        #     print("  | ")
        #     print("  | ")
        #     print(" \\\'/ \n")
        #     for i in current.data:
        #         for j in i: 
        #             print(j, end=" ")
        #         print("")
        #     if self.h_func(current.data, goal_state) == 0:
        #         break
        #     for i in current.generate_child():
        #         i.fValue = self.f_func(i, goal_state)
        #         self.open.append(i)
        #     self.closed.add(current)
        #     del self.open[0]

        #     self.open.sort(key=lambda x:x.fValue, reverse=False)

puz = Puzzle(3)
puz.solve()