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

        def calculate_distance(node1, node2):
            coor1 = node1.get_value()
            coor2 = node2.get_value()
            return abs(coor1[0] - coor2[0]) + abs(coor1[1] - coor2[1])
        
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
                            distance = calculate_distance(left_node, new_node)
                            new_node.add_edge(left_node, distance)
                            left_node.add_edge(new_node, distance)
                            left_node = new_node
                        
                        # else do nothing (meaning prev = 1, next = 1, top = 0, and bottom = 0)
                    
                    # next = 0 (Must be end of corridor)
                    else:
                        new_node = Node((row, col))
                        distance = calculate_distance(left_node, new_node)
                        new_node.add_edge(left_node, distance)
                        left_node.add_edge(new_node, distance)
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
                        distance = calculate_distance(top_row[col], new_node)
                        new_node.add_edge(top_row[col], distance)
                        top_row[col].add_edge(new_node, distance)

                    # Add new node to top_row if needed
                    top_row[col] = new_node if maze[row+1][col] else None
        
        self.exit, col = get_exit(maze, width, height)
        if(top_row[col] is None): 
            raise Exception("Maze Error: no path to exit")
        distance = calculate_distance(top_row[col], self.exit)
        self.exit.add_edge(top_row[col], distance)
        top_row[col].add_edge(self.exit, distance)
        
        return self.entrance, self.exit
            

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
    
    
    