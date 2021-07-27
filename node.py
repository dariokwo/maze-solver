# -*- coding: utf-8 -*-
class Node:
    def __init__(self, value, priority) -> None:
        self.Value = value
        self.Priority  = priority
        self.Neighbors = [] # Neighbors = [Node, ...]

    ###### Setters ######
    def set_value(self, value):
        self.Value = value

    def add_neighbor(self, neighbor, distance = None) -> None:
        # SORRY NOT SORRY!
        assert isinstance(neighbor, Node)
        
        # If distance is provided, then this is a weighted graph
        # So, Neighbors = [(Node, distance), ...]
        if distance != None:
            neighbor = (neighbor, distance)
        
        self.Neighbors.append(neighbor)

    ###### Getters ######
    def get_value(self):
        return self.Value

    def get_neighbors(self):
        return self.Neighbors

    ###### Magic methods ######
    def __str__(self):
        # Prints the current node value
        return "Node({})".format(self.Value)
        
    def __repr__(self):
        return self.__str__()


# Test Example
if __name__ == "__main__":
    root = Node(1)
    node2 = Node(2)
    node3 = Node(3)

    root.add_neighbor(node2)
    node2.add_neighbor(root)

    root.add_neighbor(node3)
    node3.add_neighbor(root)

    node2.add_neighbor(node3)

    print(root)
    print(root.get_neighbors())