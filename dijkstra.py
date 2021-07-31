from collections import deque
from node import Node
from pq import PQueue

def dijkstra(start, target, order: bool = False) -> list:
    """
    Dijkstra Algorithm: Find Shortest path between two Nodes

    input start: Start of a Linked graph
    input target: Last Node to end path
    input order: If set to true, track and return traversal order
    return: path = Shortest path = list of connected Nodes from start to target
    """
    # AVOID ANY SURPRISES
    assert isinstance(start, Node) and isinstance(target, Node)

    # Define containers
    pq = PQueue()   # Priority queue: values = [(job, priority), ... ]
    visited = {} # Visited, but not explored
    explored = {} # Visited and explored

    
    # visited[Node] = (previous node, distance from previous node)
    visited[start] = (None, 0)
    # pq.enqueue: parameters = (Node, distance from start to this node)
    pq.enqueue(start, 0)

    traversal_order = deque()
    total_distance = 0

    while pq.size() > 0:
        # Pop and explore node with smallest distance from start node
        # Rem: priority = distance from start to current node
        (current_node, total_distance) = pq.dequeue(return_priority=True)

        # Store traversal order and stop after reaching target
        if(order == True): traversal_order.append(current_node)
        if current_node == target: break
        
        # Visit all neighbors of current node
        for neighbor in current_node.get_neighbors():
            # neighbor = (node, distance) for weighted graph
            (node, distance) = neighbor
            new_distance = total_distance + distance

            # Add to PQ if not visited
            if not (node in visited):
                pq.enqueue(node, new_distance)
                visited[node] = (current_node, new_distance)

            # If visited, but new distance is smaller
            elif not (node in explored) and visited[node][1] > new_distance:
                # Remove from pQ and enqueue same node with new distance/priority
                # Also updated the visited set
                pq.remove(node, visited[node][1])
                pq.enqueue(node, new_distance)
                visited[node] = (current_node, new_distance)

        # A Node is explored after visiting all it's neighbors
        explored[current_node] = True    

    # Trace path from target to root
    path = deque()
    while target != None and target in visited:
        path.appendleft(target)
        target = visited[target][0]

    # Return path and total distance from start to target (And traversal order if needed)
    if order == True: return path, total_distance, traversal_order
    return path, total_distance

if __name__ == "__main__":
    # Creating a linked graph
    root = Node(1)
    node2 = Node(2)
    root.add_neighbor(node2, 2)
    node2.add_neighbor(root, 2)
    
    node3 = Node(3)
    root.add_neighbor(node3, 3)
    node3.add_neighbor(root, 3)
    
    node4 = Node(4)
    node2.add_neighbor(node4, 4)
    node4.add_neighbor(node2, 4)

    node3.add_neighbor(node4, 2)

    node5 = Node(5)
    node3.add_neighbor(node5, 6)
    node5.add_neighbor(node3, 6)

    target = Node(6)
    node4.add_neighbor(target, 5)
    target.add_neighbor(node4, 5)

    node4.add_neighbor(node3, 2)
    
    
    print("Dijkstra Algorithm")
    path, total_distance, traversal_order = dijkstra(root, target, order=True)
    print("Total distance: ", total_distance)
    print("Path: ", path)
    print("Traversal order: ", traversal_order)