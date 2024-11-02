import os

def readFile(path):
    with open(path, "r") as file:
        lines = file.readlines()
        
    weights = list(map(int, lines[0].split()))
    matrix = [list(lines[x].rstrip('\n')) for x in range(1, len(lines))]
    
    return weights, matrix

def writeFile(filePath, algoType, path, cost, time, memoryUsed, cntNode):
    with open(filePath, "w") as file:
        file.write(f"{algoType}")
        file.write(f"\nSteps: {len(path)}, Weight: {cost}, Node: {cntNode}, Time (ms): {(time * 1000):.2f}, Memory (MB): {memoryUsed:.2f}")
        file.write(f"\n{path}")