"""
parser.py
---------
Lecture et parsing des fichiers d'instance MPVRP-CC (.dat)
"""

from typing import List
from src.models import *
import os


def _clean_lines(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        return [l.strip() for l in f.readlines() if l.strip() and not l.startswith("//")]


def parse_instance(filepath: str) -> Instance:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Instance not found: {filepath}")

    lines = _clean_lines(filepath)

    uuid_line = lines[0]
    uuid_str = uuid_line.replace("#", "").strip()

    nb_p, nb_d, nb_g, nb_s, nb_v = map(int, lines[1].split())
    idx = 2

    transition_costs = []
    for _ in range(nb_p):
        row = list(map(float, lines[idx].split()))
        if len(row) != nb_p:
            raise ValueError("Transition cost matrix size mismatch")
        transition_costs.append(row)
        idx += 1

    vehicles = []
    for _ in range(nb_v):
        parts = list(map(int, lines[idx].split()))
        if len(parts) != 4:
            raise ValueError("Invalid vehicle line format")
        v_id, cap, garage, prod = parts
        vehicles.append(Vehicle(v_id, cap, garage, prod))
        idx += 1

    depots = []
    for _ in range(nb_d):
        parts = lines[idx].split()
        d_id = int(parts[0])
        x, y = map(float, parts[1:3])
        stock_vals = list(map(float, parts[3:]))

        if len(stock_vals) != nb_p:
            raise ValueError("Depot stock size mismatch")

        depots.append(Depot(d_id, x, y, dict(enumerate(stock_vals))))
        idx += 1

    garages = []
    for _ in range(nb_g):
        g_id, x, y = map(float, lines[idx].split())
        garages.append(Garage(int(g_id), x, y))
        idx += 1

    stations = []
    for _ in range(nb_s):
        parts = lines[idx].split()
        s_id = int(parts[0])
        x, y = map(float, parts[1:3])
        demands = list(map(float, parts[3:]))

        if len(demands) != nb_p:
            raise ValueError("Station demand size mismatch")

        demand_dict = dict(enumerate(demands))

        stations.append(
            Station(
                id=s_id,
                x=x,
                y=y,
                demand=demand_dict.copy(),
                original_demand=demand_dict.copy(),
            )
        )
        idx += 1

    return Instance(
        uuid=uuid_str,
        num_products=nb_p,
        vehicles=vehicles,
        depots=depots,
        garages=garages,
        stations=stations,
        transition_costs=transition_costs,
    )
