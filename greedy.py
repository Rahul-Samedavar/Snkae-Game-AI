from random import choice
from copy import deepcopy

class Greedy:
    def __init__(self, x_b, y_b):
        self.x_b = x_b
        self.y_b = y_b

    def adj_cells(self, x, y):
        adj = []
        adj.append((x-1, y)) if x >  0 else ""
        adj.append((x+1, y)) if x < self.x_b else ""
        adj.append((x, y-1)) if y > 0 else ""
        adj.append((x, y+1)) if y < self.y_b  else ""
        return adj

    def dist(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def choose(self, start, dest, walls, n):
        # cells = filter(lambda x: x not in walls, self.adj_cells(*start))
        # safe =  min(cells, key=lambda pos: self.dist(pos, dest)) if cells else choice(self.adj_cells(start))
        # return [safe[i] - x for i, x in enumerate(start)]
        cell, _ = self.get_optimal(start, dest, walls, n)
        return [cell[i] - x for i, x in enumerate(start)]
    
    def get_optimal(self, start, dest, walls, n):
        dist = self.dist(start, dest)
        if dist == 1 or n == 0:
            return dest, dist
        
        cells = {}
        
        w = list(deepcopy(walls))
        w.pop()
        w.insert(0, start)

        for cell in self.adj_cells(*start):
            if cell in walls:
                cells[cell] = self.x_b * self.y_b
            else:
                cells[cell] = self.get_optimal(cell, dest, w, n-1)[1] + 1
        c = min(cells, key = lambda cell: cells[cell])
        return c, cells[c]

    def cycle(self, pos):
        x, y = pos
        if x == 0:
            if y == self.y_b - 1:
                return (1, 0)
            return (0, 1)
        
        if y == 0:
            return (-1, 0)
        
        if y == 1:
            if x == self.x_b - 1:
                return (0, -1)
            if x %2 == 0:
                return (0, 1)
            return (1, 0)
        
        if y == self.y_b - 1:
            if x % 2 == 0:
                return (1, 0)
            return (0, -1)
        
        if x % 2 == 0:
            return (0, 1)
        return (0, -1)