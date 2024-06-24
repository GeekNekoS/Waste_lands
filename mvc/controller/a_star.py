import heapq


class AStar:
    """Класс AStar реализует алгоритм A* для поиска кратчайшего пути в игровом мире."""
    def __init__(self, obstacles=None):
        """Инициализация объекта AStar."""
        self.obstacles = set(obstacles if obstacles else [])

    def heuristic(self, start, goal):
        """Манхэттенское расстояние между двумя точками."""
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    def get_neighbors(self, node):
        """Получение соседних узлов для заданного узла."""
        x, y = node
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        valid_neighbors = [(nx, ny) for nx, ny in neighbors if
                           (nx, ny) not in self.obstacles]
        return valid_neighbors

    def find_path(self, start, goal):
        """Поиск кратчайшего пути от стартовой до целевой точки в игровом мире."""
        if goal in self.obstacles:
            print("Goal is inside an obstacle")
            return []

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

        print("Path not found")
        return []
