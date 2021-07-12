# Utility classes for queue, stack and node


# Node Class, structure for blocks of data 

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


# class for a FIFO queue

class nodeQueue():
    # define initial state
    def __init__(self):
        # an empty array called the horizon
        self.horizon = []

    # add a node 
    def add(self, node):
        self.horizon.append(node)

    # check the state of a node
    def state(self, state):
        return any(node.state == state for node in self.horizon)

    #check if empty
    def isEmpty(self):
        return len(self.horizon) == 0

    # remove node
    def remove(self):
        # if the queue is empty raise error
        if self.isEmpty():
            raise Exception("Empty, no items on the horizon")
        # else go to the node at index 0 
        # remove the node at index 0
        else:
            node = self.horizon[0]
            self.horizon = self.horizon[1:]
            return node


# Stack Class LIFO, inherits from queue but remove is dif
class nodeStack(nodeQueue):
     # pop a node off the stack
    def remove(self):
        # if stack is empty the raise exception
        if self.isEmpty():
            raise Exception("Empty, nothing on the horizon")
        # else go wrap around to the last node via -1, 
        # remove it and return the removed node
        else:
            node = self.horizon[-1]
            self.horizon = self.horizon[:-1]
            return node
