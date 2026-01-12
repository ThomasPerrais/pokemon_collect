import pandas as pd


def list_to_str(l: list[str]) -> str:
    return "[" + ",".join(f"\"{elt}\"" for elt in l) + "]"


def clean(text):
    """Map airtable generation names to our own generation names"""
    if text == "Galar et Hisui":
        return "Galar & Hisui"
    if text == "Paldea":
        return "Paldéa"
    return text


def create_mutation(name: str, num: int, gen: str, types: list[str], tags: list[str]) -> str:
    """Create a mutation from a dataframe line"""
    return f"mutation {{createPokemon(pokemon: {{name: \"{name}\", nationalDexNumber: {num}, generationName: \"{gen}\", types: {list_to_str(types)}, tags: {list_to_str(tags)}}}){{name}}}}"


def mutation_from_df_line(s):
    """Create a mutation from a dataframe line"""
    name = s.Name
    num = s.Number
    gen = clean(s.Generation)
    types = s.Types.split(',')
    tags = s.Tags.split(',') if isinstance(s.Tags, str) else []
    return create_mutation(name, num, gen, types, tags)


if __name__ == "__main__":
    import os
    os.chdir("/Users/thomasperrais/Documents/perso/PokemonCollect/")
    df = pd.read_csv("airtable_dumps/Pokemons-Grid view.csv")
    with open("mutations/pokemons.txt", "w") as f:
        for index, row in df.iterrows():
            f.write(mutation_from_df_line(row) + "\n")
