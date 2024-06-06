import math
import random


def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def lerp(t, a, b):
    return a + t * (b - a)


def grad(hash, x, y):
    h = hash & 15
    u = x if h < 8 else y
    v = y if h < 4 else (x if h in (12, 14) else 0)
    return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)


def perlin(x, y, permutation):
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


def generate_permutation_table(seed=None):
    permutation = list(range(256))
    if seed is not None:
        random.seed(seed)
    random.shuffle(permutation)
    return permutation
