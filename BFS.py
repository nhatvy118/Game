import copy
import queue
from classes import Node, directions
import time, psutil, os

def bfs(originalBoard, originalPlayer, originalGoals):
    board = copy.deepcopy(originalBoard)
    goals = copy.deepcopy(originalGoals)
    player = originalPlayer
    
    visited = set()
    startNode = Node(board, player, goals, "", 0)
    q = queue.Queue()

    startTime = time.time()
    if (startNode.isGoalState() == False):
        q.put(startNode)  
        visited.add(startNode.ID) 
         
    # print(board)
    
    # for r in range(len(board)):
    #     for c in range(len(board[r])):
    #         print(board[r][c].type, end='')
    #     print()
    
    cntNode = 1
    
    ok = False
    while not q.empty():
        node = q.get()
        
        if (node.isDeadlocked()): continue
        
        currentTime = time.time()
        if (currentTime - startTime > 300): return "-1", -1, -1, -1, -1
        
        # print(node.ID)
        
        # for r in range(len(node.board)):
        #     for c in range(len(node.board[r])):
        #         print(board[r][c].type, end='')
        #     print()
        
        for dir in directions:
            if (node.canMove(dir)):
                newNode = node.move(dir)
                if (newNode.ID not in visited):
                    if (newNode.isGoalState() == True):
                        node = newNode
                        ok = True
                        break
                
                    q.put(newNode)
                    cntNode += 1
                    visited.add(newNode.ID)
        
        if (ok): break
    
    path = node.path
    # print("\nResult path: ", path)
    
    # print("\nTotal Cost: ", node.cost)
    
    endTime = time.time()
    elapsedTime = endTime - startTime
    # print("\nTime in seconds: ", elapsedTime)
    
    memUsed = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
    # print("\nMemory usage in MB: ", memUsed)
    
    return path, node.cost, elapsedTime, memUsed, cntNode