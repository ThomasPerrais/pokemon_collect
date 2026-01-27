import strawberry
from datetime import date

from app.db.dto import GenerationDTO, TypeDTO, TagDTO, PokemonDTO, EraDTO, SetDTO


@strawberry.type
class PokemonGenerationGQL:
    id: int
    name: str
    release_year: int

    @classmethod
    def from_dto(cls, generation: GenerationDTO) -> "PokemonGenerationGQL":
        return cls(
            id=generation.id,
            name=generation.name,
            release_year=generation.release_year,
        )


@strawberry.type
class PokemonTypeGQL:
    id: int
    name: str

    @classmethod
    def from_dto(cls, type: TypeDTO) -> "PokemonTypeGQL":
        return cls(
            id=type.id,
            name=type.name,
        )


@strawberry.type
class PokemonTagGQL:
    id: int
    name: str

    @classmethod
    def from_dto(cls, tag: TagDTO) -> "PokemonTagGQL":
        return cls(
            id=tag.id,
            name=tag.name,
        )


# @strawberry.type
# class PokemonEvolutionGQL:
#     id: int
#     from_pokemon: "PokemonGQL"
#     to_pokemon: "PokemonGQL"
#     evolution_method: str

#     @classmethod
#     def from_dto(cls, evolution: EvolutionDTO) -> "PokemonEvolutionGQL":
#         return cls(
#             id=evolution.id,
#             from_pokemon=PokemonGQL.from_dto(evolution.from_pokemon),
#             to_pokemon=PokemonGQL.from_dto(evolution.to_pokemon),
#             evolution_method=evolution.evolution_method,
#         )


@strawberry.type
class PokemonGQL:
    id: int
    name: str
    national_dex_number: int
    generation: PokemonGenerationGQL
    types: list[PokemonTypeGQL]
    tags: list[PokemonTagGQL]

    @classmethod
    def from_dto(cls, pokemon: PokemonDTO) -> "PokemonGQL":
        return cls(
            id=pokemon.id,
            name=pokemon.name,
            national_dex_number=pokemon.national_dex_number,
            generation=PokemonGenerationGQL.from_dto(pokemon.generation),
            types=[PokemonTypeGQL.from_dto(type) for type in pokemon.types],
            tags=[PokemonTagGQL.from_dto(tag) for tag in pokemon.tags],
        )


@strawberry.type
class EraGQL:
    id: int
    name: str

    @classmethod
    def from_dto(cls, era: EraDTO) -> "EraGQL":
        return cls(
            id=era.id,
            name=era.name
        )


@strawberry.type
class SetGQL:
    id: int
    name: str
    era_index: float
    release_date: date
    abbreviation: str

    @classmethod
    def from_dto(cls, set: SetDTO) -> "SetGQL":
        return cls(
            id=set.id,
            name=set.name,
            era_index=set.era_index,
            release_date=set.release_date,
            abbreviation=set.abbreviation,
        )
