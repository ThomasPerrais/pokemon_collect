from pathlib import Path

GRAPHQL_URL = "http://localhost:8000/graphql"
HEADERS = {
    "Content-Type": "application/json",
}

BASE_DIR = Path("~/Documents/perso/PokemonCollect/").expanduser()