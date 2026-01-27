from typing import List, Optional
from strawberry.types import Info
from sqlalchemy.orm import Session

from app.db.schemas import PokemonFilterParams, SetFilterParams
from app.db.dependencies import get_db
from app.db import crud

from app.graphql.types import (
    PokemonGQL,
    PokemonTypeGQL,
    PokemonTagGQL,
    PokemonGenerationGQL,
    EraGQL,
    SetGQL,
)
from app.graphql.inputs import PokemonFilter, PokemonCreationInput, SetFilter
from datetime import date


# --- Generations ---
def get_generations_resolver(name: str | None = None) -> List[PokemonGenerationGQL]:
    db: Session = next(get_db())
    if name:
        generation = crud.get_generation_by_name(db, name)
        if generation is not None:
            return [PokemonGenerationGQL.from_dto(generation)]
        return []
    return [
        PokemonGenerationGQL.from_dto(generation)
        for generation in crud.get_generations(db)
    ]


def create_generation_resolver(name: str, release_year: int) -> PokemonGenerationGQL:
    db: Session = next(get_db())
    generation = crud.create_generation(db, name, release_year)
    return PokemonGenerationGQL.from_dto(generation)


# --- Pokemons ---
def get_pokemons_resolver(filters: Optional[PokemonFilter] = None) -> List[PokemonGQL]:
    db: Session = next(get_db())
    filter_params: PokemonFilterParams | None = None
    if filters:
        filter_params = PokemonFilterParams(
            name_regex=filters.name_regex,
            number=filters.number,
            types=filters.types,
            tags=filters.tags,
            generations=filters.generations,
        )
    return [
        PokemonGQL.from_dto(pokemon) for pokemon in crud.get_pokemons(db, filter_params)
    ]


def create_pokemon_resolver(pokemon: PokemonCreationInput) -> PokemonGQL:
    db: Session = next(get_db())
    pokemon_dto = crud.create_pokemon(
        db,
        pokemon.name,
        pokemon.national_dex_number,
        pokemon.generation_name,
        pokemon.types,
        pokemon.tags,
    )
    return PokemonGQL.from_dto(pokemon_dto)


def update_pokemon_name_resolver(id: int, name: str) -> PokemonGQL | None:
    db: Session = next(get_db())
    pokemon_dto = crud.update_pokemon_by_id(db, id, name=name)
    if pokemon_dto is None:
        return None  # Pokemon not found
    return PokemonGQL.from_dto(pokemon_dto)


# --- Types ---
def get_types_resolver(name: str | None = None) -> List[PokemonTypeGQL]:
    db: Session = next(get_db())
    if name:
        type = crud.get_type_by_name(db, name)
        if type is not None:
            return [PokemonTypeGQL.from_dto(type)]
        return []
    return [PokemonTypeGQL.from_dto(type) for type in crud.get_types(db)]


def create_type_resolver(name: str) -> PokemonTypeGQL:
    db: Session = next(get_db())
    type = crud.create_type(db, name)
    return PokemonTypeGQL.from_dto(type)


def delete_type_resolver(id: int) -> bool:
    db: Session = next(get_db())
    deleted = crud.delete_type(db, id)
    return deleted is not None


# --- Tags ---
def get_tags_resolver(name: str | None = None) -> List[PokemonTagGQL]:
    db: Session = next(get_db())
    if name:
        tag = crud.get_tag_by_name(db, name)
        if tag is not None:
            return [PokemonTagGQL.from_dto(tag)]
        return []
    return [PokemonTagGQL.from_dto(tag) for tag in crud.get_tags(db)]


def create_tag_resolver(name: str) -> PokemonTagGQL:
    db: Session = next(get_db())
    tag = crud.create_tag(db, name)
    return PokemonTagGQL.from_dto(tag)


def delete_tag_resolver(id: int) -> bool:
    db: Session = next(get_db())
    deleted = crud.delete_tag(db, id)
    return deleted is not None


# --- Eras ---
def get_eras_resolver() -> List[EraGQL]:
    db: Session = next(get_db())
    return [EraGQL.from_dto(era) for era in crud.get_eras(db)]


def create_era_resolver(name: str) -> EraGQL:
    db: Session = next(get_db())
    era = crud.create_era(db, name)
    return EraGQL.from_dto(era)


def delete_era_resolver(id: int) -> bool:
    db: Session = next(get_db())
    deleted = crud.delete_era(db, id)
    return deleted is not None


# --- Sets ---
def get_sets_resolver(filters: Optional[SetFilter] = None) -> List[SetGQL]:
    db: Session = next(get_db())
    filter_params: SetFilterParams | None = None
    if filters:
        filter_params = SetFilterParams(
            name_regex=filters.name_regex,
            era_id=filters.era_id,
            abbreviation=filters.abbreviation,
            year=filters.year,
        )
    return [SetGQL.from_dto(set) for set in crud.get_sets(db, filter_params)]


def create_set_resolver(
    name: str,
    era_id: int,
    release_date: date,
    abbreviation: str,
    era_index: float,
) -> SetGQL:
    db: Session = next(get_db())
    set = crud.create_set(db, name, era_id, release_date, era_index, abbreviation)
    return SetGQL.from_dto(set)


def delete_set_resolver(id: int) -> bool:
    db: Session = next(get_db())
    deleted = crud.delete_set(db, id)
    return deleted is not None
