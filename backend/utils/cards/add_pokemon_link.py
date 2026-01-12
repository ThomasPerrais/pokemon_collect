import json
import argparse
import requests
import re
import unidecode

from utils.constants import GRAPHQL_URL, HEADERS, BASE_DIR


SPECIAL_CASES = {
    "koraidon": ("Koraidon - forme finale", 1260),
    "miraidon": ("Miraidon - mode ultime", 1264),
    "sivallie": ("Sivallié - type normal", 965),
    "tauros de paldea": ("Tauros - forme de paldéa - race combattive", 181),
    "deoxys": ("Deoxys - forme normale", 492),
    "cheniti": ("Cheniti - cape plante", 521),
    "cheniselle": ("Cheniselle - cape plante", 524),
    "ceriflor": ("Ceriflor - temps couvert", 534),
    "sancoki": ("Sancoki - mer occident", 536),
    "tritosor": ("Tritosor - mer occident", 538),
    "giratina": ("Giratina - Forme Alternative", 615),
    "bargantua": ("Bargantua - motif rouge", 700),
    "darumacho": ("Darumacho - mode normal", 708),
    "darumacho de galar": ("Darumacho - forme de Galar, mode normal", 709),
    "boreas": ("Boréas - forme avatar", 803),
    "fulguris": ("Fulguris - forme avatar", 805),
    "demeteros": ("Démétéros - forme avatar", 809),
    "keldeo": ("Keldeo - aspect normal", 814),
    "meloetta": ("Meloetta - forme chant", 816),
    "exagide": ("Exagide - forme parade", 856),
    "xerneas": ("Xerneas - mode paisible", 896),
    "hoopa": ("Hoopa - enchaîné", 904),
    "wimessir": ("Wimessir mâle", 1105),
    "zacian": ("Zacian - héros aguerri", 1120),
    "zamazenta": ("Zamazenta - héros aguerri", 1122),
    "famignol": ("Famignol - famille de 3", 1169),
    "tapatoes": ("Tapatoès - plumage vert", 1176),
    "nigirigon": ("Nigirigon - forme courbée", 1227),
    "ogerpon masque turquoise": ("Ogerpon - masque turquoise", 1278),
    "ogerpon masque du puits": ("Ogerpon - masque du puits", 1279),
    "ogerpon masque du fourneau": ("Ogerpon - masque du fourneau", 1280),
    "ogerpon masque de la pierre": ("Ogerpon - masque de la pierre", 1281),
    "terraiste de paldea": ("Terraiste", 1231),
    "ursaking lune vermeille": ("Ursaking - lune vermeille", 1142),
    "poltchageist": ("Poltchageist - forme imitation", 1271),
    "theffroyable": ("Théffroyable - forme médiocre", 1273),
}


def _normalize_name(name: str) -> str:
    """
    Normalize the name to lowercase without accents
    """
    name = name.lower()
    # remove accents
    name = unidecode.unidecode(name)
    return name


def normalize_pokemon_name(name: str) -> str:
    """
    Normalize and standardize the pokemon name.
    Steps:
    1. Normalize the name to lowercase without accents
    2. Replace ' - forme de (hisui|galar|paldea)' by ' de \1'
    3. Replace ' - forme d'alola' by ' d'alola'
    """
    name = _normalize_name(name)
    # replace ' - forme de (hisui|galar|paldea)' by 'de \1'
    name = re.sub(" - forme de (hisui|galar|paldea)$", " de \\1", name).strip()
    name = re.sub(" - forme d'alola$", " d'alola", name).strip()
    return name


def normalize_card_name(name: str) -> str:
    """
    Normalize and standardize the card name
    Steps:
    1. Normalize the name to lowercase without accents
    2. Remove suffix ex, gx, vmax, vstar, v, etc.
    """
    name = _normalize_name(name)
    
    # # special case of DRI: remove "de la Team Rocket", "de Luth", "de Cynthia"...
    # name = re.sub(" de la team rocket$", "", name).strip()
    # name = re.sub(" de luth$", "", name).strip()
    # name = re.sub(" de cynthia$", "", name).strip()
    # name = re.sub(" de pepper$", "", name).strip()
    # name = re.sub(" d'ondine$", "", name).strip()
    # name = re.sub(" de rosemary$", "", name).strip()
    # name = re.sub(" de pierre$", "", name).strip()

    # special case of JTG: remove "de N", "de Mashynn", "de Lilie", "de Nabil"
    name = re.sub(" de n$", "", name).strip()
    name = re.sub(" de mashynn$", "", name).strip()
    name = re.sub(" de lilie$", "", name).strip()
    name = re.sub(" de nabil$", "", name).strip()
    
    # # remove suffix ex, gx, vmax, vstar, v, etc...
    name = re.sub(" (ex|gx|vmax|vstar)$", "", name).strip()
    return name


def query_pokemons() -> dict[str, tuple[str, int]]:
    """
    Return a dictionary of pokemon id and name using the graphql API
    """
    query = """
    query {
        pokemons {
            id
            name
            nationalDexNumber
        }
    }
    """
    response = requests.post(GRAPHQL_URL, headers=HEADERS, data=json.dumps({"query": query}))
    pokemons = SPECIAL_CASES
    to_skip_ids = set(id for _, id in SPECIAL_CASES.values())
    for pokemon in response.json()["data"]["pokemons"]:
        if pokemon["id"] in to_skip_ids:
            continue
        normalized_name = normalize_pokemon_name(pokemon["name"])
        if normalized_name in pokemons:
            print(f"[WARNING] Pokemon {normalized_name} already in pokemons")  # should not happen
            continue
        pokemons[normalized_name] = (pokemon["name"], pokemon["id"])
    return pokemons


def read_cards_from_json(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add pokemon link to cards using populated database of pokemons")
    parser.add_argument("pokemon_set", type=str, help="Pokemon set name (e.g. 'EV01' or 'ME01')")
    args = parser.parse_args()

    pokemon_era = args.pokemon_set[:2]

    # folder = BASE_DIR / "cards" / pokemon_era / "json"
    from pathlib import Path
    folder = Path("samples")

    cards = read_cards_from_json(str(folder / f"{args.pokemon_set}.json"))
    pokemons = query_pokemons()

    print(f"Number of cards: {len(cards)}")
    print(f"Number of pokemons: {len(pokemons)}")

    pokemon_cards = 0
    not_found_pokemon_cards = 0
    for card in cards:
        if card["type"] != "pokemon":
            continue
        pokemon_cards += 1

        pokemon_card_name = normalize_card_name(card["name"])
        if pokemon_card_name not in pokemons:
            print(f"Pokemon card name {pokemon_card_name} not found in pokemons")
            not_found_pokemon_cards += 1
            card["pokemon"] = ""
            card["pokemon_id"] = -1
            continue

        pokemon_name, pokemon_id = pokemons[pokemon_card_name]
        card["pokemon"] = pokemon_name
        card["pokemon_id"] = pokemon_id

    print(f"Linked: {pokemon_cards - not_found_pokemon_cards} / {pokemon_cards}")

    with open(folder / f"{args.pokemon_set}_linked.json", "w", encoding="utf-8") as file:
        # cards is a list of dicts, save it as a json array with each card on one line
        for card in cards:
            json.dump(card, file, ensure_ascii=False)
            file.write("\n")
