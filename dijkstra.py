from collections import deque
from node import Node
from pq import PQ

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

    visited = {}
    explored = {}

    # visited[Node] = (previous node, distance from previous node)
    visited[start] = (None, 0)
    
    # pq.enqueue accepts value = Node, and priority = distance
    pq = PQ()
    pq.enqueue(start, 0)
    traversal_order = deque()
    total_distance = 0

    print("PQ: ", pq)
    print()

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

            # Add to PQ
            if not (node in visited):
                pq.enqueue(node, new_distance)
                visited[node] = (current_node, new_distance)

            # Update distance or priority in PQ
            elif not (node in explored) and visited[node][1] > new_distance:
                # print("Remove", (node, visited[node][1]))
                pq.remove(node, visited[node][1])
                # print(pq.removed)
                pq.enqueue(node, new_distance)
                visited[node] = (current_node, new_distance)
    
        explored[current_node] = True

        print("Pop min: ", (current_node, total_distance))
        print("Neighbors", current_node.get_neighbors())
        print("PQ: ", pq)
        print("Visited", visited)
        print("explored", explored)
        print(pq.removed)
        print()
    

    path = deque()
    while target != None and target in visited:
        path.appendleft(target)
        target = visited[target][0]

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