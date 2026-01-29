"""
exporter.py
-----------
Export de solution au format officiel MPVRP-CC
"""

import time
from src.distance import euclidean
from src.cost import changeover_cost


def export_solution(instance, filepath, start_time):
    vehicles_used = 0
    product_changes = 0
    total_change_cost = 0.0
    total_distance = 0.0

    lines = []

    for v in instance.vehicles:
        if len(v.route) <= 2:
            continue

        vehicles_used += 1

        visit_seq = [f"{v.id}:"]
        prod_seq = [f"{v.id}:"]

        last_product = v.initial_product
        last_node = None

        for step in v.route:
            node_type = step[0]

            if node_type == "Garage":
                _, gid = step
                visit_seq.append(str(gid))
                prod_seq.append(f"{last_product}(0.0)")
                last_node = step

            elif node_type == "Depot":
                _, did, product, qty = step
                visit_seq.append(f"{did} [{qty}]")

                if product != last_product:
                    product_changes += 1
                    cost = changeover_cost(instance, last_product, product)
                    total_change_cost += cost
                else:
                    cost = 0.0

                prod_seq.append(f"{product}({cost})")
                last_product = product
                last_node = step

            elif node_type == "Station":
                _, sid, product, qty = step
                visit_seq.append(f"{sid} ({qty})")
                prod_seq.append(f"{product}(0.0)")
                last_node = step

        lines.append(" - ".join(visit_seq))
        lines.append(" - ".join(prod_seq))
        lines.append("")

    # Calcul distance totale
    for v in instance.vehicles:
        last = None
        for step in v.route:
            node_type = step[0]

            if node_type == "Garage":
                node = next(g for g in instance.garages if g.id == step[1])
            elif node_type == "Depot":
                node = next(d for d in instance.depots if d.id == step[1])
            elif node_type == "Station":
                node = next(s for s in instance.stations if s.id == step[1])
            else:
                continue

            if last:
                total_distance += euclidean(last, node)

            last = node

    end_time = time.time()
    resolution_time = round(end_time - start_time, 3)

    # Metrics
    lines.append(str(vehicles_used))
    lines.append(str(product_changes))
    lines.append(f"{round(total_change_cost, 2)}")
    lines.append(f"{round(total_distance, 2)}")
    lines.append("Python Solver")
    lines.append(str(resolution_time))

    with open(filepath, "w") as f:
        for l in lines:
            f.write(l + "\n")
