import random
import numpy as np
np.set_printoptions(threshold=np.inf, linewidth=np.inf)
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.colors import ListedColormap
figure(figsize=[8, 8], dpi = 100)

#defining colormaps for depicting maze as an image
cmap1 = ListedColormap(['#C35151','#82C351','#517FC3'])
cmap2 = ListedColormap(['#C35151','#82C351','#517FC3'])
cmap2.set_under('#090101')
cmap3 = ListedColormap(['#C35151','#82C351','#517FC3'])
cmap3.set_under('#090101')

class Ghosts():
  #Ghost class stores the number of ghosts in the  aze and functions through which we can initialize the ghosts and update their locations at every step

  #Count of ghosts in maze
  num_ghosts = 50

  #Taking random i,j and assigning a ghost to that cell
  def initialize_ghosts(self, maze):
    ghost_loc = {}
    while (len(ghost_loc) != self.num_ghosts):
      i = random.randint(0,50)
      j = random.randint(0,50)
      #Not putting ghost in (0,0) node as it will instantly kill the ghost 100 percent
      if (i == 0 and j == 0):
        continue
      #If value is 0, the cell in unblocked
      if (maze[i][j] == 0):
        #Subtracting 2 from the maze cell's value if a ghost is assigned to it
        maze[i][j] -= 2
        #Storing ghost locations in a list
        ghost_loc[len(ghost_loc)] = (i,j)
      else:
        continue
    return ghost_loc

  def validate_cell(self, maze, next_pos, curr_pos):
    #Checking if the ghost assigned is within the bounds of the maze
    if next_pos[0] > (len(maze) - 1) or next_pos[0] < 0 or next_pos[1] > (len(maze) - 1) or next_pos[1] < 0:
      return False

    ##If selected cell of ghost is blocked, take random value between 0 and 1 and assign blocked cell to ghost only it value is <= 0.5
    if(maze[next_pos[0]][next_pos[1]] == -1):
      x = random.random()
      if(x <= 0.5):
        next_pos = curr_pos
    
    return True

  #Function to upfate all the ghosts location after the agents move by one step
  def update_ghosts(self, maze, ghost_loc):
    ghost_num = 0
    while (ghost_num != self.num_ghosts):
      validation = False
      curr_loc = (ghost_loc[ghost_num][0],ghost_loc[ghost_num][1])
      next_loc = curr_loc
      x = random.randint(1,4)
      #Ghost moves - Up if x == 1; Down  if x == 2; Left  if x == 3; Right  if x == 4
      if (x == 1):
        next_loc = (ghost_loc[ghost_num][0]-1,ghost_loc[ghost_num][1])
      elif (x == 2):
        next_loc = (ghost_loc[ghost_num][0]+1,ghost_loc[ghost_num][1])
      elif (x == 3):
        next_loc = (ghost_loc[ghost_num][0],ghost_loc[ghost_num][1]-1)
      elif (x == 2):
        next_loc = (ghost_loc[ghost_num][0],ghost_loc[ghost_num][1]+1)

      #Function to validate if ghost is within the mazes bounds and decide its next value if the selected cell is blocked
      validation = self.validate_cell(maze, next_loc, curr_loc)
      if (validation):
        ghost_loc[ghost_num] = next_loc
        #Adding and subtracting 2 from maze cells vcalue to depict ghosts
        maze[curr_loc[0]][curr_loc[1]] += 2
        maze[next_loc[0]][next_loc[1]] -= 2
        ghost_num += 1
      else:
        continue

class mazes():
  #Mazes class stores the 

  N = 51

  def generate_maze(self):

    maze = np.array([[None for i in range(self.N)] for j in range(self.N)])

    #Possible Cell Values are incremented/decremented by [-2 = Ghost; -1 = Blocked; 0 = Unblocked; 1 = Player; 2 = Goal]

    ##Randomly marking cell as unblocked if random number between 0 and 1 is <= 0.72, otherwise marking it as blocked
    for i in range (self.N):
      for j in range (self.N):
        if random.random() <= 0.72:
          maze[i][j] = 0
        else:
          maze[i][j] = -1

    #Incrementing initial position of the player by 1
    maze[0,0] = 1
    #Incrementing initial position of the goal node by 2
    maze[self.N-1][self.N-1] = 2

    return maze

  #Function to validate the selected cell for the path we will take (before agent starts running) to validate wheter the maze is solvable or not
  def check_val_conditions(self, maze, row, col):
  
    #Checking If the cell is out of bounds of the maze
    if(row < 0 or col < 0 or row >= self.N or col >= self.N):
      return False

    # If the cell is already visited
    if(maze[row][col] >= 3):
      return False

    #Checking if the cell is blocked in the maze
    if(maze[row][col] == -1):
      return False    

    return True

  #Function fo validate using DFS whether the maze is solvable or not. Used in every iteration during the maze creation phase
  def validate_maze(self, maze):

    x_move = [-1, 0, 0, 1]
    y_move = [0, -1, 1, 0]
    solvable = False
    row = 0
    col = 0
    st = []
    st.append([row, col])

    while (len(st) > 0):
    #Popping the top coordinates of the stack (using list) and take it as next cell for DFS
      curr = st.pop()
      row = curr[0]
      col = curr[1]

      #Checking if the current popped cell is a valid cell or not
      if (self.check_val_conditions(maze, row, col) == False):
        continue

      #Incrementing current cell value by 3 to depict the path taken to validate maze
      maze[row][col] += 3

      #Marking maze as solvable if current node or cell if the goal node (50, 50)
      if (row == ((self.N) - 1) and col == ((self.N) - 1)):
        solvable = True
        st = []
        break

      # Push all the adjacent cells
      for i in range(4):
        next_x = row + x_move[i]
        next_y = col + y_move[i]
        st.append([next_x, next_y])
    
    return solvable


  #Main function to create the maze, validate its solvability, and display the maze
  def create_maze(self):

    #Possible values of the mazes validation [False: Not Yet Validated/Need to scrap maze; True: Maze OK to progress]
    #Initialized maze as unsolved
    self.validated = False

    while(self.validated != True):
      self.created_maze = self.generate_maze()
      
      maze_tmp = self.created_maze.copy()

      self.validated = self.validate_maze(maze_tmp)
      print('Validated value: ' + str(self.validated))

    print("Plotting Generated Maze")
    plt.imshow(np.array(list(self.created_maze[:, :]), dtype=np.float), cmap = cmap1, vmin = -1, vmax = 1)#'bwr' SEEMS GOOD TOO
    plt.show()
    
    print("Plotting Validated Maze with DFS path")
    plt.imshow(np.array(list(maze_tmp[:, :]), dtype=np.float), cmap = cmap2, vmin = -1, vmax = 1)#'bwr' SEEMS GOOD TOO
    plt.show()

    return self.created_maze

#Node classs defined to help with the A* algorithm
class Node():

    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

class SearchPath():

  goal = (mazes.N-1,mazes.N-1)

  def calculate_heuristic(self, current_node, child, end_node, mz):
    h = ((child.position[0] - end_node.position[0]) + (child.position[1] - end_node.position[1]))

    return h

  def calculate_path(self, mz, start):
    open_list = []
    closed_list = {}
    start_node = Node(None, start)
    start_node.g = 0
    start_node.h = 0
    start_node.f = 0
    end_node = Node(None, self.goal)
    end_node.g = 0
    end_node.h = 0
    end_node.f = 0

    if (start == self.goal):
      print("Already at goal node")
      path = []
      return path

    #setting initial node to (0, 0)
    open_list.append(start_node)

    while(len(open_list) > 0):
      current_node = open_list[0]
      current_index = 0

      #Selecting node with lowest f-score from the open list as our next node
      for index, item in enumerate(open_list):
        if item.f < current_node.f:
          current_node = item
          current_index = index
      
      #Removing the selected node from open list to add it to the closed list
      open_list.pop(current_index)
      #Adding the selected node to the closed list
      closed_list[str(current_node.position[0])+str(current_node.position[1])] = current_node

      #Checking if the current node is the Goal node
      if current_node.position == end_node.position:
        print("Found Goal Node! Goal Node parent: " + str(current_node.parent.position))
        path = []
        current = current_node
        while current is not None:
          path.append(current.position)
          current = current.parent
        return path[::-1]

      children = []
      #Checking all the 4 neighbouring nodes of the selected (current) node
      for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

        #Checking if neighbouring node is within the mazes bounds
        if node_position[0] > (len(mz) - 1) or node_position[0] < 0 or node_position[1] > (len(mz[len(mz)-1]) -1) or node_position[1] < 0:
          continue

        #Skipping cell that are blocked (have maze cell value less than 0)
        if (mz[node_position[0]][node_position[1]] < 0):
          continue
        
        #creating nodes for the neighbouring cells and storing them in a temporary list
        new_node = Node(current_node, node_position)
        children.append(new_node)

      for child in children:
        skip_child = False

        #Skipping cell that is already visited
        if (str(child.position[0])+str(child.position[1])) in closed_list.keys():
          ###print("Child " + str(child.position) + " Exists in closed list! Skipping it!")
          continue

        #Updating g value, calculating heuristic value h and the total value f (f = g + h)
        child.g = current_node.g + 1
        child.h = self.calculate_heuristic(current_node, child, end_node, mz)#kt
        child.f = child.g + child.h

        #If child node if already present in the open list, re-calculating the f-value and updating the open list if new f-value is better (lesser)
        for open_node in open_list:
          if child.position == open_node.position:
            if child.g < open_node.g:
              open_node.g = child.g
              open_node.f = open_node.h + open_node.g
              open_node.parent = current_node
            #Updating flag to True so same node it not inserted in open list again
            skip_child = True
            break
          
        if (skip_child == False):
          open_list.append(child)


class Agent1():

  #Function containing Agent 2 logic to solve the maze
  def proceed(self, maze_wo_ghost, maze, pos, ghost_loc):
    Alive = True
    ghost = Ghosts()

    print("Going to calculate path for Agent 1...")
    #Calling A* algo function to get the shortest path
    search_path = SearchPath()
    path = search_path.calculate_path(maze,pos)
    #If all paths are currently blocked (either due to blocked cell or ghost positioning)
    if not path:
      #Calculate shortest path without considering ghosts in the maze
      path = search_path.calculate_path(maze_wo_ghost,pos)

    print("Path for Agent 1: " + str(path))
    print("Agent 1 proceeding to goal...")

    #path returns current cell as 0 index of the path. popping it and increments mazes cell value for plotting the image of agent 2s traversal
    next_pos = path.pop(0)
    maze[next_pos[0]][next_pos[1]] += 3

    while (len(path) > 0):
      #Popping coordinates from the calculated path and proceeding to the goal node
      next_pos = path.pop(0)
      maze[next_pos[0]][next_pos[1]] += 3

      print("Agent1 Player at position:" + str(next_pos) + " with value: " + str(maze[next_pos[0]][next_pos[1]]))

      #updating location of the ghosts in the map
      ghost.update_ghosts(maze, ghost_loc)

      print("Ghost Location: " + str(ghost_loc))

      #Checking if the agent and any ghost are in the same cell
      if (next_pos in ghost_loc.values()):
        Alive = False
        break

    print("Plotting Agent 1's path")
    plt.imshow(np.array(list(maze[:, :]), dtype=np.float), cmap = cmap3, vmin = -1, vmax = 1)
    plt.show()

    return Alive


class Agent2():

  #Function containing Agent 2 logic to solve the maze
  def proceed(self, maze, pos, ghost_loc, move_count = None):
    Alive = True
    ghost = Ghosts()
    print("Going to calculate path for Agent 2...")
    #Re-calculating the path from the the initial start cell
    search_path = SearchPath()
    path = search_path.calculate_path(maze,pos)
    #If all paths are currently blocked, stay is current position. Appending (start, goal node) of only this move
    if not path:
      print("Player to stay")
      path = []
      path.append((0, 0))
      path.append((0, 0))

    print("Path for Agent 2: " + str(path))
    print("Agent 2 proceeding to goal...")
    
    next_pos = (0, 0)
    goal = (50, 50)
    i = 0

    #While condition updated to also work for move_count is not None (Agent 3 scenario)
    while ((len(path) > 1 and next_pos != (50,50) and move_count is None) or (move_count is not None  and i < move_count and next_pos != (50,50))):
      print("move count: " + str(move_count))
      #path returns current cell as 0 index of the path. popping that
      current_pos = path.pop(0)

      #Incremention initial start node by 3 for plotting the image of agent 1s traversal
      if (current_pos == (0,0)):
        maze[current_pos[0]][current_pos[1]] += 3

      #Fetching next cell and incrementing it by 3 for plotting the image of agent 1s traversal
      next_pos = path.pop(0)
      maze[next_pos[0]][next_pos[1]] += 3

      i += 1

      #updating location of the ghosts in the map
      ghost.update_ghosts(maze, ghost_loc)
      
      print("Ghost Location: " + str(ghost_loc))
      print("Agent 2 Player at position:" + str(next_pos) + " with value: " + str(maze[next_pos[0]][next_pos[1]]))

      #Checking if the agent and any ghost are in the same cell
      if (next_pos in ghost_loc.values()):
        Alive = False
        break
      #Break if goal node reached
      if (next_pos == goal):
        break
      #Re-calculating the path from the new current cell
      path = search_path.calculate_path(maze,next_pos)

      #If all paths are currently blocked, stay is current position. Appending (start, goal node) of only this move
      if not path:
        print("Player to stay")
        path = []
        path.append(next_pos)
        path.append(next_pos)
      print("Path for Agent 2: " + str(path))


    return Alive


class Agent3():
  #simulation count per neighbouring cell
  sim_count = 5
  #Number of steps to simulate per neighbouring cell
  move_count = 20

  #Function containing agent 3s approach to solve the maze and staying alive
  def proceed(self, maze, pos, ghost_loc):
    Alive = True
    ghost = Ghosts()
    print("Going to calculate path for Agent 3...")
    search_path = SearchPath()

    #setting next cell value to current cell
    next_pos = pos
    goal = (50, 50)
    path = []
    #appending start node to path list
    path.append((0, 0))

    mz_2 = maze.copy()

    while (next_pos != (50,50)):
      if (len(path) > 0 and path[0] == (0,0)):
        #popping initial node from path list and incrementing its maze value by 3 for plotting the image of agent 1s traversal
        current_pos = path.pop(0)
        maze[current_pos[0]][current_pos[1]] += 3

      #Taking the success count of simulations of all the neighbouring cells and the current cell. Initializing success count to zero
      success_sum = [0,0,0,0,0]
      #List containing (X,Y) pairs to add to the current cell and pick the neighbour. (0, 0) will choose the same cell
      tmpkt = [(0, -1), (-1, 0), (0, 1), (1, 0), (0, 0)]

      #variable to help choose the current neighbour being considered from tmpkt list
      i = 0
      while (i <len(tmpkt)):
        mz_2 = maze.copy()
        
        #Checking if the picked neighbour (next_pos+tmpkt[i]) is outside the maze bounds.
        #If so, increment i to point to next element in tmpkt and continue to next iteration
        if (next_pos[0]+tmpkt[i][0] > (len(maze) - 1) or next_pos[0]+tmpkt[i][0] < 0 or next_pos[1]+tmpkt[i][1] > (len(maze) - 1) or next_pos[1]+tmpkt[i][1] < 0):
          i += 1
          continue

        #Checking if the neighbouring cell is blocked or unblocked for the agent to move
        #If so, increment i to point to next element in tmpkt and continue to next iteration
        if (maze[next_pos[0]+tmpkt[i][0]][next_pos[1]+tmpkt[i][1]] < 0):
          i += 1
          continue

        #After picking an unblocked and bounded neighbourm run 5 simulations by calling Agent 2
        for j in range(self.sim_count):
          possible_next_cell = (next_pos[0]+tmpkt[i][0],next_pos[1]+tmpkt[i][1])
          print("Simulation " + str(j+1) + " for " + str(possible_next_cell))
          agent_2 = Agent2()
          mz_2 = maze.copy()
          ghost_loc_2 = ghost_loc.copy()
          f_s2 = agent_2.proceed(mz_2, (next_pos[0]+tmpkt[i][0],next_pos[1]+tmpkt[i][1]), ghost_loc_2, self.move_count)

          #If Agent 2 returned true, increment success_sum to increase the simulated success count
          if f_s2:
            success_sum[i] += 1
        i += 1

      print("success_sum = " + str(success_sum))
      max_elem = max(success_sum)
      max_index = success_sum.index(max(success_sum))

      #If max success was for right and bottom cells, pick any one randomly and add it to the path
      if (success_sum[2] == max_elem and success_sum[3] == max_elem):
        y = random.randint(0,1)
        x = (next_pos[0]+tmpkt[2 + y][0],next_pos[1]+tmpkt[2 + y][1])
        path.append(x)
      #If max success was for right cell, pick that and add it to the path
      elif (success_sum[2] == max_elem):
        x = (next_pos[0]+tmpkt[2][0],next_pos[1]+tmpkt[2][1])
        path.append(x)
      #If max success was for bottom cell, pick that and add it to the path
      elif (success_sum[3] == max_elem):
        x = (next_pos[0]+tmpkt[3][0],next_pos[1]+tmpkt[3][1])
        path.append(x)
      #Picking the cell with max success count and add it to the path
      else:
        x = (next_pos[0]+tmpkt[max_index][0],next_pos[1]+tmpkt[max_index][1])
        path.append(x)

      curr_pos = next_pos
      #Popping next cell from path
      next_pos = path.pop(0)
      #If all neighbouring cells had a success count of zero, follow agent 2s approach by taking A* from current cell
      #OR, if the selected cell has a cell value greater than 15 (visited 5 times), then follow agent 2s approach by taking A* from current cell to avoid gettign stuck
      #between only 2 cells
      if (sum(success_sum) == 0 or maze[next_pos[0]][next_pos[1]] > 15):
        print("Player following Agent 2 approach")
        path = search_path.calculate_path(maze,curr_pos)
        if (not path):
          #If all routes from the current cell to goal node are blocked (by bloked cells or ghosts), agent stays in same place
          #Adding (start, goal) node to path only for this move
          path = []
          path.append(curr_pos)
          path.append(curr_pos)
        current_pos = path.pop(0)
        next_pos = path.pop(0)
        path = []

      #Incrementing maze value by 3 for plotting the image of agent 3s traversal
      maze[next_pos[0]][next_pos[1]] += 3
      ghost.update_ghosts(maze, ghost_loc)
      print("Ghost Location in Agent3: " + str(ghost_loc))
      print("Agent 3Player at position: " + str(next_pos) + " with value: " + str(maze[next_pos[0]][next_pos[1]]))
      #Checking ghost and agents location to check if agent is alive
      if (next_pos in ghost_loc.values()):
        Alive = False
        break

      #Checking if agent has reached the goal node 
      if (next_pos == goal):
        break

    print("Plotting Agent 3's path")
    plt.imshow(np.array(list(maze[:, :]), dtype=np.float), cmap = cmap3, vmin = -1, vmax = 1)
    plt.show()

    return Alive


class Agent4():

  #Function to validate wherther the potential cell if within the maze bounds
  def choose_cell(self, maze, pos, options):
    next_pos = pos
    for i in range(len(options)):
      x =  (pos[0] + options[i][0],pos[1] + options[i][1])
      if (x[0] > (len(maze) - 1) or x[0] < 0 or x[1] > (len(maze) - 1) or x[1] < 0):
        continue
      else:
        if (maze[x[0]][x[1]] >= 0):
          next_pos = x
    return next_pos

  #Agent 4s logic to avoid ghost in a 5X5 cell with the agent at the center
  def avoid_ghost(self, maze, path, pos, ghost_loc):
    #List of (X,Y) coordinates to reach neighbouring cells of the 5X5 matrix of the maze
    check_grid = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-1,2),(0,2),(1,2),(2,2),(2,1),(2,0),(2,-1),(2,-2),(1,-2),(0,-2),(-1,-2)]
    tmp_path = []
    nearby_ghosts = []

    #Check and store ghost locations in the 5X5 grid
    for i in range(len(check_grid)):
      if ((pos[0]+check_grid[i][0],pos[1]+check_grid[i][1]) in ghost_loc.values()):
        nearby_ghosts.append((pos[0]+check_grid[i][0],pos[1]+check_grid[i][1]))

    #If no ghost in the vicinity (5X5 grid), continue using path derived from A*
    if (len(nearby_ghosts) == 0):
      return path

    print(str(len(nearby_ghosts)) + " ghosts in the 5X5 grid at cells: " + str(nearby_ghosts))
    path = []
    path.append(pos)
    
    #Checking all ghosts in the 5X5 grid
    for i in range(len(nearby_ghosts)):
      #If ghost is beneath the agent in the 5X5 grid
      if (pos[0] < nearby_ghosts[i][0]):
        #If ghost is towards the center and beneath the agent, go up, left, or right
        if (pos[1] == nearby_ghosts[i][1]):
          tmp_path = self.choose_cell(maze, pos, [(-1,0),(0,-1),(0,1)])
        #If ghost is towards the bottom on left side, go up or right
        elif (pos[1] > nearby_ghosts[i][1]):
          tmp_path = self.choose_cell(maze, pos, [(-1,0),(0,1)])
        else:
          #If ghost is towards the bottom on right side, go left or up
          tmp_path = self.choose_cell(maze, pos, [(0,-1),(-1,0)])
      #If ghost is above the agent in the 5X5 grid
      elif (pos[0] > nearby_ghosts[i][0]):
        #If ghost is towards the center and above the agent, go left, right, or down
        if (pos[1] == nearby_ghosts[i][1]):
          tmp_path = self.choose_cell(maze, pos, [(0,-1),(0,1),(1,0)])
        #If ghost is towards the top on left side, go down or right
        elif (pos[1] > nearby_ghosts[i][1]):
          tmp_path = self.choose_cell(maze, pos, [(1,0),(0,1)])
        else:
          #If ghost is towards the top on right side, go left or down
          tmp_path = self.choose_cell(maze, pos, [(0,-1),(1,0)])
      else:
        #If ghost on the same row in the 5X5 grid as the agent
        if (pos[1] > nearby_ghosts[i][1]):
          #If the ghost is on the same row and on the left side, go up, down, or right
          tmp_path = self.choose_cell(maze, pos, [(-1,0),(1,0),(0,1)])
        else:
          #If the ghost is on the same row and on the right side, go left, up, or down
          tmp_path = self.choose_cell(maze, pos, [(0,-1),(-1,0),(1,0)])
    path.append(tmp_path)

    return path

  #Main function for Agent 4. Starting point of logic
  def proceed(self, maze, pos, ghost_loc):
    Alive = True
    ghost = Ghosts()
    next_pos = (0, 0)
    goal = (50, 50)
    print("Going to calculate path for Agent 4...")
    search_path = SearchPath()
    #Calculate path from current node to goal node using A*
    path = search_path.calculate_path(maze,pos)
    #If all paths are blocked, stay in same palce
    if not path:
      print("Player to stay")
      path = []
      path.append((0, 0))
      path.append((0, 0))
    print("Path for Agent 4: " + str(path))

    while (len(path) > 1 and next_pos != (50,50)):
      #Popping current cell from path
      current_pos = path.pop(0)

      #Incrementing initial cell value in maze for depicting the path
      if (current_pos == (0,0)):
        maze[current_pos[0]][current_pos[1]] += 3

      #Popping next cell from path and incrementing its cell value for visualization
      next_pos = path.pop(0)
      maze[next_pos[0]][next_pos[1]] += 3

      #Update ghosts location
      ghost.update_ghosts(maze, ghost_loc)
      print("Ghost Location: " + str(ghost_loc))
      print("Agent 4 Player at position:" + str(next_pos) + " with value: " + str(maze[next_pos[0]][next_pos[1]]))
      #Checking if agent is alive by camparing its positions with ghosts
      if (next_pos in ghost_loc.values()):
        Alive = False
        break

      #Checking if agent is at the goal node
      if (next_pos == goal):
        break

      #Using A* to find the path from current cell to goal node
      path = search_path.calculate_path(maze,next_pos)

      #Call to Agent 4s logic to avoid ghosts in the vicinity
      path = self.avoid_ghost(maze, path, next_pos, ghost_loc)

      #Stay in same place if no path available
      if not path:
        print("Path Empty. Player to stay")
        path = []
        path.append(next_pos)
        path.append(next_pos)
      print("Path for Agent 4: " + str(path))

    print("Plotting Agent 4's path")
    plt.imshow(np.array(list(maze[:, :]), dtype=np.float), cmap = cmap3, vmin = -1, vmax = 1)
    plt.show()

    return Alive


class Agent5():

  #Taking Agent 4 as base of agent 5
  def choose_cell(self, maze, pos, options):
    next_pos = pos
    for i in range(len(options)):
      x =  (pos[0] + options[i][0],pos[1] + options[i][1])
      if (x[0] > (len(maze) - 1) or x[0] < 0 or x[1] > (len(maze) - 1) or x[1] < 0):
        continue
      else:
        if (maze[x[0]][x[1]] >= 0):
          next_pos = x
    return next_pos

  def avoid_ghost(self, maze, path, pos, ghost_loc):
    #List of (X,Y) coordinates to reach neighbouring cells of the 5X5 matrix of the maze
    check_grid = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-1,2),(0,2),(1,2),(2,2),(2,1),(2,0),(2,-1),(2,-2),(1,-2),(0,-2),(-1,-2)]
    tmp_path = []
    nearby_ghosts = []

    #Check and store ghost locations in the 5X5 grid
    for i in range(len(check_grid)):
      if ((pos[0]+check_grid[i][0],pos[1]+check_grid[i][1]) in ghost_loc.values()):
        nearby_ghosts.append((pos[0]+check_grid[i][0],pos[1]+check_grid[i][1]))

    #If no ghost in the vicinity (5X5 grid), continue using path derived from A*
    if (len(nearby_ghosts) == 0):
      return path

    print(str(len(nearby_ghosts)) + " ghosts in the 5X5 grid at cells: " + str(nearby_ghosts))
    path = []
    path.append(pos)
    
    #Checking all ghosts in the 5X5 grid
    for i in range(len(nearby_ghosts)):
      #ghosts on the bottom
      if (pos[0] < nearby_ghosts[i][0]):
        #If ghost is towards the center and  beneath the agent in the 5X5 grid
        if (pos[1] == nearby_ghosts[i][1]):
          tmp_path = self.choose_cell(maze, pos, [(-1,0),(0,-1),(0,1)])
        #If ghost is towards the bottom on left side, go up or right
        elif (pos[1] > nearby_ghosts[i][1]):
          tmp_path = self.choose_cell(maze, pos, [(-1,0),(0,1)])
        else:
          #If ghost is towards the bottom on rught side, go left or up
          tmp_path = self.choose_cell(maze, pos, [(0,-1),(-1,0)])
      #If ghost is above the agent in the 5X5 grid
      elif (pos[0] > nearby_ghosts[i][0]):
        #If ghost is towards the center and above the agent, go left, right, or down
        if (pos[1] == nearby_ghosts[i][1]):
          tmp_path = self.choose_cell(maze, pos, [(0,-1),(0,1),(1,0)])
        #If ghost is towards the top on left side, go down or right
        elif (pos[1] > nearby_ghosts[i][1]):
          tmp_path = self.choose_cell(maze, pos, [(1,0),(0,1)])
        else:
          #If ghost is towards the top on right side, go left or down
          tmp_path = self.choose_cell(maze, pos, [(0,-1),(1,0)])
      else:
        #If ghost on the same row in the 5X5 grid as the agent
        if (pos[1] > nearby_ghosts[i][1]):
          #If the ghost is on the same row and on the left side, go down, up, or right
          tmp_path = self.choose_cell(maze, pos, [(1,0),(-1,0),(0,1)])
        else:
          #If the ghost is on the same row and on the left side, go down, up, or left
          tmp_path = self.choose_cell(maze, pos, [(1,0),(-1,0),(0,-1)])
    path.append(tmp_path)

    return path

  #Main function for Agent 5. Starting point of logic
  def proceed(self, maze, pos, ghost_loc):
    Alive = True
    ghost = Ghosts()
    print("Going to calculate path for Agent 5...")
    search_path = SearchPath()
    path = search_path.calculate_path(maze,pos)
    if not path:
      print("Player to stay")
      path = []
      path.append((0, 0))
      path.append((0, 0))
    print("Agent 4 proceeding to goal...")
    next_pos = (0, 0)
    goal = (50, 50)

    while (len(path) > 1 and next_pos != (50,50)):
      #Popping current cell from path
      current_pos = path.pop(0)

      #Incrementing inirial cell value in maze for depicting the path
      if (current_pos == (0,0)):
        maze[current_pos[0]][current_pos[1]] += 3

      #Popping next cell from path and incrementing its cell value for visualization
      next_pos = path.pop(0)
      maze[next_pos[0]][next_pos[1]] += 3

      #Storing ghost location before updation. So, it will still have the positions that ghosts were at the previous cell at any state except for the initial state
      ghost_loc_temp = ghost_loc.copy()
      #Updating ghosts location
      ghost.update_ghosts(maze, ghost_loc)
      print("Current Ghost Location: " + str(ghost_loc))
      
      #Setting new ghost locations to a variable and then updating all locations in this to previous ghost locations if a ghost is in the wall
      ghost_now_prev_loc = ghost_loc.copy()

      #Iterating through all new ghost locations
      for key,value in ghost_loc.items():
        #Values of unblocked cells are -1. Values of cell with ghosta are -2
        #Value of Ghost in an unblocked cell will be -2*n for n number of ghosts in the same cell
        #Value of Ghost in a blocked cell will be (-1)+(-2*n) for n number of ghosts in the same cell.
        #So, we can figure if a ghost is in the wall if value of that ghost location is not divisible by 2
        if (maze[value[0]][value[1]] < 0 and maze[value[0]][value[1]] % 2 != 0):
          print("ghost_now_prev_loc[key]: " + str(ghost_now_prev_loc[key]) + "with value:" + str(maze[value[0]][value[1]]))
          ghost_now_prev_loc[key] = ghost_loc_temp[key]
          print("ghost_now_prev_loc[key] after update: " + str(ghost_now_prev_loc[key]) + "with value:" + str(maze[value[0]][value[1]]))
      print("Current Ghost Location visible to the agent: " + str(ghost_loc))

      print("Agent 5 Player at position:" + str(next_pos) + " with value: " + str(maze[next_pos[0]][next_pos[1]]))
      if (next_pos in ghost_loc.values()):
        Alive = False
        break
      if (next_pos == goal):
        break
      path = search_path.calculate_path(maze,next_pos)
      path = self.avoid_ghost(maze, path, next_pos, ghost_now_prev_loc)
      if not path:
        print("Player to stay")
        path = []
        path.append(next_pos)
        path.append(next_pos)
      print("Path for Agent 5: " + str(path))


    print("Plotting Agent 5's path")
    plt.imshow(np.array(list(maze[:, :]), dtype=np.float), cmap = cmap3, vmin = -1, vmax = 1)
    plt.show()

    return Alive

agnt_1_record = []
agnt_2_record = []
agnt_3_record = []
agnt_4_record = []
agnt_5_record = []

#for i in range(100):
mze = mazes()
mz = mze.create_maze()

mz_1_tmp = mz.copy()

ghost = Ghosts()
ghost_loc = ghost.initialize_ghosts(mz)
print(ghost_loc)
print("Plotting Generated Maze with Ghosts")
plt.imshow(np.array(list(mz[:, :]), dtype=np.float), cmap = cmap3, vmin = -1, vmax = 1)#'bwr' SEEMS GOOD TOO
plt.show()

for a in range(mze.N):
  print(mz[a])

start = (0,0)

agent_3 = Agent3()
mz_3 = mz.copy()
ghost_loc_3 = ghost_loc.copy()
f_s3 = agent_3.proceed(mz_3, start, ghost_loc_3)
if f_s3:
  print("Agent 3 successfully reached the goal node! Yay!")
  agnt_3_record.append(1)
else:
  print("Agent 3 died")
  agnt_3_record.append(0)
