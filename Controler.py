import numpy as np


class Controler:
    def __init__(self, x_l, y_l, snake):
        self.x_l = x_l
        self.y_l = y_l
        self.snake = snake
        self.food_pos = None
        self.path = []

    def adj_cells(self, x, y):
        adj = []
        adj.append((x-1, y)) if x >  0 else ""
        adj.append((x+1, y)) if x < self.x_l-1 else ""
        adj.append((x, y-1)) if y > 0 else ""
        adj.append((x, y+1)) if y < self.y_l-1  else ""
        return adj
    
    def dist(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def move(self, food_pos):
        if food_pos != self.food_pos or self.path == []:
            self.food_pos = food_pos
            self.find_path()
        self.snake.move_to(*self.path.pop(0))

    def find_path(self):
        walls = np.zeros(shape=(self.x_l, self.y_l))
        for i, (x, y) in enumerate(self.snake.body()):
            walls[x][y] = i + 1
        self.path, _ = self.find_optimal(self.snake.pos, self.food_pos, walls, s=0, n=5)

    def find_optimal(self, start, dest, walls, s, n):
        adj_cells = [(x, y) for x, y in self.adj_cells(*start) if walls[x][y] < s]

        if adj_cells == []:
            return [(start[0]+1, start[1])], 99999
        
        for cell in adj_cells:
            if cell == dest:
                return [dest], 0
        
        optimal_path = []
        min_dist = 99999
        for cell in adj_cells:
            
            if n:
                walls[cell[0]][cell[1]] = walls[start[0]][start[1]] + 1
                path, dist = self.find_optimal(cell, dest, walls, s+1, n-1)
                walls[cell[0]][cell[1]] = 0
            else:
                path = [cell]
                dist = self.dist(cell, dest)

            if dist == 0:
                path.insert(cell, 0)
                return path, 0

            if dist < min_dist:
                min_dist = dist
                path.insert(cell, 0)
                optimal_path = path
        return optimal_path, min_dist+1
        
