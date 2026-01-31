from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class Vehicle:
    id: int
    capacity: float
    home_garage: int
    initial_product: int
    route: List[Tuple] = field(default_factory=list)

@dataclass
class Depot:
    id: int
    x: float
    y: float
    stock: Dict[int, float]
    original_stock: Dict[int, float] = field(default_factory=dict)

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
    demand: Dict[int, float]
    original_demand: Dict[int, float]

@dataclass
class Instance:
    uuid: str
    num_products: int
    vehicles: List[Vehicle]
    depots: List[Depot]
    garages: List[Garage]
    stations: List[Station]
    transition_costs: List[List[float]]
