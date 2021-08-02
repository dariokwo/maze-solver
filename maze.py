from PIL import Image
import numpy as np

from node import Node

class IMaze:
    def __init__(self, image_source = None) -> None:
        self.Image_source = image_source
        
        self.maze_2d = np.array([])
        self.height = 0
        self.width = 0
        
        self.image = None

        self.entrance = None
        self.exit = None

        if image_source != None:
            self.get_maze2D(image_source)

    def get_maze2D(self, imgSrc = None):
        """REturn 2D maze of a given image"""

        # If image was provided in constructor
        if imgSrc == None and np.size(self.maze_2d) > 0:
            return self.maze_2d, self.width, self.height

        # Make sure image is provided
        assert imgSrc != None

        # Load and get image data
        self.image = Image.open(imgSrc)
        width, height = self.image.width, self.image.height
        maze = np.reshape(list(self.image.getdata(0)), (width, height))

        # Save data in class variables
        self.maze_2d = maze
        self.width = width
        self.height = height
        
        # Return 2D array of the image pixels, image with, and height
        return maze, width, height

    def get_mazeGraph(self, maze = None, width = None, height = None):

        # It it has already been calculated
        if maze is None and self.entrance is not None and self.exit is not None:
            return self.entrance, self.exit

        def get_entrance(maze, width):
            for col in range(1, width):
                if maze[0][col] == 1:
                    return Node((0, col)), col
            raise Exception("Maze Error: Maze have no entrance on top row")

        def get_exit(maze, width, height):
            for col in range(1, width):
                if maze[height - 1][col] == 1:
                    return Node((height - 1, col)), col
            raise Exception("Maze Error: Maze have no exit on bottom row")
        
        assert maze is not None or self.maze_2d is not None
        if(maze == None):
            maze = self.maze_2d
            width = self.width
            height = self.height

        top_row = [None] * width
        self.entrance, col = get_entrance(maze, width)
        top_row[col] = self.entrance
        
        for row in range(1, height - 1):
            left_node = None
            for col in range(1, width - 1):
                
                # Do nothing on a wall
                if maze[row][col] == 0: continue
                new_node = None
                
                # prev = 1 (left node must exit)
                if maze[row][col - 1] == 1:
                    assert left_node is not None

                    # next = 1
                    if maze[row][col+1] == 1:
                        # top = 1 or bottom = 1
                        if maze[row-1][col] == 1 or maze[row+1][col] == 1:
                            new_node = Node((row, col))
                            new_node.add_neighbor(left_node)
                            left_node.add_neighbor(new_node)
                            left_node = new_node
                        # else do nothing (meaning prev = 1, next = 1, top = 0, and bottom = 0)
                    
                    # next = 0 (Must be end of corridor)
                    else:
                        new_node = Node((row, col))
                        new_node.add_neighbor(left_node)
                        left_node.add_neighbor(new_node)
                        left_node = None
                
                # prev = 0 (No left node)
                else: 
                    # next = 1 (Must be start of a corridor)
                    if maze[row][col+1] == 1:
                        new_node = Node((row, col))
                        left_node = new_node
                    
                    # next = 0
                    else:
                        # top = 0 or bottom = 0 (Must be a dead end)
                        if maze[row-1][col] == 0 or maze[row+1][col] == 0:
                            new_node = Node((row, col))
                            
                        # else do nothing (prev = 0, next = 0, top = 1, bottom = 1)

                if new_node is not None:
                    # top col = 1 (Node exist above)
                    if maze[row - 1][col] == 1 and top_row[col] != None:
                        new_node.add_neighbor(top_row[col])
                        top_row[col].add_neighbor(new_node)

                    # Add new node to top_row if needed
                    top_row[col] = new_node if maze[row+1][col] else None
        
        self.exit, col = get_exit(maze, width, height)
        if(top_row[col] is None): 
            raise Exception("Maze Error: no path to exit")

        self.exit.add_neighbor(top_row[col])
        top_row[col].add_neighbor(self.exit)
        
        return self.entrance, self.exit



    
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

    image_source  = "./examples/tiny.png"
    maze = IMaze(image_source)
    
    maze2d, width, height = maze.get_maze2D()
    print("2D Image Maze")
    print(maze2d)
    print()
    
    maze_entrance, maze_exit = maze.get_mazeGraph()
    print("Maze connected Graph")
    print("Entrance vertex: ", maze_entrance)
    print("Exit Vertex: ", maze_exit)
    
    
    