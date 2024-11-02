import copy

class Pair:
    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        if isinstance(other, Pair):
            return (self.x == other.x and self.y == other.y)
        return False
        
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

directions = [{"name": 'D', "value": Pair(1, 0)}, 
            {"name": 'U', "value": Pair(-1, 0)}, 
            {"name": 'R', "value": Pair(0, 1)}, 
            {"name": 'L', "value": Pair(0, -1)}]
    
class Cell:
    def __init__(self, type, weight):
        self.type = type
        self.weight = weight
    
    def __str__(self):
        return f"({self.type}, {self.weight})"
    
    def __repr__(self):
        return f"({self.type}, {self.weight})"
    
class Node:
    def __init__(self, board, player: Pair, goals: list, path: str, cost: int):
        self.board = board
        self.goals = goals
        self.player = player
        self.path = path
        self.cost = cost
        self.heuristicCost = 0
        
        self.ID = str(player.x) + "P" + str(player.y)
        
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c].type == '$':
                    self.ID += "/" + str(r) + "{" + str(self.board[r][c].weight) + "}" + str(c)    
    
    def __lt__(self, other):
        if isinstance(other, Node):
            return self.cost + self.heuristicCost < other.cost + other.heuristicCost
        return NotImplemented
        
    def isGoalState(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c].type == '$':
                    if (Pair(r, c) in self.goals) == False:
                        return False
        return True
    
    def isDeadlocked(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c].type == '$':
                    
                    if (Pair(r, c) in self.goals): 
                        continue
                        
                    blocked = 0
                    for dir in directions:
                        r1 = r + dir["value"].x
                        c1 = c + dir["value"].y
                        
                        if (self.board[r1][c1].type == '#'): blocked += 1
                    
                    if (blocked >= 2): return True
        
        return False
                    
        
    def isPosValid(self, pos: Pair):
        if (pos.x < 0 or pos.x >= len(self.board)): return False
        if (pos.y < 0 or pos.y >= len(self.board[pos.x])): return False
        if (self.board[pos.x][pos.y].type == '#'): return False
        
        return True
        
    def canMove(self, direction):
        nextPos = Pair(self.player.x + direction["value"].x, self.player.y + direction["value"].y)
        if (self.isPosValid(nextPos) == False): return False
        
        # Case 1: Free cell movement
        if (self.board[nextPos.x][nextPos.y].type != '$'):
            return True
        
        # Case 2: Pushing stone
        else:
            secondNextPos = Pair(nextPos.x + direction["value"].x, nextPos.y + direction["value"].y)
            
            # 2.1: stone next to wall
            if (self.isPosValid(secondNextPos) == False): return False
            
            # 2.2: double stones
            if (self.board[secondNextPos.x][secondNextPos.y].type == '$'): return False
            
            # 2.3: moving stone
            return True
    
    def move(self, direction):
        nextPos = Pair(self.player.x + direction["value"].x, self.player.y + direction["value"].y)
        
        player = nextPos
        goals = self.goals
        cost = self.cost + 1 + self.board[nextPos.x][nextPos.y].weight
        
        # Case 1: Free cell movement
        if (self.board[nextPos.x][nextPos.y].type != '$'):
            board = copy.deepcopy(self.board)
            path = self.path + direction["name"].lower()
        
        # Case 2: Pushing stone
        else:
            secondNextPos = Pair(nextPos.x + direction["value"].x, nextPos.y + direction["value"].y)
            
            board = copy.deepcopy(self.board)
            board[secondNextPos.x][secondNextPos.y] = board[nextPos.x][nextPos.y]
            board[nextPos.x][nextPos.y] = Cell(' ', 0)
            path = self.path + direction["name"]
        
        return Node(board, player, goals, path, cost)
        