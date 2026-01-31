import time
from src.distance import euclidean
from src.cost import changeover_cost

def export_solution(instance, filepath, start_time):
    lines = []
    vehicles_used = 0
    product_changes = 0
    total_cost = 0.0
    total_distance = 0.0

    for v in instance.vehicles:
        if len(v.route) <= 2:
            continue

        vehicles_used += 1
        visit = [f"{v.id}:"]
        prod = [f"{v.id}:"]

        last_product = v.initial_product
        last_node = None

        for step in v.route:
            t = step[0]

            if t == "Garage":
                gid = step[1]
                visit.append(str(gid))
                prod.append(f"{int(last_product)}(0)")
                node = next(g for g in instance.garages if g.id == gid)

            elif t == "Depot":
                _, did, product, qty = step
                qty_i = int(round(qty))

                visit.append(f"{did} [{qty_i}]")

                if product != last_product:
                    product_changes += 1
                    c = changeover_cost(instance, last_product, product)
                    total_cost += c
                else:
                    c = 0.0

                prod.append(f"{int(product)}({int(round(c))})")
                last_product = product
                node = next(d for d in instance.depots if d.id == did)

            elif t == "Station":
                _, sid, product, qty = step
                qty_i = int(round(qty))

                visit.append(f"{sid} ({qty_i})")
                prod.append(f"{int(product)}(0)")
                node = next(s for s in instance.stations if s.id == sid)

            if last_node:
                total_distance += euclidean(last_node, node)
            last_node = node

        lines.append(" - ".join(visit))
        lines.append(" - ".join(prod))
        lines.append("")

    elapsed = round(time.time() - start_time, 3)

    lines.append(str(int(vehicles_used)))
    lines.append(str(int(product_changes)))
    lines.append(str(round(total_cost, 2)))
    lines.append(str(round(total_distance, 2)))
    lines.append("Python Solver")
    lines.append(str(elapsed))

    with open(filepath, "w") as f:
        for l in lines:
            f.write(l + "\n")
