# -*- coding: utf-8 -*-
class Node:
    def __init__(self, value) -> None:
        self.Value = value
        self.Neighbors = [] # Neighbors = [Node, ...]

    def set_value(self, value):
        self.Value = value
    
    def get_value(self):
        return self.Value

    def add_neighbor(self, neighbor, distance = None) -> None:
        # SORRY NOT SORRY!
        assert isinstance(neighbor, Node)
        
        # In case of weighted graph
        # So, Neighbors = [(Node, distance), ...]
        if distance != None: neighbor = (neighbor, distance)
        self.Neighbors.append(neighbor)

    def get_neighbors(self):
        return self.Neighbors

    def __str__(self):
        # Prints the current node value
        return "{}".format(self.Value)
        
    def __repr__(self):
        return self.__str__()


# Test Example
if __name__ == "__main__":
    root = Node(1)
    
    # Testing get_value and get_priority
    assert root.get_value() == 1
    node2 = Node(2)

    # Testing set_value
    node2.set_value(88)
    assert node2.get_value() == 88

    # Tesing add_neighbor and get_neighbor
    root.add_neighbor(node2)
    node2.add_neighbor(root)
    
    node3 = Node(3)
    root.add_neighbor(node3)
    node3.add_neighbor(root)
    node2.add_neighbor(node3)

    assert root.__str__() == "1"
    assert root.get_value() == 1
    assert len(root.get_neighbors()) == 2