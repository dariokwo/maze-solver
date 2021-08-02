"""
Priority Queue (PQ) Implementation
"""

from collections import deque
from node import Node

class PQ:
    def __init__(self, type_: str = "MIN") -> None:
        # Initializing a priority queue
        self.pQueue = []
        self.length = 0
        self.type = "MIN" if type_.upper() in ["MIN", "MINIMUM"] else "MAX"

        # It's quite expensive to remove a job or update it's priority or value in the queue; O(nlog(n))
        # So we can just mark it as removed (and enqueue an updated version)
        # Next time we dequeue an element mark as removed, we discard it, and dequeue the next one

        # This can become bad if many/most jobs in the queue are marked as removed
        # Solution idea: re-heapify after a certain threshold is reached
        # A threshold can be a ratio of removed and total number of jobs in the queue
        self.removed = {}

    def enqueue(self, value, priority) -> None:
        """Adds an element to the Priority queue"""

        # if job exist in removed set with same priority
        # Just remove it from the removed set and do nothing (Don't enqueue)
        if(value in self.removed and self.removed[value] == priority):
            del self.removed[value]
            self.length += 1
            return

        # Add job and bubble up to the right position
        self.pQueue.append(Node(value, priority))
        self.length += 1
        self._bubble_up()

    def dequeue(self, return_priority: bool = False) -> object:
        """Remove and return MIN/MAX element from queue"""
        assert self.size() > 0

        # Store top/job with min priority and pop it out
        # Move last job to top and bubble down to the right position
        result = self.pQueue[0]
        self.pQueue[0] = self.pQueue[len(self.pQueue) - 1]
        self.pQueue.pop()
        self._bubble_down()

        value = result.get_value()
        priority = result.get_priority()

        # If this job, with same priority, has been mark as removed, ignore it
        # and dequeue the next one
        if result.get_value() in self.removed and self.removed[value] == priority:
            del self.removed[value]
            return self.dequeue(return_priority)

        # Reduce queue size and return result
        self.length -= 1
        if(return_priority == False): return value
        return value, priority

    def remove(self, value, priority) -> None:
        """Deleting an element in PQ"""
        # Add to removed set and decrease length of queue

        # The priority is important here
        # Imagine if we re-enqueue a job with this value?
        # When we dequeued it later, it will be marked as removed even if it's the recent one
        # So we need the priority to tell them apart
        # If we try to re-enqueued it with same priority, then just remove it from removed set
        self.removed[value] = priority
        self.length -= 1

    def size(self):
        """Returns count of elements in pQueue"""
        return self.length

    def get_queue(self):
        """Return the whole queue"""
        return deque(self.pQueue)

    ##### Magic Methods ######
    def __str__(self):
        """Return string representation of the Priority queue"""
        result = ""
        for node in self.pQueue:
            result += "({},{}), ".format(node.get_value(), node.get_priority())
        return "[" + result + "]"

    ##### PQ SPECIFIC FUNCTIONS #####
    def _bubble_up(self):
        """Move child node up base on compare"""
        child_index = len(self.pQueue) - 1
        while child_index > 0:
            parent_index = (child_index - 1)//2
            
            # Bubble only  if check condition is not met
            if self._check(parent_index, child_index): break
            self._swap(child_index, parent_index)

            parent_index = child_index

    def _bubble_down(self) -> None:
        """Move root node down base on compare"""
        parent_index = 0
        while True:
            # Calculate and verify left/first child index
            child_index = (parent_index * 2) + 1
            if child_index > len(self.pQueue) - 1: break

            # Calculate and verify right/second child index
            second_child = (parent_index * 2) + 2
            if second_child < len(self.pQueue):
                child_index = second_child

            # Bubble only  if check condition is not met
            if self._check(parent_index, child_index): break
            self._swap(child_index, parent_index)

            parent_index = child_index

    def _check(self, parent_index:int, child_index:int) -> bool:
        """Compare two node"""
        parent_node = self.pQueue[parent_index]
        child_node = self.pQueue[child_index]

        # Parent should have smaller or equal priority to chidren in MIN PQ
        if self.type == "MIN":
            return parent_node.get_priority() <= child_node.get_priority()

        # Parent should have larger or equal priority to chidren in MAX PQ
        return parent_node.get_priority() >= child_node.get_priority()

    def _swap(self, index1:int, index2:int) -> None:
        """Swap values in a pQueue in place"""
        self.pQueue[index1], self.pQueue[index2] = self.pQueue[index2], self.pQueue[index1]


if __name__ == "__main__":
    """Testing"""
    pq = PQ()

    # Testing enqueue
    pq.enqueue(1, 0)
    pq.enqueue(3, 8)
    pq.enqueue(4, 2)
    pq.enqueue(5, 3)
    assert pq.__str__() == "[(1,0), (5,3), (4,2), (3,8), ]"

    # Testing size and dequeue
    assert pq.size() == 4
    assert pq.dequeue() == 1
    assert pq.size() == 3
    pq.__str__ == "[(4,2), (5,3), (3,8), ]"
    assert pq.dequeue() == 4
    assert pq.size() == 2
    assert pq.__str__() == "[(5,3), (3,8), ]"
    pq.enqueue(4, 2)
    assert pq.size() == 3
    pq.__str__() == "[(4,2), (5,3), (3,8), ]"
    

    # Testing remove
    pq.remove(4, 2)
    assert pq.size() == 2
    assert pq.__str__() == "[(4,2), (3,8), (5,3), ]"
    assert pq.removed == {4:2}

    assert pq.dequeue() == 5
    assert pq.removed == { }
    assert pq.size() == 1
    assert pq.__str__() == "[(3,8), ]"

