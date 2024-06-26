from typing import List, Optional
import random
import math


def fade(t: float) -> float:
    """Функция для вычисления fade функции для генерации Perlin шума."""
    return t * t * t * (t * (t * 6 - 15) + 10)


def lerp(t: float, a: float, b: float) -> float:
    """Функция для выполнения линейной интерполяции между двумя значениями a и b."""
    return a + t * (b - a)


def grad(hash: int, x: float, y: float) -> float:
    """Функция для вычисления градиента для генерации Perlin шума."""
    h = hash & 15
    u = x if h < 8 else y
    v = y if h < 4 else (x if h in (12, 14) else 0)
    return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)


def perlin(x: float, y: float, permutation: List[int]) -> float:
    """Функция для генерации двумерного Perlin шума."""
    p = permutation + permutation
    X = math.floor(x) & 255
    Y = math.floor(y) & 255
    x -= math.floor(x)
    y -= math.floor(y)
    u = fade(x)
    v = fade(y)
    A = p[X] + Y
    AA = p[A]
    AB = p[A + 1]
    B = p[X + 1] + Y
    BA = p[B]
    BB = p[B + 1]

    return lerp(v, lerp(u, grad(p[AA], x, y),
                            grad(p[BA], x - 1, y)),
                   lerp(u, grad(p[AB], x, y - 1),
                            grad(p[BB], x - 1, y - 1)))


def generate_permutation_table(seed: Optional[int] = None) -> List[int]:
    """Функция для генерации таблицы перестановок для генерации Perlin шума."""
    permutation = list(range(256))
    if seed is not None:
        random.seed(seed)
    random.shuffle(permutation)
    return permutation
