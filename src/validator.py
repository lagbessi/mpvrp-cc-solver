"""
validator.py
------------
Vérification de la validité d'une solution MPVRP-CC
"""

def validate_solution(instance):
    errors = []

    remaining = {
        (s.id, p): s.original_demand.get(p, 0)
        for s in instance.stations
        for p in range(instance.num_products)
    }

    for v in instance.vehicles:
        if not v.route:
            continue

        if v.route[0][0] != "Garage" or v.route[-1][0] != "Garage":
            errors.append(f"Vehicle {v.id} does not start/end at garage")

        current_product = None
        current_load = 0

        for step in v.route:
            node_type = step[0]

            if node_type == "Depot":
                _, depot_id, product, qty = step

                current_product = product
                current_load = qty

                if current_load > v.capacity:
                    errors.append(
                        f"Vehicle {v.id} exceeds capacity at depot {depot_id}"
                    )

            elif node_type == "Station":
                _, station_id, product, qty = step

                if product != current_product:
                    errors.append(
                        f"Vehicle {v.id} delivers wrong product at station {station_id}"
                    )

                if qty > current_load:
                    errors.append(
                        f"Vehicle {v.id} delivers more than loaded at station {station_id}"
                    )

                key = (station_id, product)
                remaining[key] -= qty
                current_load -= qty

    for (station_id, product), value in remaining.items():
        if value != 0:
            errors.append(
                f"Demand not satisfied: station {station_id}, product {product}, remaining {value}"
            )

    return errors
