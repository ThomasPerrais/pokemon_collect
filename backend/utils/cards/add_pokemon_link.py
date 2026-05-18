import json
import argparse
import requests
import re
import unidecode

from utils.constants import GRAPHQL_URL, HEADERS
from utils.io import read_objects_from_array_json


SPECIAL_CASES = {
    "koraidon": ("Koraidon - forme finale", 1260),
    "miraidon": ("Miraidon - mode ultime", 1264),
    "sivallie": ("Sivallié - type normal", 965),
    "tauros de paldea": ("Tauros - forme de paldéa - race combattive", 181),
    "deoxys": ("Deoxys - forme normale", 492),
    "deoxys forme normale": ("Deoxys - forme normale", 492),
    "deoxys forme attaque": ("Deoxys - forme attaque", 493),
    "deoxys forme defense": ("Deoxys - forme defense", 494),
    "deoxys forme vitesse": ("Deoxys - forme vitesse", 495),
    "cheniti": ("Cheniti - cape plante", 521),
    "cheniti cape plante": ("Cheniti - cape plante", 521),
    "cheniti cape sable": ("Cheniti - cape sable", 522),
    "cheniti cape dechet": ("Cheniti - cape dechet", 523),
    "cheniselle": ("Cheniselle - cape plante", 524),
    "cheniselle cape plante": ("Cheniselle - cape plante", 524),
    "cheniselle cape sable": ("Cheniselle - cape sable", 525),
    "cheniselle cape dechet": ("Cheniselle - cape dechet", 526),
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
    "shifours mille poings": ("Shifours - style mille poings", 1129),
    "shifours poing final": ("Shifours - style point final", 1127),
    "dialga originel": ("Dialga - forme originelle", 610),
    "palkia originel": ("Palkia - forme originelle", 612),
    "qwilpik de hisui": ("Qwilpik", 1146),
    "farfurex de hisui": ("Farfurex", 1145),
    "sylveroy cavalier du froid": ("Sylveroy - cavalier du froid", 1137),
    "sylveroy cavalier d'effroi": ("Sylveroy - cavalier d'effroi", 1138),
    "m. glaquette de galar": ("M. Glaquette", 1094),
    "ixon de galar": ("Ixon", 1090),
    "corayome de galar": ("Corayôme", 1092),
    "tutetekri de galar": ("Tutétékri", 1095),
    "palarticho de galar": ("Palarticho", 1093),
    "berserkatt de galar": ("Berserkatt", 1091),
    "morpheo forme solaire": ("Morphéo - forme solaire", 445),
    "morpheo soleil": ("Morphéo - forme solaire", 445),
    "morpheo forme eau de pluie": ("Morphéo - forme eau de pluie", 446),
    "morpheo pluie": ("Morphéo - forme eau de pluie", 446),
    "morpheo forme blizzard": ("Morphéo - forme blizzard", 447),
    "morpheo neige": ("Morphéo - forme blizzard", 447),
    "raflesia": ("Rafflesia", 64),
    "rafflesia": ("Rafflesia", 64),
    "necrozma ailes de l'aurore": ("Necrozma - ailes de l'aurore", 1011),
    "necrozma criniere du couchant": ("Nécrozma - crinière du couchant", 1010),
    "tritosor mer orient": ("Tritosor - mer orient", 539),
    "tritosor mer occident": ("Tritosor - mer occident", 538),
    "sancoki mer orient": ("Sancoki - mer orient", 537),
    "sancoki mer occident": ("Sancoki - mer occident", 536),
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


def extract_pokemons(name: str) -> list[str]:
    """
    Normalize and standardize the card name
    Steps:
    1. Normalize the name to lowercase without accents
    2. Remove suffix ex, gx, vmax, vstar, v, etc.
    """
    name = name.replace(" ♂", " mâle").replace(" ♀", " femelle")
    name = name.replace(" δ", "")
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
    # name = re.sub(" de n$", "", name).strip()
    # name = re.sub(" de mashynn$", "", name).strip()
    # name = re.sub(" de lilie$", "", name).strip()
    # name = re.sub(" de nabil$", "", name).strip()

    # N4 special case: remove " lumineux" and " [a-z]" (zarbi)
    # name = re.sub(" lumineux$", "", name).strip()
    # name = re.sub(" [a-z]$", "", name).strip()

    # DS special case: remove " d'holon"
    # name = re.sub(" d'holon$", "", name).strip()

    # MA special case: remove "  de team aqua"
    # name = re.sub(" de team aqua$", "", name).strip()

    # name = re.sub(" radieux$", "", name).strip()  # EB
    # name = re.sub(" prisme etoile$", "", name).strip()  # TEU
    # name = re.sub(" brillant$", "", name).strip()  # SLE
    
    # name = re.sub(" (turbo|volant|surfeur)$", "", name).strip()  # EVO
    # name = re.sub(" (turbo)$", "", name).strip()  # STS, FAC, GNR, BKP, BKT
    # name = re.sub(" (de la team aqua|de la team magma)$", "", name).strip()  # DCR
    
    # name = re.sub(" legende$", "", name).strip()  # HGSS

    # name = re.sub(" (volant|surfeur|gl|g|fb|4|c|gl niv\.x|g niv\.x|c niv\.x|fb niv\.x|4 niv\.x)$", "", name).strip()
    # name = re.sub(" [a-z!\?]$", "", name).strip()  # zarbi
    
    # special cases CEL ()
    # name = re.sub(" (volant|surfeur|obscur|de rocket|brillant|de team magma|ex especes delta|delta|star|gl niv\.x|c niv\.x)$", "", name).strip()
    
    # # remove suffix ex, gx, vmax, vstar, v, etc...
    name = re.sub("^m-", "", name).strip()
    name = re.sub("[- ](ex|gx|v|vmax|vstar|niv\.x|lv\.36)$", "", name).strip()

    name = re.sub(", ", " et ", name).strip()
    name = re.sub(" & ", " et ", name).strip()
    return name.split(" et ")


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add pokemon link to cards using populated database of pokemons")
    parser.add_argument("pokemon_set", type=str, help="Pokemon set name (e.g. 'EV01' or 'ME01')")
    args = parser.parse_args()

    pokemon_era = args.pokemon_set[:2]

    # folder = BASE_DIR / "cards" / pokemon_era / "json"
    from pathlib import Path
    folder = Path("samples")

    cards = read_objects_from_array_json(str(folder / f"{args.pokemon_set}.json"))
    pokemons = query_pokemons()

    print(f"Number of cards: {len(cards)}")
    print(f"Number of pokemons: {len(pokemons)}")

    pokemon_cards = 0
    error_card = 0
    for card in cards:
        if card["type"] != "pokemon":
            continue
        pokemon_cards += 1

        pokemon_card_names = extract_pokemons(card["name"])
        pokemon_ids = []
        pokemon_names = []
        errors = []
        for pokemon_card_name in pokemon_card_names:
            if pokemon_card_name not in pokemons:
                errors.append(f"{pokemon_card_name} not found in pokemons")
                continue
            else:
                pokemon_name, pokemon_id = pokemons[pokemon_card_name]
                pokemon_names.append(pokemon_name)
                pokemon_ids.append(pokemon_id)
        
        if errors:
            print(f"Errors for card {card['name']}: {', '.join(errors)}")
            error_card += 1

        card["pokemons"] = pokemon_names
        card["pokemon_ids"] = pokemon_ids

    print(f"Linked: {pokemon_cards - error_card} / {pokemon_cards}")

    with open(folder / f"{args.pokemon_set}_linked.json", "w", encoding="utf-8") as file:
        # cards is a list of dicts, save it as a json array with each card on one line
        for card in cards:
            json.dump(card, file, ensure_ascii=False)
            file.write("\n")
