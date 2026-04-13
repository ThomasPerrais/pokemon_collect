import argparse

from utils.io import read_objects_from_json

MAP = {
    "SVI": 3,
    "PAL": 4,
    "OBF": 5,
    "MEW": 6,
    "PAR": 7,
    "PAF": 8,
    "TEF": 9,
    "TWM": 10,
    "SFA": 11,
    "SCR": 12,
    "SSP": 13,
    "PRE": 14,
    "JTG": 15,
    "DRI": 16,
    "WHT": 17,
    "BLK": 18,
    "SSH": 19,
    "RCL": 20,
    "DAA": 21,
    "CPA": 22,
    "VIV": 23,
    "SHF": 24,
    "BST": 25,
    "CRE": 26,
    "EVS": 27,
    "CEL": 28,
    "FST": 29,
    "BRS": 30,
    "ASR": 31,
    "PGO": 32,
    "LOR": 33,
    "SIT": 34,
    "CRZ": 35,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create cards mutations from cards json files"
    )
    parser.add_argument("cards_file", type=str, help="Cards file")
    parser.add_argument("set_id", type=int, help="Set id")
    args = parser.parse_args()

    # set_id = args.set_id
    # output_file = args.cards_file.replace(".json", ".graphql")

    from pathlib import Path
    files = Path("../samples").glob("*.json")
    for file in files:

        serie = file.stem.split('_')[0]
        set_id = MAP[serie]
        print(f"processing : {file}  (serie id : {set_id})")

        # output_file = args.cards_file.replace(".json", ".graphql")
        output_file = Path("../samples") / (serie + ".graphql")
        # cards = read_objects_from_json(args.cards_file)
        cards = read_objects_from_json(file)

        with open(output_file, "w", encoding="utf-8") as f:
            for card in cards:
                if card["type"] == "pokemon":
                    f.write(
                        f"mutation {{createCard(card: {{name: \"{card['name']}\", number: {card['number']}, rarity: \"{card['rarity']}\", type: \"{card['type']}\", setId: {set_id}, pokemonId: {card['pokemon_id']}}}){{name}}}}"
                    )
                else:
                    f.write(
                        f"mutation {{createCard(card: {{name: \"{card['name']}\", number: {card['number']}, rarity: \"{card['rarity']}\", type: \"{card['type']}\", setId: {set_id}}}){{name}}}}"
                    )
                f.write("\n")
