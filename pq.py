"""
Priority Queue (PQ) Implementation
"""
from collections import deque

class PQueue:
    class Job:
        """Jobs to be stored in a priority queue (PQueue)"""
        def __init__(self, task, priority):
            self.Task = task
            self.Priority = priority
    
    def __init__(self, qtype: str = "MIN") -> None:
        # Initializing priority queue
        self.pQueue = []
        self.qLength = 0
        self.qType = "MIN" if qtype.upper() in ["MIN", "MINIMUM"] else "MAX"

        # It's quite expensive to remove or update a job's value or priority
        # So we can just mark it as removed (and add an updated version to the queue)
        # This is bad if many/most elements in the queue are in removed set
        # Solution idea: Maybe re-heapify after a certain threshold is reached
        # A threshold can be a ratio of removed and total number of elements
        self.removed = {}

    def enqueue(self, task, priority) -> None:
        """Adds an element to the Priority queue"""

        # if job exist in removed set with same priority
        # Just remove it from the removed set and do nothing (Don't enqueue)
        if self._is_removed(task, priority):
            del self.removed[task]
            self.qLength += 1
            return

        # Append new job to end of queue
        # then bubble it up to the right position
        self.pQueue.append(PQueue.Job(task, priority))
        self.qLength += 1
        self._bubble_up()

    def dequeue(self, return_priority: bool = False) -> object:
        """Remove and return MIN/MAX element from queue"""
        assert self.size() > 0

        # Store top/job with min priority and pop it out
        # then bubble down last job from top of queue to right position
        self._swap(0, len(self.pQueue) - 1)
        job = self.pQueue.pop()
        self._bubble_down()

        task = job.Task
        priority = job.Priority

        # If this task has been removed, ignore it
        # and dequeue the next one
        if self._is_removed(task, priority):
            del self.removed[task]
            return self.dequeue(return_priority)

        # Reduce queue size and return task (with priority if needed)
        self.qLength -= 1
        if(return_priority == False): return task
        return task, priority

    def remove(self, task, priority = None) -> None:
        """Delete a job in PQueue by adding it in removed set and decreasing queue size"""
        
        # The priority is important if the removed job is re-enqueued
        # with different priority

        self.removed[task] = priority
        self.qLength -= 1

    def _is_removed(self, task, priority = None):
        return task in self.removed and self.removed[task] == priority


    def size(self) -> int:
        """Returns number of jobs in pQueue"""
        return self.qLength

    def get_queue(self) -> deque:
        """Return the whole pQueue"""
        return deque(self.pQueue)

    ##### Magic Methods ######
    def __str__(self):
        """Return string representation of the PQueue"""
        result = ""
        for job in self.pQueue:
            result += "({},{}), ".format(job.Task, job.Priority)
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
        """
        Compare two job and 
        return true if the parent have less priority than child in case of MIN PQ
        or else return true if the parent have high priority than child in case of MAX PQ
        """
        parent_node = self.pQueue[parent_index]
        child_node = self.pQueue[child_index]

        # Parent should have smaller or equal priority to chidren in MIN PQ
        if self.qType == "MIN":
            return parent_node.Priority <= child_node.Priority

        # Parent should have larger or equal priority to chidren in MAX PQ
        return parent_node.Priority >= child_node.Priority

    def _swap(self, index1:int, index2:int) -> None:
        """Swap values in a pQueue in place"""
        self.pQueue[index1], self.pQueue[index2] = self.pQueue[index2], self.pQueue[index1]


if __name__ == "__main__":
    """Testing"""
    pq = PQueue()

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

