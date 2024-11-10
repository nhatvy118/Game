import copy
import heapq
from classes import Node, directions
import time, psutil, os

def uniformCostSearch(originalBoard, originalPlayer, originalGoals):
    board = copy.deepcopy(originalBoard)
    goals = copy.deepcopy(originalGoals)
    player = originalPlayer
    
    startTime = time.time()
    visited = {}
    startNode = Node(board, player, goals, "", 0)
    pq = []
    heapq.heappush(pq, startNode)
    cnt = 0
    
    # print(board)
    
    # for r in range(len(board)):
    #     for c in range(len(board[r])):
    #         print(board[r][c].type, end='')
    #     print()
    
    cntNode = 1
    
    while pq:
        currentTime = time.time()
        if (currentTime - startTime > 180): return "-1", -1, -1, -1, -1
        
        heapq.heapify(pq)
        node = heapq.heappop(pq)
        
        if (node.isGoalState()): break
        if (node.isDeadlocked()): continue
        if (node.ID in visited and visited[node.ID] != node.cost): continue

        for dir in directions:
            if (node.canMove(dir)):
                newNode = node.move(dir)
                if (newNode.ID not in visited or newNode.cost < visited[newNode.ID]):
                    heapq.heappush(pq, newNode)
                    visited[newNode.ID] = newNode.cost
                    cntNode += 1
    
    if (node.isGoalState() == False): return "-1", -1, -1, -1, -1
    path = node.path
    # print("\nResult path: ", path)
    
    # print("\nTotal Cost: ", node.cost)
    
    endTime = time.time()
    elapsedTime = endTime - startTime
    # print("\nTime in seconds: ", elapsedTime)
    
    memUsed = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
    # print("\nMemory usage in MB: ", memUsed)
    
    return path, node.cost, elapsedTime, memUsed, cntNode
    
    