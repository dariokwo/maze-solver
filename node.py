# -*- coding: utf-8 -*-
from typing import Deque

class Node:
    class Edge:
        def __init__(self, neighbor, distance = 1):
            self.Neighbor = neighbor
            self.Distance = distance

    def __init__(self, value) -> None:
        self.Value = value
        # edges = [(neighbor, distance), ...]
        # All distances = 1 for unweighted graphs
        self.edges = []
        

    def set_value(self, value):
        """Sets the value for this node"""
        self.Value = value
    
    def get_value(self):
        """Returns the value of this node"""
        return self.Value

    def add_edge(self, neighbor, distance = 1) -> None:
        """Add an edge to the list of edges for this node"""

        # SORRY NOT SORRY!
        assert isinstance(neighbor, Node)
        # edge = [(neighbor, distance), ...]
        # distance = 1, for unweighted graph
        self.edges.append(Node.Edge(neighbor, distance))

    def get_edges(self):
        """Return all edges (without weights)"""
        return [edge.Neighbor for edge in self.edges]

    def get_edges_weighted(self):
        """Return all edges (with weights)"""
        return [(edge.Neighbor, edge.Distance) for edge in self.edges]

    def __str__(self):
        """Returns a string representation of this node's value"""
        # Prints the current node value
        return "{}".format(self.Value)
        
    def __repr__(self):
        return self.__str__()


# Test Example
if __name__ == "__main__":
    root = Node(1)
    
    # Testing get_value
    assert root.get_value() == 1
    node2 = Node(2)

    # Testing set_value
    node2.set_value(88)
    assert node2.get_value() == 88

    # Tesing add_edge, get_edges, and get_edges_weighted
    root.add_edge(node2)
    node2.add_edge(root)
    assert root.get_edges() == [node2]
    assert root.get_edges_weighted() == [(node2, 1)]
    
    node3 = Node(3)
    root.add_edge(node3)
    node3.add_edge(root)
    node2.add_edge(node3)

    assert root.__str__() == "1"
    assert root.get_value() == 1
    assert len(root.get_edges()) == 2