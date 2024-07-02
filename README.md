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

#### DFS vs Dijkstra’s algorithm

Let us first compare DFS and Dijkstra's algorithms according to our problem statement.
In general, if we know that the endpoint (50,50) is far away from the start-point (0,0), DFS is a good strategy as it picks a path and proceed along that path until it ends or until we reach the goal node. Dijkstra's algorithm is in general a good way to find the shortest possible path.

However, please note that the sole purpose of validating the maze is not to find the shortest path, but it is just to very whether the maze is solvable or not. So, as per the problem description, we chose DFS over Dijkstra’s algorithm to verify the maze.

#### DFS vs BFS

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

The agent is generated in the start node (0, 0) and the goal is to traverse through the maze only along the unblocked cells and try to reach the goal node (50, 50). To succeed, the agent must also not meet any ghosts in the maze while traversing. If both the ghost and the agent enter the same cell, the agent dies.

In this project, we have used multiple strategies to achieve our goal. The agent makes use of these strategies to navigate the maze. The strategies have been implemented and data is collected through multiple iterations. We use this data to analyze each of our strategies and then compare the strategies with each other.

We first make use of three different strategies as given in the project writeup, each making use of the previous one to improve its own approach. The fourth strategy is our own algorithm, which we developed based on an approach to avoid ghosts in the vicinity of the agent. As per the project writeup, we have to try to create the fourth agent to be better than the previous three agents. To analyze that, we have run the agents with varying number of ghosts for multiple iterations. We then create a fifth strategy to work in a more low-information environment and try to run all the first 4 agents in that low-info environment as well.

# STRATEGIES

## 1. Agent 1

For agent 1, we calculate the shortest path from the start node to the goal node using A* algorithm by calling the calculate_path() function of the SearchPath class. Before the agent even starts moving in the maze, we calculate and store this shortest path. The agent 1 then blindly follows the derived shortest path while completely ignoring the ghosts in the maze. The negative aspect of this algorithm with respect to survivability of the agent is that the agent does not update its path if any ghost is nearby. Furthermore, the state of the maze changes at every step as all the ghosts move around. So, the further we go down the line, our original calculated shortest path’s accuracy decreases, and the agent might run into a ghost following the initial path.

Sample success case and failure case scenarios of Agent 1’s path is depicted below:


-Green area represents the unblocked cells where the agent can go

-Red area represents the blocked cells

-Black spots are the ghosts that move around in the maze space

-Blue line represents the path the agent has taken

![New Note](https://github.com/pandaabhishek38/Ghost-in-the-maze/assets/56110423/454662ca-be09-417f-8ad8-b56661d208de)

[Output of the success and failure case is included in the zip file under Outputs folder]

Varying ghosts from 10 to 220 by incrementing 10 ghosts and running the agent for 100 mazes, we get the below graph of Agent 1’s survivability

![Agent 1 Survivability Graph](https://github.com/pandaabhishek38/Ghost-in-the-maze/assets/56110423/e68c9ec3-8826-42f5-bde2-55b1776b0f1e)

Agent 1 starts with survivability of 86% when the number of ghosts is 10. As we increase the number of ghosts, the survivability starts decreasing. We increase the number in increments of 10. For 20 ghosts, the survivability drops down to 63%. It goes further down to 41% when we increase the ghosts by 10 again. The survivability converges down to 0% when the number of ghosts is 160.

## 2. Agent 2

For Agent 2, the agent replans its path at every step based on the current positions of the ghosts. We are using A* algorithm in this agent by calling the same function calculate_path() of class SearchPath.

This agent first calculates the shortest path from the start-point to the goal node before the agent start moving. However, unlike agent 1, this agent does not ignore the change of state and existence of the ghosts in the maze. After every step, this agent recalculates the shortest path from its current position to the end node.

In order to avoid ghosts to some extent, we have treated the cells with ghosts in them as blocked cells too. Since we are treating the cells with ghosts as blocked cells, the A* algorithm tries to find the shortest possible path to the goal node without going through any of the cells which have ghost in them. If the agent 2 cannot find any path from its current node to the goal node, it stays in its place for that turn and hopes that a path will open up in the next turn.

However, since the ghosts also move, this approach, too, is not the best one. This approach only considers the current state of the environment, but the environment changes as soon as the agent takes a step. So, the agent may still die by this approach, but survivability of agent 2 is expected to be better than that of agent 1.

Why A* over Dijkstra’s?

Since agent 2 performs shortest path search at every step, our shortest path finding algorithm needs to be good in order to reduce computation time. We chose A* over Dijkstra’s algorithm as our path finding algorithm because of the cell space that A* needs to determine and compute the shortest path from one node to another. While Dijkstra’s algorithm also finds the shortest path, but it traverses through all the nodes in the environment to find that path. On ther other hand, A* algorithm uses a heuristic to choose the enxt node and find the shortest path to the goal node. In doing so, the A* algorithm does not need to traverse through the entire maze’s environment and thus, is better than Dijkstra’s algorithm for our case.

Sample success case and failure case scenarios of Agent 2’s path is depicted below:

- Green area represents the unblocked cells where the agent can go
 
- Red area represents the blocked cells

- Black spots are the ghosts that move around in the maze space

- Blue line represents the path the agent has taken

![New Note](https://github.com/pandaabhishek38/Ghost-in-the-maze/assets/56110423/4974b3a4-339d-421d-a09c-b07c0f483c0c)

[Output of the success and failure case is included in the zip file under Outputs folder]

Varying ghosts from 10 to 220 by incrementing 10 ghosts and running the agent for 100 mazes, we get the below graph of Agent 2’s survivability

![New Note](https://github.com/pandaabhishek38/Ghost-in-the-maze/assets/56110423/0aef7d7f-c796-4b9f-b8d5-9cd565b06ac1)

Agent 2 starts with survivability of 89%, a 3% improvement compared to agent 1. As seen in the previous agent, the chances of survival starts decreasing as we increase the number of ghosts. It goes down to 73% when we increment the ghosts to 20. It goes down by a further 1% when we increase the number of ghosts to 30. It converges down to 0% when the number of ghosts are 220.

