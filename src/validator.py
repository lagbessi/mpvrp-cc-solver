

def validate_solution(instance):
    errors = []

    # --- Demandes initiales (théoriques) ---
    remaining_demand = {
        (s.id, p): s.original_demand.get(p, 0)
        for s in instance.stations
        for p in range(instance.num_products)
    }

    # --- Stocks initiaux (théoriques, jamais modifiés) ---
    remaining_stock = {
        (d.id, p): d.original_stock.get(p, 0)
        for d in instance.depots
        for p in range(instance.num_products)
    }

    # --- Vérification par véhicule ---
    for v in instance.vehicles:
        if not v.route:
            continue

        # C5 — Structure route
        if v.route[0][0] != "Garage" or v.route[-1][0] != "Garage":
            errors.append(
                f"Vehicle {v.id}: route must start and end at a garage"
            )

        current_product = None
        current_load = 0
        last_step_type = "Garage"

        for step in v.route:
            step_type = step[0]

            # -------------------
            # DEPOT
            # -------------------
            if step_type == "Depot":
                _, depot_id, product, qty = step

                # C7 — Produit valide
                if not isinstance(product, int) or product < 0 or product >= instance.num_products:
                    errors.append(
                        f"Vehicle {v.id}: invalid product id {product} at depot {depot_id}"
                    )
                    continue

                # C2 — Capacité véhicule
                if qty > v.capacity:
                    errors.append(
                        f"Vehicle {v.id}: capacity exceeded at depot {depot_id} "
                        f"(capacity={v.capacity}, loaded={qty})"
                    )

                # C1 — Stock dépôt
                key = (depot_id, product)
                if key not in remaining_stock:
                    errors.append(
                        f"Vehicle {v.id}: unknown depot {depot_id}"
                    )
                else:
                    if remaining_stock[key] < qty:
                        errors.append(
                            f"Stock exceeded: D{depot_id} prod {product} "
                            f"(stock={remaining_stock[key]}, loaded={qty})"
                        )
                    remaining_stock[key] -= qty

                # Nouveau mini-route
                current_product = product
                current_load = qty

                # C5 — Structure : deux dépôts consécutifs interdits
                if last_step_type == "Depot":
                    errors.append(
                        f"Vehicle {v.id}: two consecutive depots without visiting a station"
                    )

                last_step_type = "Depot"

            # -------------------
            # STATION
            # -------------------
            elif step_type == "Station":
                _, station_id, product, qty = step

                # C7 — Produit valide
                if not isinstance(product, int) or product < 0 or product >= instance.num_products:
                    errors.append(
                        f"Vehicle {v.id}: invalid product id {product} at station {station_id}"
                    )
                    continue

                # C4 — Produit cohérent
                if product != current_product:
                    errors.append(
                        f"Vehicle {v.id}: wrong product at station {station_id} "
                        f"(expected={current_product}, got={product})"
                    )

                # C6 — Livraison <= charge
                if qty > current_load:
                    errors.append(
                        f"Vehicle {v.id}: delivered more than loaded at station {station_id} "
                        f"(loaded={current_load}, delivered={qty})"
                    )

                # C3 — Satisfaction des demandes
                key = (station_id, product)
                if key not in remaining_demand:
                    errors.append(
                        f"Vehicle {v.id}: unknown station {station_id}"
                    )
                else:
                    remaining_demand[key] -= qty

                current_load -= qty
                last_step_type = "Station"

            # -------------------
            # GARAGE
            # -------------------
            elif step_type == "Garage":
                last_step_type = "Garage"
                current_product = None
                current_load = 0

            # -------------------
            # TYPE INCONNU
            # -------------------
            else:
                errors.append(
                    f"Vehicle {v.id}: unknown step type {step_type}"
                )

    # --- C3 — Vérification finale des demandes ---
    for (sid, p), value in remaining_demand.items():
        if value != 0:
            errors.append(
                f"Demand not satisfied: station {sid}, product {p}, remaining {value}"
            )

    return errors
