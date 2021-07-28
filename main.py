from maze import create_2Dmaze
from bfs import bfs
from dijkstra import dijkstra


def print_path(path) -> None:
    for node in path:
        print(node)
    
def main():
    
    maze_start, maze_end = create_2Dmaze("./examples/tiny.png")
    
    # Path of unweighted maze
    print("Unweighted maze path:")
    bfs_path = bfs(maze_start, maze_end)
    print_path(bfs_path)
    
    # print()
    
    # Path of unweighted maze
    # print("Weighted maze path (Shortest path):")
    # shortest_path = dijkstra(maze_start, maze_end, True)
    # print_path(shortest_path)

if __name__ == "__main__":
    main()
    