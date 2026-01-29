"""
heuristics.py
-------------
Heuristique gloutonne conforme MPVRP-CC
"""

def greedy_construct(instance):
    for v in instance.vehicles:
        v.route.clear()
        v.load = 0
        v.current_product = v.initial_product

        v.route.append(("Garage", v.home_garage))

        for product in range(instance.num_products):
            for station in instance.stations:
                demand = station.demand.get(product, 0)

                while demand > 0:
                    depot = instance.depots[0]

                    load = min(v.capacity, demand)

                    v.route.append(("Depot", depot.id, product, load))
                    v.route.append(("Station", station.id, product, load))

                    demand -= load
                    station.demand[product] = demand

        v.route.append(("Garage", v.home_garage))
