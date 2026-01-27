from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, date

from app.db import models


@dataclass
class GenerationDTO:
    id: int
    name: str
    release_year: int

    @classmethod
    def from_orm(cls, generation: models.PokemonGeneration) -> "GenerationDTO":
        return cls(
            id=generation.id,
            name=generation.name,
            release_year=generation.release_year,
        )


@dataclass
class TypeDTO:
    id: int
    name: str

    @classmethod
    def from_orm(cls, type: models.PokemonType) -> "TypeDTO":
        return cls(
            id=type.id,
            name=type.name,
        )


@dataclass
class TagDTO:
    id: int
    name: str

    @classmethod
    def from_orm(cls, tag: models.PokemonTag) -> "TagDTO":
        return cls(
            id=tag.id,
            name=tag.name,
        )


@dataclass
class PokemonDTO:
    id: int
    name: str
    national_dex_number: int
    generation: GenerationDTO
    types: List[TypeDTO]
    tags: List[TagDTO]
    #star_in_sets: List["SetDTO"]
    #cards: List["CardDTO"]

    @classmethod
    def from_orm(cls, pokemon: models.Pokemon) -> "PokemonDTO":
        return cls(
            id=pokemon.id,
            name=pokemon.name,
            national_dex_number=pokemon.national_dex_number,
            generation=GenerationDTO.from_orm(pokemon.generation),
            types=[TypeDTO.from_orm(type) for type in pokemon.types],
            tags=[TagDTO.from_orm(tag) for tag in pokemon.tags],
        )


@dataclass
class EraDTO:
    id: int
    name: str
    sets: List["SetDTO"]

    @classmethod
    def from_orm(cls, era: models.Era) -> "EraDTO":
        return cls(
            id=era.id,
            name=era.name,
            sets=[SetDTO.from_orm(set) for set in era.sets],
        )

@dataclass
class SetDTO:
    id: int
    name: str
    era_index: float
    release_date: date
    abbreviation: str
    star_pokemons: List["PokemonDTO"]

    @classmethod
    def from_orm(cls, set: models.Set) -> "SetDTO":
        return cls(
            id=set.id,
            name=set.name,
            era_index=set.era_index,
            release_date=set.release_date,
            abbreviation=set.abbreviation,
            star_pokemons=[PokemonDTO.from_orm(pokemon) for pokemon in set.star_pokemons],
        )


@dataclass
class CardDTO:
    id: int
    name: str
    number: int
    rarity: str
    type: str
    set: SetDTO
    pokemon: PokemonDTO

    @classmethod
    def from_orm(cls, card: models.Card) -> "CardDTO":
        return cls(
            id=card.id,
            name=card.name,
            number=card.number,
            rarity=card.rarity,
            type=card.type,
            set=SetDTO.from_orm(card.set),
            pokemon=PokemonDTO.from_orm(card.pokemon),
        )