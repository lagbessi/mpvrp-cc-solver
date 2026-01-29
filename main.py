"""
main.py
-------
Point d'entrée du solveur MPVRP-CC
"""

import sys
import time
from src.parser import parse_instance
from src.heuristics import greedy_construct
from src.validator import validate_solution
from src.exporter import export_solution


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py data/instances/INSTANCE.dat")
        return

    instance_path = sys.argv[1]
    solution_path = "data/solutions/Sol_" + instance_path.split("/")[-1]

    print("Loading instance...")
    instance = parse_instance(instance_path)

    start_time = time.time()

    print("Constructing solution...")
    greedy_construct(instance)

    print("Validating solution...")
    errors = validate_solution(instance)

    if errors:
        print(" Solution invalid:")
        for e in errors:
            print(" -", e)
        return

    print(" Exporting solution...")
    export_solution(instance, solution_path, start_time)

    print(" Done!")
    print(f"Solution saved to: {solution_path}")


if __name__ == "__main__":
    main()
