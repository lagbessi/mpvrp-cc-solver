"""
heuristics.py
-------------
Heuristique améliorée MPVRP-CC
- Regroupement par produit
- Choix du dépôt le plus proche
- Livraison par station la plus proche
"""

from src.distance import euclidean


def nearest_depot(node, depots):
    return min(depots, key=lambda d: euclidean(node, d))


def nearest_station(node, stations, product):
    candidates = [
        s for s in stations if s.demand.get(product, 0) > 0
    ]
    if not candidates:
        return None
    return min(candidates, key=lambda s: euclidean(node, s))


def greedy_construct(instance):
    for v in instance.vehicles:
        v.route.clear()
        v.load = 0
        v.current_product = v.initial_product

        # Start
        garage = next(g for g in instance.garages if g.id == v.home_garage)
        v.route.append(("Garage", v.home_garage))

        current_node = garage

        for product in range(instance.num_products):
            while True:
                station = nearest_station(current_node, instance.stations, product)
                if not station:
                    break

                depot = nearest_depot(current_node, instance.depots)

                demand = station.demand[product]
                load = min(v.capacity, demand)

                # Go to depot
                v.route.append(("Depot", depot.id, product, load))

                # Deliver
                v.route.append(("Station", station.id, product, load))

                station.demand[product] -= load
                current_node = station

        # Return
        v.route.append(("Garage", v.home_garage))
