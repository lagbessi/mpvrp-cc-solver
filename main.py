import sys
import time
from pathlib import Path

from src.parser import parse_instance
from src.heuristics import greedy_construct
from src.validator import validate_solution
from src.exporter import export_solution
from src.api_client import generate_instance, verify_solution

def solve(instance_path):
    print("Loading instance...")
    instance = parse_instance(instance_path)

    start = time.time()

    print("Constructing solution...")
    greedy_construct(instance)

    print("Validating solution (local)...")
    errors = validate_solution(instance)
    if errors:
        print("Local validation failed:")
        for e in errors:
            print(" -", e)
        print("Solution not sent to API")
        return

    solution_path = Path("data/solutions") / ("Sol_" + Path(instance_path).name)

    print("Exporting solution...")
    export_solution(instance, str(solution_path), start)

    print("Done!")
    print("Solution saved to:", solution_path)

    instance_id = Path(instance_path).stem

    print("Verifying with API...")
    result = verify_solution(str(instance_path), str(solution_path), instance_id)
    print(result)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("Solve instance:")
        print("  python main.py data/instances/small/INSTANCE.dat")
        print("Generate + solve:")
        print("  python main.py --generate small 12 1 2 3 42")
        return

    if sys.argv[1] == "--generate":
        size = sys.argv[2]
        s = int(sys.argv[3])
        d = int(sys.argv[4])
        p = int(sys.argv[5])
        v = int(sys.argv[6])
        seed = int(sys.argv[7])

        params = {
            "id_instance": f"API_{size}_{s}_{p}_{v}_{seed}",
            "instance_size": size,
            "nb_stations": s,
            "nb_depots": d,
            "nb_garages": 1,
            "nb_produits": p,
            "nb_vehicules": v,
            "seed": seed,
        }

        filename = f"MPVRP_API_{size}_{s}_{p}_{v}.dat"
        output = Path("data/instances/api") / filename

        print("Generating instance via API...")
        generate_instance(params, str(output))
        solve(str(output))
    else:
        solve(sys.argv[1])

if __name__ == "__main__":
    main()
