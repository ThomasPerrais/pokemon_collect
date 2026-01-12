import requests
import json
import os
from utils.constants import GRAPHQL_URL, HEADERS, BASE_DIR

os.chdir(BASE_DIR)


with open(BASE_DIR / "mutations" / "pokemons_test.txt", "r") as f:
    mutations = f.readlines()


def send_mutation(query):
    payload = {"query": query}
    response = requests.post(GRAPHQL_URL, headers=HEADERS, data=json.dumps(payload))

    if response.status_code != 200:
        raise Exception(f"HTTP error {response.status_code}: {response.text}")

    data = response.json()
    if "errors" in data:
        print("❌ GraphQL Error:", data["errors"])
    else:
        print("✅ Success:", data["data"])


if __name__ == "__main__":
    for i, mutation in enumerate(mutations, 1):
        print(f"\n--- Running mutation #{i} ---")
        send_mutation(mutation)