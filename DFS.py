import copy
from collections import deque
from classes import Node, directions
import time, psutil, os

def dfs(originalBoard, originalPlayer, originalGoals):
    board = copy.deepcopy(originalBoard)
    goals = copy.deepcopy(originalGoals)
    player = originalPlayer
    
    startTime = time.time()
    visited = set()
    startNode = Node(board, player, goals, "", 0)
    stack = deque()

    stack.append(startNode)
    visited.add(startNode.ID)
    
    cntNode = 1
    # print(board)
    
    while stack:
        currentTime = time.time()
        
        if (currentTime - startTime > 120): return "-1", -1, -1, -1, -1
        node = stack.pop()
        
        if (node.isGoalState()): break
        if (node.isDeadlocked()): continue
        
        for dir in directions:
            if (node.canMove(dir)):
                newNode = node.move(dir)
                if (newNode.ID not in visited):
                    stack.append(newNode)
                    cntNode += 1
                    visited.add(newNode.ID)
    
    path = node.path
    # print("\nResult path: ", path)
    
    # print("\nTotal Cost: ", node.cost)
    
    endTime = time.time()
    elapsedTime = endTime - startTime
    # print("\nTime in seconds: ", elapsedTime)
    
    memUsed = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
    # print("\nMemory usage in MB: ", memUsed)
    
    return path, node.cost, elapsedTime, memUsed, cntNode