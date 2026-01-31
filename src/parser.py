import os
from src.models import Vehicle, Depot, Garage, Station, Instance

def parse_instance(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)

    with open(filepath, "r") as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith("//")]

    uuid_str = lines[0].replace("#", "").strip()
    nb_p, nb_d, nb_g, nb_s, nb_v = map(int, lines[1].split())
    idx = 2

    transition_costs = []
    for _ in range(nb_p):
        transition_costs.append(list(map(float, lines[idx].split())))
        idx += 1

    vehicles = []
    for _ in range(nb_v):
        v_id, cap, garage, prod = map(int, lines[idx].split())
        vehicles.append(Vehicle(v_id, cap, garage, prod))
        idx += 1

    depots = []
    for _ in range(nb_d):
        parts = lines[idx].split()
        d_id = int(parts[0])
        x, y = map(float, parts[1:3])
        stocks = dict(enumerate(map(float, parts[3:])))
        depots.append(Depot(d_id, x, y, stocks.copy(), stocks.copy()))

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
        demands = dict(enumerate(map(float, parts[3:])))
        stations.append(
            Station(s_id, x, y, demands.copy(), demands.copy())
        )
        idx += 1

    return Instance(uuid_str, nb_p, vehicles, depots, garages, stations, transition_costs)
