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

## Agent 3

Agent 3 can be considered as further extension of agent 2. In this strategy, the agent predicts the future states of the maze if it picked and went to one cell. The agent checks its survivability if it chooses to go to its neighboring cell or even if it stays in the same place, that it, it checks its survivability for its current position, top, left, right, and the bottom cells, and then picks the best possible option as the next cell/step.

For all of the 5 cells, the agent 3 does 5 simulations, that is, 25 simulations at each step in total to choose the next cell. For each simulation, the agent 3 calls agent 2’s code and tries to simulate the next 5 steps. The agent considers that its current position is either the same cell, or one of its neighboring cells, and then it follows agent 2’s approach of re-calculating the shortest path at every step using A* algorithm for the next 5 steps. At the end of every simulation of each cell, the agent3 updates a list counter success_sum for each of the 5 cells to map how many times did the agent
survive in the simulation from a particular cell.

After all the simulations, the agent 3 then chooses the cell with the highest survivability counter value, proceeds ahead, and repeats the same until it reaches the goal node.

However, we know that for every maze, the agent 3 has to go from (0,0) to (50,50), that is, from the top-left cell to the bottom-right cell. So, we created a little bias that helps us go in the bottom or right direction in case of a tie. In this manner, even if there are multiple cells with the same survivability counter in agent 3, it will pick either right or bottom cells over the left, top, and current cells and the agent proceeds towards the area which we know is closer to the goal node.

In case the agent 3 dies in all of the simulations, that is, if the survivability counter for all cases of simulations is 0, it reverts back to agent 2’s approach and calculates the shortest path from the current cell to the goal node using A* and follows that for 1 step. After that turn, it again runs 5 simulations on each of its neighboring cells and and chooses the next cell based on the counter containing survivability of the simulations.

In Agent 3, we noticed that in some cases, the agent toggles multiple times between two given cells and doesn’t move forward. To avoid this, we have put a threshold on the number of times the agent can visit a particular cell. So, if the agent chooses the next cell based on simulations and it that cell has already been visited 5 times by the agent, then the agent again follows agent 2’s approach by finding the shortest path from the current step and follow that path for 1 step. In many instances, we have observed that by doing so, the agent 3 comes out of that toggle in about 2-3 steps.

Sample success case and failure case scenarios of Agent 3’s path is depicted below:

- Green area represents the unblocked cells where the agent can go
  
- Red area represents the blocked cells
  
- Black spots are the ghosts that move around in the maze space
  
- Blue line represents the path the agent has taken

![New Note](https://github.com/pandaabhishek38/Ghost-in-the-maze/assets/56110423/91a0d280-517f-40d0-9e0a-d0d8a5083f94)

[Output of the success and failure case is included in the zip file under Outputs folder]

Varying ghosts from 10 to 50 by incrementing 10 ghosts and running the agent for 30 mazes, we get the below graph of Agent 3’s survivability.

Note: Running agent 3 in general is a computation heavy process and takes a lot of time. So, we have ran the agent only on 30 iterations per ghost size.

![New Note](https://github.com/pandaabhishek38/Ghost-in-the-maze/assets/56110423/41daa1fd-ac8b-46ff-806b-9aaf31f2ba63)

Agent 3 starts with a survivability of 80%. As we increase the number of ghosts, the survivability goes down drastically. It goes down to 63.33% when we increment the number of ghosts to 20. When we increase the number of ghosts to 30, our survivability goes down to 30%. It increases, however, to 36.67% when we increment our number of ghosts to 40. Survivability is 30% for 50 ghosts.

## 4. Agent 4

As per the project writeup, we had to create the agent 4 with our own approach and try to make it better than the previous three agents. For this strategy, we create a 5 x 5 grid around the agent with the agent at the center of the grid. Throughout all the agents, we use a python dictionary to keep a track of the ghosts in the maze. Using this dictionary, we check for the existence of the ghosts in this 5X5 grid. If there are no ghosts in the grid, the agent simply calculates the shortest path to the goal node using A* algorithm at that step to get the next cell and moves to that. In the next turn, it will again check for ghosts in the 5X5 grid and repeat the process. The existence of the ghosts are taken under consideration while calculating the shortest path. In this way, it incorporates the strategy of agent 2 if there are no ghosts in the 5 x 5 grid.

In case there is a ghost in the grid, we decide our next move based on the location of the ghost. The idea is to move away from the ghost as far as possible to reduce the chance of our agent’s death. We have mapped multiple cases in the code to avoid ghosts in the 5X5 grid.

If a ghost is in the same column of the agent and below it, the agent will avoid moving downwards. The possible paths are either moving up, left or to the right cell. The agent checks which of them are unblocked and then move to one of them. Again, as our goal node is almost always towards the right side or bottom side, we give preference to the rightmost cell in this case (ghost is below so cannot go there) since it will move the agent closer to the goal and further away from the ghost. If the ghost is in the bottom left section of the grid, the agent avoids moving to the bottom or the left cell, since either of them would move us closer to the ghost or either of them could have ghost in them in the after this step. So, the possible move would be the top cell or the right cell. Preference is given to the right cell once again. In case the ghost is in the bottom right section of the grid, the agent avoids the bottom or the right cell and tries to move to the left or the top cell.

Similarly, the following mapping is done so the agent tries to avoid the ghost in the grid:

• If ghost is in same column and on the bottom side

  o Agent tries to move to move right, left, or up in that order of preference
  
• If ghost is in the same column and on the top side

  o Agent tries to move to move down, right, or left in that order of preference
  
• If ghost is in the same row and on the left side

  o Agent tries to move to move right, down, or up in that order of preference
  
• If ghost is in the same row and on the right side

  o Agent tries to move to move down, up, or left in that order of preference
  
• If ghost is in the top-right section of the grid

  o Agent tries to move to move left, or down in that order of preference
  
• If ghost is in the top-left section of the grid

  o Agent tries to move to move right, or down in that order of preference
  
• If ghost is in the bottom-right section of the grid

  o Agent tries to move to move left, or up in that order of preference
  
• If ghost is in the bottom-left section of the grid

  o Agent tries to move to move right, or up in that order of preference

The code iterates through the list of all ghosts and checks if they are within the 5X5 grid. If they are, the agent updates it next cell for the current step. The order of preference is simply definedby the order of (x,y) coordinates passed on to choose_cell() function of the Agent4 class. The coordinates mentioned at the last position of this array of viable options is given the maximum preference. If that cell is not available, then its previous cell is given the next preference as per the iteration.

The question may arise as to why we chose a 5x5 grid and not a 3x3 grid because for a 3x3 grid, in case the ghost is detected in the grid, it will exist in the immediate next cell of the agent. This makes it the approach very risky.

Let’s take an example of a ghost in the same row on the right side of the grid.
In our 5X5 grid, the ghost can either move to the top, bottom, or the left cell in order to avoid the ghost. But in a 3X3 grid, our options are narrowed down to just one cell, that it, the left cell in this case. But, if the left cell is blocked, then our agent’s death is guaranteed. This will not happen in a 5X5 grid as our algorithm will detect the ghost one step before the 3X3 grid. Hence, giving our agent one more step to save itself. We cannot use 4x4 matrix grid either as the agent will not be located in the center of the grid due to the even number of cells in the grid. Hence, we make use of a 5x5 in our algorithm.

Sample success case and failure case scenarios of Agent 4’s path is depicted below:

- Green area represents the unblocked cells where the agent can go

- Red area represents the blocked cells
  
- Black spots are the ghosts that move around in the maze space
  
- Blue line represents the path the agent has taken

![New Note](https://github.com/pandaabhishek38/Ghost-in-the-maze/assets/56110423/d533f645-6ed3-4753-8161-34be6bfa9590)

[Output of the success and failure case is included in the zip file under Outputs folder]

Varying ghosts from 10 to 220 by incrementing 10 ghosts and running the agent for 100 mazes, we get the below graph of Agent 4’s survivability.

![New Note](https://github.com/pandaabhishek38/Ghost-in-the-maze/assets/56110423/0538d833-b166-4e51-9014-a32385bbc30b)

Agent 4 has a survivability of 100% when the number of ghosts is 10. This is way better than agent 1, 2 and 3. The chance of survival starts reducing when we increment the number of ghosts. We increase the ghosts in increments of 10. Survivability goes down by only 1% when we increase the number of ghosts to 20. It goes down to 91% when we increase the number of ghosts to 30.Survivability goes down to 0% when the number of ghosts goes up to 220.

How did our Agent 4 stack up against the others? Why did it succeed, or why did it fail?

Comparing Agent 4 to Agent 1, Agent 2, and Agent 3:

For 10 ghosts, Agent 4’s survivability is 100% for 100 runs whereas Agent 1’s survivability is 86%, Agent 2’s survivability is 89%, and Agent 3’s survivability is 80%. Comparing these values at 10 ghosts, we can roughly determine that Agent 4 beats Agent 1, 2, and 3 at a smaller number of ghosts.

Now going further down the line and checking their survivability at 210 ghosts. Agent 4’s survivability is 2% for 100 runs whereas Agent 1’s survivability is 1%, Agent 2’s survivability is 1%, and Agent 3’s survivability is 1%. Even at this point, Agent 4 beats all other agents even for a large number of ghosts.

While Agent 4’s survivability for 220 ghosts is 0% and that of Agent 1 is 1% but considering that agent 1 moves even trying to avoid the ghosts, we can assume that luck played out in this case and can treat it as an anomaly.

Furthermore, if we look at the combined survivability graph of all the agents at the very last page of the report, we can determine that Agent 4 and Agent 5 have dominated and outperformed the first three agents most of the times.

If we look at the approach, we have taken for Agent 1, Agents 2, and Agent 3, then we may notice one thing that while computing path for these agents, we have treated cells with ghosts as blocked cells and tried to find the shortest path around them. However, in our agent 4, we track ghosts in the 5X5 grid and actively try to move the agent 4 away from the ghost. This decision of moving away from the ghost instead of taking risk and proceeding with the shortest path seems to have contributed to Agent 4’s survivability. Hence, it performed better that Agent 1, 2, and 3.

## 5. Agent 5

We make our agent 5 based on the assumption that our agent loses sight of the ghost when it moves into a blocked cell. Our agent 5 is supposed to be better suited in this low information environment. We made our agent 5 similar to our agent 4. We make a 5 x 5 matrix around the agent and check for the existence of the ghost. If there are no ghosts in the grid, we make our next move based on the shortest path calculated using A* algorithm, considering the locations of the ghosts of course. But in case there is a ghost in the grid, we make our next move away from the ghost just like we did in case of agent 4.

The difference between agent 4 and agent 5 is that the agent 4 can see all ghost’s location from the python dictionary containing locations of all agents, but agent 5 cannot see ghosts in walls.

To implement “not seeing ghost in wall”, we track the ghost’s last seen location, that is, its location in an unblocked cell just before it entered a wall and use this location in our dictionary of ghosts. We then pass this list to the agent 4’s algorithm that checks ghost in a 5X5 grid around the agent. So, in case of agent 4, if there was a ghost in a wall inside the 5X5 grid, the algorithm would have still considered its correct location. But in case of agent 5, the same algorithm will now work on the ghost’s last seen location. Now, even if our 5X5 grid does not have the ghost’s exact location, it still knows the general area (top, bottom, top-right, top-left...) where the ghost might be and our agent tries to go away from that area and hence, from the ghost.

Sample success case and failure case scenarios of Agent 5’s path is depicted below:
- Green area represents the unblocked cells where the agent can go
  
- Red area represents the blocked cells
  
- Black spots are the ghosts that move around in the maze space
  
- Blue line represents the path the agent has taken

![New Note](https://github.com/pandaabhishek38/Ghost-in-the-maze/assets/56110423/ee8e41c2-8e3a-4aaf-a539-8623d4ba78a9)

[Output of the success and failure case is included in the zip file under Outputs folder]

Varying ghosts from 10 to 220 by incrementing 10 ghosts and running the agent for 100 mazes, we get the below graph of Agent 5’s survivability

![New Note](https://github.com/pandaabhishek38/Ghost-in-the-maze/assets/56110423/ef40f578-04e0-48c4-95a6-00c15d419bd8)

Agent 5 starts with a survivability of 98% when the number of ghosts is 10. The survivability starts going down when we increment the number of ghosts. There is no change in chances of survival when we increment the number of ghosts to 20. It goes down by 9%, however, when we increase the number of ghosts to 30. Survivability goes down to 0% once we increase the number of ghosts to 220.

# Comparison between different strategies:

![New Note](https://github.com/pandaabhishek38/Ghost-in-the-maze/assets/56110423/758674ba-8fb0-4eff-82c1-599adfdbb65a)

Agent 4 has the best survivability for 10 ghosts, at nearly 100%. It is followed by agent 5 at 98%. Agent 2 has survivability of 89% and agent 1 has a survivability of 86%. Agent 3 has the lowest survivability amongst all of them, at 80%.

As we increase the number of ghosts, the survivability of each of the agents starts decreasing. Normally agent 4 is always better than all other agents, followed by agent 5, agent 2, agent 1 and agent 3 for almost any number of ghosts. However, this is not always true. In some cases, this order is changed. For example, when we increase the number of ghosts to 100, agent 2 has better survivability than agent 4 by 1%.

The survivability of all the agents eventually converges to 0 as we keep increasing the number of ghosts. Survivability of agents 2, 4 and 5 goes down to 0% when we reach 220 ghosts. And in case of agent 1, the chance of survival goes down to 0% when we increase the number of ghosts to
nearly 160 ghosts.

Agent 3 takes a lot of time to iterate. We have not been able to take enough iterations, hence we could not collect enough data. Agent 3 goes down to 30% when we increment the number of ghosts to 50. Since we do not have further data, we have represented the survivability of agent 3 as 30 % for the remainder of the graph. It is expected to converge down to 0% when we keep increasing the number of ghosts.


