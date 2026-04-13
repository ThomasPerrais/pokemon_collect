import strawberry
from typing import List, Optional

@strawberry.input
class PokemonCreationInput:
    name: str
    national_dex_number: int
    generation_name: str
    types: List[str]
    tags: List[str]


@strawberry.input
class CardCreationInput:
    name: str
    number: int
    rarity: str
    type: str
    set_id: int
    image_path: str = ""
    pokemon_id: int | None = None


@strawberry.input
class PokemonFilter:
    name_regex: Optional[str] = None
    number: Optional[int] = None
    types: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    generations: Optional[List[int]] = None


@strawberry.input
class SetFilter:
    name_regex: Optional[str] = None
    era_id: Optional[int] = None
    abbreviation: Optional[str] = None
    year: Optional[int] = None


@strawberry.input
class CardFilter:
    name_regex: Optional[str] = None
    rarity: Optional[List[str]] = None
    set_id: Optional[int] = None
    pokemon_id: Optional[int] = None
