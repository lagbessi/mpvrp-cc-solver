"""
distance.py
-----------
Fonctions de calcul de distances géographiques
"""

import math


def euclidean(a, b) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
