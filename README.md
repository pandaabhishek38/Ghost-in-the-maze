# Ghost-in-the-maze

# PROBLEM STATEMENT:
The project consists of a maze-like square grid. Some of the cells are blocked and some of them are unblocked. We create an agent at the top left corner cell - this is the start node. The goal is to reach the bottom left corner cell, which is the goal node. The maze consists of multiple obstacles in the form of ghosts. They are generated in random locations in the maze and can move anywhere within the bounds of the maze. The aim is to avoid the ghosts and reach the goal node.

# IMPLMENTATION
## 1. MAZE
We randomly generated a 51 x 51 square grid maze. The probability of each cell being blocked is 0.28 and the probability of each cell being unblocked is 0.72. The agent is free to move through the unblocked cells but cannot enter a blocked cell.

Our code flow for maze creation starts with a call to create_maze() function of mazes() class. The create_maze() function acts like the master function to create the mazes. Code flow for maze creation as be briefly described using the following steps:

1. Call to create_maze()
2. Inside loop until a generated maze is not validated
3. Call to generate_maze() which generated a random number between 0 and 1 for each cell.
If the number is <= 0.72, we mark the cell as unblocked. Else, we mark it as blocked.
4. Validate_maze() is called to validate the maze created in step 3. If there is a path from the start node to the end node, then validate_maze() returns true and maze creation is done. If it returns false, then we re-do the above steps from step-2 until we geet a ‘solvable’ maze.
Since every auto-generated maze need not be a good maze, that is, there might be some mazes where it is impossible to reach the goal node (50,50) from the start node (0,0). We reject these mazes and generate another maze until we have a solvable maze. To validate whether there is a path from the start node to the end node, we used Depth-First Search (DFS) algorithm in the validate_maze() function.

DFS vs Dijkstra’s algorithm

Let us first compare DFS and Dijkstra's algorithms according to our problem statement.
In general, if we know that the endpoint (50,50) is far away from the start-point (0,0), DFS is a good strategy as it picks a path and proceed along that path until it ends or until we reach the goal node. Dijkstra's algorithm is in general a good way to find the shortest possible path.

However, please note that the sole purpose of validating the maze is not to find the shortest path, but it is just to very whether the maze is solvable or not. So, as per the problem description, we chose DFS over Dijkstra’s algorithm to verify the maze.

DFS vs BFS

Breadth-Frist search is usually a good way to find a path, but it is considered better than DFS when the goal node is at a shallow level when compared to the entire environment over which we search. However, in our case, we know that the start node is at (0,0) and the goal node is at (50,50), that is, two points that cannot be further away from each other in our project’s environment. Because of this, choosing DFS over BFS is a better idea as BFS would take more time and it will first keep on expanding all the neighboring cells of the maze whereas we know that we need to go to the other end.

## 2. GHOSTS
The ghosts are generated at a random locations within the bounds of the maze. However, to give all the agents a chance to try to survive the maze, we have decided to not generate any ghost at the starting point as we have encountered test cases where the agent dies in a very short span if the ghost was generated at the start-point.

The initialize_ghosts() of the Ghosts class calculates random pairs of (i,j) and generates ghosts at that point until we have generated the required amount of ghosts. To not make the traversal easy on the agent, we also generate ghosts only at unblocked cells as they would be out-of-bounds for the agent.
To move the ghosts around in the maze at every step, update_ghost() function of the Ghosts class is used and the flow is as follows:

1. For every ghost in the ghost location’s dictionary, generate a random number between 1 and 4
2. If the random number is 1, ghost moves up
3. If the random number is 2, ghost moves down
4. If the random number is 3, ghost moves left
5. If the random number is 4, ghost moves right
6. Call validate_cell() of Ghosts class to validate whether the cell decided in steps 2-5 is
within the bounds of the maze and validates whether the cell is blocked or not.
  -If the cell is unblocked, move ghost to that cell
  -If the cell is blocked, either move ghost to that cell or do not change its position,
   each with a probability of 0.5

If the ghost enters the same cell as the agent, the agent will die. So, the aim of the agent is to avoid the ghosts and reach the goal node. The no. of ghosts is initialized to 10 at first and then it is increased to check the survivability of a given agent. The survivability of an agent is expected to decrease as the number of ghosts increases.

Please note that the agents and the ghosts can move only in vertical or horizontal directions.

## 3. AGENTS

