"""
heuristics.py
-------------
Heuristique gloutonne conforme MPVRP-CC
- Respecte la capacité
- Permet livraisons partielles
- Satisfait toutes les demandes
"""

from src.distance import euclidean


def greedy_construct(instance):
    for v in instance.vehicles:
        v.route.clear()
        v.load = 0
        v.current_product = v.initial_product

        # Start at garage
        v.route.append(("Garage", v.home_garage))

        for product in range(instance.num_products):
            for station in instance.stations:
                demand = station.demand.get(product, 0)

                while demand > 0:
                    # Choisir dépôt (simple : premier)
                    depot = instance.depots[0]

                    # Aller au dépôt et charger
                    v.route.append(("Depot", depot.id, product, 0))
                    v.current_product = product
                    v.load = min(v.capacity, demand)

                    # Mise à jour de la dernière ligne depot avec la vraie charge
                    v.route[-1] = ("Depot", depot.id, product, v.load)

                    # Livrer
                    delivered = v.load
                    v.route.append(("Station", station.id, product, delivered))

                    # Mise à jour demande station
                    demand -= delivered
                    station.demand[product] = demand

                    # Camion vidé
                    v.load = 0

        # Return to garage
        v.route.append(("Garage", v.home_garage))
