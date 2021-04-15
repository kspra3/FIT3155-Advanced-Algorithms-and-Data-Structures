"""
K. Sharsindra Pratheen
25636626
"""
# Parts of code obtained from geeksforgeeks.org and github.com
# Greatly modified them to follow assignment specifications and requirements.
# Majority of the concepts, implementations and pseudo-codes are from lectures and tutorials.

import heapq
from collections import Counter


class Node:
    # Initialising the variables.
    def __init__(self, char, mark):
        self.left = None
        self.right = None
        self.char = char
        self.mark = mark

    # Asserting less than condition.
    def __lt__(self, other):
        return self.mark < other.mark


def values(code):
    # Getting the unique characters.
    characters = Counter(code)
    # Initialising the heap.
    heap = []
    for i in characters:
        node = Node(i, characters[i])
        heapq.heappush(heap, node)
    root = heap[0]
    while len(heap) > 1:
        lefty = heapq.heappop(heap)
        righty = heapq.heappop(heap)
        build = Node(lefty.char + righty.char, lefty.mark + righty.mark)
        build.left = lefty
        build.right = righty
        root = build
        heapq.heappush(heap, build)
    binary = {}
    make_bin(root, "", binary)
    return binary, root


def make_bin(edge, string, bin_rep):
    if edge is None:
        return
    if edge.left is None and edge.right is None:
        if len(string) == 0:
            bin_rep[edge.char] = "1"
        else:
            bin_rep[edge.char] = string
        return
    make_bin(edge.left, string + "0", bin_rep)
    make_bin(edge.right, string + "1", bin_rep)
