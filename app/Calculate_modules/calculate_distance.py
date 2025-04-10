import math
from decimal import Decimal


def calculate_distance(loc1: list, loc2: list) -> float:
    return math.sqrt(Decimal(loc1[0] - loc2[0]) ** 2
                     + Decimal(loc1[1] - loc2[1]) ** 2)
