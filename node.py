# -*- coding: utf-8 -*-
class Node:
    def __init__(self, value, priority = None) -> None:
        self.Value = value
        self.Priority  = priority # To be use by priority queue
        self.Neighbors = [] # Neighbors = [Node, ...]

    ###### Setters ######
    def set_value(self, value):
        self.Value = value

    def set_priority(self, priority):
        self.Priority  = priority

    def add_neighbor(self, neighbor, distance = None) -> None:
        # SORRY NOT SORRY!
        assert isinstance(neighbor, Node)
        
        # This can be use as a Node for weighted graph
        # So, Neighbors = [(Node, distance), ...]
        if distance != None:
            neighbor = (neighbor, distance)
        
        self.Neighbors.append(neighbor)

    ###### Getters ######
    def get_value(self):
        return self.Value

    def get_priority(self):
        return self.Priority

    def get_neighbors(self):
        return self.Neighbors

    ###### Magic methods ######
    def __str__(self):
        # Prints the current node value
        return "{}".format(self.Value)
        
    def __repr__(self):
        return self.__str__()


# Test Example
if __name__ == "__main__":
    root = Node(1, 2)
    
    # Testing get_value and get_priority
    assert root.get_value() == 1
    assert root.get_priority() == 2

    node2 = Node(2)

    # Testing set_value and set_priority
    node2.set_value(88)
    node2.set_priority(9)
    assert node2.get_value() == 88
    assert node2.get_priority() == 9

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