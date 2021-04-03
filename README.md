# Drawings and animations using Python


## Tree
Examples of randomly generated trees of depth `14`, max deviation angle `pi/8` and child branch length ratio between `[0.5, 0.8]`:

![plot](./tree/outputs/tree1.png)
![plot](./tree/outputs/tree2.png)

## Animated tree drawing
![Alt Text](./tree/outputs/tree.gif)

## Random Maze Generation
The algorithm used to generate the maze is randomized DFS. We start with a grid having walls everywhere between any two cells. We use DFS to open walls by randomly choosing a neighbour.

![Alt Text](./maze/outputs/maze.gif)

## Maze Solving
Use DFS to solve the generated maze.

![Alt Text](./maze/outputs/mazeSolve.gif)