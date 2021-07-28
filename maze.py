from PIL import Image
import numpy as np

from node import Node
from dfs import dfs_recursive

def compress_maze(maze, width, height):
    
    start_node = end_node = None
    top_row = [None] * width
    
    
    for row in range(0, height):
        left_node = None
        horizontal_distance = 0
        
        for col in range(0, width):
            
            # Do nothing on WALL
            if(maze[row][col] == 0): continue
            new_node = None
            
            ##### Top row (Must have entrance)
            if(row == 0):
                if (maze[row][col] > 0):
                    start_node = Node((row, col))
                    top_row[col] = start_node
                    break
                else: continue
            
            ##### Last row (Find exit)
            if(row == height - 1):
                if(maze[row][col] > 0):
                    
                    # There must be an exit
                    if(top_row[col] == None):
                        raise ValueError("Maze Error: no exit in last row")
                    
                    new_node = Node((row, col))
                    vertical_distance = new_node.get_value()[0] - top_row[col].get_value()[0]
                    top_row[col].add_neighbor(new_node, vertical_distance)
                    new_node.add_neighbor(top_row[col], vertical_distance)
                    end_node = new_node
                                        
                    break
                else: continue
            
            # prev = 1 (that means left node exist)
            if(maze[row][col-1] > 0):
                horizontal_distance += 1
                
                # next = 1
                if(maze[row][col+1] > 0):
                    # top = 1 or bottom = 1
                    if(maze[row-1][col] > 0 or maze[row+1][col] > 0):
                        new_node = Node((row, col))
                        left_node.add_neighbor(new_node, horizontal_distance)
                        new_node.add_neighbor(left_node, horizontal_distance)
                        left_node = new_node
                        horizontal_distance = 0
                
                # Must be end of corridor
                else:
                    new_node = Node((row, col))
                    left_node.add_neighbor(new_node, horizontal_distance)
                    new_node.add_neighbor(left_node, horizontal_distance)
                    left_node = None # End of corridor
                    horizontal_distance = 0
            
            # prev = 0 (that means no left node exist)
            else:
                # next = 1 (Must be start of corridor)
                if(maze[row][col+1] > 0):
                     new_node = Node((row, col))
                     left_node = new_node
                     horizontal_distance = 0
                
                else:
                    # top = 0 or bottom = 0 (Must be a dead end)
                    if(maze[row- 1][col] == 0 or maze[row+1][col] == 0):
                        new_node = Node((row, col))
                        
            
            if(new_node != None):
                # top = 1 (connect new node to top node)
                if(maze[row-1][col] > 0) and top_row[col] != None:
                    vertical_distance = new_node.get_value()[0] - top_row[col].get_value()[0]
                    top_row[col].add_neighbor(new_node, vertical_distance)
                    new_node.add_neighbor(top_row[col], vertical_distance)
                    
                # Add new node to top_row if needed
                top_row[col] = new_node if maze[row+1][col] else None
                        
        # Make sure entrance exist in top row            
        if(row > 0 and start_node == None):
            raise ValueError("Maze Error: no entrance on top row")
        
        # Make sure exit exist in last row
        if(row == height - 1 and end_node == None):
            raise ValueError("Maze Error: no exit in last row")
            
    return start_node, end_node
    

def create_2Dmaze(input_image):
    
    # Load and get image data
    img = Image.open(input_image)
    width, height = img.width, img.height
    maze = np.reshape(list(img.getdata(0)), (width, height))
    
    #print(maze)
    return compress_maze(maze, width, height)
            

if __name__ == "__main__":
    maze_start, maze_end = create_2Dmaze("./examples/tiny.png")
    dfs_recursive(maze_start, maze_end, True)
    