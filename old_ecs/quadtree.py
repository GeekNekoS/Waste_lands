import pygame


class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # Pygame Rect
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary
        nw = pygame.Rect(x, y, w / 2, h / 2)
        ne = pygame.Rect(x + w / 2, y, w / 2, h / 2)
        sw = pygame.Rect(x, y + h / 2, w / 2, h / 2)
        se = pygame.Rect(x + w / 2, y + h / 2, w / 2, h / 2)
        self.northwest = QuadTree(nw, self.capacity)
        self.northeast = QuadTree(ne, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.divided = True

    def insert(self, point):
        if not self.boundary.collidepoint(point):
            return False
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        if not self.divided:
            self.subdivide()
        if self.northwest.insert(point):
            return True
        if self.northeast.insert(point):
            return True
        if self.southwest.insert(point):
            return True
        if self.southeast.insert(point):
            return True
        return False

    def query(self, range, found):
        if not self.boundary.colliderect(range):
            return
        for p in self.points:
            if range.collidepoint(p):
                found.append(p)
        if self.divided:
            self.northwest.query(range, found)
            self.northeast.query(range, found)
            self.southwest.query(range, found)
            self.southeast.query(range, found)
