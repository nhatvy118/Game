import os
from inOut import readFile, writeFile
from classes import Pair, Cell

from UCS import uniformCostSearch
from AStar import AStarAlgorithm
from BFS import bfs
from DFS import dfs

import pygame

def getKey(character):
    if (character == 'U'): return pygame.K_UP
    elif (character == 'D'): return pygame.K_DOWN
    elif (character == 'L'): return pygame.K_LEFT
    else: return pygame.K_RIGHT

def dataProcessing(weights, matrix):
    stones = []
    goals = list()
    board = []
    index = 0
    player = Pair(0, 0)
    
    for i in range(len(matrix)):
        board.append([])
        
        for j in range(len(matrix[i])):
            board[i].append(Cell(matrix[i][j], 0))
            
            if matrix[i][j] == '$':
                stones.append({"weight": weights[index], "position": Pair(i, j)})
                board[i][j].weight = weights[index]
                index += 1
            
            elif matrix[i][j] == '@':
                player = Pair(i, j)
                board[i][j].type = ' '
                
            elif matrix[i][j] == '.':
                goals.append(Pair(i, j))
                board[i][j].type = ' '
                
            elif matrix[i][j] == '*':
                stones.append({"weight": weights[index], "position": Pair(i, j)})
                board[i][j].type = '$'
                board[i][j].weight = weights[index]
                index += 1
                goals.append(Pair(i, j))
                
            elif matrix[i][j] == '+': 
                board[i][j].type =  ' '
                goals.append(Pair(i, j))
                player = Pair(i, j)
                
    return stones, player, goals, board

def process(inputPath: str, algoType: int, level: int):
    weights, matrix = readFile(inputPath)
    
    levelStr = str(level)
    if (level < 10): levelStr = '0' + levelStr

    stones, player, goals, board = dataProcessing(weights, matrix)
    algo = ""

    if (algoType == 0): 
        path, cost, time, memoryUsed, cntNode = AStarAlgorithm(board, player, goals)
        algo = "A*"
    elif (algoType == 1): 
        path, cost, time, memoryUsed, cntNode = bfs(board, player, goals)
        algo = "BFS"
    elif (algoType == 2): 
        path, cost, time, memoryUsed, cntNode = dfs(board, player, goals)
        algo = "DFS"
    else: 
        path, cost, time, memoryUsed, cntNode = uniformCostSearch(board, player, goals)
        algo = "UCS"
    
    writeFile(f"output-{levelStr}.txt", algo, path, cost, time, memoryUsed, cntNode)
    return True, path.upper()