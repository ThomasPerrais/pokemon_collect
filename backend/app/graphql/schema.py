import strawberry
from app.graphql import resolvers


# Root Query type
@strawberry.type
class Query:
    """
    Root Query type for GraphQL.
    Each field here maps to a resolver function.
    """
    # --- Generations ---
    generations = strawberry.field(
        resolver=resolvers.get_generations_resolver,
        description="Retrieve a list of all Pokémon generations.",
    )

    # --- Pokemons ---
    pokemons = strawberry.field(
        resolver=resolvers.get_pokemons_resolver,
        description="Retrieve a list of Pokémon. Can apply optional filters.",
    )

    # --- Types ---
    types = strawberry.field(
        resolver=resolvers.get_types_resolver,
        description="Retrieve a list of all Pokémon types.",
    )

    # --- Tags ---
    tags = strawberry.field(
        resolver=resolvers.get_tags_resolver,
        description="Retrieve the list of all Pokémon tags.",
    )

    # --- Eras ---
    eras = strawberry.field(
        resolver=resolvers.get_eras_resolver,
        description="Retrieve the list of all Pokémon card eras.",
    )

    # --- Sets ---
    sets = strawberry.field(
        resolver=resolvers.get_sets_resolver,
        description="Retrieve a list of Pokémon card sets. Can apply optional filters.",
    )

# --- Mutations ---
@strawberry.type
class Mutation:
    """
    Root Mutation type for GraphQL.
    Each field here maps to a resolver function.
    """
    # --- Generations ---

    create_generation = strawberry.field(
        resolver=resolvers.create_generation_resolver,
        description="Create a new Pokémon generation with its name and release year.",
    )

    # --- Pokemons ---
    create_pokemon = strawberry.field(
        resolver=resolvers.create_pokemon_resolver,
        description="Create a new Pokémon with its name, national dex number, generation name, types and tags.",
    )

    update_pokemon_name = strawberry.field(
        resolver=resolvers.update_pokemon_name_resolver,
        description="Update the name of a Pokémon by its id."
    )

    # --- Types ---
    create_pokemon_type = strawberry.field(
        resolver=resolvers.create_type_resolver,
        description="Create a new Pokémon type."
    )
    delete_pokemon_type = strawberry.field(
        resolver=resolvers.delete_type_resolver,
        description="Delete a Pokémon type."
    )

    # --- Tags ---
    create_pokemon_tag = strawberry.field(
        resolver=resolvers.create_tag_resolver,
        description="Create a new Pokémon tag."
    )
    delete_pokemon_tag = strawberry.field(
        resolver=resolvers.delete_tag_resolver,
        description="Delete a Pokémon tag."
    )

    # --- Eras ---
    create_era = strawberry.field(
        resolver=resolvers.create_era_resolver,
        description="Create a new Pokémon era with its name."
    )
    delete_era = strawberry.field(
        resolver=resolvers.delete_era_resolver,
        description="Delete a Pokémon era."
    )

    # --- Sets ---
    create_set = strawberry.field(
        resolver=resolvers.create_set_resolver,
        description="Create a new Pokémon card set with its name, era id, release date, era index and abv"
    )
    delete_set = strawberry.field(
        resolver=resolvers.delete_set_resolver,
        description="Delete a Pokémon card set."
    )


# Combine schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
