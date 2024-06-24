import heapq


class AStar:
    def __init__(self, grid_width, grid_height, obstacles=None):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.obstacles = set(obstacles if obstacles else [])

    def heuristic(self, start, goal):
        # Манхэттенское расстояние
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    def get_neighbors(self, node):
        x, y = node
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        valid_neighbors = [(nx, ny) for nx, ny in neighbors if
                           0 <= nx < self.grid_width and 0 <= ny < self.grid_height and (nx, ny) not in self.obstacles]
        return valid_neighbors

    def find_path(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1  # Всегда 1, если нет других затрат

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # Если не удалось найти путь
        print("Path not found")
        return []
