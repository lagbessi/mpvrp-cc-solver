import requests
from pathlib import Path

API_URL = "https://mpvrp-cc.onrender.com"

def generate_instance(params, output_path):
    url = f"{API_URL}/generator/generate"

    payload = {
        "id_instance": params["id_instance"],
        "instance_size": params["instance_size"],
        "nb_stations": int(params["nb_stations"]),
        "nb_depots": int(params["nb_depots"]),
        "nb_garages": int(params["nb_garages"]),
        "nb_produits": int(params["nb_produits"]),
        "nb_vehicules": int(params["nb_vehicules"]),
        "seed": int(params["seed"]),
    }

    r = requests.post(url, json=payload, timeout=60)
    if r.status_code != 200:
        print("API error:", r.status_code)
        print("Response:", r.text)

    r.raise_for_status()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(r.text)

def verify_solution(instance_path, solution_path, id_instance):
    url = f"{API_URL}/model/verify"

    with open(instance_path, "rb") as i, open(solution_path, "rb") as s:
        files = {
            "instance_file": ("instance.dat", i, "text/plain"),
            "solution_file": ("solution.dat", s, "text/plain"),
        }

        data = {
            "id_instance": id_instance
        }

        r = requests.post(url, files=files, data=data, timeout=60)

        if r.status_code != 200:
            print("API error:", r.status_code)
            print("Response:", r.text)

        r.raise_for_status()
        return r.json()
