from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Pokemon, PokemonType, PokemonTag, PokemonGeneration, Era, Set
from app.db.filters import apply_pokemon_filters, apply_set_filters
from app.db.schemas import PokemonFilterParams, SetFilterParams
from app.db import dto
from datetime import date
from typing import Any


# --- Generations ---
def get_generations(db: Session) -> list[dto.GenerationDTO]:
    generations = db.scalars(select(PokemonGeneration)).all()
    return [dto.GenerationDTO.from_orm(generation) for generation in generations]


def get_generation_by_name(db: Session, name: str) -> dto.GenerationDTO | None:
    stmt = select(PokemonGeneration).where(PokemonGeneration.name == name)
    generation = db.scalars(stmt).one_or_none()
    return dto.GenerationDTO.from_orm(generation) if generation else None


def create_generation(db: Session, name: str, release_year: int) -> dto.GenerationDTO:
    generation = PokemonGeneration(name=name, release_year=release_year)
    try:
        db.add(generation)
        db.commit()
        db.refresh(generation)
        return dto.GenerationDTO.from_orm(generation)
    except Exception:
        db.rollback()
        raise


# --- Pokemons ---
def get_pokemons(
    db: Session, filters: PokemonFilterParams | None = None
) -> list[dto.PokemonDTO]:
    stmt = select(Pokemon)
    if filters:
        stmt = apply_pokemon_filters(stmt, filters)
    pokemons = db.scalars(stmt).all()
    return [dto.PokemonDTO.from_orm(pokemon) for pokemon in pokemons]


def create_pokemon(
    db: Session,
    name: str,
    national_dex_number: int,
    generation_name: str,
    type_names: list[str],
    tag_names: list[str],
) -> dto.PokemonDTO:
    stmt = select(PokemonGeneration).where(PokemonGeneration.name == generation_name)
    generation = db.scalars(stmt).one_or_none()
    if not generation:
        raise Exception("Generation not found")

    types = db.query(PokemonType).filter(PokemonType.name.in_(type_names)).all()
    if len(types) != len(type_names):
        raise Exception("One or more types not found")

    tags = db.query(PokemonTag).filter(PokemonTag.name.in_(tag_names)).all()
    if len(tags) != len(tag_names):
        raise Exception("One or more tags not found")

    pokemon = Pokemon(
        name=name,
        national_dex_number=national_dex_number,
        generation=generation,
        types=types,
        tags=tags,
    )
    try:
        db.add(pokemon)
        db.commit()
        db.refresh(pokemon)
        return dto.PokemonDTO.from_orm(pokemon)
    except Exception:
        db.rollback()
        raise


def update_pokemon_by_id(
    db: Session,
    id: int,
    **kwargs: Any,
) -> dto.PokemonDTO | None:
    pokemon = db.query(Pokemon).filter(Pokemon.id == id).first()
    if not pokemon:
        return None
    for key, value in kwargs.items():
        setattr(pokemon, key, value)
    db.commit()
    db.refresh(pokemon)
    return dto.PokemonDTO.from_orm(pokemon)


# --- Types ---
def get_types(db: Session) -> list[dto.TypeDTO]:
    types = db.query(PokemonType).all()
    return [dto.TypeDTO.from_orm(type) for type in types]


def get_type_by_name(db: Session, name: str) -> dto.TypeDTO | None:
    type = db.query(PokemonType).filter(PokemonType.name == name).first()
    return dto.TypeDTO.from_orm(type) if type else None


def create_type(db: Session, name: str) -> dto.TypeDTO:
    type = PokemonType(name=name)
    db.add(type)
    db.commit()
    db.refresh(type)
    return dto.TypeDTO.from_orm(type)


def delete_type(db: Session, id: int) -> dto.TypeDTO | None:
    type = db.query(PokemonType).filter(PokemonType.id == id).first()
    if type:
        db.delete(type)
        db.commit()
    return dto.TypeDTO.from_orm(type) if type else None


# --- Tags ---
def get_tags(db: Session) -> list[dto.TagDTO]:
    tags = db.query(PokemonTag).all()
    return [dto.TagDTO.from_orm(tag) for tag in tags]


def get_tag_by_name(db: Session, name: str) -> dto.TagDTO | None:
    tag = db.query(PokemonTag).filter(PokemonTag.name == name).first()
    return dto.TagDTO.from_orm(tag) if tag else None


def create_tag(db: Session, name: str) -> dto.TagDTO:
    tag = PokemonTag(name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return dto.TagDTO.from_orm(tag)


def delete_tag(db: Session, id: int) -> dto.TagDTO | None:
    tag = db.query(PokemonTag).filter(PokemonTag.id == id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return dto.TagDTO.from_orm(tag) if tag else None


# --- Eras ---
def get_eras(db: Session) -> list[dto.EraDTO]:
    eras = db.query(Era).all()
    return [dto.EraDTO.from_orm(era) for era in eras]


def create_era(db: Session, name: str) -> dto.EraDTO:
    era = Era(name=name)
    db.add(era)
    db.commit()
    db.refresh(era)
    return dto.EraDTO.from_orm(era)


def delete_era(db: Session, id: int) -> dto.EraDTO | None:
    era = db.query(Era).filter(Era.id == id).first()
    if era:
        db.delete(era)
        db.commit()
    return dto.EraDTO.from_orm(era) if era else None


# --- Sets ---
def get_sets(db: Session, filters: SetFilterParams | None = None) -> list[dto.SetDTO]:
    stmt = select(Set)
    if filters:
        stmt = apply_set_filters(stmt, filters)
    sets = db.scalars(stmt).all()
    return [dto.SetDTO.from_orm(set) for set in sets]


def create_set(
    db: Session,
    name: str,
    era_id: int,
    release_date: date,
    era_index: float,
    abbreviation: str,
) -> dto.SetDTO:
    era = db.query(Era).filter(Era.id == era_id).first()
    if not era:
        raise Exception("Era not found")
    set = Set(
        name=name,
        era_index=era_index,
        era=era,
        release_date=release_date,
        abbreviation=abbreviation,
    )
    db.add(set)
    db.commit()
    db.refresh(set)
    return dto.SetDTO.from_orm(set)


def delete_set(db: Session, id: int) -> dto.SetDTO | None:
    set = db.query(Set).filter(Set.id == id).first()
    if set:
        db.delete(set)
        db.commit()
    return dto.SetDTO.from_orm(set) if set else None
