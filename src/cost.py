def changeover_cost(instance, p1, p2):
   
    try:
        return instance.transition_costs[int(p1)][int(p2)]
    except (IndexError, TypeError, ValueError):
        return 0.0
