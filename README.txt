# Ares's Adventure

This project is a Python-based Sokoban game using Pygame, featuring AI pathfinding algorithms including Depth First Search (DFS), Breadth First Search (BFS), Uniform Cost Search (UCS), and A*. The game allows players to select levels and algorithms, providing an interactive way to explore and visualize different pathfinding techniques in action.

## SOKOBAN INTRODUCTION

Sokoban is a classic puzzle video game where the player pushes crates or stones around a warehouse, with the goal of placing them in designated goal locations. The game is played on a grid of squares, where each square can either be a floor or a wall. Some floor squares contain stones, and others are marked as goal locations.

The player can move horizontally or vertically onto empty squares but cannot move through walls or stones. To move a box, the player must walk up to it and push it into the adjacent empty square. stones cannot be pulled, nor can they be pushed into squares with walls or other stones. The puzzle is solved when all stones are successfully placed at their corresponding goal locations.

## Team members

Lê Công Quốc Hân - Đào Bá Thành - Phạm Ngọc Phương Uyên - Huỳnh Phan Nhật Vy

## System Requirements:
-   Python 3.x
-   Libraries specified in `requirements.txt`


## Features

-  Interactive GUI built with Pygame
-  AI Pathfinding Algorithms:
   -  Depth First Search (DFS)
   -  Breadth First Search (BFS)
   -  Uniform Cost Search (UCS)
   -  A* Search (A*)
-  Level selection and algorithm choice for solving levels
-  Console-based testing for unit validation

## Installation

Install Dependencies

```sh
$ pip install -r requirements.txt
```

### Run game

#### Step 1: Launching the game

Run the command below

```sh
$ python main.py
```

Upon starting, you’ll see a main menu where you can choose:

-  DFS explores as far as possible along each branch before backtracking.
-  BFS ensures the shortest solution in terms of moves but can be slower.
-  UCS optimizes the total cost of moves.
-  A* uses heuristics to find an efficient path.

#### Step 2: Selecting a level  

_Choose a level between 1 and 12._

#### Step 3: Start the game

Press Enter to begin solving the level with the chosen algorithm. Observe the AI as it calculates the path to solve the puzzle.

While the program is solving the puzzle (which may take approximately 1 to 3 minutes), you can cancel the process at any time by pressing the Return on the top left of the game screen.

Once the puzzle is solved, the game will view the completed result.