from collections import deque

from maze import IMaze
import dijkstra
import bfs
import dfs


def print_Graph_EdgeList(start_node):
    visited = {start_node: True}
    queue = deque([start_node])
    
    while len(queue) > 0:
        node = queue.pop()
        print("[Node{} Neighbors: [".format(node), end=" ")
        
        for neighbor in node.get_neighbors():
            if neighbor not in visited:
                queue.appendleft(neighbor)
                visited[neighbor] = True
            
            print(neighbor, end=", ")
            
        print(']')
    
def main():
    
    image_source  = "./examples/tiny.png"
    maze = IMaze(image_source)
    
    maze2d, width, height = maze.get_maze2D()
    print("2D Image Maze")
    print(maze2d)
    print()
    
    maze_entrance, maze_exit = maze.get_mazeGraph()
    print("Maze connected Graph")
    print_Graph_EdgeList(maze_entrance)
    print()
    
    print("Entrance vertex: ", maze_entrance)
    print("Exit Vertex: ", maze_exit)
    print()
    
    path, traversal_order  = bfs.bfs(maze_entrance, maze_exit, order=True)
    print("Find Path from Entrance to Exit using Bread First Search")
    print("Path", path)
    print("Traversal Order", traversal_order)
    print()
    
    path, traversal_order  = dfs.dfs(maze_entrance, maze_exit, order=True)
    print("Find Path from Entrance to Exit using Depth First Search")
    print("Path", path)
    print("Traversal Order", traversal_order)
    print()
    
    path, traversal_order  = dfs.dfs_recursive(maze_entrance, maze_exit, order=True)
    print("Find Path from Entrance to Exit using Recursive Depth First Search")
    print("Path", path)
    print("Traversal Order", traversal_order)
    print()

    print("Find Shortest Path and distance from Entrance to Exit using Dijkstra's Algorithm")
    path, total_distance, traversal_order = dijkstra.dijkstra(maze_entrance, maze_exit, order=True)
    print("Total distance: ", total_distance)
    print("Path: ", path)
    print("Traversal order: ", traversal_order)
    

if __name__ == "__main__":
    main()
    