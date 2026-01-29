"""
models.py
---------
Structures de données principales pour le solveur MPVRP-CC
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class Vehicle:
    id: int
    capacity: float
    home_garage: int
    initial_product: int

    current_product: int = field(init=False)
    route: List[Tuple] = field(default_factory=list)
    load: float = field(default=0.0)

    def __post_init__(self):
        self.current_product = self.initial_product

    def reset(self):
        """Réinitialise l'état du véhicule"""
        self.current_product = self.initial_product
        self.route.clear()
        self.load = 0.0


@dataclass
class Depot:
    id: int
    x: float
    y: float
    stock: Dict[int, float]  # produit -> quantité disponible


@dataclass
class Garage:
    id: int
    x: float
    y: float


@dataclass
class Station:
    id: int
    x: float
    y: float
    demand: Dict[int, float]  # produit -> demande restante


@dataclass
class Instance:
    uuid: str
    num_products: int
    vehicles: List[Vehicle]
    depots: List[Depot]
    garages: List[Garage]
    stations: List[Station]
    transition_costs: List[List[float]]
