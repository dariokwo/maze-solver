# -*- coding: utf-8 -*-
from collections import deque
from node import Node

def dfs(root, target, order: bool = False) -> deque:
    """
    DFS to find path between two Nodes

    input root: Root of a Linked graph
    input target: Last Node to end path
    input order: If set to true, track and return traversal order
    return: path = List of connected Nodes from root to target

    Time complexity: O(V+E)
    Space complexity: O(V)
    """
    # AVOID ANY SURPRISES
    assert isinstance(root, Node) and isinstance(target, Node)
    
    visited = {} # key = current node, value = previous node
    stack = deque([root])
    visited[root] = None
    traversal_order = deque()
    
    while len(stack) > 0:
        
        current_node = stack.pop()
        # Track traversal order (Only if needed)
        if(order == True): traversal_order.append(current_node)
        # Stop after reaching target
        if current_node == target: break
        
        # Push all neighbors to our stack
        for neighbor in current_node.get_edges():
            if not (neighbor in visited):
                stack.append(neighbor) # LIFO
                visited[neighbor] = current_node

    # Trace path from target to root
    path = deque()
    while target != None and target in visited:
        path.appendleft(target)
        target = visited[target]

    # Return path (And traversal order if needed)
    if order == True: return path, traversal_order
    return path

def dfs_recursive(root, target, order: bool = False) -> deque:
    """Depth First Algorithm using recursive method"""

    # AVOID ANY SURPRISES
    assert isinstance(root, Node) and isinstance(target, Node)

    visited = {}
    traversal_order = deque()

    def recur(root, previous = None):
        visited[root] = previous
        # Track traversal order (Only if needed)
        if order == True: traversal_order.append(root)
        # Stop after reaching target node
        if root == target: return
        
        # Visit all neighbors
        for neighbor in root.get_edges():
            if not (neighbor in visited):
                recur(neighbor, root)

    recur(root)
    # Trace path from target to root
    path = deque()
    while target != None and target in visited:
        path.appendleft(target)
        target = visited[target]

    # Return path (And traversal order if needed)
    if order == True: return path, traversal_order
    return path

if __name__ == "__main__":
    # Creating a linked graph
    root = Node(1)
    node2 = Node(2)
    root.add_edge(node2)
    node2.add_edge(root)
    
    node3 = Node(3)
    root.add_edge(node3)
    node3.add_edge(root)
    
    node4 = Node(4)
    node2.add_edge(node4)
    node4.add_edge(node2)

    node3.add_edge(node4)

    node5 = Node(5)
    node3.add_edge(node5)
    node5.add_edge(node3)

    target = Node(6)
    node4.add_edge(target)
    target.add_edge(node4)

    node4.add_edge(node3)
    
    # Depth First Search
    path, traversal_order  = dfs(root, target, order=True)
    assert path == deque([root, node3, node4, target])
    assert traversal_order == deque([root, node3, node5, node4, target])
    
    # Depth First Search Recursive Algorithm
    path, traversal_order  = dfs_recursive(root, target, order=True)
    assert path == deque([root, node2, node4, target])
    assert traversal_order == deque([root, node2, node4, target, node3, node5])