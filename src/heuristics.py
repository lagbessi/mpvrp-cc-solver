
def greedy_construct(instance):
    for v in instance.vehicles:
        v.route.clear()
        v.route.append(("Garage", v.home_garage))

        for product in range(instance.num_products):
            for station in instance.stations:
                demand = station.demand.get(product, 0)

                while demand > 0:
                    depot = None
                    for d in instance.depots:
                        if d.stock.get(product, 0) > 0:
                            depot = d
                            break

                    if depot is None:
                        return

                    load = min(
                        v.capacity,
                        demand,
                        depot.stock.get(product, 0)
                    )

                    v.route.append(("Depot", depot.id, product, load))
                    depot.stock[product] -= load

                    v.route.append(("Station", station.id, product, load))
                    demand -= load
                    station.demand[product] = demand

        v.route.append(("Garage", v.home_garage))
