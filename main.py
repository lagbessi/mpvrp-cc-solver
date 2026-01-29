"""
main.py
-------
Point d'entrée du solveur MPVRP-CC
"""

import sys
from src.parser import parse_instance
from src.heuristics import greedy_construct


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py data/instances/INSTANCE.dat")
        return

    instance_path = sys.argv[1]

    print("🔍 Loading instance...")
    instance = parse_instance(instance_path)

    print("🚛 Constructing solution...")
    greedy_construct(instance)

    print("✅ Solution constructed successfully")
    print(f"Vehicles used: {len(instance.vehicles)}")


if __name__ == "__main__":
    main()
