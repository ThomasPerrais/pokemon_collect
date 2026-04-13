from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PokemonFilterParams:
    name_regex: Optional[str] = None
    number: Optional[int] = None
    types: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    generations: Optional[List[int]] = None


@dataclass
class SetFilterParams:
    name_regex: Optional[str] = None
    era_id: Optional[int] = None
    abbreviation: Optional[str] = None
    year: Optional[int] = None


@dataclass
class CardFilterParams:
    name_regex: Optional[str] = None
    rarity: Optional[List[str]] = None
    set_id: Optional[int] = None
    pokemon_id: Optional[int] = None
