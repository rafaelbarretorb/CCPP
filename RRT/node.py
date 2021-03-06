#!/usr/bin/env python

class Node(object):
    def __init__(self, point, parent, cost=0.0, id=0):
        super(Node, self).__init__() # parent is a Node too
        self.point = point  # position
        self.parent = parent  # parent Node
        self.cost = cost  # only for RRT* variations
        self.id = id  # only for RRT*-Smart