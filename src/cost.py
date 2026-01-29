"""
cost.py
-------
Gestion des coûts de changement de produit
"""


def changeover_cost(instance, from_product: int, to_product: int) -> float:
    return instance.transition_costs[from_product][to_product]
