"""
heuristics.py
-------------
Heuristiques de construction de solution
"""

from src.distance import euclidean


def greedy_construct(instance):
    """
    Stratégie simple :
    - Chaque véhicule traite les demandes par produit
    - Charge au dépôt le plus proche
    - Livre les stations les plus proches
    """

    for vehicle in instance.vehicles:
        # Start at garage
        vehicle.route.append(("Garage", vehicle.home_garage))

        for product in range(instance.num_products):
            for station in instance.stations:
                demand = station.demand.get(product, 0)

                if demand <= 0:
                    continue

                depot = instance.depots[0]  # simple : premier dépôt

                # Load
                vehicle.route.append(("Depot", depot.id, product, demand))

                # Deliver
                vehicle.route.append(("Station", station.id, product, demand))

                station.demand[product] = 0

        # Return to garage
        vehicle.route.append(("Garage", vehicle.home_garage))
